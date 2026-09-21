# Rev I.1 assembly and next print

**TEST-FIT - PHYSICAL VALIDATION PENDING.** This is the current R3-compatible fit assembly. Rev I remains historical. Continue the original R3 print already underway; it is reused unchanged.

**M.4 update:** enclosure/faceplate clearance passes, and ARM/PULL/LED positions match with the PCB component side facing the faceplate. The I.1 cradle print is unaffected. See [fit audit](REV_M4_FIT_AUDIT.md).

## Print order

1. Finish `IPC101_RevA_RearCarrier_R3.stl`. Check PCB hole alignment, seating and underside component clearance.
2. Print [Cradle Rev I.1](CrossWind_IPC101_Cradle_RevI1_PRINT.stl), **168 x 118 x 7 mm**. It accepts the unmodified R3 part and holds four PCB mounting nuts. Dry-fit R3 before adding hardware.
3. Print [Bezel Rev I.1](CrossWind_IPC101_Bezel_RevI1_PRINT.stl), **168 x 118 x 22.46 mm**. It provides faceplate mounting pads and four structural spacing posts. With the cradle, R3 and PCB, this establishes the provisional **16.5 mm faceplate-back to PCB-top** spacing.
4. After the stack fits, print [Box Rev I.1](CrossWind_IPC101_Box_RevI1_PRINT.stl), **174 x 131.912 x 108.384 mm**. Reuse the Rev H bracket and wiring plate.

Use the PRINT orientations with the established PETG/PETG-HF profile. Cradle prints rear-down: inspect the small nut-pocket bridges and supports below the relieved attachment lands. Bezel prints face-down with its posts upward; its corner pads start on the bed. Shell prints floor-down; inspect supports for receivers, roof and internal seats. All new parts fit the 256 mm build envelope. Mesh validation is not slicer validation. Check the actual slice before starting; keep support scars off datum faces and clear screw passages.

The shell's accepted external shape, 47-degree face, face position, and frozen Rev H receiver/rail/pin geometry are unchanged. Internal clearance and the four attachment seats changed; **use the I.1 shell with the I.1 cradle/bezel**. The I.1 shell retains the front-opening correction. No new bracket or faceplate is required.

## How it fastens together

The cradle is a separate frame around and behind R3. R3's posts, 3.4 mm through-holes, rails and cross-ribs are taken directly from the supplied STL. Four screws pass through the PCB, R3 and cradle to ordinary hex nuts captured at the cradle rear. The bezel is removable so it does not block those screws.

Four long screws outside the PCB outline pass through the bezel posts and cradle mounting slots into the shell's insert seats. Tightening these clamps plastic structure to plastic structure; the PCB carries no enclosure or faceplate mounting loads. The faceplate attaches independently to four insert pockets on the bezel. The bezel's rear posts contact the cradle at 46.688 mm2 per post in the ideal model.

The cradle's inward-open U-slots are intentional, not broken holes. The bezel locates the long screws, and R3 locates in the cradle with nominal 0.30 mm side clearance. The slots avoid a tangent bore at the nest edge and allow the original R3 outline to remain unchanged.

## Provisional hardware for the fit build

Hardware below is modeled for clearance, not a confirmed inventory or purchasing instruction. Match actual screws and inserts before assembly; do not heat inserts into R3's through-holes.

| Connection | Quantity | Provisional hardware | Modeled fit |
|---|---:|---|---|
| PCB + R3 + cradle | 4 | M3 x 14 socket screws | 5.5 mm head diameter, 3 mm head height; no washer in stack |
| Captured PCB nuts | 4 | M3 hex nuts | 5.5 mm across flats, 2.4 mm thick; pockets 5.8 mm AF x 2.6 mm deep |
| Bezel + cradle to shell | 4 | M3 x 30 socket screws | 5.5 mm head diameter, 3 mm head height; head bears at front datum |
| Shell seats | 4 | M3 heat-set inserts | 4.2 mm x 6 mm blind pilot; actual supplier fit/length must agree |
| Faceplate to bezel | 4 | M3 x 6 socket screws | Assumes 2 mm faceplate; 4 mm nominal insert engagement |
| Bezel faceplate pads | 4 | M3 heat-set inserts | 4.2 mm x 6 mm through pilot; inserts must remain flush/recessed |

A modeled PCB screw reaches face-local Z=30.5 mm and clears the shell. Cassette screws reach Z=30 mm, giving 4.54 mm nominal engagement from the shell seat at Z=25.46. A washer, thicker faceplate, different head, or different insert changes this calculation. Avoid screw bottoming and PCB bending. Check copper/component clearance around the actual board mounting holes.

## Bench assembly

