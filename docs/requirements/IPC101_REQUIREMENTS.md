# IPC-101 P0 Requirements

Status terms: **LOCKED** is supported by IPC-100 source or a selected component; **PROVISIONAL** requires prototype validation; **BLOCKED** needs external data.

| ID | Requirement | Status / verification |
|---|---|---|
| FUN-001 | Provide dedicated START, PULL, and physically distinct STOP controls. | LOCKED; inspection/test |
| FUN-002 | Provide LEFT, RIGHT, UP, DOWN, and SELECT navigation (seven ordinary inputs total with START/PULL). | LOCKED; functional test |
| FUN-003 | Provide a phone-independent 128x64 Hosyond 2.42-inch I2C SSD1309 display (ASIN B0G2RFLG1L) connected through IPC-101 J4/J2 to IPC-100 J6. | PROVISIONAL; sample qualification and measured mounting pattern required |
| ARC-001 | IPC-100 remains system authority; IPC-101 contains no MCU or radio. | LOCKED; schematic inspection |
| ARC-002 | Ordinary controls use IPC-100 J10 at 3.3 V, 100 kHz, <=100 mA, <=0.30 m, no clock stretching or live mating. | LOCKED; IPC-100 contract |
| ARC-003 | The keypad peripheral uses allowed 7-bit address 0x34. | LOCKED; TCA8418 |
| SAF-001 | STOP uses the dedicated J8A supervised pair and is never combined with logic ground. | LOCKED; continuity/isolation test |
| SAF-002 | Opening STOP shall retain IPC-100's hardware inhibit behavior; firmware debounce shall not delay it. | LOCKED; system test |
| ELE-001 | Ordinary switches shall have a defined idle state and hardware debounce. | LOCKED; TCA8418 internal pull-ups/debounce |
| ELE-002 | IPC-101 shall not add I2C pull-ups because IPC-100 owns the segmented-bus pull-ups. | LOCKED; schematic inspection |
| ELE-003 | Local 3.3 V decoupling shall include 100 nF at U1 and 4.7 uF bulk near J1. | LOCKED; inspection |
| ELE-004 | IPC-101 J10 interface current shall remain below 100 mA. | LOCKED; calculated <5 mA typical |
| MECH-001 | PCB outline shall be 100 x 140 mm with four M3 mounting holes for P0. | PROVISIONAL; enclosure measurement |
| MECH-002 | Controls shall follow DISPLAY / NAV / START-STOP / PULL hierarchy. | LOCKED; drawing inspection |
| ENV-001 | Components shall be enclosed against weather; no bare-board IP claim is permitted. | LOCKED |
| MFG-001 | Through-hole operator controls and 0805 passives are preferred; U1 may require stencil/reflow. | LOCKED |
| VAL-001 | Native ERC, DRC, footprint inspection, and first-article continuity shall pass before fabrication release. | BLOCKED; KiCad CLI and received-part checks |

IPC-101 does not duplicate safety qualification, drive motors, source high current, implement wireless communication, or provide an independent system controller. Enclosure, overlay, sealing boots, and final panel thickness are outside P0 until measured.
