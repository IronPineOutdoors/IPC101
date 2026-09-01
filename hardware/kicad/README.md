# IPC-101 KiCad Source

The PCB is a physical P0 placement/routing study with real pad/net assignments. The schematic file is a KiCad-native human-review connectivity capture rather than a symbol/netlist-complete release schematic. This is deliberate: no native KiCad installation is available here to validate generated symbol libraries, and releasing an unverified synthetic netlist would be unsafe.

## Known CAD holds

- SW3 is marked `VERIFY`; compare its six-pad geometry and direction pin map to an actual Adafruit 504.
- U1 uses the TI RTW-24 4 x 4 mm pin numbering and 2.7 mm exposed pad; peer-review stencil segmentation and courtyard.
- U1 unused GPIOs are directly tied high in the PCB study. The release schematic should replace these with 100 kOhm pull-ups if TI's received-revision datasheet/firmware initialization review requires series resistance.
- J1 and J3 exact supplier footprints/courtyards require library comparison.
- Routed segments are a first-pass topology; native DRC and interactive cleanup are mandatory.
- The B.Cu ground zone excludes the isolated STOP nets by net assignment, but clearance must be confirmed by DRC.

Do not fabricate directly from these files. Close the holds, re-annotate from the released schematic, update PCB from schematic, then run ERC/DRC and plot review.