1. Check the R3 print against the PCB. All four posts should meet the board without rocking or forcing holes into alignment.
2. Fit four nuts into the cradle rear pockets. Hold them in place during bench assembly; they are slip pockets, not guaranteed press fits.
3. Place R3 in the cradle, posts toward the PCB. Place the PCB on R3 with its component side toward the faceplate and ARM/PULL beneath their labeled openings (see the M.4 audit), and install the four M3 x 14 screws from the component side. Tighten only enough to seat the stack.
4. Rest the bezel posts on the cradle's four front lands. Fit the existing faceplate to the bezel. Before heat-setting anything, confirm the faceplate model/thickness and insert sizes. This bench stack can be measured before printing the shell; hold it gently together for the measurement.
5. Measure the back-of-faceplate to PCB-top gap at all four corners: target **16.5 mm**. Check OLED connector/harness routing, P504 body and six wires, ARM/PULL travel, LED reserve, and PCB underside clearance over R3 ribs. Check with the actual populated board; the reference board in CAD is bare.
6. Once these pass, install the shell inserts, place the cradle/R3/PCB in the shell, add the bezel, and insert four M3 x 30 screws through the exposed outboard holes. The modeled faceplate does not cover these heads, so faceplate and bezel may be handled as one unit. Attach/connect actual controls without pinching wires.
7. Reuse the Rev H wiring plate and bracket. Test docking, retaining-pin access and at least 70 mm upward removal travel.

## Service sequence

Disconnect power and external wiring. Remove the four outboard long screws; support the cradle while doing this because those screws also retain it. Lift the faceplate/bezel forward and unplug its harnesses. The PCB screw heads are now directly exposed. Either lift out the cradle/R3/PCB assembly or remove the PCB screws to lift the board out normal to its plane. No sideways threading behind permanent faceplate bosses is needed. Nut retention during service is manual until confirmed on the print.

## What is established and what remains

**Established in CAD:** unchanged R3 geometry; 150 x 100 x 1.56 PCB reference; four board mounting centres; provisional 16.5 spacing; pairwise part clearance; modeled PCB, cassette and faceplate screw/nut clearance; axial driver access; independent bezel/PCB/R3 removal; unchanged outer shell bounds and exact rear mount geometry; connected closed exports; front aperture free of membrane faces.

**Physical gates before calling the control box complete:**

- R3 and cradle fit, hardware dimensions/retention, actual populated-board and harness clearance, measured stack and control travel.
- The supplied M.4 source confirms 2 mm faceplate thickness and its actual rear cradle clears I.1. Verification and preview now use both supplied material STLs. PCB registration is explicitly X=150-Xpcb, Y=Ypcb, with the component side facing the faceplate; see [M.4 fit audit](REV_M4_FIT_AUDIT.md). P504/LED/cap refinements wait for the measured stack.
- Connector selection and environmental sealing. This fit assembly has unsealed bezel/shell and faceplate/bezel joints; the bezel now has a nominal 3 mm overlap beneath the faceplate edge (verified uninterrupted over 2.5 mm), but gasket section/compression and the shell-to-bezel seal are not designed. A sealing revision and leak test are required before outdoor use. The removable wiring plate avoids reprinting the shell when a connector is selected.

**Do not claim physical fit, weather resistance or load qualification from these checks.** The remaining work is measured fit and sealing closeout.

## Files and reproduction

Sources: `generate_rev_i1.py`, `verify_rev_i1.py`, `preview_rev_i1.py`. Geometry markings use `RI1 TEST`. Original R3 and Rev H artifacts remain available. Superseded Rev I exports are preserved unchanged in `archive/superseded-rev-i/`. The six new STLs have `INSTALLED` assembly coordinates and `PRINT` bed coordinates. Results are saved in [RevI1_verification.json](RevI1_verification.json); views in [RevI1_preview.png](RevI1_preview.png).

```powershell
python -B mechanical/enclosure/generate_rev_i1.py
python -B mechanical/enclosure/verify_rev_i1.py
python -B mechanical/enclosure/preview_rev_i1.py
```

Requires Python, manifold3d, numpy and trimesh. `FACEPLATE_TO_PCB_TOP` in the new generator controls R3 placement, cradle depth, bezel post length and shell seat position together. The shell's exterior depth is finite: regenerate and rerun verification after a parameter change, and revise the physical marking before a changed fit print.

The new verifier checks 71 bracket positions and 66 positions for each service motion, actual exported mesh topology and front-aperture triangles, the existing wiring plate/port, floor/rear witnesses, R3 support annuli, nut/screw/driver envelopes, stack spacing, and print bounds. Component and harness shapes are not inferred from photographs. The known unchanged Rev H bracket STL pin-tangency limitation remains documented in the main README.
