# Fabrication outputs

The validated IPC-101 Rev C order package is in `IPC101_RevC/`.

Use these three files for a JLCPCB PCB-plus-assembly quote:

- `IPC101_RevC_Gerbers.zip`
- `IPC101_RevC_JLCPCB_BOM.csv`
- `IPC101_RevC_JLCPCB_CPL.csv`

The Gerber ZIP contains both copper layers, paste, mask, silkscreen, board outline, and separate PTH/NPTH drill files. The BOM/CPL cover the selected top-side SMT assembly only. Controls, LED, OLED pass-through connectors J2/J4, STOP connector, test loops, OLED, caps, and mechanical hardware are listed separately for hand installation.

Read `IPC101_RevC/ORDER_NOTES.md` before uploading. Inspect every layer in the manufacturer's viewer and confirm U1 pin 1 and J1 mating direction before approving production.

Source validation reports remain under `hardware/kicad/`:

- DRC: 0 violations and 0 unconnected pads
- ERC: 0 errors
