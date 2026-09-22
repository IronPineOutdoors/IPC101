# IPC-101 enclosure - current Rev I.1 fit build

**Start with [PRINT THESE](PRINT_THESE.md).** It identifies the cradle versus bezel and links only the current print choices.

[Current N1.4 faceplate: 8 mm P504 opening, compact tree + IPO and preview](faceplate/REV_N14_FACEPLATE.md).

- [Assembly order, hardware and fit measurements](structure/REV_I1_ASSEMBLY.md)
- [I1 structure/service preview with earlier faceplate](structure/RevI1_preview.png)
- [Measured R1 labeled caps (guide shows earlier N1.2 faceplate)](controls/buttons/R1_BUTTON_CAPS.md)
- [Tree traced from supplied wordmark and N1.2 reprint files](faceplate/history/REV_N12_FACEPLATE.md)
- [Current panel/cap preview](faceplate/N14_faceplate_preview.png)
- [N1 button alignment and tree correction basis](faceplate/history/REV_N1_FACEPLATE.md)
- [Historical M4 audit, superseded by physical misalignment report](faceplate/history/REV_M4_FIT_AUDIT.md)
- [Verification results](structure/RevI1_verification.json)
- [Received IDEC STOP switch and mounting measurements](controls/stop/side-pod/STOP_XA1E_BV302R.md)
- [Printable S1 STOP side pod, hardware and assembly](controls/stop/side-pod/STOP_S1_ASSEMBLY.md)
- [S1 STOP installation preview](controls/stop/side-pod/STOP_S1_preview.png)

Status: **TEST-FIT / PHYSICAL VALIDATION PENDING**. I.1 reuses the original R3 carrier and unchanged Rev H bracket/wiring plate. N1.4 uses measured ARM-left/PULL-right positions, compact traced tree + IPO, and an enlarged 8 mm P504 opening, with labels on R1 caps. Cradle dry fit and STOP coupon operation were reported successful; N1.4 directional travel, R1 cap operation, populated-board/harness, hardware and sealing checks remain.

## Current files versus history

Current I.1 parts, original R3, N1.4/R1 print files (earlier faceplates retained as history), and the authoritative Rev H mounting baseline are grouped by component in the subfolders below. **The Rev H box STLs are mounting-reference geometry, not the box to print for I.1.** Print the I.1 box from the guide.

Superseded Rev G and Rev I exports, exploratory H/H1/H2 SCAD files, and their notes are under [archive](archive/README.md). They are retained for engineering history, not current printing. The earlier long README is preserved as [development history](archive/DEVELOPMENT_HISTORY.md).

Some older Python files remain in `tooling/` because the current build imports their geometry helpers, STL writer, or verification functions. Their presence does not make their old parts current:

- `generate_rev_h.py`: authoritative preserved mount geometry.
- `generate_crosswind_control_box.py`: shared STL writer; its historical Rev G command exports into the archive.
- `generate_rev_i.py`, `verify_rev_i.py`, `preview_rev_i.py`: retained baseline/helpers; historical Rev I exports and preview use the archive.

## Generate and verify the current assembly

```powershell
python -B mechanical/enclosure/tooling/generate_rev_i1.py
python -B mechanical/enclosure/tooling/verify_rev_i1.py
python -B mechanical/enclosure/tooling/preview_rev_i1.py
```

Dependencies: Python, manifold3d, numpy and trimesh. `INSTALLED` files share assembly coordinates; use the guide's `PRINT` files in the slicer. Archive cleanup changes file organization only, not current print geometry.

## Folder guide

- `structure/`: I.1 box, cradle and bezel; print and assembly-view exports.
- `faceplate/`: current N1.4 faceplate; earlier revisions in `faceplate/history/`.
- `carrier/`: original R3 carrier.
- `mounting/`: Rev H bracket, wiring plate and reference box.
- `controls/`: buttons, navigation fit coupon, LED tests, and STOP concepts.
- `branding/`: artwork and branding studies.
- `tooling/`: generation, preview and verification scripts; `artifact_paths.json` maps their outputs.
- `archive/`: superseded enclosure designs and development history.
