# IPC-101 Mechanical Revision Marking Standard

Status: **ACTIVE DEVELOPMENT STANDARD**  
Established: 2026-09-20

Physical prototype parts should carry a human-readable part/revision mark whenever there is enough non-cosmetic surface area. This is intended to prevent similar prototype prints from being confused during fit testing.

## Format

Preferred full marking:

`IPC101-[PART]-[REV]`

Examples:

- `IPC101-P504-R4.9`
- `IPC101-CARRIER-R1`
- `IPC101-ENC-RH`
- `IPC101-FP-N1`

For small parts, use the shortest unambiguous marking, for example:

- `P504 R4.9`
- `N1`
- `LED R1`

Use `TEST` where practical for intentionally non-final fit-check parts, e.g. `P504 R4.9 TEST`.

## Placement

Revision marks belong on hidden/non-cosmetic surfaces:

- Faceplate: rear surface
- Enclosure: inside or bottom
- PCB carrier/chassis: unused rail or underside
- P504 pedestal: underside
- LED holder: rear/underside
- ARM/PULL caps: underside if sufficient printable area

Do not place engineering revision text on the visible operator face unless specifically required.

## Print geometry

For FDM prototype parts, start with approximately **0.3–0.5 mm recessed/embossed depth** and use lettering large enough to print reliably with the current 0.4 mm nozzle. Increase text size or simplify the mark rather than creating fragile fine lettering.

Revision marking must not weaken a load-bearing wall, sealing surface, snap feature, heat-set-insert boss, fastener land, or tight-tolerance mating surface.

## Revision handling

- Change the physical revision mark whenever geometry changes in a way that affects fit, function, assembly, or testing.
- Cosmetic-only slicer changes do not require a CAD revision unless they alter the physical part.
- Do not reprint already validated parts solely to add a revision mark.
- CAD/source, exported STL and documentation should use matching revision identifiers.
- Record physical validation results in the repository before calling a geometry **FROZEN**.
- Keep superseded files identifiable; do not silently overwrite a prior tested revision with different geometry.

## Prototype vs production numbering

The current R/N-style identifiers are development revisions, not final Iron Pine Outdoors production part numbers. A formal production part-number system will be established later when assemblies approach production-candidate status.

## Current application

Apply this standard beginning with the next generated revisions of:

- P504 pedestal/retainer
- IPC-101 carrier/chassis
- redesigned enclosure
- N.1 faceplate
- LED lens/holder
- ARM/PULL button caps
