# IPC-101 Rev C prototype order

Recommended first order: two assembled prototype boards. Do not order production quantity until the received Adafruit 504, OLED, caps, and faceplate have passed physical fit testing.

## PCB fabrication settings

- Dimensions: 150 x 100 mm
- Layers: 2
- Material: FR-4
- Finished thickness: 1.6 mm
- Copper: 1 oz
- Solder mask: customer preference
- Surface finish: lead-free HASL or ENIG; ENIG is preferred for the fine-pitch U1 prototype
- Minimum track/space: 0.20/0.15 mm
- Minimum finished drill: 0.30 mm
- Impedance control: no
- Castellated holes: no
- Edge plating: no
- Gold fingers: no
- Panelization: no; single design

Upload `IPC101_RevC_Gerbers.zip` for PCB fabrication.

## JLCPCB assembly settings

- Assembly side: top only
- Quantity: 2 prototypes
- Upload `IPC101_RevC_JLCPCB_BOM.csv` as the BOM.
- Upload `IPC101_RevC_JLCPCB_CPL.csv` as the component placement file.
- Confirm every footprint overlay in JLCPCB's viewer, especially U1 pin 1 and J1 mating direction. J2 and J4 are hand-installed.
- Approve any unavoidable rotation correction only after comparing the viewer with `IPC101_RevC_assembly_reference.pdf`.
- Do not substitute U1 with a different package or suffix.

SW1, SW2, SW3, D1, J2, J3, J4, the test loops, and the faceplate-mounted OLED are intentionally excluded from SMT assembly; see `IPC101_RevC_HAND_INSTALL.csv`. The OLED branch enters IPC-101 at J4 and leaves at J2; continuity-check all five pins before attaching the display.

## Release checks already completed

- KiCad full DRC: 0 violations, 0 unconnected pads
- KiCad error-level ERC: 0 violations
- Gerber layers and separate PTH/NPTH Excellon drill files generated
- Board statistics confirm a 150 x 100 mm, two-layer, 1.6 mm design

Inventory and assembly-library availability can change between quote and order. The LCSC identifiers in the BOM were checked on 2026-09-04, but the ordering portal remains authoritative at checkout.
