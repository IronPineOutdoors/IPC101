# IPC-101 Rev C prototype order

Recommended first order: two assembled prototype boards. Do not order production quantity until the received Adafruit 504, OLED, caps, and faceplate have passed physical fit testing.

## Solder-mask correction ? 2026-09-07

Upload **`IPC101_RevC_MaskFix_Gerbers.zip`** as the replacement manufacturing file. The earlier `IPC101_RevC_Gerbers.zip` is obsolete and must not be uploaded.

The original local package contained 48 top SMT mask openings but no bottom mask openings. All 29 solderable through-hole pads were missing both mask layers in the source PCB. This revision adds both layers to those pads: the corrected exports have 77 top openings and 29 bottom openings. JLCPCB reported both mask layers missing from the submitted order; the exact earlier portal upload has not been recovered, so that discrepancy cannot be resolved from the local archive alone.

Solder mask is required on **both sides with openings at the solderable pads**. Neither all-over tin nor all-over mask ink is intended. In the replacement-file viewer, confirm the top and bottom mask layers are recognized and the through-hole component pads are exposed on both faces. The board dimensions, copper, drills, placement, BOM, and CPL are unchanged by this correction. The D1 reference label moved to the fabrication layer to clear the newly exposed LED pads. Continue to use the existing Rev C BOM and CPL.

The package generator now checks every solderable pad for its required mask layer, verifies mask flashes at pad centres in both generated Gerbers and the ZIP, and stops on any KiCad or validation failure.

## PCB fabrication settings

- Dimensions: 150 x 100 mm
- Layers: 2
- Material: FR-4
- Finished thickness: 1.6 mm
- Copper: 1 oz
- Solder mask: both sides, openings at solderable pads; color is customer preference
- Surface finish: lead-free HASL or ENIG; ENIG is preferred for the fine-pitch U1 prototype
- Minimum track/space: 0.20/0.15 mm
- Minimum finished drill: 0.30 mm
- Impedance control: no
- Castellated holes: no
- Edge plating: no
- Gold fingers: no
- Panelization: no; single design

Upload `IPC101_RevC_MaskFix_Gerbers.zip` for PCB fabrication.

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
