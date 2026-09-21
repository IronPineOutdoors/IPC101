> **Current R3-compatible fit build: Rev I.1.** See [print order, hardware and assembly guide](REV_I1_ASSEMBLY.md) and [preview](RevI1_preview.png). Reuses the original R3 print. Earlier revisions below are historical; physical validation is pending.

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

## Current redesign direction â€” updated 2026-09-21

The existing physical CrossWind mount uses **channels that the enclosure fits/slides into**. This slide-channel engagement is now a **required preserved interface**.

Rev H/H1/H2 incorrectly treated the Rev G screw-hole pattern and gross rear dimensions as the complete mounting interface. That was insufficient. Rev H2 is rejected and must not be used as the mounting baseline.

Current working requirements:

- Preserve the proven enclosure-to-mount **channel engagement geometry exactly** in the next revision.
- Preserve the docking/channel region as a fixed datum; redesign the enclosure body only forward of that retained interface.
- Preserve the established IPC-101 faceplate footprint and control layout.
- Design the PCB carrier/chassis and enclosure as a matched assembly rather than forcing IPC-101 into the Rev G upper geometry.
- Current nominal spacing from the **back surface of the faceplate to the top surface of IPC-101 is approximately 16.5 mm**. This is a prototype design target, not yet a fabrication-frozen dimension; it was selected to provide clearance for the OLED wiring/harness connectors.
- The carrier/chassis should establish the PCB-to-faceplate relationship and carry the PCB mechanically. The enclosure should primarily provide structure, mounting and environmental protection.
- Provide a rear/upper-rear flush panel connector for the IPC-101-to-CrossWind-Alpha harness after the actual connector is selected. Connector family, cutout and pin count remain **TBD**.
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

---

## Rev I enclosure and carrier — TEST-FIT / PHYSICAL VALIDATION PENDING

This section supersedes the earlier "current redesign direction" where H-like names are ambiguous. The authoritative `generate_rev_h.py`, `CrossWind_IPC101_Box_RevH_*`, `Bracket_RevH_*`, and `Wiring_Plate_RevH_*` define the actual mounting baseline. The exploratory `Control_Box_RevH_TESTFIT.scad`, `RevH1_TESTFIT.scad`, and `RevH2_TESTFIT.scad` are **SUPERSEDED** and were not used for Rev I mounting geometry.

### Preserved interface and new artifacts

**FROZEN / PRESERVED:** unchanged Rev H bracket; the exact two external receiver solids extracted from the authoritative box at Y=-10..0; original rail/slot clearances, stops, transverse pin bore, installed coordinates and detachable slide concept. No Rev I bracket exists. Reuse the Rev H wiring plate too: its 44 x 18 mm port, four fastener positions and blank connector area remain. No connector family or cutout has been selected.

New sources: `generate_rev_i.py`, `verify_rev_i.py`, `preview_rev_i.py`. New printable artifacts: `CrossWind_IPC101_Box_RevI_{INSTALLED,PRINT}.stl` and `CrossWind_IPC101_Carrier_RevI_{INSTALLED,PRINT}.stl`. `RevI_preview.png` shows open shell, rear with bracket, installed side, carrier/PCB, exploded stack and center cutaway. Colors: grey shell/bracket, tan carrier, green PCB, ivory faceplate envelope. Reference PCB and faceplate are verification geometry, not new production designs.

### Datums, dimensions and load path

Units are mm. Face-local +Z points inward; Z=0 is the back of the faceplate. Angle remains 47 degrees. Face origin is the Rev H origin shifted 8 mm outward along installed Y; this is a deliberate prototype clearance allowance, not a change to docking coordinates. Faceplate footprint and four mounting centres remain 150 x 100 and (5,5), (145,5), (5,95), (145,95).

- Shell installed bounds: X=-9..165, Y=-10..121.912, Z=0..108.384; overall **174 x 131.912 x 108.384 mm**. Including the existing bracket and wiring plate: **174 x 136.912 x 111.384 mm**, excluding controls.
- Carrier PRINT bounds: **168 x 118 x 25.06 mm**. Installed bounds: X=-6..162, Y=16.327..119.718, Z=7.534..106.338.
- `FACEPLATE_TO_PCB_TOP = 16.5` is **PROVISIONAL**. Board rear seating plane is 18.06; carrier rear datum is 25.06. Changing the named spacing parameter moves the rear seats/frame and shell attachment seats together. Re-run all checks after any change; the shell depth is finite.
- Board thickness uses the user's confirmed **1.56** measurement. KiCad's nominal setup is **1.60**. Board outline and mounting centres agree with repository geometry. Hole reference diameter is 3.2; verify the fabricated holes before hardware assembly.
- Front shell aperture is 170 x 120, surrounding a 168 x 118 removable carrier bezel. Nominal opening-edge shell wall is 2 mm; rear and floor retain at least the tested 2.5 mm witness thickness outside intentional pockets/port. Carrier front/rear rails are 3 mm thick and 8 mm wide.

