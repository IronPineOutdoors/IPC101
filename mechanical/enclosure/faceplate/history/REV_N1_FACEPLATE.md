# N1 faceplate — current reprint files

Status: **CAD VERIFIED; PHYSICAL REPRINT FIT PENDING**. Replaces M4 for the next faceplate print. R3, I1 bezel/cradle/shell and the S1 STOP pod/cover geometry are unchanged.

The subsequent [N1.1 faceplate and R1 labeled caps](../../controls/buttons/R1_BUTTON_CAPS.md) are the current choice when using labels on the cap faces. N1 remains compatible and retains duplicate panel labels.

## Corrected layout

Viewed from the operator/front, upright:

| Feature | X from left edge | Y from bottom | Basis |
|---|---:|---:|---|
| ARM, left | 46.88 | 20.75 | User's measured X and confirmed function; existing Y |
| PULL, right | 115.67 | 20.75 | 150 minus user's 34.33 mm right-edge measurement; existing Y |
| D-pad/P504 | 45 | 63.5 | Existing wired faceplate position |
| OLED | 103.5 | 63.5 | Existing wired faceplate position |
| LED | 68.5 | 31 | Existing wired faceplate position |

The user confirmed ARM left/PULL right and reported the OLED/D-pad positions were swapped on the PCB. The replacement follows the physical button measurements; it does not infer function labels by flipping the PCB file. Wired OLED and navigation locations on the faceplate remain as M4. Labels now follow their corrected button openings.

M4's operator-view button centers were 33.5 and 103.5 mm. N1 moves them right by 13.38 and 12.17 mm respectively. The measured 68.79 mm spacing differs from the PCB file's 70 mm nominal spacing; retain that distinction and verify the physical fit. The optional N1 button-check strip uses the same measured locations. Vertical positions and aperture sizes were not changed or remeasured.

The tree now has stepped branches and a flat-bottomed trunk. The former pointed base joined the OUTDOORS lettering; N1 leaves a verified approximately 1.03 mm gap. White recesses and black artwork are regenerated together. A hidden rear `IPC101-FP-N1` mark identifies the new print.

## Print together as one two-material object

- [White PETG-HF body](CrossWind_IPC101_Faceplate_RevN1_WHITE_PETGHF.stl)
- [Black AMS inlay](CrossWind_IPC101_Faceplate_RevN1_BLACK_AMS.stl)
- [Actual export preview, including logo close-up](N1_faceplate_preview.png)

Select both STLs together and import as parts of **one object**, preserving their original common coordinates. Assign white and black materials. Do not independently center/arrange them, and do not mirror either file. Front surface is at Z=0, on the print bed. Match the successful M4 material/profile; use 0.20 mm or finer layers and check the first-layer inlays in the slicer. The artwork is 0.55 mm deep. Outline is 150 x 100 mm, panel thickness 2 mm, total height 4.8 mm including the rear navigation cradle.

Export X is 150 minus operator X because these files are oriented front-down. ARM therefore appears at exported X=103.12 and PULL at X=34.33. The [preview](N1_faceplate_preview.png) shows the readable operator view. That manufacturing conversion is intentional and already applied; do not add another mirror operation.

After printing, fit the faceplate to the existing bezel and confirm both buttons move freely without preload before tightening. Check the actual populated board, harness and P504 motion. The optional alignment strip remains available if another quick position check is preferred first.

## Checks and reproduction

`N1_faceplate_verification.json` records closed/wound meshes (one white body, 37 separate black inlay bodies), matching material recesses, complete button openings at the corrected locations, separated tree/lettering and unchanged combined body geometry outside the button/revision-mark regions. The rear P504 cradle is unchanged. Tiny overlap residuals below 0.001 mm3 reflect exported mesh precision.

`verify_rev_i1.py` passes with the N1 faceplate: shell, cradle, bezel, hardware and driver clearance; front service paths; exact Rev H mounting interface; original six I1 print exports. `generate_stop_s1.py` passes all 280 S1 checks against the N1 assembly. These checks do not establish physical button travel, populated-board clearance, structural qualification or weather sealing.

SCAD source: `CrossWind_IPC101_Faceplate_RevN1.scad`. Render both materials with OpenSCAD, tested with 2021.01 and installed Liberation Sans fonts:

```powershell
python -B mechanical/enclosure/tooling/render_faceplate_n1.py --openscad "C:\path\to\openscad.com"
python -B mechanical/enclosure/tooling/verify_faceplate_n1.py
python -B mechanical/enclosure/tooling/verify_rev_i1.py
python -B mechanical/enclosure/tooling/preview_faceplate_n1.py
```

M4 files remain identifiable as historical references; do not select them for this reprint.
