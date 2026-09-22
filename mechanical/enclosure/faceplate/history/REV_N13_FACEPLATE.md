# N1.3 — compact tree and IPO option

**Superseded for reprinting by [N1.4](../REV_N14_FACEPLATE.md): same artwork, enlarged 8 mm P504 aperture. N1.3 retains the restrictive 6.2 mm opening.**

This option replaces the full IRON PINE / OUTDOORS group with the actual traced tree and bold **IPO** below it. CrossWind keeps its existing size and graphics, making the product name more prominent. N1.2 remains available with the full wordmark.

- [Side-by-side and badge close-up](N13_faceplate_preview.png)
- [N1.3 white faceplate](CrossWind_IPC101_Faceplate_RevN13_WHITE_PETGHF.stl)
- [N1.3 black inlay](CrossWind_IPC101_Faceplate_RevN13_BLACK_AMS.stl)

Import the white/black pair together as parts of one object. Preserve their common coordinates; do not mirror or combine revisions. Use the existing face-down PETG/two-material profile and inspect the first layers for legible IPO lettering and the tree's center channels.

The tree is 12.5 mm tall at its original aspect ratio, approximately 13.51 mm wide. IPO uses 3.2 mm bold font sizing, the same sizing used for the R1 cap labels; actual glyph bounds and spacing are recorded in `N13_faceplate_verification.json`. The combined badge is approximately 17 mm tall. It replaces the small OUTDOORS lettering rather than shrinking it further. This is a CAD-verified print option; physical lettering quality remains to be checked.

All button centers, apertures, mounting holes, panel thickness, rear P504 cradle and R1 cap geometry remain unchanged. The hidden revision mark is `IPC101-FP-N1.3`. The verifier checks that combined mechanical geometry outside that mark matches N1.2, CrossWind artwork is unchanged, the tree matches its source mesh, IPO has three separate glyphs with clear space below the tree, and both caps clear the plate through 21 inward positions each.

```powershell
python -B mechanical/enclosure/tooling/render_faceplate_n1.py --revision N13 --openscad "C:\path\to\openscad.com"
python -B mechanical/enclosure/tooling/verify_faceplate_n13.py
python -B mechanical/enclosure/tooling/preview_faceplate_n13.py
```

Keep the `branding/iron_pine_tree_unit.stl` dependency with the faceplate SCAD source. No previously printed mechanical part needs changing for this badge option.
