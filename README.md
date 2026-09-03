# Iron Pine Outdoors IPC-101

IPC-101 is a prototype operator-control-panel PCB for IPC-100. Revision P0 implements seven ordinary controls through a TCA8418 keypad scanner on IPC-100's protected 3.3 V J10 I2C expansion branch, physically carries the Hosyond 2.42-inch SSD1309 prototype display connected by a dedicated five-wire harness to IPC-100 J6, and carries the normally-closed STOP contact only on a separate J8A harness.

## Release state

**P0 engineering prototype candidate — fabrication hold.** The schematic, routed PCB, BOM, mechanical coordinates, interface reconciliation, and bench plan are captured. Static CAD checks pass. Native KiCad ERC/DRC and Gerber generation are blocked because `kicad-cli` is not installed in this environment. Fabrication also requires physical verification of the Adafruit 504 production footprint and a peer review of the TCA8418 WQFN land pattern.

The PCB outline and control coordinates are provisional until an enclosure and front-panel stack are measured. The bare PCB has no ingress rating.

## Architecture

- START, PULL: Omron B3F-4055 12 mm through-hole tactile switches.
- Navigation: Adafruit 504 five-way through-hole switch (LEFT/RIGHT/UP/DOWN/SELECT).
- STOP: Omron A22NE-M-PD01-N, normally-closed contact, panel mounted; its two wires remain isolated from PCB logic and pass through dedicated connector J3.
- Key scanner: TI TCA8418RTWR at fixed I2C address `0x34`, polled by IPC-100; 7x1 matrix.
- Display: Hosyond 2.42-inch 128x64 I2C SSD1309 module (Amazon ASIN B0G2RFLG1L), mounted on IPC-101 using the corrected Crosswind control-panel fit-print geometry and connected directly to IPC-100 J6 by five wires.
- IPC-100 ordinary-control link: J10, JST GH 4-pin, 3.3 V / 100 mA / 100 kHz I2C.

## Repository map

- `docs/` — controlled requirements, decisions, interfaces, mechanics, and test plan.
- `hardware/kicad/` — KiCad project, schematic, routed PCB, and project-local footprints.
- `hardware/bom/` — prototype BOM.
- `hardware/fabrication/` — release notes and generation instructions; generated plots are intentionally absent pending native DRC.
- `mechanical/` — panel coordinate and cutout data.
- `manufacturing/` — assembly and inspection notes.

## Next action

Open the CAD in KiCad 9 or newer, verify U1 and SW3 footprints against received parts, run ERC/DRC, then build one hand/contract-assembled board and execute the staged bench test plan before connecting motion hardware.
