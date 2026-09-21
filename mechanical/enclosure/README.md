# Crosswind IPC-101 enclosure Rev H ? fit prototype

Rev H keeps the existing Rev C 150 x 100 mm faceplate and 47-degree angle, raises its lower edge from 7.5 to 32 mm, and separates the Crosswind mounting bracket from the enclosure. Rev G files remain for comparison; use the Rev H files below for the next fit evaluation.

## Files

- `CrossWind_IPC101_Box_RevH_PRINT.stl`: enclosure, floor on the print bed.
- `CrossWind_IPC101_Bracket_RevH_PRINT.stl`: Crosswind bracket, flat back on the bed.
- `CrossWind_IPC101_Wiring_Plate_RevH_PRINT.stl`: blank underside wiring plate.
- Corresponding `INSTALLED` files share one assembly coordinate system.
- `RevH_preview.png`: front without faceplate, rear with bracket, and side with faceplate. Blue is enclosure, gold bracket, green wiring plate.

## Faceplate and sealing geometry

All four mounting seats are defined at the same exact face-local Z=0 plane, using the Rev C hole centres (5,5), (145,5), (5,95), and (145,95) mm. The previous hull approximation and -1.2 mm seat offset are not used. The seating plane is also the rear face of the installed faceplate. Inserts load from the front into 4.2 mm diameter, 6 mm deep pockets. Confirm the actual insert specification and keep inserts flush or slightly below the seat.

A continuous 2 mm wide, 0.8 mm deep rectangular gasket groove runs inside the mounting screws (outer bounds X=8..142, Y=8..92 in panel coordinates). A nominal 1 mm thick gasket would compress to 0.8 mm when the plate reaches its hard seats; actual material/compression must be qualified. Use a continuous cut gasket, not four loose strips. The service opening is 128 x 78 mm. Its 5 mm deep rim may require OLED spacers: the existing 73 mm module extends to X=10 mm, slightly over the X=11 mm opening edge. Verify the complete PCB/display/control stack before printing a final assembly.

The rear is closed with no wood screw penetrations. The floor has a 44 x 18 mm wiring opening and a 66 x 36 x 3 mm removable blank plate. Four M3 screws at installed X=50/106, Y=9/33 attach to blind insert pockets. Its gasket groove is 2 mm wide by 0.8 mm deep, outside the opening and inside the screws. Select the connector from actual conductor count, cable diameter, electrical requirements, and mating access; add its manufacturer cutout to this plate. The blank seals the opening but cannot pass wires yet. No connector has been selected or electrical interface changed.

These are sealing provisions, not a demonstrated waterproof assembly. The existing display, navigation, LED, and button openings still need seals, and the printed shell and gasket compression require physical leak testing. Rain versus hose exposure remains unspecified.

## Detachable Crosswind bracket

The bracket is 140 x 92 mm with four 4.5 mm wood-screw clearance holes on 128 x 75 mm centres. Screw heads are exposed with the box removed; use heads no larger than 9.5 mm diameter and 3 mm projection. Confirm wood screw length for the actual Crosswind mounting surface.

Two external T rails slide into receivers on the closed enclosure back. Nominal side clearance is 0.4 mm and head-depth clearance is 0.35 mm per side. Lower the box onto the bracket, align the transverse 3.4 mm hole, and install a removable 3 mm retaining pin with positive clip retention through the left receiver and rail (approximately 20 mm grip; measure the printed part). The pin retains the box vertically; magnets are not required. Allow at least 65 mm of upward travel and access to the pin for removal. Manually unplug wiring before removal. Rail load capacity and pin accessibility require a mounted fit trial; this is not a qualified structural mount.

The assembled body is about 156 mm wide, 104.2 mm high, and 122.3 mm deep from the wood plane to the frontmost shell edge, excluding the faceplate and controls. The extra depth comes from moving the top of the inclined face outward to 32 mm to provide usable internal clearance. Check this projection on Crosswind before accepting the revision.

## Future transparent cover

Keep the top and sides available for a separate cover hinge/latch design. No hinge, magnet pocket, or cover is committed in this revision. During the Crosswind fit trial reserve a provisional 15 mm beyond the top and sides and 15 mm outward from the faceplate, then measure actual cap heights and opening sweep. The cover must not obstruct the bracket removal path. Transparent filament appearance and cover fit can be evaluated after enclosure fit is accepted.

## Print and fit sequence

