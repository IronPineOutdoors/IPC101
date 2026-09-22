# N1.4 faceplate - enlarged P504 opening

The user confirmed the hole edge blocks directional movement while select works. N1.4 enlarges the front P504 aperture from **6.2 to 8.0 mm**, adding **0.9 mm clearance per side**. It keeps N1.3's compact traced tree + IPO and CrossWind artwork, measured ARM-left/PULL-right alignment, 2 mm plate, and exact rear P504 cradle. Existing R1 labeled caps and I.1 structure remain unchanged.

- [White faceplate](CrossWind_IPC101_Faceplate_RevN14_WHITE_PETGHF.stl)
- [Black inlay](CrossWind_IPC101_Faceplate_RevN14_BLACK_AMS.stl)
- [Preview and opening comparison](N14_faceplate_preview.png)

Import both files as parts of one object, preserve their shared coordinates, and use the existing face-down two-material profile. Do not mirror the parts. The rear revision mark is IPC101-FP-N1.4.

The exports pass closed-mesh checks, aperture clearance, unchanged rear cradle/artwork checks, and 42 ARM/PULL clearance checks. A reference 5 mm hub clears at 1.4 mm radial offsets in eight directions; this is a reference envelope, not a measurement of the installed cap. Actual four-direction movement, select and return remain to be checked with the assembled hardware. The [8 mm coupon](P504_DIRECTIONAL_FIT.md) provides the same opening and cradle for a smaller test print.

```powershell
python -B mechanical/enclosure/render_faceplate_n1.py --revision N14 --openscad "C:\path\to\openscad.com"
python -B mechanical/enclosure/verify_faceplate_n14.py
python -B mechanical/enclosure/preview_faceplate_n14.py
```

Keep branding/iron_pine_tree_unit.stl with the SCAD source. Earlier N1-N1.3 exports still have the 6.2 mm opening and are superseded for this reprint.