The PCB rests on four rear corner pads, with independent front-accessible mounting screws. Separate front corner pads support the faceplate; outboard posts and rails carry loads to four shell seats at face-local (-5,20), (-5,80), (155,20), (155,80). No switch, display, wire or solder joint supports the assembly. The component area between corner mounting lands is open. The outboard rails make the visible bezel larger than the original faceplate; this is an intentional fit-validation allowance.

Attachment hardware is a **prototype assumption**: M3 inserts in 4.2 mm diameter x 6 mm blind pockets; carrier attachment bores 3.4 mm with 6.5 mm head/driver clearance. Confirm actual insert OD/length, head diameter, screw engagement and driver reach before heating inserts. Faceplate pockets pass through the 6 mm front pads; PCB-seat pockets retain about 1 mm backing. Do not allow insert or screw protrusion into the PCB stack. Select screw lengths from the measured stack and chosen insert, not a generic length. Four carrier screws bear on the rear rail at the bottom of the driver recess.

### Assembly, printing and measurements

Print **the carrier first**, rear frame on the bed as supplied in PRINT orientation. Use PETG/PETG-HF with a 0.4 mm nozzle and inspect the slicer: the upper perimeter rail and corner pads require localized supports. Keep support scars off seating faces and clean the bores without enlarging them arbitrarily. Shell PRINT stands on its closed floor; inspect supports under receiver bottoms, internal roof and attachment seats. Both parts fit within a 256 mm build envelope. This verifies size, not printer calibration or support-free manufacture. Start with four perimeters; qualify actual walls, insert retention and rail strength on the first print.

With the carrier outside the shell, slide the bare PCB in through the open end between its front and rear frames; the verifier checks this board-only path. Fasten the PCB to the rear seats from the front, install the carrier in the shell, then attach the existing faceplate to its independent front seats. For service remove faceplate, unplug harnesses, remove four outboard carrier screws, and lift the cassette normal to the face. Board removal from the cassette reverses the end-insertion path. Populated-board and attached-harness service paths still require physical testing.

Measure/check on the carrier print:

1. All four PCB holes and faceplate holes, flat seating, board edge clearance and insert retention; do not bow the PCB by tightening.
2. Actual faceplate-back to PCB-top distance at all four corners, nominal 16.5. Record printed board thickness and any seat/support cleanup.
3. OLED connector and harness bend clearance, P504 cradle/pedestal and six-lead routing, ARM/PULL motion and wiring, LED holder reserve and access to all screw heads. No final cap-stem lengths follow from this CAD alone.
4. Side insertion/removal of the populated PCB and front cassette removal with the actual wiring disconnected.

Then print the shell and reuse the Rev H bracket/wiring plate. Check full rail engagement, pin access and positive retention, at least 70 mm available upward withdrawal travel, CrossWind projection, cassette fit, shell seat contact, and blank plate removal. Measure connector/cable/hand envelope before selecting a flush connector. Hidden recessed marks read `IPC101-ENC-RI TEST` and `IPC101-CARRIER-RI TEST`.

At initial Rev I generation, no R3 carrier or N/M.4 faceplate source was found. R3 was subsequently supplied and inspected; see the comparison below. N/M.4 remains unavailable. Existing Rev C/D faceplate generators and coordinate files were inspected but their obsolete control layout is not claimed as N/M.4. The preview uses only a 150 x 100 x 2 faceplate envelope with four mounting holes. Actual N/M.4 back features, assembled OLED/header dimensions, harness bend radii, P504 swept movement, populated PCB underside heights and final hardware remain **PHYSICAL VALIDATION PENDING**. Known P504 body/cradle, actuator and LED dimensions supplied for this task are context, not sufficient coordinates for a complete component collision model. Central control space is unobstructed; component-level clearance is not certified. N.1 artwork/aperture/caps/LED refinements remain deferred.

Environmental shell only: rear/floor are closed except the intentional removable bottom service port. Carrier-to-shell clearance is an unsealed prototype joint, and faceplate sealing has not been engineered/qualified for this larger cassette. Keep the prototype dry; gasket lands/compression and leak testing are required before outdoor deployment. No waterproof claim is made.

### Reproduction and verification

