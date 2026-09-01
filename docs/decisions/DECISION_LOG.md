# IPC-101 P0 Decision Log

| ID | Decision | Reason | Status |
|---|---|---|---|
| D-001 | IPC-100 remains controller; no ESP32/radio on IPC-101. | Product boundary and minimum complexity. | Accepted |
| D-002 | Use 12 mm B3F-4055 for START/PULL. | Glove target, cap support, THT stability, sourcing. | Accepted |
| D-003 | Use Adafruit 504 five-way navigation. | Direct manual-direction mapping beats encoder semantics. | Accepted with footprint hold |
| D-004 | Use J10 instead of J8B for ordinary controls. | J8B has only five input signals; seven are required. | Accepted; IPC-100 ECO required |
| D-005 | Use TCA8418 at 0x34 in a 7x1 matrix. | Fits J10 released address window and switch common topology. | Accepted |
| D-006 | Poll event FIFO; do not add an interrupt wire. | J10 is four conductors; preserves frozen connector. | Accepted |
| D-007 | Keep OLED on dedicated IPC-100 J6. | Preserves display power/reset contract and one-accessory J10 rule. | Accepted |
| D-008 | STOP is panel-mounted NC on J8A only. | Preserves supervised hardware inhibit and open-wire safety response. | Accepted; exact operator review required |
| D-009 | Provisional 100 x 140 mm panel PCB. | Supports useful prototype spacing without claiming enclosure fit. | Provisional |
| D-010 | Withhold fabrication plots. | Native ERC/DRC and two footprint gates are not closed. | Hold |
