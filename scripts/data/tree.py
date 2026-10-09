"""tree — what the repository holds at HEAD, from the clones: tests, workflows, manifests, lines by language.

    tree_facts(git_dir, repo, lines_cfg) -> {tests, workflows, manifest}     paths from `git ls-tree`, a few blobs
    scan_head(head_dir, repo, lines_cfg) -> {lines, test_functions}         needs the blobs of HEAD (a depth-1 clone)
    lines_by_language(head_dir, repo, lines_cfg) -> {language: lines}        scan_head's lines
    main_language(lines) -> str | None                                       the largest programming language
    lines_config(cfg) -> {exclude_dirs, exclude}                             chart.toml [lines]

Definitions (docs/data/AUDIT.md is the record):
  tests      files whose name is test_*.py, *_test.py, *_test.go, *.test.ts/.tsx/.js, *.spec.ts, *Tests.swift,
             or any .rs file under a `tests/` directory; vendored directories excluded.
  workflows  files .github/workflows/*.yml|yaml.
  manifest   declared (top-level, not transitive) dependency names from Cargo.toml, pyproject.toml, package.json,
             go.mod and Package.swift found at the repository root or one directory down (depth ≤ 2), in file
             order, deduplicated; dev/test groups left out. requirements.txt is not a manifest here.
  test_functions  test functions at HEAD, Rust and Python only: `#[test]`, `#[tokio::test]` (with or without
             arguments) and `#[rstest]` attributes in any .rs file (Rust unit tests live inline, in
             `#[cfg(test)]` modules), and `def test_…(` / `async def test_…(` in the Python files pytest
             collects (`test_*.py`, `*_test.py`); same exclusions as `lines`. None when the repository has
             no Rust or Python file, and (derive) a 0 is stated only when Rust or Python is the main
             language, so a Swift repository with one helper script never reads "0 tests". Swift, Go and
             JavaScript tests are counted only as files (`tests`).
  main_language  the language with most `lines`, leaving out markup and data (Markdown, JSON, YAML, TOML,
             HTML, CSS) unless nothing else is there.
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
NOT_PROGRAMS = {"Markdown", "JSON", "YAML", "TOML", "HTML", "CSS"}
RUST_TEST = re.compile(rb"^[ \t]*#\[[ \t]*(?:(?:tokio::)?test|rstest)[ \t]*[\](]", re.M)
PY_TEST = re.compile(rb"^[ \t]*(?:async[ \t]+)?def[ \t]+test_\w*[ \t]*\(", re.M)
PY_COLLECTED = re.compile(r"(^|/)(test_[^/]*|[^/]*_test)\.py$")   # the files pytest collects by default
TEST_FUNCTION_RX = {"Rust": RUST_TEST, "Python": PY_TEST}
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

def main_language(lines: dict[str, int] | None) -> str | None:
    """The programming language with most lines; markup and data only when nothing else is there."""
    if not lines:
        return None
    ranked = sorted(((n, lang) for lang, n in lines.items() if n > 0), key=lambda t: (-t[0], t[1]))
    programs = [lang for _n, lang in ranked if lang not in NOT_PROGRAMS]
    return (programs or [lang for _n, lang in ranked] or [None])[0]


def lines_by_language(head_dir: str, repo: str, lines_cfg: dict | None = None) -> dict[str, int] | None:
    """Newlines per language over HEAD's text files (a clone that holds HEAD's blobs). None when git fails."""
    return scan_head(head_dir, repo, lines_cfg)["lines"]


def scan_head(head_dir: str, repo: str, lines_cfg: dict | None = None) -> dict:
    """{lines: {language: lines} | None, test_functions: int | None} in one pass over HEAD's blobs."""
    lines_cfg = lines_cfg or lines_config(None)
    try:
        listing = _git(head_dir, "ls-tree", "-r", "-l", "HEAD")
    except RuntimeError:
        return {"lines": None, "test_functions": None}
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
            wanted.append((parts[2], lang, path))
    if not wanted:
        return {"lines": {}, "test_functions": None}
    counts: Counter = Counter()
    tests: Counter = Counter()
    proc = subprocess.Popen(["git", f"--git-dir={head_dir}", "cat-file", "--batch"], stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE)

    def feed() -> None:   # on its own thread: writing every id before reading would fill both pipes and stall
        try:
            for sha, _lang, _path in wanted:
                proc.stdin.write((sha + "\n").encode())
            proc.stdin.close()
        except (BrokenPipeError, OSError):
            pass

    try:
        threading.Thread(target=feed, daemon=True).start()
        rd = proc.stdout
        for sha, lang, path in wanted:
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
            rx = TEST_FUNCTION_RX.get(lang)
            if rx is not None and (lang != "Python" or PY_COLLECTED.search(path)):
                tests[lang] += len(rx.findall(data))
    finally:
        proc.wait(timeout=300)
    has_rust_or_python = any(lang in TEST_FUNCTION_RX for _sha, lang, _path in wanted)
    return {"lines": dict(sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))),
            "test_functions": sum(tests.values()) if has_rust_or_python else None}
