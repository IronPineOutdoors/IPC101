# Crosswind IPC-101 control box Rev D

This enclosure replaces the provisional blue Crosswind control pod shown in the September 4 fit-test photos. It retains the comfortable 47-degree face angle while removing the features that made the first pod difficult to mount.

Use `CrossWind_IPC101_Control_Box_RevD_PRINT.stl` for slicing. The installed-orientation STL is supplied for assembly checks and CAD visualization.

## Mounting improvements

- 156 mm enclosure width with 3 mm registration margins around the 150 mm faceplate
- Four internal rear mounting pads with 4.5 mm wood-screw clearance holes and 9.5 mm recessed-head pockets
- Mounting screws are installed from inside while the faceplate is removed
- Flat rear datum at the wooden mounting surface; no projecting tabs behind the wood plane
- Four 11 mm face bosses with 3.4 mm screw clearance and captive M3 hex-nut traps
- 1.2 mm lateral faceplate registration rails
- 42 x 20 mm bottom cable exit for the keypad, OLED, and STOP harness groups
- 3 mm nominal walls and the retained 47-degree viewing angle

The current model assumes the same 101.6 mm (4 inch) wooden vertical mounting surface shown in the photos. Use pan-head or washer-head wood screws no larger than 9.5 mm at the head. Insert four standard M3 nuts into the face-boss traps before installing the IPC-101 PCB/faceplate stack.

Print the `PRINT` file with its flat wooden-mounting plane on the build plate. The rear pads and shell edges provide bed contact while the 47-degree face remains self-supporting. PETG or ASA is preferred for the outdoor prototype. Use at least four perimeters and 25 percent infill. Confirm screw length, cable bend clearance, faceplate seating, and access to all four wood screws on a fit print before outdoor service.

Regenerate with:

```powershell
python .\generate_crosswind_control_box.py
```

Requires `manifold3d`.
