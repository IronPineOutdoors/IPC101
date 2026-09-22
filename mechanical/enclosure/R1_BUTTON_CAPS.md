# ARM/PULL caps R1 and matching N1.2 faceplate

Status: **PRINTABLE FIT PROTOTYPE — CAD VERIFIED; PHYSICAL FIT PENDING**.

The user measured 12.82 mm from the front of the faceplate to the unpressed button face, with approximately 2.05 mm faceplate thickness. That gives 10.77 mm from the back of the plate to the button. This replaces the earlier estimate for cap reach; it does not alter the printed cradle or nominal PCB CAD spacing.

R1 is a sliding plunger with a retaining flange behind the faceplate. Its flat 5.5 mm diameter stem tip contacts the reported 6 mm actuator; it is not a socket or press fit. Both caps use the supplied shared measurement. Confirm both actual switches during assembly.

| Dimension | R1 value |
|---|---:|
| Face above measured faceplate front at rest | 1.50 mm |
| Guide through opening | 15.2 x 10.0 mm, radius 2 corners |
| Existing N1 opening | 16.0 x 10.8 mm, radius 2 corners |
| Rear retaining flange | 18.0 x 12.8 x 1.0 mm |
| Stem beyond rear flange | 9.57 mm |
| Tip reach from faceplate back | 10.57 mm |
| Provisional resting gap to actuator | 0.20 mm |
| Total cap depth, including face and stem | 14.12 mm |
| Flush black label depth | 0.60 mm |

## Print files

Print one cap first to check travel before making the second. The same stem geometry is used for ARM and PULL.

| Cap | White body | Black face label |
|---|---|---|
| ARM | [ARM white](CrossWind_IPC101_ARM_Cap_R1_WHITE_PETGHF.stl) | [ARM black](CrossWind_IPC101_ARM_Cap_R1_BLACK_AMS.stl) |
| PULL | [PULL white](CrossWind_IPC101_PULL_Cap_R1_WHITE_PETGHF.stl) | [PULL black](CrossWind_IPC101_PULL_Cap_R1_BLACK_AMS.stl) |

Import each cap's white/black pair as parts of **one object**. Import the other cap as a separate object; importing all four files into a single object would superimpose the two caps. Preserve each pair's shared coordinates and do not mirror them. The complete words are already oriented to read from the operator side.

Print face/lettering down on the bed with the stem upward. Use PETG, 0.20 mm layers, four walls and solid infill for these small parts. Inspect the first three layers for the 0.6 mm flush lettering. The rear flange has 1.4 mm ledges around the guide; inspect the slicer's overhangs and use local support under these ledges if needed. Clean the flange undersides and guide surfaces without rounding away the retaining ledge. Avoid an elephant foot around the sliding guide. `A-R1` / `P-R1` is recessed on the rear flange.

## Assembly and first fit

Insert each cap from the back of the faceplate, with its labeled face through the opening and the flange retained behind it. ARM goes in the left opening, PULL in the right when viewed from the front. Keep the loose caps supported while attaching the faceplate to the bezel; they are not captive when the plate is removed from the assembly.

Confirm each cap slides without binding, the switch is unpressed at rest, and light pressure actuates and releases it reliably. The return comes from the switch; a loose plunger may retain a small amount of free play. The 0.20 mm gap is provisional and does not guarantee return in every orientation. If either cap sticks or holds a switch pressed, stop and report which one and whether the flange/guide or stem is contacting. Do not force the cap. R1 adds no positive overtravel stop; the 1 mm CAD motion sweep is geometric clearance, not an instruction to compress the switch by 1 mm.

## Faceplate with labels on caps only

The [N1.2 tree correction](REV_N12_FACEPLATE.md) supersedes the generic tree in N1.1. R1 cap geometry is unchanged.

The matching **N1.2** faceplate removes the duplicate ARM/PULL text above the openings. It retains N1's measured button locations and uses the tree traced from the supplied wordmark, with unchanged OLED/D-pad locations, mounting holes and rear cradle. Its hidden rear mark reads `IPC101-FP-N1.2`. Existing N1 remains mechanically compatible with these caps if already printed.

- [N1.2 white faceplate](CrossWind_IPC101_Faceplate_RevN12_WHITE_PETGHF.stl)
- [N1.2 black inlay](CrossWind_IPC101_Faceplate_RevN12_BLACK_AMS.stl)
- [Caps and panel preview](R1_button_caps_preview.png)

Use the N1.2 pair for the upcoming full faceplate reprint with labeled caps. Import them together as one object, just like the N1 pair. Do not combine N1 and N1.2 materials.

## Verification and source

`R1_button_caps_verification.json` records 332 checks: closed/wound cap bodies and inlays; release gap; flange retention; 21 positions over 1 mm of geometric inward travel for each cap against both faceplates, bezel, cradle, R3, bare PCB and shell; hardware clearance; and preserved N1.2 structural geometry. Actual switch movement, component envelopes, fit of both printed caps and environmental sealing remain physical checks.

Sources: `CrossWind_IPC101_Button_Caps_R1.scad`, `CrossWind_IPC101_Faceplate_RevN12.scad`.

```powershell
python -B mechanical/enclosure/render_button_caps_r1.py --openscad "C:\path\to\openscad.com"
python -B mechanical/enclosure/render_faceplate_n1.py --revision N12 --openscad "C:\path\to\openscad.com"
python -B mechanical/enclosure/verify_button_caps_r1.py
python -B mechanical/enclosure/preview_button_caps_r1.py
```

Old Rev C cap files remain historical references; their short stems do not match this measured stack.
