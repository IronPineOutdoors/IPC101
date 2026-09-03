# IPC-101 P0 Static Validation Record

Date: 2026-09-01. Environment: Windows workspace; KiCad 10 CLI located at `D:\KiCad\bin\kicad-cli.exe` (not on PATH).

| Check | Result | Evidence / limitation |
|---|---|---|
| Required repository files | PASS | All requested paths present |
| S-expression parenthesis balance | PASS | Schematic and PCB counts equal after correction |
| Duplicate PCB reference names | PASS | U1, SW1–3, J1/J3, C1/C2, R1, TP1–4, DS1, H1–4 unique |
| Unassigned footprint review | PASS for PCB study | Every PCB reference has explicit pads; panel SSTOP is intentionally off-board |
| Connector pinout review | PASS static | J1 matches IPC-100 J10 order; J3 matches J8A pair |
| STOP isolation review | PASS static | STOP nets occur only at J3 pads; no zone/net connection |
| Logic-voltage review | PASS static | U1 is 1.65–3.6 V; J10 is protected 3.3 V |
| Current budget | PASS analysis | <5 mA target versus 100 mA J10 limit; OLED separately powered |
| OLED orientation/interface | BLOCKED | Hosyond 2.42-inch SSD1309 B0G2RFLG1L selected for prototype; received-sample pinout, mounting, 3.3 V behavior, address, pull-ups, current, reset population, and backfeed still require qualification |
| SW3 orientation/footprint | BLOCKED | Supplier gives similar-part datasheet; received sample needed |
| U1 land/stencil review | BLOCKED | Peer review/1:1 plot and assembly capability needed |
| Board/mount clearance | PASS static / PROVISIONAL | 100 x 140 mm outline and coordinates coherent; enclosure unmeasured |
| ERC | PASS WITH WARNINGS | KiCad 10 native ERC: 0 errors, 52 warnings; warnings are embedded-library registration, off-grid endpoints, intentional isolated STOP labels, and reviewable pin-type warnings |
| DRC | FAIL / HOLD | KiCad 10 native DRC generated 2026-09-02: 108 violations, including no-net track shorts and missing connections; routing requires a separate repair pass |
| Gerber/drill generation | WITHHELD | Depends on ERC/DRC and footprint closure |

This record does not authorize fabrication.
