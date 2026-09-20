# Crosswind IPC-101 control box Rev G

This enclosure replaces the provisional blue Crosswind control pod shown in the September 4 fit-test photos. It retains the comfortable 47-degree face angle while removing the features that made the first pod difficult to mount.

Use `CrossWind_IPC101_Control_Box_RevG_PRINT.stl` for slicing. The installed-orientation STL is supplied for assembly checks and CAD visualization. Rev G keeps the unobstructed service opening and extends all four faceplate bosses 1.2 mm outward so their screw-hole faces are coplanar with the faceplate seating datum. Earlier enclosure STLs are obsolete.

## Mounting improvements

- 156 mm enclosure width with 3 mm registration margins around the 150 mm faceplate
- Four internal rear mounting pads with 4.5 mm wood-screw clearance holes, 9.5 mm recessed-head pockets, and 11 mm straight driver-access tunnels
- Mounting screws are installed from inside while the faceplate is removed
- Flat rear datum at the wooden mounting surface; no projecting tabs behind the wood plane
- Four 11 mm face bosses with front-loaded 4.2 x 6.0 mm M3 heat-set-insert pockets and 3.2 mm screw relief
- 1.2 mm lateral faceplate registration rails
- 42 x 20 mm bottom cable exit for the keypad, OLED, and STOP harness groups
- One unobstructed 136 x 86 mm front service opening inside the perimeter rim
- 3 mm nominal walls and the retained 47-degree viewing angle

The current model assumes the same 101.6 mm (4 inch) wooden vertical mounting surface shown in the photos. Use pan-head or washer-head wood screws no larger than 9.5 mm at the head. Install and heat-test four M3 inserts from the face side before installing the IPC-101 PCB/faceplate stack; adjust the 4.2 mm pilot in the generator if the selected insert supplier specifies another hole size.

Print the `PRINT` file with its flat wooden-mounting plane on the build plate. The rear pads and shell edges provide bed contact while the 47-degree face remains self-supporting. PETG or ASA is preferred for the outdoor prototype. Use at least four perimeters and 25 percent infill. Confirm screw length, cable bend clearance, faceplate seating, and access to all four wood screws on a fit print before outdoor service.

## Current redesign direction — 2026-09-20

Rev G remains the reference for the **proven mounting-bracket / wooden mounting interface**, but its upper enclosure geometry is no longer considered frozen.

Physical IPC-101/faceplate mock-up testing found that the Rev G upper wall angle and screw-receptacle/boss geometry interfere with the PCB/control-panel stack. The next enclosure revision should therefore preserve the useful Rev G mounting-bracket interface while redesigning the enclosure body around IPC-101.

Current working requirements:

- Preserve the Rev G mounting-bracket / wooden mounting interface unless testing identifies a problem with it.
- Preserve the established IPC-101 faceplate footprint and control layout.
- Design the PCB carrier/chassis and enclosure as a matched assembly rather than forcing IPC-101 into the Rev G upper geometry.
- Current nominal spacing from the **back surface of the faceplate to the top surface of IPC-101 is approximately 16.5 mm**. This is a prototype design target, not yet a fabrication-frozen dimension; it was selected to provide clearance for the OLED wiring/harness connectors.
- The carrier/chassis should establish the PCB-to-faceplate relationship and carry the PCB mechanically. The enclosure should primarily provide structure, mounting and environmental protection.
- Provide a rear panel connector for the IPC-101-to-CrossWind-Alpha harness. Connector family, cutout and pin count remain **TBD** until the required Alpha interface conductors are confirmed.
- Avoid internal screw bosses or wall slopes that intrude into the IPC-101/control-component envelope.
- Maintain service access so the control-panel/PCB assembly can be removed without disturbing the CrossWind mounting interface.

Do not use the approximately 16.5 mm spacing as a final drilling/fabrication dimension until the carrier fit test verifies OLED, P504, ARM/PULL switch and harness clearances.

## Development record

As mechanical work progresses, record useful confirmed dimensions, physical fit-test results, superseded assumptions and revision decisions in the repository rather than relying only on conversation history. CAD/STL revisions should be accompanied by source files and a short status note identifying whether they are conceptual, test-fit, physically validated or frozen.

Regenerate Rev G with:

```powershell
python .\generate_crosswind_control_box.py
```

Requires `manifold3d`.
