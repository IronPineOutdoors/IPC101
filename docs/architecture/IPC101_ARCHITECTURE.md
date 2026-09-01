# IPC-101 Architecture

IPC-101 is a passive/keypad-peripheral panel. Seven ordinary keys form a 7-row by 1-column matrix read by U1, a TI TCA8418 at address 0x34. IPC-100 polls the event FIFO over its protected J10 I2C branch; INT is not exported because J10 has no interrupt conductor. The scanner provides hardware debounce and pull-ups, so no per-key RC networks are used.

| Matrix position | Function |
|---|---|
| R0/C0 | LEFT |
| R1/C0 | RIGHT |
| R2/C0 | UP |
| R3/C0 | DOWN |
| R4/C0 | SELECT |
| R5/C0 | START |
| R6/C0 | PULL |

Unused TCA8418 GPIOs are pulled to 3.3 V as required by the datasheet. RESET is pulled high. INT is available at a test pad and polling is mandatory.

The display is intentionally not placed on J10. It remains an IPC-100 J6 peripheral at address 0x3C, preserving J10's one-accessory/address contract. IPC-101 provides the physical mounting pattern, while a short dedicated J6-to-OLED harness serves the module.

STOP is a panel-mounted normally-closed switch on its own two-conductor harness. J3 is only a mechanically convenient pass-through/termination point; neither conductor connects to GND, copper pours, U1, or J1.

## Power budget

| Load | Conservative allocation |
|---|---:|
| TCA8418 active/polling | 1 mA |
| Pull/reset leakage and test points | <1 mA |
| Margin | 8 mA |
| IPC-101 J10 design target | 10 mA maximum |

The OLED is powered from J6 and is not included in J10 current. Adafruit reports roughly 25 mA typical depending on lit pixels; IPC-100 allocates 150 mA to OLED_VCC.

## Firmware contract

IPC-100 shall enable J10/EXPANSION_VCC, configure the 100 kHz segment, probe 0x34, program R0-R6/C0 as a keypad, enable debounce/event FIFO, and poll at 10–20 ms. On loss of the panel or malformed events, ordinary commands default inactive. START and PULL are edge-qualified in product firmware. No IPC-101 event may bypass STOP, limit, watchdog, or actuator-permit logic.
