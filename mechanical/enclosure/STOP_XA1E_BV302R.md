# Received STOP switch - IDEC XA1E-BV302R

Status: **HARDWARE RECEIVED (user report); MOUNTING FIT PENDING**.

The user identified the received part as `XA1E BV302R`. IDEC lists `XA1E-BV302R` and the regional formatting `XA1E-BV302-R`.

Manufacturer-confirmed characteristics:

- 16 mm nominal panel-mount family; do not interpret this as a finalized printed cutout/tolerance.
- 29 mm red mushroom operator, non-illuminated.
- Two normally closed contacts (2NC), solder terminals.
- Push-lock operation with pull or turn reset; removable contact-block type.

Sources: [IDEC exact-part page](https://www.idec.com/en-eu/switches-indicator-lights/switches-pushbuttons/emergency-stop-switches/xa-16mm-estop/xa1e-bv302r), [IDEC US part page](https://www.idec.com/en-us/switches-indicator-lights/switches-pushbuttons/emergency-stop-switches/xa-16mm-estop/xa1e-bv302-r). Checked 2026-09-21. Do not substitute the dimensions of the different `BV3U02` unibody model.

## Mechanical integration

The old P0 layout's 22.3 mm STOP cutout is superseded for this received part. Its old panel coordinates are also not a placement decision for Rev I.1. M.4 currently has no dedicated STOP mounting opening.

Before assigning a cutout or location, confirm the manufacturer's exact mounting drawing for this variant and measure the received part:

- Panel-seating surface to rear terminal tips, including any fitted terminal cover.
- Maximum rear body and locking-nut width/diameter.
- Allowed panel thickness, locking/keying features, and hand/tool access for installation.
- Additional wire/solder-joint clearance and actuator access/reset motion at the proposed location.

The 16.5 mm PCB stack is not evidence that this switch fits behind the faceplate. Check the full switch and wire envelope against PCB, R3, cradle, bezel, shell and bracket withdrawal before adding geometry. The current bezel/cradle print sequence continues unchanged; no STOP hole or placeholder box has been added.

## Electrical interface context

The repository's [IPC-100/IPC-101 interface](../../docs/interface/IPC100_IPC101_INTERFACE.md) specifies an isolated NC STOP pair on J3: pin 1 `STOP_IN_RAW`, pin 2 `STOP_RETURN`, carried to IPC-100 J8A. Neither signal is ground. Received-switch terminal markings, continuity and final contact allocation remain to be checked before wiring. This arrival note does not change the safety circuit or assign the second NC contact.
