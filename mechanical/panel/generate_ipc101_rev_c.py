#!/usr/bin/env python3
"""Generate the IPC-101 Rev C faceplate and operator caps in millimetres.

The 150 x 100 mm faceplate geometry is derived from the supplied CrossWind
Rev B test-fit model.  When viewed from the branded/front surface, the
2.42-inch OLED is on the operator's left and the Adafruit 504 control is on the
right.  ARM/PULL and the centered RGB aperture retain the verified Rev B
centres.
"""

from __future__ import annotations

import math
import struct
from pathlib import Path

import manifold3d as m3d

SEGMENTS = 96
PANEL = (150.0, 100.0, 2.0)
MOUNT_CENTRES = ((5.0, 5.0), (145.0, 5.0), (5.0, 95.0), (145.0, 95.0))
OLED_CENTRE = (46.5, 63.5)
OLED_WINDOW = (57.0, 28.0)
OLED_HOLE_SPAN = (68.8, 38.8)
NAV_CENTRE = (105.0, 63.5)
ARM_CENTRE = (33.5, 20.75)
PULL_CENTRE = (103.5, 20.75)
LED_CENTRE = (68.5, 31.0)
NAV_APERTURE = 8.0

# Compact 5x7 block font used for recessed, printable product branding.  This
# keeps the source model self-contained rather than depending on a workstation
# font that might change between exports.
FONT = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "C": ("01111", "10000", "10000", "10000", "10000", "10000", "01111"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "I": ("11111", "00100", "00100", "00100", "00100", "00100", "11111"),
    "N": ("10001", "11001", "11001", "10101", "10011", "10011", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "W": ("10001", "10001", "10001", "10101", "10101", "10101", "01010"),
}


def cylinder(diameter: float, height: float, centre: tuple[float, float], z: float = -0.5) -> m3d.Manifold:
    return m3d.Manifold.cylinder(height, diameter / 2.0, circular_segments=SEGMENTS).translate((centre[0], centre[1], z))


def rounded_box(width: float, height: float, radius: float, depth: float) -> m3d.Manifold:
    core_x = m3d.Manifold.cube((width - 2 * radius, height, depth)).translate((radius, 0, 0))
    core_y = m3d.Manifold.cube((width, height - 2 * radius, depth)).translate((0, radius, 0))
    corners = []
    for x in (radius, width - radius):
        for y in (radius, height - radius):
            corners.append(m3d.Manifold.cylinder(depth, radius, circular_segments=SEGMENTS).translate((x, y, 0)))
    return core_x + core_y + m3d.Manifold.batch_boolean(corners, m3d.OpType.Add)


def engraved_text(text: str, centre_x: float, baseline_y: float, pixel: float,
                  depth: float = 0.65) -> m3d.Manifold:
    advance = 6 * pixel
    width = max(0.0, len(text) * advance - pixel)
    origin_x = centre_x - width / 2
    pixels = []
    cell = pixel * 0.82
    inset = (pixel - cell) / 2
    for index, character in enumerate(text):
        if character == " ":
            continue
        for row, pattern in enumerate(FONT[character]):
            for column, enabled in enumerate(pattern):
                if enabled == "1":
                    pixels.append(m3d.Manifold.cube((cell, cell, depth + 0.1)).translate((
                        origin_x + index * advance + column * pixel + inset,
                        baseline_y + (6 - row) * pixel + inset,
                        PANEL[2] - depth,
                    )))
    return m3d.Manifold.batch_boolean(pixels, m3d.OpType.Add)


def build_faceplate() -> m3d.Manifold:
    plate = m3d.Manifold.cube(PANEL)
    cuts = [cylinder(3.2, 3.0, centre) for centre in MOUNT_CENTRES]
    cuts.append(m3d.Manifold.cube((OLED_WINDOW[0], OLED_WINDOW[1], 3.0)).translate((
        OLED_CENTRE[0] - OLED_WINDOW[0] / 2,
        OLED_CENTRE[1] - OLED_WINDOW[1] / 2,
        -0.5,
    )))
    for dx in (-OLED_HOLE_SPAN[0] / 2, OLED_HOLE_SPAN[0] / 2):
        for dy in (-OLED_HOLE_SPAN[1] / 2, OLED_HOLE_SPAN[1] / 2):
            cuts.append(cylinder(3.2, 3.0, (OLED_CENTRE[0] + dx, OLED_CENTRE[1] + dy)))
    cuts.extend((
        cylinder(NAV_APERTURE, 3.0, NAV_CENTRE),
        cylinder(5.2, 3.0, LED_CENTRE),
    ))
    for centre in (ARM_CENTRE, PULL_CENTRE):
        aperture = rounded_box(16.0, 10.8, 2.0, 3.0).translate((centre[0] - 8.0, centre[1] - 5.4, -0.5))
        cuts.append(aperture)
    branding = engraved_text("CROSSWIND", 75.0, 7.0, 0.82)
    branding += engraved_text("IRON PINE OUTDOORS", 75.0, 4.0, 0.34)
    return plate - m3d.Manifold.batch_boolean(cuts + [branding], m3d.OpType.Add)


def build_tactile_cap() -> m3d.Manifold:
    top = rounded_box(15.2, 10.0, 2.0, 2.55).translate((-7.6, -5.0, 0))
    flange = rounded_box(18.0, 12.8, 2.3, 0.95).translate((-9.0, -6.4, 2.55))
    boss = m3d.Manifold.cylinder(0.65, 2.75, circular_segments=SEGMENTS).translate((0, 0, 3.5))
    return top + flange + boss


def build_nav_cap() -> m3d.Manifold:
    horizontal = rounded_box(18.0, 7.2, 1.8, 2.8).translate((-9.0, -3.6, 0))
    vertical = rounded_box(7.2, 18.0, 1.8, 2.8).translate((-3.6, -9.0, 0))
    hub = m3d.Manifold.cylinder(1.0, 5.0, circular_segments=SEGMENTS).translate((0, 0, 2.8))
    socket = m3d.Manifold.cylinder(1.5, 3.1, circular_segments=SEGMENTS).translate((0, 0, 2.6))
    return horizontal + vertical + hub - socket


def write_binary_stl(path: Path, solid: m3d.Manifold, label: bytes) -> None:
    mesh = solid.to_mesh()
    vertices = mesh.vert_properties[:, :3]
    triangles = mesh.tri_verts
    with path.open("wb") as out:
        out.write(label[:80].ljust(80, b"\0"))
        out.write(struct.pack("<I", len(triangles)))
        for indices in triangles:
            points = [vertices[int(index)] for index in indices]
            a, b, c = points
            u = b - a
            v = c - a
            normal = (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])
            length = math.sqrt(sum(float(value) ** 2 for value in normal))
            normal = tuple(float(value) / length for value in normal) if length else (0.0, 0.0, 0.0)
            out.write(struct.pack("<12fH", *normal, *(float(value) for point in points for value in point), 0))


if __name__ == "__main__":
    output = Path(__file__).resolve().parent
    models = {
        "CrossWind_ControlPanel_RevC_IPC101.stl": (build_faceplate(), b"IPC-101 Rev C faceplate"),
        "CrossWind_Tactile_Button_Cap_RevC_IPC101.stl": (build_tactile_cap(), b"IPC-101 Rev C tactile cap"),
        "CrossWind_Adafruit504_Nav_Cap_RevC_IPC101.stl": (build_nav_cap(), b"IPC-101 Rev C navigation cap"),
    }
    for filename, (model, label) in models.items():
        if model.is_empty() or model.status() != m3d.Error.NoError:
            raise RuntimeError(f"Invalid model {filename}: {model.status()}")
        write_binary_stl(output / filename, model, label)
        print(f"Generated {filename}: {model.num_tri()} triangles")
