"""route — the way into rustmapper, checked against the code (round 6, SPEC §5.3–5.4).

    verify_route(spec, read_head, read_release, head_sha, release) -> dict    routes.<name>
    handoff_state(spec, read_writer_head, read_writer_release, read_reader, ...) -> dict    one handoffs[] entry
    head_of(git_dir) -> {sha, short, date}                                    repos[].head
    struct_fields(src, struct) -> list[str]                                   `pub <name>:` lines of a Rust struct
    list_literal(src, name) -> list[str]                                      a Python list assigned to `name`
    command_name(scripts) -> str                                              the command the image prints
    wheel_words(wheels) -> str                                                the platform note, or ""

An anchor is `{path}` (the file exists), `{path, text}` (the file contains the literal) or `{path, absent}` (the
file does not contain it). An entry is verified only when every `head` anchor holds in the repository at its HEAD
and every `release` anchor holds in the released sdist: what the image draws is true of the code a visitor reads
and of the release pip installs. The sheet draws verified entries only; check.py fails on any other.

`read_*` are callables path -> str | None, so the tests run on fixture trees and the build on clones.
"""
from __future__ import annotations

import ast
import fnmatch
import re
import subprocess

KINDS = ("stop", "trap", "end", "export")
STATES = ("runs", "fields differ", "no reader")


# ---------------------------------------------------------------- anchors

def check_anchor(read, anchor: dict) -> str | None:
    """None when the anchor holds, else a short reason naming the file and the string."""
    path = str(anchor.get("path") or "")
    if not path:
        return "anchor without a path"
    src = read(path)
    if src is None:
        return f"{path}: file missing"
    if "text" in anchor and str(anchor["text"]) not in src:
        return f"{path}: no {anchor['text']!r}"
    if "absent" in anchor and str(anchor["absent"]) in src:
        return f"{path}: contains {anchor['absent']!r}"
    return None


def check_anchors(read, anchors: list[dict] | None, where: str) -> list[str]:
    return [f"{where} {r}" for a in anchors or [] if (r := check_anchor(read, a))]


def verify_route(spec: dict, read_head, read_release, head_sha: str | None, release: str | None) -> dict:
    """chart.toml [route.<name>] -> {repo, head_sha, release, header, header_verified, entries[]}.

    `read_head` is None when there is no clone this run, `read_release` None when there is no sdist: every
    anchor on that side then fails with the reason, so nothing is drawn on faith."""
    def reader(fn, side):
        return fn if fn is not None else (lambda _p: None)

    rh, rr = reader(read_head, "head"), reader(read_release, "release")
    no_head = [] if read_head is not None else ["head: no clone of the repository this run"]
    no_rel = [] if read_release is not None else ["release: no sdist this run"]
    header_missing = (no_head or check_anchors(rh, spec.get("header_anchors"), "head")) + \
        (no_rel or check_anchors(rr, spec.get("header_anchors"), "release"))
    entries = []
    for e in spec.get("entry") or []:
        kind = str(e.get("kind") or "stop")
        if kind not in KINDS:
            raise ValueError(f"route entry {e.get('id')}: kind {kind!r} not in {KINDS}")
        if not e.get("head") or not e.get("release"):
            raise ValueError(f"route entry {e.get('id')}: needs head and release anchors")
        mh = no_head or check_anchors(rh, e.get("head"), "head")
        mr = no_rel or check_anchors(rr, e.get("release"), "release")
        entries.append({"id": str(e["id"]), "kind": kind, "file": e.get("file") or None, "text": str(e["text"]),
                        "verified_head": not mh, "verified_release": not mr, "missing": mh + mr})
    gates = {}
    for gname, anchors in (spec.get("gates") or {}).items():   # HEAD-only conditions for README lines (SPEC §4.5)
        miss = no_head or check_anchors(rh, anchors, "head")
        gates[gname] = {"ok": not miss, "missing": miss}
    ids = [x["id"] for x in entries]
    if len(set(ids)) != len(ids):
        raise ValueError(f"route ids not unique: {ids}")
    return {"repo": spec.get("repo"), "head_sha": head_sha, "release": release, "header": spec.get("header"),
            "header_verified": not header_missing, "header_missing": header_missing, "entries": entries,
            "gates": gates}


