# Top STOP roof R3 - paired release access

[Preview](TOP_STOP_R3_preview.png) | [CAD verification](TOP_STOP_R3_verification.json)

The user confirmed that the R2 pocket accepts and mounts the contact block. The remaining difficulty is reaching the lower white release, pushing it upward, then twisting the block off. The block can attach in two opposite orientations. R3 retains the confirmed 41 mm pocket and removes material on both X sides, perpendicular to the mounting-hole key axis, to provide upward release approaches.

Two opposed 14 mm wide slots run from the underside to Z136.5. They leave 4.5 mm of material to the exterior top face, including the unchanged 2.5 mm mounting land. The keyed hole, four roof attachments, locating shoulders and compatibility with both existing bases remain unchanged. Slots do not imply a weather seal; sealing remains unfinished.

## Superseded release-slot alignment

Physical R3 testing found release difficult even with a small screwdriver. The user identified a roughly 45-degree clockwise slot correction viewed from underneath. Use the [R4 coupon and roof](TOP_STOP_R4.md) for the next trial.

## Historical R3 coupon instructions

[Release coupon R3 PRINT](CrossWind_IPC101_Top_STOP_Release_Coupon_R3_PRINT.stl)

This replaces the complicated cut-out roof section used for the previous coupon. It is a simple 47 mm diameter, 32 mm tall central pocket with the same 41 mm bore, keyed mounting hole, mounting thickness and release slots. It omits the surrounding roof skirts, ledges and wire tie tab. It is intended to test local switch/release access, not the full housing assembly.

- Use the exported orientation: flat keyed-hole face on the bed, large pocket opening upward.
- Use 0.20 mm layers and **supports OFF for this coupon**. A layer-section check at that spacing confirms each higher cross-section stays within the preceding section; there are no upper ledges that require bridging. This geometric check does not guarantee extrusion or adhesion quality.
- Install the operator and retaining nut. Insert and lock the contact block, then reach the lower white release through a slot, push it up and twist the block off. Repeat with the contact block installed in the opposite orientation.
- Test with the coupon held securely and power disconnected. The actual latch stroke and finger/tool dimensions have not been measured, so this physical check determines whether the proposed access is adequate.

If release is comfortable in both orientations, print [Roof R3 PRINT](CrossWind_IPC101_Top_STOP_Roof_R3_PRINT.stl). Do not use the old R1/R2 roof for the next full print. Keep the existing base and roof hardware. Inspect the full roof's support preview separately; the no-support instruction applies only to the simplified coupon.

Next after roof printing: assemble the actual STOP operator/contact block with the roof off, verify locking/release and terminal/harness access, then fit the populated roof to the base. Roof fastener clamp-up still needs the actual M3 x 30 screws. Harness layout and electrical interface limits remain unresolved and are not changed here.

## Verification

All 539 existing R2 insertion, rotation, mounting and service checks pass on the R3 roof. Additional checks confirm the release corridors contain no roof material, the revision only removes material from R2, the coupon is self-supporting by 0.20 mm section comparison, and all four exports are connected, watertight and consistently wound. Actual release accessibility remains pending the coupon test.

```powershell
python -B mechanical/enclosure/tooling/generate_top_stop_r3.py
python -B mechanical/enclosure/tooling/preview_top_stop_r3.py
```
