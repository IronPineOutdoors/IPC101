# N1 faceplate correction in progress

Not a finished faceplate release. M4 remains on reprint hold.

## Physical button measurements, 2026-09-21

User measured the PCB upright, component/buttons facing the operator:

| Position | Measurement | Center from operator's left edge |
|---|---|---|
| Left button | 46.88 mm from left edge | 46.88 mm |
| Right button | 34.33 mm from right edge | 115.67 mm, assuming 150 mm PCB width |

These differ from M4's operator-view openings at 33.5 and 103.5 mm. Required measured shifts are +13.38 and +12.17 mm, respectively. Do not mirror the entire faceplate to fix this: that would also move the display, navigation mount and artwork.

The measured spacing is 68.79 mm; the PCB file's nominal button spacing is 70 mm. Preserve the reported measurements as measurements, not as a claim that the PCB design changed. Check the strip physically before adopting them in a finished faceplate. The left/right ARM/PULL function assignment is awaiting user confirmation; no labels are assigned by the strip.

## Optional quick alignment print

`CrossWind_IPC101_Button_Check_N1_PRINT.stl`: 150 x 35 x 2 mm strip, with the original two lower mounting holes and original 16 x 10.8 mm rounded button openings. Vertical button coordinate remains 20.75 mm from the bottom; the user has not remeasured it. Recessed N1 TEST is on the rear face.

Print flat as exported. Fit the strip at the bottom of the bezel using its two lower mounting holes, rear marking toward the PCB. Check both real buttons without forcing the strip or preloading the controls. No need to interrupt the STOP pod/cover prints for this check.

The strip's exported X coordinates are 103.12 and 34.33 mm. This is the existing face-down manufacturing convention, which reverses X relative to the operator view; it does not undo the measured correction. Generator: `python -B mechanical/enclosure/generate_n1_button_check.py`. Watertight export and bezel/cradle/bare-PCB clearance results are in `N1_button_check.json`.

## Tree correction

Inspection of M4 shows that the tree base extends into the OUTDOORS lettering: its connected black mesh includes part of that lettering. Planned correction is a distinct flat-bottomed trunk separated from the text. Final white recesses and black inlay must be generated and verified together. No corrected full-faceplate STL has yet been issued.
