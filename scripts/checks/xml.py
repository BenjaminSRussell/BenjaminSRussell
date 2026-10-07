"""xml — every sheet parses, carries no live text or script, and every reference resolves.

T10 check 2: lxml parses (xml.dom fallback); no <text> <script> <style> or external href; ids
unique and sheet-prefixed; every href="#x" / url(#x) / SMIL `x.begin` resolves; values/keyTimes
lengths agree; a frozen fade-in starts from opacity="0"."""
from __future__ import annotations

import re
import xml.etree.ElementTree as ET

from checks import Finding, fail, warn

TIER = "fast"
SVG_NS = "{http://www.w3.org/2000/svg}"
XLINK = "{http://www.w3.org/1999/xlink}href"
FORBIDDEN = ("text", "tspan", "textPath", "script", "style", "foreignObject", "image", "animateMotion")
ANIM = ("animate", "animateTransform", "set", "animateColor")
_URL_RE = re.compile(r"url\(#([^)]+)\)")
_TIMING_RE = re.compile(r"(?<![\w.-])([A-Za-z_][\w-]*)\.(?:begin|end|repeat\(\d+\))")


def _parse(text: str, where: str) -> tuple[ET.Element | None, Finding | None]:
    try:
        import lxml.etree as LX  # type: ignore
        try:
            LX.fromstring(text.encode("utf-8"))
        except LX.XMLSyntaxError as exc:
            return None, fail("XML-PARSE", f"{exc.msg} (line {exc.lineno})", where)
    except ImportError:
        pass
    try:
        return ET.fromstring(text), None
    except ET.ParseError as exc:
        return None, fail("XML-PARSE", str(exc), where)


def _local(tag: str) -> str:
    return tag.split("}", 1)[1] if "}" in tag else tag


def check_one(ctx, name: str) -> list[Finding]:
    text = ctx.svg_text(name)
    root, err = _parse(text, name)
    if err:
        return [err]
    out: list[Finding] = []
    sheet = ctx.sheet_of(name)
    if _local(root.tag) != "svg":
        return [fail("XML-ROOT", f"root is <{_local(root.tag)}>, not <svg>", name)]
    if "viewBox" not in root.attrib:
        out.append(fail("XML-VIEWBOX", "no viewBox on <svg>", name))
    ids: dict[str, int] = {}
    refs: list[tuple[str, str]] = []   # (id, how)
    for el in root.iter():
        tag = _local(el.tag)
        if tag in FORBIDDEN:
            out.append(fail("XML-FORBIDDEN", f"<{tag}> is not allowed in a sheet", name))
        i = el.get("id")
        if i is not None:
            ids[i] = ids.get(i, 0) + 1
            if not i.startswith(sheet + "-"):
                out.append(fail("XML-ID-PREFIX", f'id="{i}" lacks the {sheet}- prefix', name))
        href = el.get("href") or el.get(XLINK)
        if href is not None:
            if href.startswith("#"):
                refs.append((href[1:], f"<{tag} href>"))
            else:
                out.append(fail("XML-EXTERNAL-HREF", f"<{tag}> references {href[:60]!r}", name))
        for attr, val in el.attrib.items():
            for m in _URL_RE.finditer(val):
                refs.append((m.group(1), f"{attr}=url(#)"))
        if tag in ANIM:
            for attr in ("begin", "end"):
                for m in _TIMING_RE.finditer(el.get(attr, "")):
                    refs.append((m.group(1), f"<{tag} {attr}>"))
            vals, kt = el.get("values"), el.get("keyTimes")
            if vals is not None and kt is not None:
                nv, nk = len([v for v in vals.split(";") if v.strip() != ""]), len([t for t in kt.split(";") if t.strip() != ""])
                if nv != nk:
                    out.append(fail("XML-KEYTIMES", f"<{tag}> has {nv} values but {nk} keyTimes", name))
            if el.get("repeatCount") == "indefinite" and tag == "set":
                out.append(warn("XML-SET-LOOP", "<set repeatCount=indefinite> is meaningless", name))
    for i, n in ids.items():
        if n > 1:
            out.append(fail("XML-ID-DUP", f'id="{i}" appears {n} times', name))
    for i, how in refs:
        if i not in ids:
            out.append(fail("XML-REF", f"{how} references #{i}, which does not exist", name))
    # a frozen fade-in must start on paper that is already transparent, or it pops
    parent_of = {c: p for p in root.iter() for c in p}
    for el in root.iter():
        if _local(el.tag) != "animate" or el.get("attributeName") != "opacity" or el.get("fill") != "freeze":
            continue
        vals = (el.get("values") or el.get("from") or "").split(";")
        if vals and vals[0].strip() in ("0", "0.0"):
            p = parent_of.get(el)
            if p is not None and p.get("opacity", "").strip() not in ("0", "0.0"):
                out.append(fail("XML-FADE-BASE", f"frozen fade-in on <{_local(p.tag)}> without opacity=\"0\" base", name))
    # editions agree with the report
    if ctx.report and name in ctx.report.get("sheets", {}):
        e = ctx.report["sheets"][name]
        vb = (root.get("viewBox") or "").split()
        if len(vb) == 4 and (int(float(vb[2])), int(float(vb[3]))) != (e.get("w"), e.get("h")):
            out.append(fail("XML-SIZE", f"viewBox {vb[2]}×{vb[3]} but report says {e.get('w')}×{e.get('h')}", name))
    return out


def check(ctx) -> list[Finding]:
    out: list[Finding] = []
    for name in ctx.svgs:
        out += check_one(ctx, name)
    return out
