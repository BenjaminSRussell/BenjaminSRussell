"""tree — what the repository holds at HEAD, from the clones: tests, workflows, manifests, lines by language.

    tree_facts(git_dir, repo, lines_cfg) -> {tests, workflows, manifest}     paths from `git ls-tree`, a few blobs
    lines_by_language(head_dir, repo, lines_cfg) -> {language: lines}        needs the blobs of HEAD (a depth-1 clone)
    lines_config(cfg) -> {exclude_dirs, exclude}                             chart.toml [lines]

Definitions (docs/data/AUDIT.md is the record):
  tests      files whose name is test_*.py, *_test.py, *_test.go, *.test.ts/.tsx/.js, *.spec.ts, *Tests.swift,
             or any .rs file under a `tests/` directory; vendored directories excluded.
  workflows  files .github/workflows/*.yml|yaml.
  manifest   declared (top-level, not transitive) dependency names from Cargo.toml, pyproject.toml, package.json,
             go.mod and Package.swift found at the repository root or one directory down (depth ≤ 2), in file
             order, deduplicated; dev/test groups left out. requirements.txt is not a manifest here.
  lines      newline count of text files at HEAD whose extension names a programming language, with the
             vendored, build and generated directories of `[lines] exclude_dirs` and the per-repository
             `[lines.exclude]` paths left out. Binary files (a NUL in the first 8 KB) and files over
             512 KB (data tables and generated bundles saved with a source extension) are skipped.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import threading
from collections import Counter

EXCLUDE_DIRS = ["node_modules", "vendor", "target", "build", "dist", ".venv", "venv", "__pycache__",
                "site-packages", "third_party", ".git"]
LANGUAGES = {
    ".py": "Python", ".rs": "Rust", ".swift": "Swift", ".c": "C", ".h": "C", ".cc": "C++", ".cpp": "C++", ".hpp": "C++",
    ".ts": "TypeScript", ".tsx": "TypeScript", ".js": "JavaScript", ".jsx": "JavaScript", ".mjs": "JavaScript",
    ".go": "Go", ".sh": "Shell", ".bash": "Shell", ".html": "HTML", ".css": "CSS", ".scss": "CSS", ".sql": "SQL",
    ".java": "Java", ".kt": "Kotlin", ".rb": "Ruby", ".lua": "Lua", ".m": "Objective-C", ".metal": "Metal",
    ".glsl": "GLSL", ".vert": "GLSL", ".frag": "GLSL", ".zig": "Zig", ".cs": "C#", ".php": "PHP", ".r": "R",
}
TEST_PATTERNS = [re.compile(p) for p in (
    r"(^|/)test_[^/]*\.py$", r"(^|/)[^/]*_test\.py$", r"(^|/)[^/]*_test\.go$", r"(^|/)[^/]*\.test\.(ts|tsx|js)$",
    r"(^|/)[^/]*\.spec\.ts$", r"(^|/)[^/]*Tests\.swift$", r"(^|/)tests/.*\.rs$")]
WORKFLOW = re.compile(r"^\.github/workflows/[^/]+\.ya?ml$")
MANIFESTS = ("Cargo.toml", "pyproject.toml", "package.json", "go.mod", "Package.swift")
MANIFEST_CAP = 40
MAX_FILE_BYTES = 512 * 1024   # a source file over 512 KB is data or generated output, not typed; skipped


def lines_config(cfg: dict | None) -> dict:
    sec = (cfg or {}).get("lines") or {}
    dirs = list(sec.get("exclude_dirs") or EXCLUDE_DIRS)
    per_repo = {k: list(v) for k, v in (sec.get("exclude") or {}).items() if isinstance(v, list)}
    return {"exclude_dirs": dirs, "exclude": per_repo}


def excluded(path: str, repo: str, lines_cfg: dict) -> bool:
    parts = path.split("/")
    if any(p in lines_cfg.get("exclude_dirs", EXCLUDE_DIRS) for p in parts[:-1]):
        return True
    for prefix in lines_cfg.get("exclude", {}).get(repo, []):
        prefix = prefix.strip("/")
        if path == prefix or path.startswith(prefix + "/"):
            return True
    return False


def _git(git_dir: str, *args: str, timeout: int = 120) -> str:
    r = subprocess.run(["git", f"--git-dir={git_dir}", *args], capture_output=True, text=True, timeout=timeout)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip()[:200])
    return r.stdout


def paths_at_head(git_dir: str) -> list[str]:
    try:
        return _git(git_dir, "ls-tree", "-r", "--name-only", "HEAD").split("\n")
    except RuntimeError:
        return []


def blob_at_head(git_dir: str, path: str) -> str | None:
    try:
        return _git(git_dir, "show", f"HEAD:{path}")
    except RuntimeError:
        return None


# ---------------------------------------------------------------- tests, workflows, manifests

def count_tests(paths: list[str], repo: str, lines_cfg: dict) -> int:
    return sum(1 for p in paths if p and not excluded(p, repo, lines_cfg) and any(rx.search(p) for rx in TEST_PATTERNS))


def count_workflows(paths: list[str]) -> int:
    return sum(1 for p in paths if WORKFLOW.match(p))


def _pep508_name(spec: str) -> str | None:
    m = re.match(r"\s*([A-Za-z0-9][A-Za-z0-9._-]*)", spec)
    return m.group(1).lower() if m else None


def deps_from(name: str, text: str) -> list[str]:
    """Declared dependency names from one manifest's text; [] when it cannot be read."""
    out: list[str] = []
    try:
        if name == "Cargo.toml":
            import tomllib
            d = tomllib.loads(text)
            out += list((d.get("dependencies") or {}).keys())
            for t in (d.get("target") or {}).values():
                out += list((t.get("dependencies") or {}).keys())
        elif name == "pyproject.toml":
            import tomllib
            d = tomllib.loads(text)
            proj = d.get("project") or {}
            out += [n for n in (_pep508_name(s) for s in proj.get("dependencies") or []) if n]
            poetry = ((d.get("tool") or {}).get("poetry") or {}).get("dependencies") or {}
            out += [k.lower() for k in poetry if k.lower() != "python"]
        elif name == "package.json":
            d = json.loads(text)
            out += list((d.get("dependencies") or {}).keys())
        elif name == "go.mod":
            block = False
            for line in text.splitlines():
                s = line.strip()
                if s.startswith("require ("):
                    block = True
                    continue
                if block and s == ")":
                    block = False
                    continue
                m = re.match(r"(?:require\s+)?(\S+)\s+v\S+", s) if (block or s.startswith("require ")) else None
                if m and "// indirect" not in s:
                    segs = m.group(1).rstrip("/").split("/")
                    if len(segs) > 1 and re.fullmatch(r"v\d+", segs[-1]):   # a major-version suffix is not the name
                        segs.pop()
                    out.append(segs[-1])
        elif name == "Package.swift":
            for m in re.finditer(r'\.package\((?:[^)]*?url:\s*"([^"]+)"|[^)]*?name:\s*"([^"]+)")', text):
                url, pkg = m.group(1), m.group(2)
                out.append((url or pkg).rstrip("/").removesuffix(".git").split("/")[-1])
    except Exception:
        return []
    seen, uniq = set(), []
    for n in out:
        if n and n not in seen:
            seen.add(n)
            uniq.append(n)
    return uniq