def drawn(route: dict | None) -> list[dict]:
    """The entries the image may draw: verified at HEAD and in the release."""
    return [e for e in (route or {}).get("entries") or [] if e.get("verified_head") and e.get("verified_release")]


def unverified(route: dict | None) -> list[dict]:
    return [e for e in (route or {}).get("entries") or [] if not (e.get("verified_head") and e.get("verified_release"))]


# ---------------------------------------------------------------- the hand-offs

_STRUCT = re.compile(r"pub\s+struct\s+(\w+)\s*(?:<[^>{]*>)?\s*\{")
_FIELD = re.compile(r"^\s*pub\s+(?:\([^)]*\)\s+)?(r#)?([A-Za-z_]\w*)\s*:", re.M)


def struct_fields(src: str | None, struct: str) -> list[str]:
    """The `pub <name>:` fields inside `pub struct <struct> { … }`, in order. Raises when there is no such struct
    or it has no public field: a parse that finds nothing must never pass as an empty field set."""
    for m in _STRUCT.finditer(src or ""):
        if m.group(1) != struct:
            continue
        depth, i = 1, m.end()
        while i < len(src) and depth:
            depth += {"{": 1, "}": -1}.get(src[i], 0)
            i += 1
        body = src[m.end():i - 1]
        body = re.sub(r"//[^\n]*", "", body)
        fields = [f.group(2) for f in _FIELD.finditer(body)]
        if not fields:
            raise ValueError(f"pub struct {struct} has no public field")
        return fields
    raise ValueError(f"no pub struct {struct}")


def list_literal(src: str | None, name: str) -> list[str]:
    """The list of strings assigned to `name` at module level, read with ast.literal_eval. Raises when absent."""
    try:
        tree = ast.parse(src or "")
    except SyntaxError as exc:
        raise ValueError(f"cannot parse the reader: {exc}") from None
    for node in tree.body:
        targets = node.targets if isinstance(node, ast.Assign) else [node.target] if isinstance(node, ast.AnnAssign) else []
        if any(isinstance(t, ast.Name) and t.id == name for t in targets) and node.value is not None:
            val = ast.literal_eval(node.value)
            if not isinstance(val, (list, tuple)) or not val or not all(isinstance(v, str) for v in val):
                raise ValueError(f"{name} is not a non-empty list of strings")
            return list(val)
    raise ValueError(f"no {name} = [...] in the reader")


def handoff_state(spec: dict, read_writer_head, read_writer_release, read_reader, list_reader=None,
                  from_sha: str | None = None, to_sha: str | None = None, release: str | None = None) -> dict:
    """One `[[handoffs]]` entry -> its computed state.

    kind "fields": the writer's struct at HEAD and in the release, the reader's list at its HEAD, and the reader's
    test file. `runs` iff reader ⊆ writer on both sides and the test exists; `fields differ` when a field is
    missing; `no reader` when the reader file is gone. kind "mention": the writer file exists, and the reader is
    any file of the receiving repository naming one of `mentions` (`list_reader()` -> [(path, text)]); none ->
    `no reader`."""
    kind = spec.get("kind", "fields")
    out = {"id": spec["id"], "from": spec.get("from"), "to": spec.get("to"), "file": spec.get("file"),
           "from_sha": from_sha, "to_sha": to_sha, "release": release, "reader_fields": [],
           "writer_fields_head": [], "writer_fields_release": [], "reader": spec.get("reader"),
           "test": None, "state": "no reader"}
    if kind == "mention":
        writer = spec.get("writer")
        out["writer"] = writer
        if read_writer_head is None or read_writer_head(writer) is None:
            out["state"] = "no writer"
            return out
        words = [str(w).lower() for w in spec.get("mentions") or []]
        hits = sorted(p for p, text in (list_reader() if list_reader else []) if any(w in (text or "").lower() for w in words))
        out["readers"] = hits
        out["state"] = "runs" if hits else "no reader"
        return out
    struct = spec["writer_struct"]
    out["writer_fields_head"] = struct_fields(read_writer_head(spec["writer"]) if read_writer_head else None, struct)
    out["writer_fields_release"] = struct_fields(
        read_writer_release(spec["writer"]) if read_writer_release else None, struct)
    src = read_reader(spec["reader"]) if read_reader else None
    if src is None:
        return out
    out["reader_fields"] = list_literal(src, spec["reader_list"])
    test = spec.get("test")
    out["test"] = test if test and read_reader(test) is not None else None
    need = set(out["reader_fields"])
    ok = need <= set(out["writer_fields_head"]) and need <= set(out["writer_fields_release"])
    out["missing_fields"] = sorted(need - set(out["writer_fields_head"]) | need - set(out["writer_fields_release"]))
    out["state"] = "runs" if ok and out["test"] else "fields differ" if not ok else "no test"
    return out


