# Tree traced from supplied Iron Pine artwork

`iron_pine_transparent_wordmark.png` is an unchanged copy of the user-supplied file from `Crosswind/branding/iron-pine/`. The other supplied mockup sheet and small reference image were visual references; the transparent wordmark supplies the geometry.

`trace_tree.py` selects the main tree and its separate center triangle from the alpha channel. It excludes adjoining letters and OUTDOORS. This preserves the original swept branches, open central channel, small center triangle, asymmetric raster outline and aspect ratio. It does not substitute a generic pine or a font glyph.

The trace removes isolated raster pinholes of at most 4 square pixels and simplifies the pixel staircase with 0.7 pixel tolerance. `tree_trace_verification.json` records the source SHA-256, crop, seed pixels, threshold, approximately 98.9% silhouette intersection-over-union and maximum boundary deviation under 0.085 mm at the final print size. These compare the vector with the thresholded source alpha, not with an unavailable original vector master.

Outputs:

- `iron_pine_tree_trace.svg`: editable vector silhouette in source-pixel coordinates.
- `iron_pine_tree_trace.scad`: normalized polygon paths, height 1 and bottom Y=0.
- `iron_pine_tree_unit.stl`: closed two-component extrusion of the same trace, thickness 0.55 mm. N1.2 imports this mesh to avoid OpenSCAD 2021's failed triangulation of the detailed raster contour. It is a source dependency; keep it beside the SCAD/SVG.

The faceplate scales the tree to 13.26 mm high and approximately 14.33 mm wide, retaining its source aspect ratio. The tree remains separated from the existing OUTDOORS text. Very fine tapered tips can be shortened by a 0.4 mm nozzle; inspect the sliced first layers rather than thickening the brand shape without evidence.

Regenerate with `python -B mechanical/enclosure/branding/trace_tree.py`. Requires numpy, scipy, shapely, pymupdf and the project's manifold3d/STL helper. No source image is modified.
