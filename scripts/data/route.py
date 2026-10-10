"""route — the way into rustmapper, checked against the code (round 6, SPEC §5.3–5.4).

    verify_route(spec, read_head, read_release, head_sha, release) -> dict    routes.<name>
    handoff_state(spec, read_writer_head, read_writer_release, read_reader, ...) -> dict    one handoffs[] entry
    head_of(git_dir) -> {sha, short, date}                                    repos[].head
    struct_fields(src, struct) -> list[str]                                   `pub <name>:` lines of a Rust struct
    list_literal(src, name) -> list[str]                                      a Python list assigned to `name`
    resolve(route, runcheck) -> list[dict]                                    each entry as the image may draw it
    command_name(scripts) -> str                                              the command the image prints
    wheel_words(wheels) -> str                                                the platform note, or ""

An anchor is `{path}` (the file exists), `{path, text}` (the file contains the literal), `{path, absent}` (the
file does not contain it) or `{path, const}` (the file defines that numeric constant, whose value `{const:NAME}` in
the entry's text prints); `fn` narrows `text` and `absent` to one Rust function's body. An entry's desk file label
is drawn only when a path ending in that name is among its anchors on each side it describes (`label_for`). An entry is verified only when every `head` anchor holds in the repository at its HEAD
and every `release` anchor holds in the released sdist: what the image draws is true of the code a visitor reads
and of the release pip installs. An entry with `scope = "release"` describes the release only (what pip installs,
e.g. a default that HEAD has since changed); it needs release anchors and no head anchors.

Round 6, review 1: a string in a file shows the code exists, not that it works. An entry may also name run-check
probes (scripts/runcheck.py step ids): `runs` must have passed, `fails` must have failed, in the run check of the
released version. An entry may list alternatives under `instead`, each with its own text, anchors and probes; the
first candidate (the entry itself, then each alternative in order) whose anchors and probes all hold is the one
drawn. `{secs:<step>}` in a text is that step's measured wall time. An alternative whose text is "" retires the
entry once it holds (round 6, review 3): the fault is gone, so nothing is drawn and nothing fails. Value anchors
`{path, field}` (a struct literal's `field: 20`) and `{path, arg}` (a clap argument's `default_value`) print as
`{field:NAME}` and `{arg:NAME}`, as `{const:NAME}` does; `equals` pins the value. Review round 4: a clap default
may be a string (`default_value = "./sitemap.xml"`), printed without its leading `./`; `block` narrows an anchor to
the braces after that name (one clap subcommand, `ExportSitemap { … }`), as `fn` does to a function. Entries of
kind `text` are README sentences, checked the same way and never drawn. Review round 5: `before` makes an order anchor
(`text` first appears before `before`, in the narrowed body: the WAL's fsync before the redb commit), and a `text`
entry with `ci = "<job prefix>"` prints only while CI passed at the sha the route was read at with such a job
(`ci_ok`). The sheet draws verified entries only; check.py
fails on any other.

Review round 6: a string in a file shows a setter exists, not that anything calls it with a value (0.1.3 has
`host_state.crawl_delay_secs = delay`, and its only producer always passes None). A wording that makes a condition
(`unless`, `when`, `only`, `if`: CONDITIONAL) is verified only when it names a run-check probe (`runs` / `fails`) or
carries an anchor marked `producer = true` that is not an assignment to a field (SETTER): the code that decides,
not the code that stores. A `text` entry may also name a `gate` (a HEAD gate in `gates`); the README prints it only
while that gate holds (render_readme.text_entries). Review round 8: `para = true` starts a new paragraph with it.
Review round 9: `item = true` makes it an item of the cautions list under the install block; `{quiet}` in a text is
`quiet_secs` of the release's `arg:timeout` and `const:MAX_FAILURES_THRESHOLD` value anchors, and a probe that
records `quiet_secs` must have waited at least that long.

`read_*` are callables path -> str | None, so the tests run on fixture trees and the build on clones.
"""
from __future__ import annotations

import ast
import fnmatch
import re
import subprocess

