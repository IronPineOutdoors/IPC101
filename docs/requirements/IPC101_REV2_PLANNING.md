# IPC-101 Rev 2 planning notes

Recorded 2026-09-25 from user direction. This is the next-board requirements backlog, not a released PCB revision or authorization to fabricate. Current KiCad/Rev C fabrication files are unchanged. "Rev 2" is the user's next-board designation; assign the formal fabrication revision consistently before release.

## System context

IPC-101 replaces the improvised Alpha panel now, connected to the existing ESP32; IPC-100 is still in development and is a later host. Build a new Alpha harness instead of assuming the old panel harness is directly compatible. The Crosswind repo contains the Alpha firmware and adapter plan: GPIO21 SDA, GPIO22 SCL, GPIO5 OLED reset, OLED and BME280 on the shared bus. IPC-101 keypad/RGB firmware migration and STOP integration remain separate unfinished work. Do not apply IPC-100-only interface assumptions to Alpha without reconciliation.

## Requested board changes

| Item | Rev 2 direction | Evidence or decisions needed before layout release |
|---|---|---|
| BME280 support | Add an explicit electrical connection and planned physical accommodation for the BME280. Avoid an undocumented external SDA/SCL splice. Label power, ground, SDA and SCL clearly. | Confirm actual breakout dimensions, pin order, mounting holes, voltage interface, address and pull-ups. Decide whether the sensor mounts on IPC-101 or uses a dedicated remote connector; preserve useful ambient airflow and avoid enclosure/board heat bias. Reconcile Alpha shared-bus operation with future IPC-100 connections. |
| Adafruit 504 / SW3 | Correct the reported pin alignment in the PCB footprint. | Measure the received switch's six pins, row spacing, offsets and orientation against the current board. Confirm center/common and all five directional/select mappings by continuity. Do not substitute a generic footprint or assume this is only a faceplate-hole issue. Check PCB footprint, actuator center and panel opening together. |
| Input connector at rear | Evaluate moving/orienting the input connector(s) onto the rear face of the PCB to receive the harness arriving through the rear tunnel. This is a candidate layout change, not a frozen position. | Clarify rear face versus rear board edge in assembly coordinates. Check mating direction, connector height, latch access, cable bend/strain relief, R3 carrier and cradle clearance, populated-board access and full slide/removal travel. Keep the required STOP connection distinct; consolidation is not automatically approved by this mechanical note. |
| Direct-mounted OLED | Orient and position the OLED header so the received Hosyond SSD1309 module can mount directly to IPC-101, like the buttons, 504 and LED, rather than relying on the present faceplate-to-board display harness. | Measure actual module header pitch, pin order, direction, module outline and four mounting holes. Confirm module front/back orientation and required reset connection. Choose mating-header type and standoff height to align the screen with the faceplate. Support the module mechanically with standoffs/fasteners; do not make the electrical header carry panel loads. Check display removal, solder access and clearance against adjacent controls. |
| Complete silkscreen / stencil identification | Every component receives a readable reference designator. Add useful functional labels for controls and connectors; mark pin 1, polarity and orientation where applicable. Add pin/function legends where space allows, including BME, OLED/reset and isolated STOP. | Review top and bottom silkscreen against assembled hardware, solder-mask openings and fabrication minimums. Connector legends must match the released pinout and viewing direction. Include an assembly drawing when parts obscure their own references. |
| Board identity and branding | Add the approved Iron Pine/CrossWind logo and the IPC-101 part number on the PCB, plus the released revision identifier. | Choose approved vector artwork and exact part-number/revision format; verify legibility at actual size. Keep logos/text off pads, holes, component keepouts and mating surfaces. |

## Related physical feedback to carry forward

- ARM/PULL stems: user removed approximately 1.5 mm from PULL and reports good operation. User requests the same reduction for both caps; ARM is not yet physically verified. This is a cap/mechanical correction, not grounds to relocate switches without a complete stack check. Current nominal R1 dimensions imply 8.07 mm stem beyond the rear flange after that reduction.
- Roof R2 accepts the STOP block; R3 adds access to its push-up release. Keep STOP service access in the populated-board and harness assembly review.
- The rear tunnel's 50 mm bore ring passed the user's connector clearance check. Full harness bending and slide-and-pull service motion are not yet validated.
- Direct OLED mounting and rear connector changes can alter the PCB/faceplate/carrier stack. Preserve proven datums where possible and explicitly revise affected enclosure parts if necessary.

## Release checks for the next board

1. Record the actual BME module, 504 pin measurements, OLED connector/mount geometry and rear harness mating envelope.
2. Establish a dimensioned component-side and rear-side assembly layout, including the populated R3/cradle/faceplate stack and accessible connector latches.
3. Reconcile Alpha and future IPC-100 power, I2C topology, pull-ups, reset, connector pinouts and separate STOP handling. Document required firmware changes; do not assume hardware wiring alone enables IPC-101.
4. Print a 1:1 PCB layout or mechanical gauge and trial-fit the received 504, OLED and sensor hardware before ordering.
5. Complete schematic/PCB review, ERC/DRC, silkscreen/polarity inspection, and updated BOM, assembly drawings, harness documentation and fabrication revision marking.
6. Bench-check the assembled board, display, BME and each control before motion integration. Physical fit does not establish electrical or firmware acceptance.
