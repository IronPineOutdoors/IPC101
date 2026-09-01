# Fabrication Outputs — HOLD

Gerbers, drill, position, and IPC-356 files are intentionally not checked in because native KiCad DRC could not be run and two footprints require physical review. Generating plots before those gates would create misleading fabrication artifacts.

After opening/saving in KiCad 9 or newer and closing the holds:

```powershell
kicad-cli sch erc hardware/kicad/IPC101.kicad_sch -o hardware/fabrication/IPC101_ERC.rpt
kicad-cli pcb drc hardware/kicad/IPC101.kicad_pcb -o hardware/fabrication/IPC101_DRC.rpt
kicad-cli pcb gerbers hardware/kicad/IPC101.kicad_pcb -o hardware/fabrication/gerbers
kicad-cli pcb drill hardware/kicad/IPC101.kicad_pcb -o hardware/fabrication/gerbers/
kicad-cli pcb pos hardware/kicad/IPC101.kicad_pcb -o hardware/fabrication/IPC101_P0_POS.csv --format csv --units mm
```

Review output layer list, apertures, plated/non-plated drills, outline closure, solder-mask slivers, paste on U1 exposed pad, board dimensions, and 1:1 footprint plots before quoting.
