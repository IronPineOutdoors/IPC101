# IPC101 Rev C solder-mask replacement verification

Date: 2026-09-07. Tools: KiCad 10.0.5 CLI and bundled pcbnew Python.

- Source: 29 PTH pads have F.Mask and B.Mask; 48 SMD pads have assembly-side mask.
- Final ZIP: 77 top and 29 bottom mask flashes; every solderable pad centre found.
- ZIP CRC and exact equality with the exported fabrication files: pass.
- Native full DRC with existing project rules: 0 violations, 0 unconnected pads, 0 footprint errors. Existing ignored checks remain listed in `../../kicad/IPC101_DRC.rpt`.
- Copper, paste, outline, and drill geometry compared with the superseded ZIP: unchanged (generation timestamps ignored).
- D1 reference moved from F.Silkscreen to F.Fab to eliminate its overlap with the newly opened LED pads. Its position and copper remain unchanged.
- Three regression tests: pass (missing source mask rejected, generator restores mask, empty bottom Gerber rejected, corrected exports accepted).
- Bottom-side KiCad render visually inspected: plated component pads exposed; surrounding board masked. See `IPC101_RevC_MaskFix_bottom.png`.
- Existing BOM and CPL retained. No component, wiring, or placement changes.

Replacement file: `IPC101_RevC_MaskFix_Gerbers.zip`

SHA-256: `b067c8119ed9dd976859ae5bafc6f1a0de8f3087623b31338226f0208bbb1501`

Superseded ZIP SHA-256: `eb56a3955d9e1595866eb4c8b064eb22091e3c1dcf8799918ab6c56337e5c303`

Run `generate_package.ps1` to export with DRC and source/Gerber/archive mask checks. Run `D:/KiCad/bin/python.exe hardware/fabrication/IPC101_RevC/test_solder_mask.py` from the project root for regression checks.

This resolves the demonstrated mask omission. Manufacturer layer recognition and assembly orientation must still be checked in the replacement-file viewer before production approval. No upload or production approval was performed in this task.
