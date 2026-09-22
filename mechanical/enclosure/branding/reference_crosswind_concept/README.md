# Supplied CrossWind artwork on faceplate

Visual study requested 2026-09-22. Uses the supplied crosswind_transparent_logo.png alpha silhouette, retaining the actual slanted lettering and swept forms. The preferred upper-left stacked tree branding remains. CrossWind is 58 x 13.176 mm, placed 78 mm from the left and 3 mm from the top.

[Faceplate preview](faceplate.png) / [CrossWind detail](crosswind_detail.png). The source PNG is preserved unchanged with SHA-256 in trace_report.json. Trace uses alpha >180, discards components under 100 pixels and pinholes up to 4 square pixels, and simplifies by 0.7 pixel. Silhouette intersection-over-union is 0.991. Metallic shading is flattened into a monochrome inlay concept; fine tapered ends still need printability review before CAD release.

Regenerate with `python -B mechanical/enclosure/tooling/preview_reference_crosswind.py`. Uses the previous stacked_brand_wind_concept/faceplate.svg for the panel and approved tree layout. Production SCAD/STLs remain unchanged. The LED hole remains the N1.4 5.2 mm reference pending bubble tests; cap outlines are schematic, with shaft shortening pending physical measurements.