1. Slice the three PRINT files. The box stands on its floor; use localized supports beneath the rear receiver bottoms and inspect the upper internal roof in the slicer. The bracket prints back-down. Check rail-slot bridging before committing to the print. Mesh verification does not establish support-free printability.
2. Before heat-setting inserts, check that the bare Rev C faceplate rests on all four seats without rocking and that screws align. Check display/PCB rear clearance and button travel with the actual parts.
3. Install inserts and gaskets; tighten evenly and check perimeter contact. Four screws and the existing 2 mm plate may not provide uniform gasket pressure without further reinforcement.
4. Mount the bracket, fit the rails and retaining pin, and confirm connector/hand clearance on Crosswind. Select the connector and cut only the removable wiring plate.
5. Fit seals to the remaining front openings and perform an unpowered leak test before claiming weather resistance.

Regenerate and verify with Python plus `manifold3d` and `numpy`:

```powershell
python mechanical/enclosure/generate_rev_h.py
python mechanical/enclosure/verify_rev_h.py
```

Verification checks connected closed meshes, zero box/bracket and box/port-plate interference, the actual Rev C faceplate against the enclosure, all four coplanar seating annuli, and bracket withdrawal at 71 positions. It also regenerates the preview. Physical print tolerances, component stack, mounting loads, and waterproofing remain unverified.

---

# Crosswind IPC-101 control box Rev G

This enclosure replaces the provisional blue Crosswind control pod shown in the September 4 fit-test photos. It retains the comfortable 47-degree face angle while removing the features that made the first pod difficult to mount.

For historical Rev G only, use `CrossWind_IPC101_Control_Box_RevG_PRINT.stl` for slicing. The installed-orientation STL is supplied for assembly checks and CAD visualization. Rev G keeps the unobstructed service opening and extends all four faceplate bosses 1.2 mm outward so their screw-hole faces are coplanar with the faceplate seating datum. Earlier enclosure STLs are obsolete.

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

## Current redesign direction — corrected 2026-09-21

The newly synced local files establish the **authoritative Rev H mounting architecture**:

- `CrossWind_IPC101_Box_RevH_INSTALLED.stl`
- `CrossWind_IPC101_Box_RevH_PRINT.stl`
- `CrossWind_IPC101_Bracket_RevH_INSTALLED.stl`
- `CrossWind_IPC101_Bracket_RevH_PRINT.stl`
- `CrossWind_IPC101_Wiring_Plate_RevH_INSTALLED.stl`
- `CrossWind_IPC101_Wiring_Plate_RevH_PRINT.stl`
- `generate_rev_h.py`
- `verify_rev_h.py`

Rev H already contains the required removable mounting interface: two external T-slot receivers on the enclosure mate with two T rails on the separate bracket, with a transverse retaining-pin feature. This **box-to-bracket interface is now the preserved mounting datum** for the next enclosure revision.

The files `CrossWind_IPC101_Control_Box_RevH_TESTFIT.scad`, `...RevH1_TESTFIT.scad`, and `...RevH2_TESTFIT.scad` were later exploratory test models and do **not** supersede the synced Rev H box/bracket assembly. They are retained only as development history and should not be used as the mounting baseline.

Current working requirements:

- Preserve the Rev H bracket geometry and the enclosure's mating T-slot receiver geometry unless physical testing identifies a problem.
- Redesign only the enclosure/control-stack region needed to fit IPC-101, OLED harness, P504 assembly, ARM/PULL controls and service wiring.
- Preserve the established IPC-101 faceplate footprint and control layout.
- Current nominal spacing from the **back surface of the faceplate to the top surface of IPC-101 is approximately 16.5 mm**. This remains a prototype target pending physical carrier validation.
- The PCB carrier/chassis should establish the PCB-to-faceplate relationship and carry the PCB mechanically.
- Keep a removable/flush connector provision for the IPC-101-to-CrossWind-Alpha harness, but do not cut the final connector opening until the actual connector is selected.
- Avoid internal bosses or wall slopes that intrude into the IPC-101/control-component envelope.
- Maintain service access so the operator panel/PCB assembly can be removed without disturbing the bracket mounted to CrossWind.

The next enclosure revision should start from `generate_rev_h.py`, preserving `build_bracket()` and the mating T-slot receiver geometry in `build_box()` as the known-good interface.

## Development record

As mechanical work progresses, record useful confirmed dimensions, physical fit-test results, superseded assumptions and revision decisions in the repository rather than relying only on conversation history. CAD/STL revisions should be accompanied by source files and a short status note identifying whether they are conceptual, test-fit, physically validated or frozen.

Regenerate Rev G with:

```powershell
python .\generate_crosswind_control_box.py
```

Requires `manifold3d`.
