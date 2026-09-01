# IPC-101 KiCad Source

The PCB is a physical P0 placement/routing study with real pad/net assignments. The schematic is now a connected KiCad schematic with embedded project symbols, assigned footprints, named nets, power/decoupling, the seven-key matrix, test points, and the isolated J8A STOP connector. KiCad 10 parses it successfully and native ERC reports zero errors; remaining warnings are documented library/grid and intentional isolated-interface warnings.

## Known CAD holds

- SW3 is marked `VERIFY`; compare its six-pad geometry and direction pin map to an actual Adafruit 504.
- U1 uses the TI RTW-24 4 x 4 mm pin numbering and 2.7 mm exposed pad; peer-review stencil segmentation and courtyard.
- U1 unused GPIOs are directly tied high in the schematic and PCB study. Replace these with 100 kOhm pull-ups if TI's received-revision datasheet/firmware initialization review requires series resistance.
- J1 and J3 exact supplier footprints/courtyards require library comparison.
- Routed segments are a first-pass topology; native DRC and interactive cleanup are mandatory.
- The B.Cu ground zone excludes the isolated STOP nets by net assignment, but clearance must be confirmed by DRC.

Do not fabricate directly from these files. Close the holds, register or replace the embedded custom libraries, update PCB from schematic, reroute, then run ERC/DRC and plot review.
