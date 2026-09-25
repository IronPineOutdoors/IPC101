# Top STOP roof R2 - underside insertion correction

[Preview](TOP_STOP_R2_preview.png) | [Verification](TOP_STOP_R2_verification.json)

User feedback: the printed R1 roof fits the enclosure, and the retaining nut can be installed by hand. The rear contact block cannot enter the underside opening. Its measured maximum cross-section is 27.3 x 27.3 mm, rotates about its center, and has no reported protrusions beyond that measurement. The earlier checks tested the stationary body in its final position and missed the restrictive underside access path.

R2 opens a continuous 41 mm diameter path from below the roof to the underside of its 2.5 mm top mounting land. A centrally rotating 27.3 mm square sweeps 38.608 mm diameter, leaving approximately 1.196 mm nominal radial clearance. A 47 mm outside-diameter reinforcement surrounds the upper pocket from Z109 to Z138.5; the lower entry is relieved to preserve the base fit. This slightly changes the outside shape near the switch pocket. The top keyed hole, top mounting land, four screw mounts and locating shoulders remain unchanged.

## Physical feedback and next revision

The user confirmed that the switch mounts successfully in R2. Release is difficult because the lower white tab must be reached and pushed upward before twisting off. The R2 coupon also produced loose strands at upper features. Use the [R3 paired-access roof and simplified release coupon](TOP_STOP_R3.md) for the next print.

## Historical R2 coupon instructions

[Access coupon R2 PRINT](CrossWind_IPC101_Top_STOP_Access_Coupon_R2_PRINT.stl) reproduces the central roof section, including the full access pocket and keyed mounting hole. Use the exported orientation: top face against the bed, underside access upward. Inspect the support preview; avoid filling the vertical access pocket with unnecessary support. The user restored PETG support Top Z distance to 0.20 mm after prior prints used 0 mm and were difficult to separate. Do not restore zero gap for PETG-on-PETG supports.

Fit the operator and nut to this coupon, then insert the actual contact block from the underside and twist it into lock. Confirm removal as well, and verify terminals and wires do not catch. This is a test of the complete insertion-and-turn sequence, not just passage through a ring. Report any contact point before another full roof print.

Once that physical test passes, use [Roof R2 PRINT](CrossWind_IPC101_Top_STOP_Roof_R2_PRINT.stl). Assemble the switch/contact block with the roof removed from the enclosure, then attach the roof. The base's smaller cable passage is not an installation opening for the contact block.

R2 reuses both the original top STOP R1 base and the rear-tunnel R1 enclosure base, plus the same four provisional M3 x 30 screws. No replacement base or locator coupon is needed for this correction. R1 roof files remain for history and should not be selected for this switch installation.

## Verification and limits

539 CAD interference checks pass. These include a continuous cylindrical insertion/rotation envelope, 72 angular positions at five insertion depths, both base variants during roof removal, current stack clearance and 71 rear-mount slide positions. A regression check reproduces 473.852 mm3 of R1 obstruction during insertion. Exact geometry comparisons confirm the top land/keyed hole and roof attachments are unchanged. All four exported meshes are connected, watertight and consistently wound.

The 30.5 mm block depth remains the previous conservative package assumption; only the 27.3 mm square and central rotation are measured/confirmed. Actual wires, fingers and tools are not modeled. Physical twist-lock fit, support cleanup and weather sealing remain unverified.

```powershell
python -B mechanical/enclosure/tooling/generate_top_stop_r2.py
python -B mechanical/enclosure/tooling/preview_top_stop_r2.py
```
