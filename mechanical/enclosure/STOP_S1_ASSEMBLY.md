# STOP side pod S1 — physical fit prototype

Adds the received IDEC XA1E-BV302R to the existing I1 control panel. No reprint or drilling of the M4 faceplate, R3 carrier, I1 bezel/cradle, shell or Rev H mounting interface is required. The pod occupies the side at face-local X=-42 mm, Y=50 mm. See `STOP_S1_preview.png` for location. Overall control-box width increases by 57 mm; check space at the actual machine.

Current assembly reference: the [N1 replacement faceplate](REV_N1_FACEPLATE.md) has also passed S1 clearance checks. The pod/cover STLs already printing are unchanged.

## Print

**COUPON ACCEPTED, 2026-09-21:** the user subsequently confirmed that the switch works fine, attributing the initial apparent restriction to incorrect seating. The coupon-related pod print hold is lifted; no geometry change is indicated. Full pod assembly, wiring clearance and mounting stiffness still require physical checks.

1. Print `CrossWind_IPC101_STOP_Coupon_S1_PRINT.stl` first. This 40 × 40 × 2.5 mm coupon checks the keyed hole, gasket and locking ring against your actual switch. The nut must clamp the panel and the anti-rotation tab must engage without force. Check the printed hole with calipers; tune printer compensation or lightly finish it within the specified cutout tolerance if necessary.
2. Print `CrossWind_IPC101_STOP_Pod_S1_PRINT.stl`, front down as exported: 68 × 80 × 48 mm.
3. Print `CrossWind_IPC101_STOP_Cover_S1_PRINT.stl`, flat as exported: 54 × 60 × 3 mm.

PETG, 0.20 mm layers, six walls, six top/bottom layers, 40% infill are starting settings. These orientations need no supports. Keep the mounting land clean of brim/elephant foot. The cover pilot holes are provisional 2.7 mm: check/tap for M3 without splitting the bosses. Engraved STOP-S1 identifies the revision. Python `generate_stop_s1.py` is the editable source; run it to regenerate STL and verification results.

## Hardware and assembly

- Two M3 × 35 socket-head screws replace the two M3 × 30 cassette screws on the pod side. Reuse the existing shell inserts. Do not add washers under these two heads: the 5 mm pod flange and extra 5 mm screw length preserve the original engagement and screw-tip position.
- Four M3 × 10 screws retain the 3 mm rear cover, with 7 mm engagement in the pod's blind pilot holes. Start gently; do not overtighten printed threads.
- Use the switch's original gasket, locking ring and complete contact block. No receiver socket is needed.
- Provide insulated wire, terminal insulation and a small cable tie for the two strain-relief holes. Cable entry protection at the existing bottom wiring plate must match the cable/grommet actually used.

With the control box unpowered, remove the pod-side cassette screws, seat the pod's flat mounting flange against the front of the bezel, and install the M3 × 35 screws. Both attachment points must be tight with the flange fully seated. The mounting load goes through the cassette attachment points into the shell, not through the PCB.

Unlock the switch operator before separating its contact block. Follow IDEC's bayonet-ring instructions. Insert the operator from the pod front, with its anti-rotation tab toward the key notch. The circular rear recess leaves a 2.5 mm panel land. Refit the original locking ring, then align and fully latch the contact block. IDEC specifies 0.88 N·m maximum for its locking ring; this is not a validated tightening torque for this printed mount. Check for cracking, panel distortion and looseness.

Leave slack behind the contacts. Route the insulated cable through the 7 × 6 mm split exit at the pod's lower rear edge and secure it using the adjacent tie holes. Route externally to the existing bottom wiring plate; remove/drill that replaceable plate for your selected protected cable entry. Do not pass a bare cable across a sharp drilled edge or into the bracket rails. This version does not supply a selected cable gland, weather seal or pre-sized wiring-plate hole. Fit the rear cover without pinching the cable.

For front service, remove the pod's two attachment screws and support it alongside the enclosure with cable slack before removing the cassette. Do not hang it from its solder joints. The cover can be removed independently for contact-block access.

## Drawing basis and verification limits

Manufacturer-authored [IDEC XA catalog, printed pages 326–329](https://spectechind.com/Documents/idecxacatalog.pdf), checked 2026-09-21: exact solder-terminal 2NC model; nominal Ø16 family; Ø29 operator; cutout Ø16.2–16.4 mm, key width 1.7–1.9 mm, keyed overall height 17.9–18.1 mm; allowed panel thickness 0.5–3.7 mm; nominal rear depth 27.9 mm. S1 uses the tolerance midpoints (16.3, 1.8, 18.0 mm). These are CAD dimensions, not a guarantee of FDM output size. Do not substitute the unibody switch drawing.

Clearance modeling deliberately reserves a Ø32 mm locking-ring envelope followed by a 32 × 32 mm body envelope reaching 33 mm behind the mounting land, plus 12.5 mm space to the rear cover. It represents installation clearance, not exact switch geometry. The model includes a simplified red front operator only for preview.

`STOP_S1_verification.json`: six watertight, consistently wound, single-component exports; no solid overlap with I1 shell, bezel, cradle, R3 or actual M4 plate/PCB; replacement fastener clearance; full contact-block rotational envelope; 71 bracket slide positions; 66 forward pod-removal positions; 41 rear-cover withdrawal positions. Check actual cable routing and tool access physically. CAD checks do not establish impact strength, fatigue, environmental sealing, emergency-stop system compliance or the complete assembled fit. Before use, verify the mount does not flex/rotate/loosen during push and reset, the contact block is fully locked, and the STOP circuit works in the assembled machine.

The existing isolated NC STOP interface remains unchanged. Confirm terminals and continuity before wiring; this mechanical accessory does not assign the second NC contact.
