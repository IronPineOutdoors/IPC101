# IPC-100 / IPC-101 Interface Reconciliation

Source reviewed: sibling `IPC100` Rev A documentation and preliminary Sheet 09 capture, including Package 10R and the Rev A EBOM (reviewed 2026-09-01).

| IPC-101 need | IPC-100 interface | Disposition |
|---|---|---|
| 7 ordinary keys | J8B exposes only encoder A/B/SW and ARM/FIRE | J8B inadequate; do not overload semantics |
| 3.3 V peripheral + I2C | J10: EXPANSION_VCC, GND, SDA, SCL | Use J10; exact fit after population/firmware enable |
| OLED | J6: OLED_VCC, GND, SDA, SCL, RESET | Route J6 to IPC-101 J4, pass through to J2, then use a short five-wire harness to the faceplate-mounted display |
| Hardware STOP | J8A: STOP_IN_RAW, STOP_RETURN | Use isolated NC switch pair |

## J1 — ordinary controls (IPC-100 J10)

Board connector: JST `SM04B-GHS-TB(LF)(SN)`; mating housing `GHR-04V-S`, contacts `SSHL-002T-P0.2`, 26–28 AWG. Pin order follows IPC-100 J10 Sheet 09 symbol order and must be confirmed by harness drawing before crimping.

| Pin | Signal | Rule |
|---:|---|---|
| 1 | EXPANSION_VCC | protected switched 3.3 V, <=100 mA |
| 2 | GND | logic return |
| 3 | J10_I2C_SDA | IPC-100 owns pull-up/protection |
| 4 | J10_I2C_SCL | 100 kHz; no clock stretching |

Maximum harness length 0.30 m. Power-off mating only. No external power/backfeed. One accessory. U1 fixed address 0x34 lies in released 0x30–0x37 range.

## OLED harness and IPC-101 pass-through

IPC-100 J6 connects to IPC-101 J4 using JST GH wiring: pin 1 OLED_VCC, 2 OLED_GND, 3 OLED_SDA, 4 OLED_SCL, 5 active-low OLED_RESET. IPC-101 passes those five nets directly to J2, a keyed JST XH output with the identical pin order. A short J2-to-module harness adapts to the received OLED's 2.54 mm header. Do not assume the module pin order: inspect its markings and continuity-check both harnesses before power is applied. Limit the complete branch to 0.20 m/50 pF and use address 0x3C or 0x3D. The selected module must operate from 3.0–3.45 V, draw no more than 100 mA continuously/150 mA for 20 ms, have no fixed I2C pull-up below 47 kΩ, meet the released unpowered leakage/backfeed limits, and expose active-low RESET. The listing's statement that `RES` is not soldered by default must be resolved on the received sample; a functional reset conductor is required by the J6 contract.

## J3 — STOP pass-through

| Pin | Signal |
|---:|---|
| 1 | STOP_IN_RAW |
| 2 | STOP_RETURN |

Use an NC contact so an open wire asserts/faults STOP. Neither pin is ground. Use unique two-position Phoenix hardware matching IPC-100 J8A and label both harness ends `SAFETY STOP — J8A`; keep it physically incompatible with ordinary UI connectors.

## Smallest IPC-100 ECO

1. Populate/release J10 and its already designed protected 3.3 V branch.
2. Add the TCA8418 address 0x34 driver and the matrix mapping.
3. Enable 10–20 ms polling without an interrupt conductor.
4. Add IPC-101 presence/fault telemetry; absence keeps commands inactive.

No ESP32 GPIO reassignment, J8B pinout change, or safety-path change is required.
