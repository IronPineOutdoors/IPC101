# Top STOP R4 - release slots rotated clockwise

[Preview](TOP_STOP_R4_preview.png) | [Verification](TOP_STOP_R4_verification.json)

R3 accepted the switch, but the user found pushing the white release with a small screwdriver very difficult. User identified approximately 45 degrees of angular misalignment and specified **clockwise when looking into the open underside**. R4 rotates the two opposed release approaches by that amount; the mounting key stays unchanged. In installed coordinates this is +45 degrees about Z.

The 41 mm pocket, 14 mm nominal slot width, slot height, mounting land and roof attachments are retained. The relief is bounded at installed Y=-9 and Y=27 to preserve the front/rear outer skin rather than cutting through it; the approach remains open from below. Both base variants remain compatible.

## Next print

[Release coupon R4 PRINT](CrossWind_IPC101_Top_STOP_Release_Coupon_R4_PRINT.stl)

Use the supplied orientation, flat keyed-hole face down and large pocket opening up. Use 0.20 mm layers and **supports OFF for this coupon**. The cross-section support check passes in this orientation. This is a local access fixture, not a full-roof printability test.

Mount the switch and check that the slot now aligns with the lower white release: push it up and twist the contact block off. Repeat in the opposite block orientation. The 45-degree correction comes from user observation rather than a dimensioned latch drawing, so physical accessibility still needs confirmation. Do not force the tab.

If both orientations release comfortably, the next full print is [Roof R4 PRINT](CrossWind_IPC101_Top_STOP_Roof_R4_PRINT.stl). Inspect its supports independently; the no-support instruction applies only to the coupon. Keep the existing base and hardware.

All 539 inherited insertion/rotation/service checks pass, plus the coupon layer-support and release-corridor checks. Four exports are watertight, consistently wound, single connected meshes. No physical-release success is claimed yet. R3 is retained as history.

```powershell
python -B mechanical/enclosure/tooling/generate_top_stop_r4.py
python -B mechanical/enclosure/tooling/preview_top_stop_r4.py
```
