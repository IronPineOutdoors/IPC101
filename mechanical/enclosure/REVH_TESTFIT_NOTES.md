# IPC-101 Enclosure Rev H — Test-Fit Notes

Status: **TEST-FIT / NOT FABRICATION-FROZEN**  
Date: 2026-09-20

Rev H begins the enclosure redesign after the physical IPC-101 mock-up showed that the Rev G upper wall angle / face-boss arrangement conflicts with the PCB and control-panel stack.

## Preserved from Rev G

The rear wood mounting interface remains the datum for Rev H:

- body width: 156 mm
- wood mount X: 16 and 140 mm
- wood mount Z: 28 and 70 mm
- wood screw clearance: 4.5 mm
- head recess: 9.5 mm
- straight driver access: 11 mm
- mounting pads: 24 x 20 x 4 mm
- nominal wall: 3 mm
- 47 degree operator viewing angle retained for this test revision

## Rev H control stack

Current physical mock-up target:

- faceplate back surface to IPC-101 PCB top: **~16.5 mm**
- IPC-101 PCB thickness: **1.56 mm**
- four confirmed IPC-101 corner holes: (5,5), (145,5), (5,95), (145,95)

Rev H experiments with a common corner stack so the faceplate/PCB relationship is controlled mechanically. This is intentionally a test architecture and may change after the first fit check.

The 16.5 mm spacing is provisional. It was chosen to allow OLED wiring/harness connector clearance and must be physically verified before freezing button-cap height or production enclosure dimensions.

## Rear Alpha connector

Rev H reserves a **34 x 26 mm generic connector-cassette bay** on the rear. This is not the final connector cutout.

The intent is to use a removable connector-specific insert so the enclosure does not need to be reprinted if the IPC-101-to-Alpha connector family changes during Alpha development.

Connector family, pin count, keying, sealing and final insert dimensions remain TBD pending electrical interface confirmation.

## Physical marking

Rev H carries the hidden mark:

`IPC101-ENC-RH TEST`

This follows `mechanical/REVISION_MARKING_STANDARD.md`.

## Test objectives

Before Rev H can advance:

1. Verify preserved rear mounting interface still fits the CrossWind Alpha mounting location.
2. Verify PCB/faceplate stack can physically occupy the redesigned upper volume.
3. Verify ~16.5 mm faceplate-to-PCB-top spacing clears the OLED harness/connectors.
4. Check P504 pedestal/retainer clearance.
5. Check ARM/PULL actuator relationship; this measurement will drive final button-cap stems.
6. Verify all four corner fasteners can be installed/removed without PCB/component interference.
7. Verify rear connector bay is accessible and leaves adequate cable bend/service space.
8. Identify any unnecessary enclosure volume before the next revision.

Do not treat Rev H as production geometry. It is deliberately generous so interference can be found before the enclosure is tightened around the assembly.
