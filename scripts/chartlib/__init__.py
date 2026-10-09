"""chartlib — the one drawing library every sheet calls (T6; MASTERPLAN §3.2).

    field      Field.from_soundings · Coast · contours · Contour · compact_path · smooth_path ·
               monotone_path · contour_labels · break_anchor · draw_contours · bracket_test
    water      tint_bands · coastline · danger_lines · hatch · coast_vignette · unsurveyed_band ·
               approximate_fringe
    place      Feature · place_features · solve_radii · feature_polygons · spot_heights ·
               soundings_along · soundings_lean · PlaceReport · RadiusReport
    symbols    symbol_defs · use · sloop · lateral · light · halo · lit_core · traffic_signal · horn ·
               anchorage · wreck · waypoint · station · fix · ldg_triangle · doubt · correction · serpent · tick ·
               rock · rock_d
    furniture  stroke · width · set_night · Jitter · frame · margin_graticule · two_ring_rose · clock_rose ·
               Zone · source_diagram ·
               area_key · paper · plate_mark · course · course_samples · lateral_offset · track_lines ·
               check_lines · restricted_line

Text is never drawn here: functions that letter take `label_cb(text, x, y, role, **kw) -> str`
(T5's engine, wired by the sheet). LETTERING maps each class of chart lettering to its T5 role
and the slant convention (upright = measured / land, italic = floating / water / illustrative).

Calling order for a chart sheet: paper → Field → solve_radii → contours → tint_bands → coastline →
coast_vignette → danger_lines → hatch/unsurveyed_band → draw_contours → contour_labels →
symbols/course → frame → furniture.
"""
from .field import (Field, Coast, Kernel, FieldReport, Contour, contours, compact_path, parse_path, smooth_path,
                    gaps_in_rect, broken_polylines_multi,
                    monotone_path, contour_labels, break_anchor, broken_polylines, draw_contours, clip_polyline,
                    bracket_test, band_of, closed_check, bump, fmt, polygon_area, polygon_centroid,
                    point_in_polygon, polyline_length, feature_kernel, KERNEL_RATIO, DEFAULT_LEVELS,
                    lu_solve, solve_ridge)
from .water import (tint_bands, coastline, danger_lines, hatch, coast_vignette, unsurveyed_band,
                    approximate_fringe, level_polygons, HATCH)
from .place import (Feature, PlaceReport, RadiusReport, place_features, solve_radii, feature_polygons,
                    spot_heights, soundings_along, soundings_lean, halton, dist_to_polyline, kind_of)
from .symbols import (SYMBOL_NAMES, symbol_defs, symbol_ids, use, sloop, lateral, light, flare, halo, lit_core,
                      traffic_signal, horn, anchorage, wreck, waypoint, station, fix, ldg_triangle, rep_ring,
                      ed_islet, correction_mark, correction, doubt, serpent, tick, rock, rock_d, SLOOP_DETAIL,
                      SLOOP_GLYPH)
from .furniture import (Jitter, stroke, op, width, set_night, weight_factor, frame, margin_graticule, two_ring_rose,
                        clock_rose, Zone, source_diagram,
                        area_key, paper, plate_mark, course, course_samples, compass_bearing, lateral_offset,
                        track_lines, check_lines, restricted_line, catmull_rom, polyline_at, hatch_lines,
                        hatch_paths)

# class of lettering -> (T5 role, slant). Upright: measured, land, structures. Italic: floating
# things, water names, illustrative figures, doubt (07, 13, STANDARDS 1).
LETTERING = {
    "island-name":      ("place-land", "upright"),
    "shoal-name":       ("place-water", "italic"),
    "sea-name":         ("sea-name", "italic"),
    "harbour-name":     ("title", "upright"),
    "spot-height":      ("label", "upright"),
    "sounding":         ("texture", "upright"),
    "sounding-illustrative": ("texture-italic", "italic"),
    "contour-figure":   ("contour-figure", "upright"),
    "bearing":          ("label", "upright"),
    "mark-label":       ("label-italic", "italic"),     # R "2" Fl R 4s — floating things slope
    "light-label":      ("label", "upright"),           # Grafana Lt · Fl 15s — a structure
    "doubt":            ("label-italic", "italic"),     # ED · Rep · SD · PA
    "wreck-label":      ("label-italic", "italic"),     # Wk 'YY
    "fix-label":        ("label", "upright"),           # OCT 2025 (measured)
    "note":             ("note", "italic"),             # the pencil note
    "caption":          ("label-caps", "upright"),
    "unit-line":        ("label-caps", "upright"),
    "var-label":        ("label-caps", "upright"),
    "rose-numeral":     ("label", "upright"),
    "zone-letter":      ("label", "upright"),
    "legend":           ("label", "upright"),
    "correction-old":   ("texture", "upright"),
    "correction-new":   ("texture-italic", "italic"),
    "area-key":         ("texture", "upright"),
}

__all__ = [n for n in dir() if not n.startswith("_")]
