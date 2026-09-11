# IPC-101 Rev C arrival and first-power checklist

Prepared 2026-09-11. This is a working acceptance record, not evidence of a passed
test. Mark each item PASS / FAIL / PENDING with measurements and notes.

## Identify the delivered build

- [ ] Record order number, board quantity, delivery date, board ID/serial and photos of both faces.
- [ ] Compare the actual order confirmation/approved assembly list with the local package. The saved recommendation is two top-side assembled prototypes; actual vendor approval and substitutions have not been checked here.
- [ ] Confirm PCB Rev C, 150 x 100 mm, nominal 1.6 mm FR-4, two layers.
- [ ] Confirm the vendor accepted `IPC101_RevC_MaskFix_Gerbers.zip`. The earlier Gerber ZIP is obsolete. Inspect exposed through-hole solder pads on BOTH faces; mask covering those pads is a discrepancy to resolve before soldering.
- [ ] Use the existing Rev C assembly reference, BOM and CPL; the mask correction did not change copper, drills or placement.

Reference set: [order notes](../../hardware/fabrication/IPC101_RevC/ORDER_NOTES.md),
[assembly drawing](../../hardware/fabrication/IPC101_RevC/IPC101_RevC_assembly_reference.pdf),
[assembly BOM](../../hardware/fabrication/IPC101_RevC/IPC101_RevC_JLCPCB_BOM.csv),
[hand-install list](../../hardware/fabrication/IPC101_RevC/IPC101_RevC_HAND_INSTALL.csv).
Paths in this paragraph are relative to this checklist's directory.

## Prepare before delivery

- [ ] Gather multimeter, magnification, fine soldering tools, flux, solder wick, ESD-safe work surface and a current-limited 3.3 V bench supply.
- [ ] Prepare keyed breakout leads so first power does not require loose probes on adjacent connector pins.
- [ ] Have a 3.3 V-compatible I2C host/fixture available. Confirm its pull-ups and voltage before connecting it. A USB connection or I/O line must not back-power the board.
- [ ] Verify availability of IPC-100 J10 power/firmware support or a standalone scanner test fixture. Existing Crosswind direct-GPIO firmware is not proof of a working TCA8418 integration.
- [ ] Inventory the following items; quantities are PER BOARD. Count spares separately.

| Ref / item | Qty | Expected part or action | On hand / missing |
| --- | ---: | --- | --- |
| SW1, SW2 | 2 | B3F-4055 tactile switches; dry-fit cap reach before soldering | |
| SW3 | 1 | Adafruit 504; verify actual six-pin orientation and fit | |
| D1 | 1 | 5 mm COMMON-ANODE RGB LED; verify R-A-G-B order against board | |
| J2 | 1 | JST B5B-XH-A five-pin vertical through-hole header | |
| J3 | 1 | Two-pin 3.81 mm STOP header and matching plug; final part/mate must match IPC-100 J8A | |
| J4 | 1 | JST SM05B-GHS-TB five-pin horizontal SMT header; hand installation | |
| TP1-TP4 | 4 optional | 1 mm through-hole test loops | |
| OLED | 1 | Hosyond 2.42-inch SSD1309, B0G2RFLG1L; inspect actual header and RESET | |
| J1 harness | 1 | GH four-pin mate GHR-04V-S, correct contacts; 26-28 AWG per interface | |
| J4 input harness | 1 | GH five-pin mate GHR-05V-S and correct contacts | |
| J2 output harness | 1 | Matching five-pin XH housing/contacts to actual OLED header | |
| STOP operator/harness | 1 | Actual NC contact assembly, isolated pair; verify received part and connector compatibility | |
| PCB/panel hardware | set | M3 screws/standoffs/inserts; lengths selected from actual stack | |
| TPU fixture hardware | set | Four M3 bolts, washers and nuts per coupon; M3 x 12 mm is a starting candidate | |

The records disagree on STOP operator branding (BOM specifies Omron; TPU notes
mention IDEC). Identify the actual received operator/contact block; do not order
an assumed replacement from that wording. START in the logical matrix and ARM
on the faceplate/BOM also need explicit firmware-semantic reconciliation.

### Rigid prints and TPU preparation

