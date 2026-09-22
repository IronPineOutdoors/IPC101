#!/usr/bin/env python3
"""Generate the Crosswind IPC-101 angled control-panel enclosure.

Installed coordinates are X across the 156 mm box, Y outward from the wooden
mounting surface, and Z upward.  The 150 x 100 mm faceplate is inclined 47
degrees upward from vertical.  The exported STL is rotated face-down for a
support-light print.
"""

from __future__ import annotations

import math
import struct
from pathlib import Path

import manifold3d as m3d

PANEL_W = 150.0
PANEL_H = 100.0
SIDE_MARGIN = 3.0
BODY_W = PANEL_W + 2 * SIDE_MARGIN
TILT = 47.0
WOOD_H = 101.6
TOP_PROJECTION = 8.0
LOWER_Z = 7.5
WALL = 3.0
FACE_RIM = 7.0
SEGMENTS = 64

# Faceplate/PCB mounting system. All inserts load from the exposed face.
PANEL_HOLES = ((5.0, 5.0), (145.0, 5.0), (5.0, 95.0), (145.0, 95.0))
FACE_BOSS_D = 11.0
FACE_BOSS_DEPTH = 9.0
FACE_DATUM_OFFSET = -1.2
M3_INSERT_PILOT = 4.2
M3_INSERT_DEPTH = 6.0
M3_RELIEF = 3.2

# Rear wood mounting pads, measured in installed coordinates.
WOOD_HOLE_X = (16.0, BODY_W - 16.0)
WOOD_HOLE_Z = (28.0, 70.0)
WOOD_PAD_W = 24.0
WOOD_PAD_H = 20.0
WOOD_PAD_DEPTH = 4.0
WOOD_CLEARANCE = 4.5
WOOD_HEAD_D = 9.5
DRIVER_ACCESS_D = 11.0

CABLE_EXIT_W = 42.0
CABLE_EXIT_H = 20.0


def beam(width: float, y: float, z: float) -> m3d.Manifold:
    return m3d.Manifold.cube((width, 0.2, 0.2)).translate((0.0, y, z))


def wedge(width: float, x_offset: float,
          profile: list[tuple[float, float]]) -> m3d.Manifold:
    return m3d.Manifold.batch_hull([beam(width, y, z) for y, z in profile]).translate((x_offset, 0, 0))


def panel_feature(feature: m3d.Manifold, x: float, vertical: float,
                  normal: float = 0.0) -> m3d.Manifold:
    """Map panel-local XYZ geometry to the installed inclined face."""
    bottom_projection = TOP_PROJECTION + PANEL_H * math.sin(math.radians(TILT))
    return feature.translate((x, vertical, normal)).rotate((90 + TILT, 0, 0)).translate((
        SIDE_MARGIN, bottom_projection, LOWER_Z,
    ))


def y_cylinder(length: float, diameter: float, x: float, y: float, z: float,
               segments: int = SEGMENTS) -> m3d.Manifold:
    """Cylinder extending in installed +Y from its supplied origin."""
    return m3d.Manifold.cylinder(length, diameter / 2, circular_segments=segments).rotate((-90, 0, 0)).translate((x, y, z))


