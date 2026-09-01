# IPC-101 P0 Bench Test Plan

Do not connect motors or actuator power during stages 1–5. Record board serial, CAD revision, IPC-100 firmware hash, instruments, and results.

1. **Incoming inspection:** compare SW3 pins and U1 land pattern to received parts; inspect pin 1, shorts, solder, mounting clearance, labels, and OLED hole spacing.
2. **Unpowered continuity:** verify no 3V3/GND short; J3 pins are isolated from GND, 3V3, and board copper; NC STOP gives continuity only when released.
3. **Current-limited power:** apply 3.3 V at J1 with 20 mA limit. Confirm <5 mA idle target, U1 VCC, RESET high, and no heating.
4. **I2C:** at 100 kHz detect only U1 at 0x34 on J10. Confirm no clock stretching and acceptable rise time with final harness.
5. **Key matrix:** press/release every control 100 times; verify exactly one mapped event per transition, no ghost key, FIFO overflow, stuck event, or cross-action. Test simultaneous adjacent keys.
6. **Fault injection:** unplug J1, open matrix traces where practical, short each row/column through 1 kOhm, reset, and cycle power. Ordinary commands must default inactive.
7. **STOP:** with actuators disconnected, verify opening J3/pressing STOP removes hardware permit within IPC-100 released timing and reports STOP/fault. A wedged I2C bus must not delay it.
8. **OLED:** connect only by J6 harness; confirm address 0x3C, startup, all-pixel pattern, orientation, contrast, current, and pull-up/rise-time compatibility.
9. **System dry run:** simulated loads only; exercise every mapped action and confirm STOP dominates every state.
10. **Mechanical/environmental prototype:** glove trial, 500 cycles, harness tug, vibration, condensation inspection in intended enclosure, and -10 to +50 C screening unless superseded.

Release requires signed results, native ERC/DRC reports, reviewed Gerbers/drills, and closure of SW3/U1 footprint holds.