KINDS = ("stop", "step", "note", "trap", "end", "export", "text")   # text: a README sentence, checked, never drawn
CONDITIONAL = re.compile(r"\b(unless|when|only|if)\b", re.I)    # review round 6: words that state a condition
SETTER = re.compile(r"\b\w+(?:\.\w+)+\s*=(?!=)")                 # `host_state.crawl_delay_secs = delay`
STATES = ("runs", "fields differ", "no reader")


# ---------------------------------------------------------------- anchors

_CONST = r"\bconst\s+{name}\s*:\s*[\w:<>]+\s*=\s*([0-9][0-9_]*(?:\.[0-9]+)?)\s*;"
_FIELD_INIT = r"\b{name}\s*:\s*([0-9][0-9_]*)\b"            # a struct literal's field: `max_inflight: 20,`
_ARG_DEFAULT = r'default_value\s*=\s*"([^"]*)"(?:(?!#\[arg)[\s\S])*?\b{name}\s*:'   # clap: the arg's default


def fn_body(src: str, name: str) -> str | None:
    """The body of `fn <name>(…) { … }` in Rust source, braces matched; None when there is no such function."""
    m = re.search(rf"\bfn\s+{re.escape(name)}\s*[<(]", src or "")
    if not m:
        return None
    i = src.find("{", m.end())
    if i < 0:
        return None
    depth, j = 1, i + 1
    while j < len(src) and depth:
        depth += {"{": 1, "}": -1}.get(src[j], 0)
        j += 1
    return src[i + 1:j - 1]


def block_body(src: str, name: str) -> str | None:
    """The braces after `<name> {` (a clap subcommand variant, a struct literal), matched; None when absent."""
    m = re.search(rf"\b{re.escape(name)}\s*\{{", src or "")
    if not m:
        return None
    depth, j = 1, m.end()
    while j < len(src) and depth:
        depth += {"{": 1, "}": -1}.get(src[j], 0)
        j += 1
    return src[m.end():j - 1]


def narrow(src: str | None, anchor: dict) -> tuple[str | None, str]:
    """The part of `src` an anchor speaks of (`fn`, then `block`), and a name for it; (None, why) when absent."""
    where = str(anchor.get("path") or "")
    if src is None:
        return None, f"{where}: file missing"
    for key, fn in (("fn", fn_body), ("block", block_body)):
        if anchor.get(key):
            src = fn(src, str(anchor[key]))
            if src is None:
                return None, f"{where}: no {'fn ' if key == 'fn' else ''}{anchor[key]}"
            where += f" {'fn ' if key == 'fn' else ''}{anchor[key]}"
    return src, where


def const_value(src: str | None, name: str) -> str | None:
    """`const BATCH_TIMEOUT_MS: u64 = 50;` -> "50" (underscores dropped); None when the constant is not there."""
    m = re.search(_CONST.format(name=re.escape(name)), src or "")
    return m.group(1).replace("_", "") if m else None


def field_value(src: str | None, name: str) -> str | None:
    """`max_inflight: 20,` -> "20": the first numeric literal given to that field; None when there is none."""
    m = re.search(_FIELD_INIT.format(name=re.escape(name)), src or "")
    return m.group(1).replace("_", "") if m else None


def arg_value(src: str | None, name: str) -> str | None:
    """`#[arg(short, long, default_value = "256", …)] workers: usize` -> "256": the first clap default of that arg
    (underscores dropped from a number; a string as written, `./sitemap.xml`)."""
    m = re.search(_ARG_DEFAULT.format(name=re.escape(name)), src or "")
    if not m:
        return None
    v = m.group(1)
    return v.replace("_", "") if re.fullmatch(r"[0-9][0-9_]*", v) else v


VALUE_KINDS = {"const": const_value, "field": field_value, "arg": arg_value}


