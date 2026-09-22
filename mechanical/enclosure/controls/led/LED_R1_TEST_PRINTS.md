# LED bubble R1 - fit and optical test prints

The recorded RGB LED body is approximately diameter 5.10 x 8.88 mm. N1.4 has a 5.2 mm opening, which cannot accommodate a printed shell around that LED. These new samples establish a candidate lens and panel opening before revising the full faceplate. No existing lens model was found in the repository.

[Preview](LED_R1_preview.png)

| Bubble tab number | Internal pocket diameter | Print file |
|---|---|---|
| 1 | 5.3 mm | [Bubble 1](CrossWind_IPC101_LED_R1_Bubble_1_Bore5.3_PRINT.stl) |
| 2 | 5.5 mm | [Bubble 2 - start here](CrossWind_IPC101_LED_R1_Bubble_2_Bore5.5_PRINT.stl) |
| 3 | 5.7 mm | [Bubble 3](CrossWind_IPC101_LED_R1_Bubble_3_Bore5.7_PRINT.stl) |

[Panel-hole strip](CrossWind_IPC101_LED_R1_Hole_Strip_PRINT.stl): holes 1 / 2 / 3 are 8.0 / 8.2 / 8.4 mm. Thickness 2.05 mm matches the reported faceplate measurement; footprint 72 x 25 mm.

All bubbles have a 7.8 mm outside diameter, a 10 mm rear flange and a temporary numbered handling tab. The neck spans 2.05 mm of panel above the 1 mm flange. The hemispherical dome projects 3.9 mm beyond the panel. Wall thickness varies from 1.25 to 1.05 mm with the pocket sizes. The LED pocket is open from the rear and has a domed roof. These are trial dimensions, not an established final lens specification.

Print bubble 2 first in the clear/translucent material intended for the lens, flange/tab flat on the bed and dome upward as exported. Start with 0.16 mm layers and no internal supports; inspect the domed pocket roof for sagging that could affect fit. Print the strip flat in the same material/profile used for the faceplate. White/opaque samples can test fit but will not establish the clear-material light appearance. Keep separate samples as separate slicer objects and arrange them apart.

1. Try the LED gently in bubble 2 from the rear; do not force it or push on its leads. Try bubble 1 for a closer fit or bubble 3 if tight. The actual LED flange/body shape may limit insertion and needs checking.
2. Insert the bubble from the strip's rear so the dome projects through a hole and the flange stays behind. Choose the smallest hole that seats freely without force. Do not enlarge the full faceplate yet.
3. Hold the LED in place for a light check using its existing correctly wired circuit. Compare visibility of each color from the front and side. Record any hotspots, weak brightness or excessive diffusion.
4. Report both numbers separately: bubble number and strip-hole number, plus the material used and any seating issue.

These samples have no final snap, LED retainer, wire strain relief or weather seal. Support the LED during testing. The temporary tab is for identification/handling, not the final mounting feature. Do not modify the PCB holes. Final retention and assembled clearance must be designed after testing; this coupon does not validate the complete populated-board stack.

Source: generate_led_bubble_r1.py. LED_R1_verification.json records four closed single-solid meshes and nine nominal bubble-to-panel clearance checks. Actual printed fit and optical performance are pending.

Other outstanding faceplate work: stacked upper-left Iron/Pine/Outdoors branding is a visual concept; wind-stroke redesign is pending. R1 ARM/PULL shafts were reported to preload actuators during assembly; final shortening awaits the user's trimmed measurements. Do not treat the earlier cap-clearance checks as proof of the physical actuator stack.
