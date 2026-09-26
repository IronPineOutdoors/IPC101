# Current IPC-101 print list

Updated 2026-09-26. Current build: rear-entry base and tunnel bracket/collar, R4 STOP roof, I.1 cradle/bezel, R3 carrier and N1.4 faceplate.

## Next: clear LED tests

- [Bubble 2, 5.5 mm pocket](controls/led/CrossWind_IPC101_LED_R1_Bubble_2_Bore5.5_PRINT.stl): clear/translucent material, flange down, dome up, 0.16 mm layers, no internal supports; inspect the slice.
- [Panel-hole strip](controls/led/CrossWind_IPC101_LED_R1_Hole_Strip_PRINT.stl): flat, using the faceplate material/profile.
- Keep bubbles 1 and 3 for alternate fits. See [LED test instructions](controls/led/LED_R1_TEST_PRINTS.md).

These are fit/optical samples, not a completed retainer or weather seal. Rev 2 mounts the LED directly on the PCB.

## Current assembly and replacements

| Part | Print file | Status |
|---|---|---|
| Rear-entry base | [Base](mounting/rear-tunnel-r1/CrossWind_IPC101_Rear_Tunnel_Base_R1_PRINT.stl) | Printed; sidewall damaged during support removal. Use for fits, replace after checks. |
| STOP roof | [R4 roof](controls/stop/top-mounted/CrossWind_IPC101_Top_STOP_Roof_R4_PRINT.stl) | Printed; coupon fit reported perfect. Full clamp-up pending. |
| Tunnel bracket | [Bracket](mounting/rear-tunnel-r1/CrossWind_IPC101_Rear_Tunnel_Bracket_R1_PRINT.stl) | Printed. |
| Tunnel collar | [Collar](mounting/rear-tunnel-r1/CrossWind_IPC101_Rear_Tunnel_Collar_R1_PRINT.stl) | Printed. |
| Cradle | [I.1 cradle](structure/CrossWind_IPC101_Cradle_RevI1_PRINT.stl) | Reuse printed part. |
| Bezel | [I.1 bezel](structure/CrossWind_IPC101_Bezel_RevI1_PRINT.stl) | Reuse existing part. |
| PCB carrier | [R3 carrier](carrier/IPC101_RevA_RearCarrier_R3.stl) | Reuse existing part. |
| Faceplate | [N1.4 white](faceplate/CrossWind_IPC101_Faceplate_RevN14_WHITE_PETGHF.stl) + [black inlay](faceplate/CrossWind_IPC101_Faceplate_RevN14_BLACK_AMS.stl) | Current plate; LED lens opening/retention not finalized. |
| Navigation cap | [P504 cap](../panel/CrossWind_Adafruit504_Nav_Cap_RevC_IPC101.stl) | Retained current navigation cap. |

Keep the [P504 clearance coupon](controls/navigation/P504_DIRECTIONAL_FIT.md), STOP pilot coupon and wall template: their remaining checks have not all been confirmed. Do not cut the plywood before actual harness-motion checks.

R1 ARM/PULL cap files remain in `controls/buttons/` with their labels, but the user trimmed about 1.5 mm from PULL; original exports do not contain that correction. See [cap feedback](controls/buttons/R1_BUTTON_CAPS.md).

## Cleanup and reference geometry

Superseded G/I enclosure exports, old C/D panels and caps, side-pod S1, STOP roofs R1-R3, earlier top-entry base and completed access/bore coupons were removed from the working tree. Recover them from Git history or regenerate from retained sources if needed. No Git history was rewritten.

Older faceplate meshes in `faceplate/history/`, the Rev H mounting meshes and I.1 installed box remain because CAD reference/comparison tools use them. They are not the current print choices. Historical generators may recreate retired exports and their historical verification tools may require regeneration first. `artifact_paths.json` retains historical output destinations for that purpose.

The saved `CrossWind_IPC101_Box.3mf` is retained as a user slicer project; its revision/settings have not been established as the current print authority. TPU experiments remain pending, not confirmed superseded.

Before another large print, finish stack/control fit, roof clamp-up and actual harness slide/removal checks. Sealing remains unfinished.
