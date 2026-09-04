# IPC-101 Rev C Control Panel

The Rev C mechanical set replaces the Crosswind Rev B encoder layout with the IPC-101 operator layout while retaining the verified 150 x 100 mm panel envelope, corner fasteners, ARM/PULL centres, and OLED hole spacing.

Generated files:

- `CrossWind_ControlPanel_RevC_IPC101.stl`
- `CrossWind_Tactile_Button_Cap_RevC_IPC101.stl`
- `CrossWind_Adafruit504_Nav_Cap_RevC_IPC101.stl`

Run `python generate_ipc101_rev_c.py` to regenerate the models. Dimensions are millimetres. Viewed from the recessed-logo/front surface, the OLED is on the operator's left, the Adafruit 504 navigation control is on the right, ARM and PULL are below, and the RGB indicator aperture is centred between the buttons and display row. The D-pad aperture is 8.0 mm for added cap clearance.

Use `CrossWind_ARM_Button_Cap_RevC_IPC101.stl` and `CrossWind_PULL_Button_Cap_RevC_IPC101.stl` for the installed controls. They retain the verified generic tactile-cap fit and add 0.45 mm raised lettering on the operator-facing surface. `CrossWind_Tactile_Button_Cap_RevC_IPC101.stl` remains available as an unlabeled spare.

The power-switch region is reserved but is intentionally not cut until its exact rated part and mounting geometry are selected. Print a faceplate and both caps for fit verification before production fabrication.