# ---------------------------------------------------------------- HEAD, commands, wheels

def head_of(git_dir: str) -> dict | None:
    """{sha, short, date}: HEAD of the clone and its committer date (no sweep exclusion: it dates the code read)."""
    try:
        sha = subprocess.run(["git", f"--git-dir={git_dir}", "rev-parse", "HEAD"], capture_output=True, text=True,
                             timeout=30, check=True).stdout.strip()
        date = subprocess.run(["git", f"--git-dir={git_dir}", "log", "-1", "--format=%cs", "HEAD"],
                              capture_output=True, text=True, timeout=30, check=True).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return None
    if not re.fullmatch(r"[0-9a-f]{40}", sha) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date):
        return None
    return {"sha": sha, "short": sha[:7], "date": date}


def command_name(scripts: list[str] | None, project: str = "rustmapper") -> str:
    """`rustmapper` when the wheel ships it, else the first executable it ships. None shipped: raise."""
    scripts = [s for s in scripts or [] if s]
    if not scripts:
        raise RuntimeError("edition.scripts is empty: the release ships no command, so the image prints none")
    return project if project in scripts else scripts[0]


_PLATFORMS = (("linux", "x86_64", "Linux x86_64"), ("macosx", "arm64", "macOS arm64"),
              ("macosx", "x86_64", "macOS x86_64"), ("win", "amd64", "Windows x86_64"),
              ("linux", "aarch64", "Linux arm64"))
COMMON = ("Linux x86_64", "macOS arm64", "Windows x86_64")


def wheel_platforms(wheels: list[str] | None) -> list[tuple[str, str]]:
    """['cp313-cp313-macosx_11_0_arm64'] -> [('macOS arm64', 'Python 3.13')]; abi3 / py3 -> 'Python 3'."""
    out = []
    for tag in wheels or []:
        parts = str(tag).split("-")
        if len(parts) < 3:
            continue
        py, plat = parts[0], parts[-1]
        name = next((n for os_, arch, n in _PLATFORMS if os_ in plat and arch in plat), None)   # manylinux_2_17_x86_64
        if name is None and plat == "any":
            name = "any platform"
        if name is None:
            continue
        m = re.fullmatch(r"cp(\d)(\d+)", py)
        pyv = f"Python {m.group(1)}.{m.group(2)}" if m and "abi3" not in tag else "Python 3"
        out.append((name, pyv))
    return out


def wheel_words(wheels: list[str] | None) -> str:
    """The platform note for strangers: "prebuilt for macOS arm64 + Python 3.13; elsewhere pip needs Rust".
    Empty when the wheels cover Linux x86_64, macOS arm64 and Windows x86_64 (or one is pure Python)."""
    plats = wheel_platforms(wheels)
    names = {n for n, _ in plats}
    if "any platform" in names or all(c in names for c in COMMON):
        return ""
    if not plats:
        return "no prebuilt wheel; pip needs Rust"
    by: dict[str, list[str]] = {}
    for n, v in plats:
        by.setdefault(n, [])
        if v not in by[n]:
            by[n].append(v)
    pieces = [f"{n} + {', '.join(sorted(vs))}" for n, vs in by.items()]
    return f"prebuilt for {' and '.join(pieces)}; elsewhere pip needs Rust"


def glob_match(pattern: str, paths: list[str]) -> list[str]:
    return [p for p in paths if fnmatch.fnmatch(p, pattern)]
