# Rev M.4 faceplate / Rev I.1 fit audit

Status: **CAD CLEARANCE PASS - PHYSICAL VALIDATION PENDING**.

The supplied SCAD and both material STLs are retained unchanged. I.1 verification and preview now use the actual M.4 geometry rather than the plain faceplate envelope. No shell, cradle, bezel, R3 or faceplate print geometry changed in this integration.

## Source geometry

- Faceplate: 150 x 100 x 2 mm, four 3.2 mm mounting holes at (5,5), (145,5), (5,95), (145,95).
- White export bounds: (0,0,0)..(150,100,4.8). It is one watertight connected mesh.
- Black export: 36 watertight disconnected inlay bodies, intentionally separate lettering/graphics; Z=0..0.55. Load white and black in their shared coordinates, not as independently arranged objects.
- P504 rear cradle: 10.70 mm pocket, nominal 14.70 mm outside width, 2.80 mm projection behind the plate. Its slots and corner walls are included in the collision model.
- P504 aperture remains 6.2 mm, LED aperture 5.2 mm, and OLED window 57 x 28 mm. No N.1 aperture, artwork or cap changes were made.

## Assembly coordinate registration

The SCAD already applies `whole_mirror()` about X=75 to both exports. Do not mirror those STLs again. Their operator face is at raw Z=0 and back surface at raw Z=2. The assembly reference keeps exported X/Y and subtracts 2 mm from Z; consequently the back surface is at assembly Z=0 and the P504 cradle projects inward to Z=2.8.

The PCB component side must face the faceplate. Register the repository PCB coordinates as:

```
Xassembly = 150 - Xpcb
Yassembly = Ypcb
Zassembly = PCB_BACK - Zpcb
```

For a board whose bottom is Zpcb=0 and top is Zpcb=1.56, this is a physical 180-degree rotation about Y followed by translation. It puts the board top at Z=16.5 and bottom at Z=18.06. It is not a mirrored fabricated PCB. The rectangular board outline and symmetric four-hole pattern are unchanged, so the current R3/cradle print needs no modification.

The initial direct-XY comparison was inappropriate for this component-side-out orientation and produced a false ARM/PULL discrepancy. The corrected comparison reads placements from the actual repository `hardware/kicad/IPC101.kicad_pcb` and checks these against the supplied SCAD/export apertures:

| Control | Repository PCB X,Y | Installed PCB X,Y | M.4 aperture X,Y | Result |
|---|---|---|---|---|
| ARM / SW1 | 33.5,20.75 | 116.5,20.75 | 116.5,20.75 | Aligned |
| PULL / SW2 | 103.5,20.75 | 46.5,20.75 | 46.5,20.75 | Aligned |
| LED / D1 | 68.5,31 | 81.5,31 | 81.5,31 | Aligned reference; LED remains separately supported/wired |
| Navigation / SW3 | 105,63.5 | 45,63.5 | 105,63.5 | Faceplate-mounted P504 uses six flexible leads |
| OLED / DS1 | 46.5,63.5 | 103.5,63.5 | 46.5,63.5 | Faceplate-mounted display uses a harness |

OLED and P504 do not sit on their PCB footprint coordinates in this assembly. This follows the wired, faceplate-supported architecture; do not install them as rigid structural connections between PCB and faceplate. Physical wire lengths, connector orientation and strain relief remain to be checked.

## Checks passed

- Both actual faceplate materials, including the rear cradle, clear I.1 shell, bezel, cradle, R3 and bare-board reference.
- Four faceplate holes and control apertures agree with the registration above; board-mounted ARM/PULL positions align with their openings.
- Faceplate and cassette screw envelopes and driver access pass with the actual faceplate in place. PCB screw access passes with the faceplate/bezel removed.
- All previous I.1 checks still pass: six closed connected exports, exact Rev H interface, rail/pin clearance, front aperture, service motions, rear/floor/port integrity, R3 support, 16.5 mm spacing and print bounds.
- Updated `RevI1_preview.png` was visually inspected with actual white panel and black inlays.

These checks do not model the mounted display, harness connectors, P504 pedestal/cap travel, final button caps, LED holder or every populated PCB component. They therefore establish shell/faceplate compatibility and coordinate alignment, not complete populated-assembly validation.

## Next physical check

Finish the cradle print. Check that R3 seats without force and the four holes/nut pockets fit. Print the I.1 bezel next. Place the actual PCB with its component side facing the faceplate and check ARM beneath ARM and PULL beneath PULL before tightening. Measure the 16.5 mm gap at all four corners and exercise both controls without preload. Check the OLED harness and P504 leads while lifting the bezel off for service. Keep final cap stems, pedestal/aperture refinement and gasket compression adjustable until these measurements are recorded.