```powershell
python mechanical/enclosure/generate_rev_i.py
python mechanical/enclosure/verify_rev_i.py
python mechanical/enclosure/preview_rev_i.py
python mechanical/enclosure/verify_rev_h.py
```

Dependencies: Python, manifold3d, numpy, trimesh. Verification checks generated and exported Rev I closed, consistently wound, connected meshes, bounds and print-bed placement; exact Boolean equality of the entire preserved rear interface; zero installed and 71-position (0..70 mm) bracket interference; pin passage; carrier/PCB/faceplate clearance; 66 front cassette withdrawal positions; bare-board end insertion; four PCB seat annuli and bores; parameterized spacing; rear/floor witness solids and unobstructed service port. Export checks compare bounds and volumes to their source solids. Preview inspection supplements these checks; neither proves physical fit or loading.

**Inherited Rev H export limitation:** the frozen bracket's pin bore is exactly tangent to its stem face at installed Y=-5.3, Z=40, across X=27..33. Both existing bracket STLs have one welded edge with four incident triangles, so trimesh does not classify them as watertight. The authoritative manifold model passes the original indexed-edge verification. This is explicitly reported by the Rev I audit, not silently repaired or called a new Rev I failure. Existing bracket files remain unchanged; inspect the known working bracket's slicer behavior. All newly generated Rev I exports must pass strict welded-mesh checks without exceptions.


### Recovered R3 carrier - inspected 2026-09-21

The user subsequently supplied `IPC101_RevA_RearCarrier_R3.scad` and `.stl`. Both were inspected without modification. They are the recovered reference for the previously tested rear carrier; this inspection establishes no additional physical validation.

R3 has bounds (-3,-3,0)..(153,103,7.4): 156 x 106 x 7.4 mm. The source defines a 2.4 mm base, 6 mm perimeter rails, 5 mm cross-ribs, and four 8 mm diameter posts rising 5 mm above the base. Their 3.4 mm through-holes are at (5,5), (145,5), (5,95), (145,95). The STL is watertight and one connected component; its bounds agree with the source and volume is approximately 12,503.585 mm3.

Hole centres agree exactly with Rev I, but fastening geometry differs: initial Rev I uses 9 mm rear pads and 4.2 mm insert pockets. Initial Rev I therefore does not inherit the full R3 board attachment geometry and must not be represented as R3-derived.

For comparison at the provisional 16.5 mm faceplate-to-PCB-top spacing, reflect R3 in Z and translate by 25.46 mm in face-local Z. Post tops meet the PCB rear at 18.06 mm; the base occupies Z=23.06..25.46. Applying the existing Rev I face transform gives zero PCB-reference intersection (numerical residual below 1e-4 mm3), but 58.426 mm3 shell intersection at the carrier seats. The existing Rev I attachment datum is 25.06 mm, 0.40 mm forward of the R3 base rear. R3 is not a drop-in replacement and lacks the Rev I faceplate/support attachment structure.

The next geometry integration should preserve R3 board centres, 8 mm posts and 3.4 mm through-holes, provide an explicit removable fastener arrangement, and reconcile rear frame/seat depth. Its cross-ribs require populated-PCB underside and harness clearance checks. Initial Rev I generator/STLs remain unchanged by this comparison. Do not print the current Rev I carrier expecting R3 hardware compatibility; settle this integration before another carrier fit print.

Input SHA-256:

- SCAD: `A941E9DEE239ED2F806CC3225EB164D02C7B2587D38E852663961E12626AAF39`
- STL: `3D8C7A564F197CA7FEAC8A0377CF2ECFAA3A88A208E170DEBEB5657B0888346F`


### Rev I front-opening export correction - 2026-09-21

The initial Rev I shell exports contained four large coincident, opposite-facing triangles across the nominal front aperture. These zero-volume sheets made the shell appear closed despite passing the previous volume-intersection and welded-edge checks. The cavity cutter now extends 1 mm outside the face datum rather than ending coplanar with it. This removes the spurious faces without changing the intended shell volume, carrier seats, dimensions or frozen Rev H mounting interface. Regenerated Rev I shell STLs supersede the initial defective exports; the originals remain in Git history. The verifier now checks actual exported triangles at the front aperture in both orientations.

Intended attachment sequence for the initial Rev I cassette: insert the PCB into the separate carrier and fasten it to its four rear pads; insert the carrier through the open shell front and secure it to the four recessed outboard shell seats; attach the faceplate to the four front corner pads on the carrier. Faceplate screws do not attach directly to the shell. The separate carrier is required for this arrangement. Actual fastener/driver access and the recovered R3 integration remain pending; this correction alone does not make R3 compatible. Do not print the initial cassette pending that integration.