def check_anchor(read, anchor: dict) -> str | None:
    """None when the anchor holds, else a short reason naming the file and the string.

    `fn` narrows `text` / `absent` to that function's body (so "the export path never opens the WAL" can be said of
    one function, not the whole file); `const` holds when the file defines that numeric constant."""
    path = str(anchor.get("path") or "")
    if not path:
        return "anchor without a path"
    src, where = narrow(read(path), anchor)
    if src is None:
        return where
    if "text" in anchor and str(anchor["text"]) not in src:
        return f"{where}: no {anchor['text']!r}"
    if "absent" in anchor and str(anchor["absent"]) in src:
        return f"{where}: contains {anchor['absent']!r}"
    if "before" in anchor:
        # review round 5: an order anchor; `text` first appears before `before` does (the WAL's fsync before the
        # redb commit, in one function's body)
        later = str(anchor["before"])
        if later not in src:
            return f"{where}: no {later!r}"
        if "text" in anchor and src.find(str(anchor["text"])) > src.find(later):
            return f"{where}: {anchor['text']!r} comes after {later!r}"
    for kind, fn in VALUE_KINDS.items():
        if anchor.get(kind):
            v = fn(src, str(anchor[kind]))
            if v is None:
                return f"{where}: no {kind} {anchor[kind]}"
            if "equals" in anchor and v != str(anchor["equals"]):
                return f"{where}: {kind} {anchor[kind]} is {v}, not {anchor['equals']}"
    return None


def check_anchors(read, anchors: list[dict] | None, where: str) -> list[str]:
    return [f"{where} {r}" for a in anchors or [] if (r := check_anchor(read, a))]


def anchor_consts(read, anchors: list[dict] | None) -> dict[str, str]:
    """{"const:NAME" | "field:NAME" | "arg:NAME": value} for every value anchor that holds (`fn` narrows the read)."""
    out = {}
    for a in anchors or []:
        for kind, fn in VALUE_KINDS.items():
            if a.get(kind) and check_anchor(read, a) is None:
                src, _ = narrow(read(str(a["path"])), a)
                out[f"{kind}:{a[kind]}"] = fn(src, str(a[kind]))
    return out


_CONST_REF = re.compile(r"\{((?:const|field|arg):\w+)\}")
_QUIET = "{quiet}"
QUIET_FROM = ("arg:timeout", "const:MAX_FAILURES_THRESHOLD")


