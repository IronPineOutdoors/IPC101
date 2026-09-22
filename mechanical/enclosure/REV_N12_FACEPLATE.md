# N1.2 faceplate — tree from the actual Iron Pine wordmark

Current reprint revision for use with the R1 labeled ARM/PULL caps. Replaces N1.1's generic pine with a trace of the supplied transparent wordmark. The outline includes the swept branches, open center and separate center triangle, at the original aspect ratio. See [trace provenance](branding/README.md).

## Print these together

- [N1.2 white faceplate](CrossWind_IPC101_Faceplate_RevN12_WHITE_PETGHF.stl)
- [N1.2 black inlay](CrossWind_IPC101_Faceplate_RevN12_BLACK_AMS.stl)
- [Actual faceplate and tree close-up](N12_faceplate_preview.png)
- [Panel with R1 caps](R1_button_caps_preview.png)

Import the white/black pair as parts of **one object** with their shared coordinates. Do not mirror or independently center them. Front/graphics print at Z=0. Use the same two-color faceplate settings as N1.1 and inspect the tree's center channels and narrow tapered ends in the slicer's first layers. Artwork depth remains 0.55 mm. Do not mix material files from different revisions.

## Preserved fit

ARM remains left at 46.88 mm and PULL right at 115.67 mm from the operator-facing left edge, both 20.75 mm above the bottom. All aperture dimensions, OLED/D-pad locations, rear P504 cradle, faceplate thickness, mounting holes and R1 cap fit are unchanged. Labels remain on the caps, without duplicate panel ARM/PULL text. No existing cap, cradle, bezel, shell or STOP pod requires reprinting for this artwork change.

The hidden rear mark is `IPC101-FP-N1.2`. IRON/PINE/OUTDOORS lettering and the CrossWind graphics remain the existing faceplate artwork; only the tree is traced from the supplied logo.

## Verification and reproduction

`N12_faceplate_verification.json` checks the exported tree against the traced polygons, the two original tree components, white/black mesh validity, tree-to-OUTDOORS clearance, preserved surrounding artwork and combined mechanical geometry against N1.1 outside the rear revision mark. `R1_button_caps_verification.json` checks the caps against N1.2. These are CAD checks; the physical reprint and first-layer details remain to be checked.

```powershell
python -B mechanical/enclosure/branding/trace_tree.py
python -B mechanical/enclosure/render_faceplate_n1.py --revision N12 --openscad "C:\path\to\openscad.com"
python -B mechanical/enclosure/verify_faceplate_n12.py
python -B mechanical/enclosure/verify_button_caps_r1.py
python -B mechanical/enclosure/preview_faceplate_n12.py
python -B mechanical/enclosure/preview_button_caps_r1.py
```

The SCAD and the `branding/` trace dependencies must stay together. Earlier N1/N1.1 exports remain identifiable historical alternatives; use the N1.2 pair for the requested logo correction.