- [ ] Dry-fit the Rev H enclosure, detachable bracket, retaining pin and wiring plate.
- [ ] Use the Rev D faceplate for the next trial: its OLED is shifted 8 mm right. PCB fabrication remains Rev C. Do not force the display onto the PCB's old OLED mounting pattern.
- [ ] Check actual PCB, display, connectors and standoffs together; envelope checks alone did not verify the complete stack.
- [ ] Print two matching rigid clamp frames for each TPU coupon fixture now.
- [ ] When TPU arrives, start with `ARM_PULL_TPU_WEB_0.6mm.stl`, flat as exported. Follow the actual filament profile/drying guidance; ordinary TPU uses the A1 external spool, not AMS Lite.
- [ ] Compare 0.4/0.6/0.8 mm webs and navigation coupons for return, force, defects and permanent deformation. Record material, settings and cycle count.
- [ ] Do not drill the faceplate to the coupon's 44 x 38 mm fixture pattern. These are standalone experiments, not drop-in boots or qualified waterproof seals. Keep STOP uncovered.
- [ ] Select the actual enclosure cable-entry connector/gland before modifying the blank Rev H wiring plate; its current model has no wire passage.

See [panel revisions](../../mechanical/panel/README.md),
[TPU procedure](../../mechanical/panel/tpu-prototypes/README.md), and
[Rev H enclosure](../../mechanical/enclosure/README.md).

## Incoming assembly inspection — no power

- [ ] Expected factory population: U1 TCA8418RTWR (one), R1 10 kOhm (one), R2-R4 1 kOhm (three), C1 100 nF (one), C2 4.7 uF (one), J1 GH four-pin (one). Compare with vendor-approved substitutions, not just the older general BOM.
- [ ] Inspect U1 orientation/pin 1 and visible perimeter joints, bridges, shifted parts, damaged tracks and loose debris. Visual inspection cannot establish hidden exposed-pad wetting.
- [ ] Inspect all J1 pins and anchors. Verify connector pin numbering from the PCB/netlist and housing, not an assumed wire-side view.
- [ ] Confirm hand-install omissions match the list above; J4 is intentionally NOT factory populated in the saved assembly package.
- [ ] Dry-fit SW1/SW2/SW3, caps, LED and the faceplate before committing solder height. No switch should be held pressed by the assembled panel.
- [ ] Hand-solder missing parts with power disconnected; inspect J4's fine-pitch joints and anchors especially carefully.
- [ ] Confirm the common-anode LED and its actual lead order; do not substitute the common-cathode module used in the existing Alpha wiring.
- [ ] Clean only with methods compatible with the switches; do not wash unsealed switches by default.

## Harness and unpowered electrical checks

All pin numbers below are BOARD connector numbers. Verify the mating housing's
numbering/orientation before crimping. Disconnect host, supply and USB power.

| Connector | Pins in order | Source / destination |
| --- | --- | --- |
| J1 | 1: 3.3 V, 2: GND, 3: SDA, 4: SCL | IPC-100 J10; max 0.30 m harness |
| J4 | 1: OLED_VCC, 2: OLED_GND, 3: SDA, 4: SCL, 5: active-low RESET | IPC-100 J6 input |
| J2 | Same five positions as J4 | Output to actual display header; adapt its pin order as marked |
| J3 | 1: STOP_IN_RAW, 2: STOP_RETURN | Separate NC STOP circuit to IPC-100 J8A; neither is logic ground |

- [ ] Measure J1 power-to-ground resistance; record initial and settled values. Investigate a persistent near-short; capacitor charging is not itself a short. No arbitrary resistance threshold is established here.
- [ ] Verify J4-to-J2 continuity 1-to-1 through all five positions, no adjacent shorts, and isolation from J1 nets.
- [ ] Verify J3's two nets are isolated from logic supply/ground and other circuitry. Check the NC switch separately: released = closed, operated = open.
- [ ] Verify every harness end-to-end and inspect crimp retention. Label J1 controls, J4 OLED input, J2 OLED output and SAFETY STOP/J8A distinctly.
- [ ] Inspect the OLED's actual header labels and RESET population. Resolve any unsoldered RES connection before connecting it; do not assume the five module pins match J2 physically.

## First power — keypad board only