def quiet_secs(timeout: int, threshold: int) -> int:
    """Review round 9: how long a release's `Received work item` lines may normally stop on a live crawl. A fetch runs
    up to the --timeout (reqwest: from connect to the body's end); after a failure the host waits 2^failures s, and it
    is dropped at `threshold` failures, so the longest wait is 2^(threshold - 1); the backoff is counted in whole
    seconds (1 s more). The sum, rounded up to the next 10: 20 + 4 + 1 -> 30."""
    raw = int(timeout) + 2 ** max(0, int(threshold) - 1) + 1
    return -(-raw // 10) * 10


def _num(v: str) -> str:
    """50000 -> "50,000" (a figure a reader reads); 256 and 50 stay as they are; a path default "./sitemap.xml"
    prints as the file's name, "sitemap.xml" (review round 4: where the export writes, relative to where you are)."""
    if v.startswith("./"):
        return v[2:]
    if re.fullmatch(r"[0-9]+\.0+", v):          # review round 5: `const THROTTLE_THRESHOLD_MS: f64 = 500.0` -> 500
        v = v.split(".")[0]
    return f"{int(v):,}" if v.isdigit() and len(v) > 4 else v


def label_for(file: str | None, head: list[dict] | None, release: list[dict] | None, scope: str) -> str | None:
    """The desk file label, only when it is true for the code it labels: a path ending in that name is among the
    release anchors, and among the head anchors too unless the entry describes the release only (round 6, review 2:
    0.1.3 has no governor.rs, so G1 carries no label)."""
    if not file:
        return None

    def named(anchors):
        return any(str(a.get("path") or "") == file or str(a.get("path") or "").endswith("/" + file)
                   for a in anchors or [])
    if not named(release):
        return None
    if scope != "release" and not named(head):
        return None
    return file


def producers(e: dict) -> list[dict]:
    """The anchors marked `producer = true` that are not field assignments (review round 6)."""
    return [a for a in (e.get("head") or []) + (e.get("release") or [])
            if a.get("producer") and not SETTER.search(str(a.get("text") or ""))]


def _candidate(e: dict, rh, rr, no_head: list, no_rel: list, scope: str, eid: str, file: str | None = None,
               kind: str = "stop") -> dict:
    """One candidate wording of an entry, with its anchors checked on both sides. `{const:NAME}` in the text is the
    value of that constant, read from the code through a `const` anchor; head and release must agree on it."""
    if not e.get("release") or (scope != "release" and not e.get("head")):
        raise ValueError(f"route entry {eid}: needs release anchors" + ("" if scope == "release" else " and head anchors"))
    if scope == "release":
        mh = check_anchors(rh, e.get("head"), "head") if e.get("head") and not no_head else []
    else:
        mh = no_head or check_anchors(rh, e.get("head"), "head")
    mr = no_rel or check_anchors(rr, e.get("release"), "release")
    text = str(e["text"])
    consts_h = anchor_consts(rh, e.get("head")) if not no_head else {}
    consts_r = anchor_consts(rr, e.get("release")) if not no_rel else {}
    for ref in _CONST_REF.findall(text):
        vr, vh = consts_r.get(ref), consts_h.get(ref)
        name = ref.split(":", 1)[1]
        if vr is None and scope == "release" and vh is not None and e.get("from_head"):
            vr = vh          # a figure the release lacks but main states (the sitemap format's 50,000 URLs)
        if vr is None:
            mr = mr + [f"release: no {ref.split(':')[0]} anchor for {{{ref}}}"]
            continue
        if scope != "release" and vh is not None and vh != vr:
            mh = mh + [f"head {name} = {vh}, release {name} = {vr}: the figure differs"]
            continue
        text = text.replace(f"{{{ref}}}", _num(vr))
    quiet = None
    if _QUIET in text:
        got = [consts_r.get(k) for k in QUIET_FROM]
        if all(v is not None and str(v).isdigit() for v in got):
            quiet = quiet_secs(int(got[0]), int(got[1]))
            text = text.replace(_QUIET, str(quiet))
        else:
            mr = mr + [f"release: {{quiet}} needs value anchors {' and '.join(QUIET_FROM)}"]
    # an end's `file` is what the run writes (data/sitemap.jsonl), not a source file: it is not a label
    # review round 6: a condition needs a probe or the code that decides it, never a setter alone
    cond = CONDITIONAL.search(text)
    if cond and not (e.get("runs") or e.get("fails")) and not producers(e):
        mr = mr + [f"{cond.group(1)!r} states a condition, and no probe and no producer anchor stands behind it"]
    label = (e.get("file") or file) if kind in ("end", "export") else \
        label_for(e.get("file") or file, e.get("head"), e.get("release"), scope)
    rec_q = {"quiet": quiet} if quiet is not None else {}
    return {"text": text, "file": label, "verified_head": not mh, "verified_release": not mr, **rec_q,
            "missing": mh + mr, "runs": [str(x) for x in e.get("runs") or []],
            "fails": [str(x) for x in e.get("fails") or []],
            "paths": {"head": sorted({str(a.get("path")) for a in e.get("head") or []}),
                      "release": sorted({str(a.get("path")) for a in e.get("release") or []})}}


def verify_route(spec: dict, read_head, read_release, head_sha: str | None, release: str | None) -> dict:
    """chart.toml [route.<name>] -> {repo, head_sha, release, header, header_verified, entries[]}.

    `read_head` is None when there is no clone this run, `read_release` None when there is no sdist: every
    anchor on that side then fails with the reason, so nothing is drawn on faith."""
    def reader(fn, side):
        return fn if fn is not None else (lambda _p: None)

    rh, rr = reader(read_head, "head"), reader(read_release, "release")
    no_head = [] if read_head is not None else ["head: no clone of the repository this run"]
    no_rel = [] if read_release is not None else ["release: no sdist this run"]
    hh = spec.get("header_head", spec.get("header_anchors"))
    hr = spec.get("header_release", spec.get("header_anchors"))
    header_missing = (no_head or check_anchors(rh, hh, "head")) + (no_rel or check_anchors(rr, hr, "release"))
    entries = []
    for e in spec.get("entry") or []:
        kind = str(e.get("kind") or "stop")
        eid = str(e.get("id"))
        if kind not in KINDS:
            raise ValueError(f"route entry {eid}: kind {kind!r} not in {KINDS}")
        scope = str(e.get("scope") or "both")
        first = _candidate(e, rh, rr, no_head, no_rel, scope, eid, kind=kind)
        rec = {"id": eid, "kind": kind, "scope": scope, "loop": bool(e.get("loop")), **first}
        if e.get("ci"):          # review round 5: a README sentence that also rests on CI at HEAD (`ci_ok`)
            rec["ci"] = str(e["ci"])
        if e.get("gate"):        # review round 6: a README sentence that also rests on a HEAD gate (`gates`)
            rec["gate"] = str(e["gate"])
        if e.get("para"):        # review round 8: a README sentence that starts a new paragraph
            rec["para"] = True
        if e.get("item"):        # review round 9: a README caution, one item of the list under the install block
            rec["item"] = True
        alts = [_candidate(a, rh, rr, no_head, no_rel, scope, eid, e.get("file"), kind) for a in e.get("instead") or []]
        if alts:
            rec["instead"] = alts
        entries.append(rec)
    gates = {}
    for gname, anchors in (spec.get("gates") or {}).items():   # HEAD-only conditions for README lines (SPEC §4.5)
        miss = no_head or check_anchors(rh, anchors, "head")
        gates[gname] = {"ok": not miss, "missing": miss}
    # review round 4: release-only conditions for README lines (what pip installs: the export's default paths, Redis
    # off unless asked); a value anchor's value is kept, so the README can print it
    for gname, anchors in (spec.get("release_gates") or {}).items():
        miss = no_rel or check_anchors(rr, anchors, "release")
        gates[gname] = {"ok": not miss, "missing": miss, "scope": "release",
                        "values": anchor_consts(rr, anchors) if not no_rel else {}}
    ids = [x["id"] for x in entries]
    if len(set(ids)) != len(ids):
        raise ValueError(f"route ids not unique: {ids}")
    return {"repo": spec.get("repo"), "head_sha": head_sha, "release": release, "header": spec.get("header"),
            "header_verified": not header_missing, "header_missing": header_missing,
            "header_runs": [str(x) for x in spec.get("header_runs") or []], "entries": entries, "gates": gates,
            **({"list_lead": str(spec["list_lead"])} if spec.get("list_lead") else {})}


# ---------------------------------------------------------------- the run check's probes

def steps_of(runcheck: dict | None, release: str | None = None) -> dict[str, dict] | None:
    """{step id: step} from the run check, or None when there is none (or it tested another version)."""
    if not isinstance(runcheck, dict):
        return None
    if release is not None and str(runcheck.get("version")) != str(release):
        return None
    return {str(s["id"]): s for s in runcheck.get("steps") or [] if isinstance(s, dict) and s.get("id")}


def run_missing(cand: dict, steps: dict[str, dict] | None) -> list[str]:
    """Why a candidate's probes do not hold: [] when every `runs` step passed and every `fails` step failed."""
    need = [(sid, True) for sid in cand.get("runs") or []] + [(sid, False) for sid in cand.get("fails") or []]
    if not need:
        return []
    if steps is None:
        return ["run check: none recorded for this release"]
    out = []
    for sid, want in need:
        st = steps.get(sid)
        if st is None:
            out.append(f"run check: no step {sid}")
        elif bool(st.get("ok")) != want:
            out.append(f"run check: {sid} {'failed' if want else 'passed'} ({str(st.get('detail') or '')[:120]})")
        elif want and cand.get("quiet") is not None and st.get("quiet_secs") is not None \
                and float(st["quiet_secs"]) < float(cand["quiet"]):
            # review round 9: the probe waited less than the quiet the text prints
            out.append(f"run check: {sid} waited {st['quiet_secs']} s of quiet, the text says {cand['quiet']} s")
    return out


_SECS = re.compile(r"\{secs:([\w-]+)\}")


def fill_secs(text: str, steps: dict[str, dict] | None) -> str | None:
    """`{secs:<step>}` -> that step's wall time in whole seconds; None when a step or its time is missing."""
    bad = False

    def sub(m):
        nonlocal bad
        st = (steps or {}).get(m.group(1)) or {}
        if st.get("secs") is None:
            bad = True
            return m.group(0)
        return f"{float(st['secs']):.0f}"
    out = _SECS.sub(sub, text)
    return None if bad else out


def resolve(route: dict | None, runcheck: dict | None = None) -> list[dict]:
    """Each entry as the image may draw it: the first candidate whose anchors and probes all hold, with
    `verified` true; or, when none holds, the entry's own wording with `verified` false and every reason."""
    route = route or {}
    steps = steps_of(runcheck, route.get("release"))
    out = []
    for e in route.get("entries") or []:
        cands = [e] + list(e.get("instead") or [])
        reasons: list[str] = []
        chosen = None
        for i, c in enumerate(cands):
            miss = list(c.get("missing") or [])
            if not (c.get("verified_head") and c.get("verified_release")) and not miss:
                miss = ["anchors do not hold"]
            miss += run_missing(c, steps)
            text = fill_secs(str(c.get("text") or ""), steps)
            if text is None:
                miss.append("run check: no time for a {secs:…} figure")
            if not miss:
                chosen = dict(c, text=text)
                break
            reasons += [f"[{i}] {m}" if len(cands) > 1 else m for m in miss]
        base = {"id": e.get("id"), "kind": e.get("kind"), "scope": e.get("scope", "both"), "loop": bool(e.get("loop"))}
        if e.get("ci"):
            base["ci"] = e["ci"]
        if e.get("gate"):
            base["gate"] = e["gate"]
        if e.get("para"):
            base["para"] = True
        if e.get("item"):
            base["item"] = True
        if chosen is not None:
            # an alternative with no words retires the entry: the fault it named is gone (round 6, review 3: once a
            # release ends by itself, there is no hazard to draw), so it is neither drawn nor unverified
            out.append({**base, "text": chosen["text"], "file": chosen.get("file") if "file" in chosen else e.get("file"),
                        "verified": True, "missing": [], "retired": not str(chosen["text"]).strip(),
                        "fails": list(chosen.get("fails") or [])})
        else:
            out.append({**base, "text": e.get("text"), "file": e.get("file"), "verified": False, "missing": reasons})
    return out


def ci_ok(repo: dict | None, head_sha: str | None, job_prefix: str) -> tuple[bool, str]:
    """Review round 5: CI ran at the sha the route was read at and passed, with a job whose name starts with
    `job_prefix` (`Test (ubuntu-latest, stable)` runs `cargo test`). (True, "") or (False, why)."""
    ci = (repo or {}).get("ci") or {}
    sha = ((repo or {}).get("head") or {}).get("sha")
    if ci.get("conclusion") != "success":
        return False, f"CI {ci.get('conclusion') or 'not recorded'}"
    if not sha or ci.get("head_sha") != sha or (head_sha and head_sha != sha):
        return False, f"CI ran at {str(ci.get('head_sha'))[:7]}, the route was read at {str(head_sha or sha)[:7]}"
    if not any(str(j.get("name") or "").startswith(job_prefix) and j.get("conclusion") == "success"
               for j in ci.get("jobs") or [] if isinstance(j, dict)):
        return False, f"no passing CI job named {job_prefix}*"
    return True, ""


def header_ok(route: dict | None, runcheck: dict | None = None) -> tuple[bool, list[str]]:
    route = route or {}
    miss = list(route.get("header_missing") or [])
    if not route.get("header_verified") and not miss:
        miss = ["anchors do not hold"]
    miss += run_missing({"runs": route.get("header_runs") or []}, steps_of(runcheck, route.get("release")))
    return not miss, miss


def drawn(route: dict | None, runcheck: dict | None = None) -> list[dict]:
    """The entries the image may draw: anchors hold (at HEAD and in the release, or in the release for a release-only
    entry) and the run-check probes they name came out as stated."""
    return [e for e in resolve(route, runcheck) if e["verified"] and not e.get("retired")]


def unverified(route: dict | None, runcheck: dict | None = None) -> list[dict]:
    return [e for e in resolve(route, runcheck) if not e["verified"]]


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
    # review round 4: what the receiving side does with the file, when its reader says so (`does`: {verb, text[]})
    does = spec.get("does") or {}
    if does.get("verb") and does.get("text"):
        out["does"] = does["verb"] if all(str(t) in src for t in does["text"]) else None
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
