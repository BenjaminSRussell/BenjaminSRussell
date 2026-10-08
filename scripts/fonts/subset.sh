#!/usr/bin/env bash
# subset.sh — reproduce every font file in scripts/fonts/ from the google/fonts originals.
#
# Usage:  scripts/fonts/subset.sh [SRC_DIR]
#   SRC_DIR  a directory holding the unsubsetted .ttf originals (default: a fresh download of the
#            eight files below from raw.githubusercontent.com/google/fonts/main into a temp dir).
#
# Three families, one unicode set, one feature set (T5 §2.3, MASTERPLAN decision 13):
#   Instrument Serif      Regular, Italic                      ofl/instrumentserif
#   IBM Plex Sans Cond.   Regular, Italic, Light (night)       ofl/ibmplexsanscondensed
#   IBM Plex Mono         Regular, Medium, Italic, Light       ofl/ibmplexmono
# Features kept: kern (GPOS pairs), liga (fi fl ffi ffl), subs/sups (encoded sub/superscript digits).
# Hinting dropped (we ship outlines), CFF desubroutinized (not applicable to these TrueType cuts, harmless),
# glyph names kept so the type engine can address `periodcentered`, `fi`, `uni2080` by name.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RAW="https://raw.githubusercontent.com/google/fonts/main/ofl"

# Codepoints: ASCII; nbsp; degree; middot; multiply; eacute; thin + hair space (synthesised by the engine,
# kept here so a cmap hit is possible if a cut ever ships them); en/em dash; quotes; bullet; ellipsis;
# prime/double prime; subscript digits 0-9; arrows left/up/right/down/north-east; minus; full and light
# shade blocks (log tape); check mark; geometric shapes (triangles, diamonds, circles) for marks.
# Codepoints a family lacks are skipped silently (pyftsubset --ignore-missing-unicodes is the default).
UNICODES='U+0020-007E,U+00A0,U+00B0,U+00B7,U+00D7,U+00E9,U+2009-200A,U+2013-2014,U+2018-2019,U+201C-201D,U+2022,U+2026,U+2032-2033,U+2080-2089,U+2190-2193,U+2197,U+2212,U+2588,U+2591,U+2713,U+25B2-25B3,U+25C6-25C7,U+25CB,U+25CF'
FEATURES='kern,liga,subs,sups'

declare -a FILES=(
  "instrumentserif/InstrumentSerif-Regular.ttf"
  "instrumentserif/InstrumentSerif-Italic.ttf"
  "ibmplexsanscondensed/IBMPlexSansCondensed-Regular.ttf"
  "ibmplexsanscondensed/IBMPlexSansCondensed-Italic.ttf"
  "ibmplexsanscondensed/IBMPlexSansCondensed-Light.ttf"
  "ibmplexmono/IBMPlexMono-Regular.ttf"
  "ibmplexmono/IBMPlexMono-Medium.ttf"
  "ibmplexmono/IBMPlexMono-Italic.ttf"
  "ibmplexmono/IBMPlexMono-Light.ttf"
)
declare -A LICENSES=(
  ["instrumentserif"]="LICENSE-InstrumentSerif.txt"
  ["ibmplexsanscondensed"]="LICENSE-IBMPlexSansCondensed.txt"
  ["ibmplexmono"]="LICENSE-IBMPlexMono.txt"
)

SRC="${1:-}"
if [[ -z "$SRC" ]]; then
  SRC="$(mktemp -d)"
  trap 'rm -rf "$SRC"' EXIT
  for rel in "${FILES[@]}"; do
    curl -sS -f -L -o "$SRC/$(basename "$rel")" "$RAW/$rel"
  done
  for fam in "${!LICENSES[@]}"; do
    curl -sS -f -L -o "$HERE/${LICENSES[$fam]}" "$RAW/$fam/OFL.txt"
  done
fi

for rel in "${FILES[@]}"; do
  name="$(basename "$rel")"
  pyftsubset "$SRC/$name" \
    --unicodes="$UNICODES" \
    --layout-features="$FEATURES" \
    --glyph-names --no-hinting --desubroutinize \
    --output-file="$HERE/$name"
  printf '%-40s %6d bytes\n' "$name" "$(stat -c %s "$HERE/$name")"
done
