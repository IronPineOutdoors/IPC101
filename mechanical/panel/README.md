# Rev D OLED fit correction

For the next enclosure fit trial, print **`CrossWind_ControlPanel_RevD_OLED_8mm_Right_IPC101.stl`**. This addresses the reported OLED collision with the enclosure's left sidewall by shifting the display window and all four OLED mounting holes 8 mm right as viewed from the front.

- Faceplate remains 150 x 100 x 2 mm; its four enclosure mounting holes are unchanged.
- OLED centre: (54.5, 63.5) mm. Window remains 57 x 28 mm.
- OLED hole centres: X=20.1/88.9 mm, Y=44.1/82.9 mm; hole diameter 3.2 mm.
- ARM/PULL, navigation, LED and existing engraved branding remain unchanged.
- This is only the OLED fit correction. The illustrated swoosh-logo/STOP concept has not been incorporated into this STL.
- Manufactured PCB geometry is unchanged. OLED mounting holes on that PCB remain at the old location; the shifted OLED mounts to the faceplate and uses its harness, not a forced alignment to the PCB's old OLED holes.

Run `python mechanical/panel/generate_ipc101_rev_d.py` from the project root. Rev D reuses the Rev C faceplate builder with an explicit OLED centre; the Rev C generator retains its original default and historical exports. `IPC101_RevD_FACEPLATE_COORDINATES.csv` is faceplate-only and does not supersede PCB fabrication coordinates.

Geometric checks passed: one valid connected solid; exact panel bounds; four display and four enclosure mounting holes open; window open; zero faceplate overlap with Rev H shell. The nominal 73 x 43 mm OLED PCB envelope ends at X=91 mm, leaving 5 mm to the 18 mm navigation-cap envelope. A 1.6 mm thick OLED board envelope clears the Rev H shell at tested rear offsets of 3, 5, 10 and 15 mm. These are envelope checks, not a verification of the actual OLED glass, connectors, screws, standoffs or full controller-PCB stack. Fit the actual assembly before tightening the faceplate.

---

# IPC-101 Rev C Control Panel

The Rev C mechanical set replaces the Crosswind Rev B encoder layout with the IPC-101 operator layout while retaining the verified 150 x 100 mm panel envelope, corner fasteners, ARM/PULL centres, and OLED hole spacing.

Generated files:

- `CrossWind_ControlPanel_RevC_IPC101.stl`
- `CrossWind_Tactile_Button_Cap_RevC_IPC101.stl`
- `CrossWind_Adafruit504_Nav_Cap_RevC_IPC101.stl`

Run `python generate_ipc101_rev_c.py` to regenerate the models. Dimensions are millimetres. Viewed from the recessed-logo/front surface, the OLED is on the operator's left, the Adafruit 504 navigation control is on the right, ARM and PULL are below, and the RGB indicator aperture is centred between the buttons and display row. The D-pad aperture is 8.0 mm for added cap clearance.

Use `CrossWind_ARM_Button_Cap_RevC_IPC101.stl` and `CrossWind_PULL_Button_Cap_RevC_IPC101.stl` for the installed controls. They retain the verified generic tactile-cap fit and add 0.45 mm raised lettering on the operator-facing surface. `CrossWind_Tactile_Button_Cap_RevC_IPC101.stl` remains available as an unlabeled spare.

The Adafruit 504 navigation cap uses the proven TrailBoss P504 receptacle: a 3.30 x 3.30 mm square socket, 3.50 mm deep, with a 1.80 mm face floor. Its 5.0 mm rear hub clears the faceplate's revised 8.0 mm opening.

The power-switch region is reserved but is intentionally not cut until its exact rated part and mounting geometry are selected. Print a faceplate and both caps for fit verification before production fabrication.
