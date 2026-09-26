# Integrated top STOP housing R1 ? fit prototype

> Export cleanup, 2026-09-26: superseded print links below are historical. Use `mechanical/enclosure/PRINT_THESE.md` for current parts. Source and Git history retain regeneration/recovery information.

[Assembly, section and roof-removal preview](TOP_STOP_R1_preview.png).

R1 develops the top STOP concept into a two-piece housing with four top-access screws, locating shoulders and an internal harness tie tab. The roof retains the rounded full-width profile and sloped front transition. The STOP mounting surface is Z141 mm, 32.616 mm above the I.1 shell maximum. The conservative switch envelope and 2.5 mm keyed mounting land are retained from the packaging study. This is an engineering fit prototype, not a weather-sealed final release.

## What changes

The base replaces the I.1 box and adds four attachment bosses plus the existing 24 x 24 mm cable passage. The R3 carrier, cradle, bezel and Rev H detachable mount are reused. The roof lifts vertically after removing four screws; remove it before withdrawing the front cassette. This roof is not a bolt-on accessory for an unmodified I.1 box.

Four M3 x 30 socket screws seat at Z138 and engage 9 mm of 2.7 mm printed pilot below the Z117 support plane. The pilots stop at Z107, leaving 8 mm of boss below the bore. Hardware dimensions are provisional; use the coupons to establish fit in the chosen material before committing to a large print. Do not force a tight screw or assume a printed pilot is suitable for repeated service without testing.

Each boss has a 7 mm diameter, 2 mm high locating shoulder. Its roof socket is 7.6 mm diameter and 2.4 mm deep: 0.3 mm radial and 0.4 mm end clearance. The inherited lower-skirt contact is relieved by 0.3 mm along each axis. Four shoulders locate the roof; the coupons test local clearance, while the full-width prototype must still demonstrate simultaneous engagement without binding. The roof has 6.4 mm head wells and modeled clearance for a 7 mm driver envelope.

A two-slot tie tab on the roof underside supports the harness independently of the switch terminals. A 20 x 20 x 10 mm wire reserve and a 36 mm diameter mounting-nut access envelope are checked. Real leads, bends and populated board components remain to be measured. Allow enough service slack or a suitable disconnect to lift the roof; the CAD withdrawal check does not simulate flexible wires.

## R2 access correction

The user found that the contact block cannot enter the R1 underside opening. Use the [R2 access coupon and revised roof](TOP_STOP_R2.md) for the correction. The roof-to-base fit and nut installation were reported workable.

## Physical feedback

The user reports that the locator coupons slide together well. Keep the current locator clearance. Screw engagement and full clamp-up remain untested; M3 x 30 screws were not available.

A [rear-entry base variant](../../../mounting/rear-tunnel-r1/README.md) now reuses this roof and closes the old bottom wiring port. It is a fit prototype pending actual harness-motion checks.

## Print and fit order

1. Print the [pilot coupon](CrossWind_IPC101_Top_STOP_Pilot_Coupon_R1_PRINT.stl) and roof coupon (retired export; recover from Git history). Check the locator slip fit, screw-head recess, M3 x 30 engagement and clamp-up. Stop if the boss cracks, the screw bottoms or the thread strips.
2. Print the roof (retired export; recover from Git history) to check the actual STOP body, mounting nut, terminal access and tie tab. The export places the top surface on the bed; inspect support requirements for the recessed locating sockets and tie tab in the slicer.
3. Print the replacement base (retired export; recover from Git history) after the small fits pass. It sits on its bottom; inspect supports under the sloped shell and added bosses.
4. Dry assemble all four shoulders and screws, then verify roof removal, complete cassette withdrawal, mount sliding, actual wire routing, STOP actuation and reset access.

`INSTALLED` exports retain shared assembly coordinates and are for assembly review. `PRINT` exports are moved to the bed and fit within a 256 mm cube. Existing I.1 and side-pod S1 print files remain available; the older PRINT THESE guide continues to identify the established fit build.

## Verification and remaining design work

[Machine-readable results](TOP_STOP_R1_verification.json) cover connected watertight exports, static stack clearance, roof/base separation, switch and nut envelopes, screw/driver clearance, unchanged rear mounting interface, 71 bracket positions, 66 complete-cassette positions and 51 roof-lift positions.

The roof seam, switch gasket and screw wells still need a sealing design. There is no water-ingress rating. Printed-pilot strength, long-term retention, populated-board clearance, harness flex and actual operator access require physical verification. The preview uses N1.4 faceplate geometry; approved artwork integration is a separate remaining step.

Regenerate from the repository root:

```powershell
python -B mechanical/enclosure/tooling/generate_top_stop_r1.py
python -B mechanical/enclosure/tooling/preview_top_stop_r1.py
```
