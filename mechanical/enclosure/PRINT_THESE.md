# PRINT THESE - IPC-101 Rev I.1

**2026-09-22: user confirmed P504 contact at the hole edge. Use the [N1.4 faceplate](faceplate/REV_N14_FACEPLATE.md), with an 8 mm opening instead of 6.2 mm.** Actual directional travel still needs a physical check; the optional [small coupon](controls/navigation/P504_DIRECTIONAL_FIT.md) checks the same opening before a full print.

**2026-09-21: cradle print complete; user reports the dry fit looks good.** Reuse the printed cradle, bezel and R3 carrier. Next small print: the STOP switch-fit coupon below. Before the box print, check the populated PCB, faceplate, control travel and harness clearance in the assembled stack.

| Part | How to recognize it | Exact print file |
|---|---|---|
| **CRADLE - printed; reuse** | Flat frame/nest with rear nut pockets; **168 x 118 x 7 mm** | [CrossWind_IPC101_Cradle_RevI1_PRINT.stl](structure/CrossWind_IPC101_Cradle_RevI1_PRINT.stl) |
| **BEZEL** | Faceplate support with four tall spacing posts; **168 x 118 x 22.46 mm** | [CrossWind_IPC101_Bezel_RevI1_PRINT.stl](structure/CrossWind_IPC101_Bezel_RevI1_PRINT.stl) |
| **R3 CARRIER - reuse the print you have** | PCB support with cross-ribs and four round posts; **156 x 106 x 7.4 mm** | [IPC101_RevA_RearCarrier_R3.stl](carrier/IPC101_RevA_RearCarrier_R3.stl) |
| **BOX - after checking the stack** | Open-front enclosure; **174 x 131.912 x 108.384 mm** | [CrossWind_IPC101_Box_RevI1_PRINT.stl](structure/CrossWind_IPC101_Box_RevI1_PRINT.stl) |
| **BRACKET - reuse Rev H** | Detachable mount with two T rails | [CrossWind_IPC101_Bracket_RevH_PRINT.stl](mounting/CrossWind_IPC101_Bracket_RevH_PRINT.stl) |
| **WIRING PLATE - reuse Rev H** | Flat blank plate for the bottom service opening | [CrossWind_IPC101_Wiring_Plate_RevH_PRINT.stl](mounting/CrossWind_IPC101_Wiring_Plate_RevH_PRINT.stl) |

## LED bubble test prints

Start with [bubble 2 and the panel-hole strip](controls/led/LED_R1_TEST_PRINTS.md). Select LED-pocket fit and panel-hole size before another full faceplate revision. The current 5.2 mm LED hole is not sized for these bubbles.

**ARM/PULL cap update:** user reports the R1 shafts preload the actuators when assembled. Final shaft lengths await trimming measurements; do not reprint unchanged R1 caps expecting that issue to be fixed.

## Faceplate and labeled buttons - N1.4 / R1

Use **N1.4** for the reprint: enlarged P504 opening, compact traced tree + IPO, corrected ARM-left/PULL-right positions, and labels on the existing R1 caps. See [preview and details](faceplate/REV_N14_FACEPLATE.md).

- [N1.4 WHITE faceplate](faceplate/CrossWind_IPC101_Faceplate_RevN14_WHITE_PETGHF.stl)
- [N1.4 BLACK inlay](faceplate/CrossWind_IPC101_Faceplate_RevN14_BLACK_AMS.stl)
- [R1 ARM cap body](controls/buttons/CrossWind_IPC101_ARM_Cap_R1_WHITE_PETGHF.stl) + [ARM face label](controls/buttons/CrossWind_IPC101_ARM_Cap_R1_BLACK_AMS.stl)
- [R1 PULL cap body](controls/buttons/CrossWind_IPC101_PULL_Cap_R1_WHITE_PETGHF.stl) + [PULL face label](controls/buttons/CrossWind_IPC101_PULL_Cap_R1_BLACK_AMS.stl)

Import each white/black pair as parts of one object. The two caps are separate objects; do not superimpose all four cap files. Preserve shared coordinates and do not mirror. Print one cap first and check movement/return before making the second. See [measured stem dimensions and assembly](controls/buttons/R1_BUTTON_CAPS.md) and [current preview](controls/buttons/R1_button_caps_preview.png).

Earlier N1 through N1.3 faceplates retain the restrictive 6.2 mm P504 opening; do not select them for this reprint. M4 is superseded. The optional [button-position strip](faceplate/history/CrossWind_IPC101_Button_Check_N1_PRINT.stl) shares the corrected hole centers.

## Received STOP switch — S1 side pod

The STOP accessory reuses the printed cradle and bezel.

**STOP COUPON ACCEPTED:** the user confirmed normal operation after correcting the seating (2026-09-21). Proceed with the pod and rear cover; the coupon-related print hold is lifted.

1. [Small switch-fit coupon — tested; reuse](controls/stop/side-pod/CrossWind_IPC101_STOP_Coupon_S1_PRINT.stl)
2. [STOP pod](controls/stop/side-pod/CrossWind_IPC101_STOP_Pod_S1_PRINT.stl)
3. [Rear cover](controls/stop/side-pod/CrossWind_IPC101_STOP_Cover_S1_PRINT.stl)

See the [preview](controls/stop/side-pod/STOP_S1_preview.png) and [S1 assembly/hardware guide](controls/stop/side-pod/STOP_S1_ASSEMBLY.md). Requires two M3×35 replacement cassette screws and four M3×10 cover screws. Physical switch fit and mounting stiffness remain to be checked.

## Fit sequence

1. Fit R3 into the cradle; check flat seating, all four bolt holes and the M3 nut pockets.
2. Add the PCB and bezel/faceplate. Check component-side-out orientation and the provisional **16.5 mm faceplate-back to PCB-top** gap.
3. Check actual OLED harness, P504 wires and ARM/PULL motion before starting the box print.
4. Use the [assembly guide](structure/REV_I1_ASSEMBLY.md) for provisional screws/inserts, print supports, service access and remaining physical checks.

**Do not select parts from `archive/` for this assembly.** The Rev H box in `mounting/` is a preserved mounting reference, not the I.1 enclosure. `INSTALLED` files are for assembly viewing; select the `PRINT` files above for slicing.
