# Top STOP R4 - release slots rotated clockwise

> Export cleanup, 2026-09-26: superseded print links below are historical. Use `mechanical/enclosure/PRINT_THESE.md` for current parts. Source and Git history retain regeneration/recovery information.

[Preview](TOP_STOP_R4_preview.png) | [Verification](TOP_STOP_R4_verification.json)

R3 accepted the switch, but the user found pushing the white release with a small screwdriver very difficult. User identified approximately 45 degrees of angular misalignment and specified **clockwise when looking into the open underside**. R4 rotates the two opposed release approaches by that amount; the mounting key stays unchanged. In installed coordinates this is +45 degrees about Z.

The 41 mm pocket, 14 mm nominal slot width, slot height, mounting land and roof attachments are retained. The relief is bounded at installed Y=-9 and Y=27 to preserve the front/rear outer skin rather than cutting through it; the approach remains open from below. Both base variants remain compatible.

## Physical checkpoint - 2026-09-26

The user reports the coupon fit is perfect and the R4 roof is printed. Coupon exports were retired after this report. Full assembly, screw clamp-up and sealing remain unverified.

## Historical coupon procedure

Release coupon R4 PRINT (retired export; recover from Git history)

Use the supplied orientation, flat keyed-hole face down and large pocket opening up. Use 0.20 mm layers and **supports OFF for this coupon**. The cross-section support check passes in this orientation. This is a local access fixture, not a full-roof printability test.

Mount the switch and check that the slot now aligns with the lower white release: push it up and twist the contact block off. Repeat in the opposite block orientation. The 45-degree correction comes from user observation rather than a dimensioned latch drawing, so physical accessibility still needs confirmation. Do not force the tab.

If both orientations release comfortably, the next full print is [Roof R4 PRINT](CrossWind_IPC101_Top_STOP_Roof_R4_PRINT.stl). Inspect its supports independently; the no-support instruction applies only to the coupon. Keep the existing base and hardware.

All 539 inherited insertion/rotation/service checks pass, plus the coupon layer-support and release-corridor checks. Four exports are watertight, consistently wound, single connected meshes. User feedback now reports perfect coupon fit; both-orientation release was not separately described. R3 is retained as history.

```powershell
python -B mechanical/enclosure/tooling/generate_top_stop_r4.py
python -B mechanical/enclosure/tooling/preview_top_stop_r4.py
```
