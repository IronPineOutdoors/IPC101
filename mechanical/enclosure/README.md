# IPC-101 enclosure - current Rev I.1 fit build

**Start with [PRINT THESE](PRINT_THESE.md).** It identifies the cradle versus bezel and links only the current print choices.

- [Assembly order, hardware and fit measurements](REV_I1_ASSEMBLY.md)
- [Current assembly preview](RevI1_preview.png)
- [Current N1 faceplate reprint and measured alignment](REV_N1_FACEPLATE.md)
- [N1 faceplate/updated tree preview](N1_faceplate_preview.png)
- [Historical M4 audit, superseded by physical misalignment report](REV_M4_FIT_AUDIT.md)
- [Verification results](RevI1_verification.json)
- [Received IDEC STOP switch and mounting measurements](STOP_XA1E_BV302R.md)
- [Printable S1 STOP side pod, hardware and assembly](STOP_S1_ASSEMBLY.md)
- [S1 STOP installation preview](STOP_S1_preview.png)

Status: **TEST-FIT / PHYSICAL VALIDATION PENDING**. I.1 reuses the original R3 carrier and unchanged Rev H bracket/wiring plate. N1 replaces M4 using measured ARM-left/PULL-right positions and corrected tree artwork. Cradle dry fit and STOP coupon operation were reported successful; the N1 reprint, populated-board/harness, hardware and sealing checks remain.

## Current files versus history

Current I.1 parts, original R3, both N1 material files (M4 retained as history), and the authoritative Rev H mounting baseline remain in this folder. **The Rev H box STLs are mounting-reference geometry, not the box to print for I.1.** Print the I.1 box from the guide.

Superseded Rev G and Rev I exports, exploratory H/H1/H2 SCAD files, and their notes are under [archive](archive/README.md). They are retained for engineering history, not current printing. The earlier long README is preserved as [development history](archive/DEVELOPMENT_HISTORY.md).

Some older Python files remain here because the current build imports their geometry helpers, STL writer, or verification functions. Their presence does not make their old parts current:

- `generate_rev_h.py`: authoritative preserved mount geometry.
- `generate_crosswind_control_box.py`: shared STL writer; its historical Rev G command exports into the archive.
- `generate_rev_i.py`, `verify_rev_i.py`, `preview_rev_i.py`: retained baseline/helpers; historical Rev I exports and preview use the archive.

## Generate and verify the current assembly

```powershell
python -B mechanical/enclosure/generate_rev_i1.py
python -B mechanical/enclosure/verify_rev_i1.py
python -B mechanical/enclosure/preview_rev_i1.py
```

Dependencies: Python, manifold3d, numpy and trimesh. `INSTALLED` files share assembly coordinates; use the guide's `PRINT` files in the slicer. Archive cleanup changes file organization only, not current print geometry.
