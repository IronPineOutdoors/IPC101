# Iron Pine Outdoors IPC-101

IPC-101 is a prototype operator-control-panel PCB for IPC-100. Revision P0 implements seven ordinary controls through a TCA8418 keypad scanner on IPC-100's protected 3.3 V J10 I2C expansion branch, physically carries the Hosyond 2.42-inch SSD1309 prototype display connected by a dedicated five-wire harness to IPC-100 J6, and carries the normally-closed STOP contact only on a separate J8A harness.

## Release state

**Rev C prototype fabrication package corrected for solder mask.** Use [IPC101_RevC_MaskFix_Gerbers.zip](hardware/fabrication/IPC101_RevC/IPC101_RevC_MaskFix_Gerbers.zip) and the existing Rev C BOM/CPL. The superseded package omitted through-hole solder-mask openings; the replacement contains verified top and bottom openings. Full KiCad DRC passes with 0 violations and 0 unconnected pads. See [order notes](hardware/fabrication/IPC101_RevC/ORDER_NOTES.md) and [verification results](hardware/fabrication/IPC101_RevC/MASK_FIX_VALIDATION.md).

The Rev C board is 150 x 100 mm. Physical control/display/faceplate fit remains a prototype acceptance check; the bare PCB has no ingress rating.

## Architecture

- START, PULL: Omron B3F-4055 12 mm through-hole tactile switches.
- Navigation: Adafruit 504 five-way through-hole switch (LEFT/RIGHT/UP/DOWN/SELECT).
- STOP: Omron A22NE-M-PD01-N, normally-closed contact, panel mounted; its two wires remain isolated from PCB logic and pass through dedicated connector J3.
- Key scanner: TI TCA8418RTWR at fixed I2C address `0x34`, polled by IPC-100; 7x1 matrix.
- Display: Hosyond 2.42-inch 128x64 I2C SSD1309 module (Amazon ASIN B0G2RFLG1L), mounted to the faceplate using the corrected Crosswind geometry and connected through IPC-101 J2/J4 to IPC-100 J6.
- IPC-100 ordinary-control link: J10, JST GH 4-pin, 3.3 V / 100 mA / 100 kHz I2C.

## Repository map

- `docs/` — controlled requirements, decisions, interfaces, mechanics, and test plan.
- `hardware/kicad/` — KiCad project, schematic, routed PCB, and project-local footprints.
- `hardware/bom/` — prototype BOM.
- `hardware/fabrication/` — release notes and generation instructions; verified Gerbers, drills, and assembly outputs are included.
- `mechanical/` — panel coordinate and cutout data.
- `manufacturing/` — assembly and inspection notes.

## Next action

Prepare for the incoming boards with the [Rev C arrival and first-power checklist](docs/testing/IPC101_REVC_ARRIVAL_CHECKLIST.md). It covers the actual order comparison, hand-installed parts, Rev D/Rev H mechanical fit, TPU coupons, harness verification, staged power-up, and result recording. Receipt and acceptance of the replacement manufacturing file must be confirmed against the order; the local package alone does not establish what was fabricated.

Upload the replacement Gerber ZIP to the held JLCPCB order and confirm both solder-mask layers in its viewer. Review assembly orientation before approving production, then fit-test and electrically validate the first prototype before connecting motion hardware.