def manifest(git_dir: str, paths: list[str]) -> dict | None:
    """{files: [...], deps: [...]} from the manifests at depth ≤ 2, or None when there is none."""
    files = sorted(p for p in paths if p.count("/") <= 1 and os.path.basename(p) in MANIFESTS)
    if not files:
        return None
    deps: list[str] = []
    for p in files:
        text = blob_at_head(git_dir, p)
        if text is not None:
            deps += deps_from(os.path.basename(p), text)
    seen, uniq = set(), []
    for n in deps:
        if n not in seen:
            seen.add(n)
            uniq.append(n)
    return {"files": files, "deps": uniq[:MANIFEST_CAP]}


def tree_facts(git_dir: str, repo: str, lines_cfg: dict | None = None) -> dict:
    lines_cfg = lines_cfg or lines_config(None)
    paths = paths_at_head(git_dir)
    return {"tests": count_tests(paths, repo, lines_cfg), "workflows": count_workflows(paths),
            "manifest": manifest(git_dir, paths)}


# ---------------------------------------------------------------- lines by language

def lines_by_language(head_dir: str, repo: str, lines_cfg: dict | None = None) -> dict[str, int] | None:
    """Newlines per language over HEAD's text files (a clone that holds HEAD's blobs). None when git fails."""
    lines_cfg = lines_cfg or lines_config(None)
    try:
        listing = _git(head_dir, "ls-tree", "-r", "-l", "HEAD")
    except RuntimeError:
        return None
    wanted: list[tuple[str, str]] = []
    for line in listing.splitlines():
        meta, _, path = line.partition("\t")
        parts = meta.split()
        if len(parts) < 4 or parts[1] != "blob":
            continue
        lang = LANGUAGES.get(os.path.splitext(path)[1].lower())
        try:
            size = int(parts[3])
        except ValueError:
            size = 0
        if lang and size <= MAX_FILE_BYTES and not excluded(path, repo, lines_cfg):
            wanted.append((parts[2], lang))
    if not wanted:
        return {}
    counts: Counter = Counter()
    proc = subprocess.Popen(["git", f"--git-dir={head_dir}", "cat-file", "--batch"], stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE)

    def feed() -> None:   # on its own thread: writing every id before reading would fill both pipes and stall
        try:
            for sha, _lang in wanted:
                proc.stdin.write((sha + "\n").encode())
            proc.stdin.close()
        except (BrokenPipeError, OSError):
            pass

    try:
        threading.Thread(target=feed, daemon=True).start()
        rd = proc.stdout
        for sha, lang in wanted:
            header = rd.readline()
            if not header:
                break
            parts = header.split()
            if len(parts) < 3 or parts[1] == b"missing":
                continue
            size = int(parts[2])
            data = rd.read(size)
            rd.read(1)   # the trailing newline git adds after each object
            if b"\0" in data[:8192]:
                continue
            n = data.count(b"\n")
            if data and not data.endswith(b"\n"):
                n += 1
            counts[lang] += n
    finally:
        proc.wait(timeout=300)
    return dict(sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])))