Motor and thrower/actuator power remain disconnected. Leave OLED and IPC-100
disconnected for standalone supply testing; never parallel the bench supply
with the IPC-100 output. Do not power J3.

- [ ] Set supply to 3.3 V and 20 mA current limit; output OFF while connecting J1 pin 1 positive and pin 2 return.
- [ ] Turn on; record voltage and idle current. Existing bench target is below 5 mA with status LED channels off. If the supply current-limits, voltage collapses or a component heats, switch off and inspect before increasing the limit.
- [ ] Verify U1 VCC and RESET high using the schematic to identify pads; avoid bridging fine-pitch pins with probes.
- [ ] Check power-off discharge and absence of unintended power from attached instruments/host.

## Keypad and indicator checks

- [ ] With a correctly powered 3.3 V host and appropriate bus pull-ups, detect U1 at 7-bit address 0x34, 100 kHz. IPC-101 does not add J1 I2C pull-ups; IPC-100 owns them in the final system.
- [ ] Confirm the host configures R0-R6/C0, debounce and FIFO, and polls at 10-20 ms. Address detection alone does not prove button operation.
- [ ] Check these seven functions individually, then adjacent simultaneous presses:

| Matrix | Expected raw function | Press/release result |
| --- | --- | --- |
| R0/C0 | LEFT | |
| R1/C0 | RIGHT | |
| R2/C0 | UP | |
| R3/C0 | DOWN | |
| R4/C0 | SELECT | |
| R5/C0 | START (faceplate ARM; verify intended host action) | |
| R6/C0 | PULL | |

- [ ] Repeat each key 100 times per existing bench plan: one event per transition, no cross-action, ghosting, stuck events or FIFO overflow.
- [ ] Exercise D1 colors with the intended driver configuration; record channel identity and current separately from the LED-off idle test.
- [ ] Confirm disconnect/reset of the panel leaves ordinary commands inactive. Defer invasive trace-opening and fault injection to the controlled bench plan; do not cut the new board as an arrival test.

## OLED branch — separate power test

- [ ] Use the separate J4/J2 branch, not J1 power or its 20 mA keypad-only limit.
- [ ] Use current-limited 3.3 V, selected for the verified module. Record startup and steady current; interface limits are 100 mA continuous and 150 mA for at most 20 ms. Those limits are acceptance criteria, not proof that this sample meets them.
- [ ] Verify 0x3C or 0x3D, functional RESET, cold startup, all-pixel pattern, orientation, contrast and no unintended backfeed when unpowered.
- [ ] Check final branch length/capacitance (0.20 m / 50 pF), pull-ups and rise time against the interface. Fixed OLED pull-ups below 47 kOhm are an unresolved compatibility issue to assess, not something to ignore because the display lights.

## Integrated dry run and release record

- [ ] With actuators disconnected, verify the actual STOP path removes hardware permit within IPC-100's released timing; record the applicable requirement and measurement. Verify a stuck I2C bus cannot delay STOP.
- [ ] Verify ordinary key mapping, ARM/START meaning, PULL interlocks and power-cycle defaults with the actual host firmware; record firmware hash and fixture/IPC-100 revision.
- [ ] Reassemble with selected TPU/rigid actuators and repeat key-return/preload checks before committing sealing or adhesives.
- [ ] Record remaining fit, firmware, OLED, STOP and weather-sealing issues. Electrical bench acceptance is not weather or motion-system release.

| Record | Value |
| --- | --- |
| Board ID / order / PCB revision | |
| MaskFix order confirmation | |
| Actual assembly substitutions | |
| Host hardware / firmware hash | |
| Supply voltage / current limit / LED-off idle current | |
| U1 VCC / RESET / I2C result | |
| OLED startup / steady current / reset result | |
| STOP requirement / measured response | |
| Faceplate / enclosure / TPU configuration | |
| Failed checks / next action | |
| Tested by / date / acceptance scope | |

Authority: [interface](../interface/IPC100_IPC101_INTERFACE.md),
[architecture](../architecture/IPC101_ARCHITECTURE.md), and
[full bench plan](IPC101_BENCH_TEST_PLAN.md). The older P0 static-validation record
predates the Rev C release and contains superseded board dimensions and release
status; use the Rev C fabrication package for incoming-board identity.