def build_installed_box() -> m3d.Manifold:
    run = PANEL_H * math.sin(math.radians(TILT))
    rise = PANEL_H * math.cos(math.radians(TILT))
    bottom_projection = TOP_PROJECTION + run
    bottom_front = (bottom_projection, LOWER_Z)
    top_front = (TOP_PROJECTION, LOWER_Z + rise)

    outer = wedge(BODY_W, 0, [
        (0, 0), bottom_front, top_front, (0, WOOD_H - 0.2),
    ])

    inset_rise = FACE_RIM * math.cos(math.radians(TILT))
    inset_run = FACE_RIM * math.sin(math.radians(TILT))
    cavity = wedge(BODY_W - 2 * FACE_RIM, FACE_RIM, [
        (-1, WALL),
        (bottom_front[0] + 5 - inset_run, bottom_front[1] + inset_rise),
        (top_front[0] + 5 + inset_run, top_front[1] - inset_rise),
        (-1, WOOD_H - WALL),
    ])
    box = outer - cavity

    # The hull-derived cavity can leave transverse webs behind the inclined
    # face.  Rev F explicitly clears one continuous service opening so the
    # OLED fasteners, PCB, faceplate hardware, and rear wood screws are all
    # reachable with the faceplate removed.  Corner bosses are added afterward.
    service_opening = panel_feature(
        m3d.Manifold.cube((PANEL_W - 2 * FACE_RIM, PANEL_H - 2 * FACE_RIM, 100)),
        FACE_RIM, FACE_RIM, -1,
    )
    box -= service_opening

    # Four broad rear pads create a positive, flush mounting surface against
    # the wood.  Counterbored holes remain reachable with the faceplate off.
    pads = []
    wood_holes = []
    counterbores = []
    driver_tunnels = []
    for x in WOOD_HOLE_X:
        for z in WOOD_HOLE_Z:
            pads.append(m3d.Manifold.cube((WOOD_PAD_W, WOOD_PAD_DEPTH, WOOD_PAD_H)).translate((
                x - WOOD_PAD_W / 2, 0, z - WOOD_PAD_H / 2,
            )))
            wood_holes.append(y_cylinder(WOOD_PAD_DEPTH + 2, WOOD_CLEARANCE, x, -1, z))
            counterbores.append(y_cylinder(WOOD_PAD_DEPTH, WOOD_HEAD_D, x, 1.4, z))
            # Guarantee a straight screwdriver path through either transverse
            # rim while the faceplate is removed.
            driver_tunnels.append(y_cylinder(100, DRIVER_ACCESS_D, x, 1.4, z))
    box += m3d.Manifold.batch_boolean(pads, m3d.OpType.Add)
    box -= m3d.Manifold.batch_boolean(wood_holes + counterbores + driver_tunnels, m3d.OpType.Add)

    # Front-loaded heat-set inserts replace Rev D's inaccessible rear nut traps.
    bosses = []
    insert_pockets = []
    relief_holes = []
    for x, y in PANEL_HOLES:
        bosses.append(panel_feature(
            m3d.Manifold.cylinder(FACE_BOSS_DEPTH - FACE_DATUM_OFFSET,
                                  FACE_BOSS_D / 2, circular_segments=SEGMENTS),
            x, y, FACE_DATUM_OFFSET,
        ))
        insert_pockets.append(panel_feature(
            m3d.Manifold.cylinder(M3_INSERT_DEPTH + 0.2, M3_INSERT_PILOT / 2,
                                  circular_segments=SEGMENTS), x, y, FACE_DATUM_OFFSET - 0.1,
        ))
        relief_holes.append(panel_feature(
            m3d.Manifold.cylinder(FACE_BOSS_DEPTH - M3_INSERT_DEPTH + 0.2,
                                  M3_RELIEF / 2, circular_segments=SEGMENTS),
            x, y, FACE_DATUM_OFFSET + M3_INSERT_DEPTH - 0.1,
        ))
    box += m3d.Manifold.batch_boolean(bosses, m3d.OpType.Add)
    box -= m3d.Manifold.batch_boolean(insert_pockets + relief_holes, m3d.OpType.Add)

    # Low side rails register the faceplate laterally without trapping it.
    rail_depth = 1.2
    rail_width = 1.2
    for local_x in (-rail_width, PANEL_W):
        rail = m3d.Manifold.cube((rail_width, PANEL_H, rail_depth))
        box += panel_feature(rail, local_x, 0, -rail_depth)

    # Large centered exit clears the three IPC-100 harness groups and allows a
    # split-grommet or printed strain-relief insert to be added later.
    cable_exit = m3d.Manifold.cube((CABLE_EXIT_W, 12, CABLE_EXIT_H)).translate((
        (BODY_W - CABLE_EXIT_W) / 2, -2, -1,
    ))
    box -= cable_exit

    # Enforce the wood plane: no feature may project behind Y=0.
    bounds = box.bounding_box()
    if bounds[1] < 0:
        trim = m3d.Manifold.cube((BODY_W + 4, -bounds[1] + 1, WOOD_H + 4)).translate((-2, bounds[1] - 1, -2))
        box -= trim
    return box


def orient_for_print(box: m3d.Manifold) -> m3d.Manifold:
    # Put the flat wooden-mounting plane on the bed.  Unlike the provisional
    # pod's face-down export, this transformation never trims functional
    # geometry.  The 47-degree face remains within the intended self-supporting
    # range while the broad rear pads and shell edges provide bed contact.
    printable = box.rotate((90, 0, 0))
    bounds = printable.bounding_box()
    return printable.translate((-bounds[0], -bounds[1], -bounds[2]))


def write_binary_stl(path: Path, solid: m3d.Manifold) -> None:
    mesh = solid.to_mesh()
    vertices = mesh.vert_properties[:, :3]
    triangles = mesh.tri_verts
    with path.open("wb") as out:
        out.write(b"Crosswind IPC-101 control box Rev G".ljust(80, b"\0"))
        out.write(struct.pack("<I", len(triangles)))
        for indices in triangles:
            points = [vertices[int(index)] for index in indices]
            a, b, c = points
            u, v = b - a, c - a
            normal = (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])
            length = math.sqrt(sum(float(value) ** 2 for value in normal))
            normal = tuple(float(value) / length for value in normal) if length else (0, 0, 0)
            out.write(struct.pack("<12fH", *normal, *(float(value) for point in points for value in point), 0))


if __name__ == "__main__":
    output = Path(__file__).resolve().parent.parent / "archive" / "superseded-rev-g"
    output.mkdir(parents=True, exist_ok=True)
    models = {
        "CrossWind_IPC101_Control_Box_RevG_PRINT.stl": orient_for_print(build_installed_box()),
        "CrossWind_IPC101_Control_Box_RevG_INSTALLED.stl": build_installed_box(),
    }
    for name, model in models.items():
        if model.is_empty() or model.status() != m3d.Error.NoError:
            raise RuntimeError(f"Invalid {name}: {model.status()}")
        write_binary_stl(output / name, model)
        print(f"Generated {name}: {model.num_tri()} triangles, {model.volume():.1f} mm^3")
