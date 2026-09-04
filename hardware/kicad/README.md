# IPC-101 Rev C KiCad Source

This directory contains the fabrication-oriented Rev C operator-control board for the Crosswind control-panel replacement.

## Rev C layout

- Board outline: 150 x 100 mm, matching the Rev C faceplate.
- OLED: left-side 2.42-inch Hosyond/SSD1309 mechanical pattern. The display mounts to the faceplate and uses its own five-wire harness to IPC-100 J6 (`OLED_VCC`, `GND`, `SDA`, `SCL`, `RESET`).
- Navigation: Adafruit 504 five-way switch at the right side of the display row.
- Lower controls: ARM at left and PULL at right.
- Indicator: PCB-mounted 5 mm common-anode RGB LED centered between the lower controls and display row.
- Power-switch region: mechanically reserved only; no cutout or footprint is committed until the rated switch is selected.

The IPC-101 board connects to IPC-100 through J1 for `+3V3`, `GND`, `SDA`, and `SCL`. J3 remains the isolated STOP interface. The OLED harness is intentionally not routed through IPC-101.

## Electrical implementation

- U1: TCA8418 keypad/GPIO controller in TI RTW-24 QFN.
- SW1: ARM; SW2: PULL; SW3: LEFT/RIGHT/UP/DOWN/SELECT.
- D1: 5 mm common-anode RGB LED.
- R2/R3/R4: 1 kOhm current-limiting resistors.
- RGB GPIO assignment: COL6/pad 15 red, COL7/pad 16 green, COL8/pad 17 blue.
- Two copper layers with 0.20 mm signal tracks, 0.15 mm clearance, and 0.50/0.30 mm vias.
- F.Cu `+3V3` plane and B.Cu ground plane with explicit island stitching.

`generate_rev_c_pcb.py` reproducibly rebuilds the placed and routed geometry from the embedded footprints. Run it with KiCad's bundled Python, then refill zones and rerun DRC if any placement or routing is edited interactively.

## Validation

- `IPC101_DRC.rpt`: full KiCad DRC, 0 violations and 0 unconnected items.
- `IPC101_ERC.rpt`: KiCad error-level ERC, 0 violations.
- `IPC101_RevC_3D.png`: top-side KiCad render for placement review.
- `IPC101_RevC.net.xml`: exported schematic netlist for parity/review tooling.

Before ordering a production quantity, print the Rev C faceplate and both caps, assemble one PCB, verify the Adafruit 504 physical pin orientation against the received part, and confirm the selected OLED module's header order before building the harness.
