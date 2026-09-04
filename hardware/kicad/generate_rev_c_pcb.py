#!/usr/bin/env python3
"""Rebuild IPC-101 as the 150 x 100 mm Rev C Crosswind panel PCB."""

from __future__ import annotations

from pathlib import Path
from collections import defaultdict
from heapq import heappop, heappush
import math

import pcbnew

HERE = Path(__file__).resolve().parent
BOARD_PATH = HERE / "IPC101.kicad_pcb"
KICAD_FOOTPRINTS = Path(r"D:\KiCad\share\kicad\footprints")
MM = pcbnew.FromMM


def point(x: float, y: float) -> pcbnew.VECTOR2I:
    return pcbnew.VECTOR2I(MM(x), MM(y))


def set_position(board: pcbnew.BOARD, reference: str, x: float, y: float, angle: float = 0) -> None:
    footprint = board.FindFootprintByReference(reference)
    if footprint is None:
        raise KeyError(reference)
    footprint.SetPosition(point(x, y))
    footprint.SetOrientationDegrees(angle)


def net(board: pcbnew.BOARD, name: str) -> pcbnew.NETINFO_ITEM:
    item = board.FindNet(name)
    if item is None:
        item = pcbnew.NETINFO_ITEM(board, name)
        board.Add(item)
    return item


def pad(footprint: pcbnew.FOOTPRINT, number: str) -> pcbnew.PAD:
    candidates = [item for item in footprint.Pads() if item.GetNumber() == number]
    if not candidates:
        raise KeyError(f"{footprint.GetReference()} pad {number}")
    return candidates[0]


def clone_resistor(board: pcbnew.BOARD, source: pcbnew.FOOTPRINT, reference: str,
                   value: str, x: float, y: float, first_net: str, second_net: str) -> pcbnew.FOOTPRINT:
    footprint = pcbnew.FOOTPRINT(source)
    footprint.SetReference(reference)
    footprint.SetValue(value)
    footprint.SetPosition(point(x, y))
    footprint.SetOrientationDegrees(90)
    pad(footprint, "1").SetNet(net(board, first_net))
    pad(footprint, "2").SetNet(net(board, second_net))
    board.Add(footprint)
    return footprint


def add_rgb_led(board: pcbnew.BOARD) -> pcbnew.FOOTPRINT:
    footprint = pcbnew.FOOTPRINT(board)
    footprint.SetReference("D1")
    footprint.SetValue("5MM RGB COMMON ANODE")
    footprint.SetPosition(point(68.5, 31.0))
    footprint.SetFPID(pcbnew.LIB_ID())
    for diameter, layer in ((5.0, pcbnew.F_Fab), (5.2, pcbnew.F_Fab)):
        circle = pcbnew.PCB_SHAPE(footprint)
        circle.SetShape(pcbnew.SHAPE_T_CIRCLE)
        circle.SetCenter(point(68.5, 31.0))
        circle.SetEnd(point(68.5 + diameter / 2, 31.0))
        circle.SetLayer(layer)
        circle.SetWidth(MM(0.2))
        footprint.Add(circle)
    definitions = (
        ("1", -1.905, "/RGB_R_K"),
        ("2", -0.635, "/+3V3"),
        ("3", 0.635, "/RGB_G_K"),
        ("4", 1.905, "/RGB_B_K"),
    )
    for number, x, net_name in definitions:
        item = pcbnew.PAD(footprint)
        item.SetNumber(number)
        item.SetAttribute(pcbnew.PAD_ATTRIB_PTH)
        item.SetShape(pcbnew.PAD_SHAPE_CIRCLE if number != "2" else pcbnew.PAD_SHAPE_RECTANGLE)
        item.SetSize(point(1.0, 1.0))
        item.SetDrillSize(point(0.6, 0.6))
        item.SetPosition(point(68.5 + x, 31.0))
        layers = pcbnew.LSET.AllCuMask()
        layers.AddLayerSet(pcbnew.LSET.AllTechMask())
        item.SetLayerSet(layers)
        item.SetNet(net(board, net_name))
        footprint.Add(item)
    board.Add(footprint)
    return footprint


def load_connector(board: pcbnew.BOARD, library: str, name: str, reference: str,
                   value: str, x: float, y: float, angle: float,
                   pin_nets: dict[str, str]) -> pcbnew.FOOTPRINT:
    footprint = pcbnew.FootprintLoad(str(KICAD_FOOTPRINTS / f"{library}.pretty"), name)
    if footprint is None:
        raise FileNotFoundError(f"Unable to load {library}:{name}")
    footprint.SetReference(reference)
    footprint.SetValue(value)
    footprint.SetPosition(point(x, y))
    footprint.SetOrientationDegrees(angle)
    make_footprint_self_contained(footprint)
    for number, net_name in pin_nets.items():
        pad(footprint, number).SetNet(net(board, net_name))
    board.Add(footprint)
    return footprint


def track(board: pcbnew.BOARD, start: pcbnew.VECTOR2I, end: pcbnew.VECTOR2I,
          net_item: pcbnew.NETINFO_ITEM, layer: int = pcbnew.F_Cu, width: float = 0.2) -> None:
    if start == end:
        return
    item = pcbnew.PCB_TRACK(board)
    item.SetStart(start)
    item.SetEnd(end)
    item.SetWidth(MM(width))
    item.SetLayer(layer)
    item.SetNet(net_item)
    board.Add(item)


def route_l(board: pcbnew.BOARD, a: pcbnew.PAD, b: pcbnew.PAD,
            layer: int = pcbnew.F_Cu, horizontal_first: bool = True, width: float = 0.25) -> None:
    start, end = a.GetPosition(), b.GetPosition()
    corner = pcbnew.VECTOR2I(end.x, start.y) if horizontal_first else pcbnew.VECTOR2I(start.x, end.y)
    track(board, start, corner, a.GetNet(), layer, width)
    track(board, corner, end, a.GetNet(), layer, width)


def add_via(board: pcbnew.BOARD, xy: tuple[float, float], net_item: pcbnew.NETINFO_ITEM) -> None:
    item = pcbnew.PCB_VIA(board)
    item.SetPosition(point(*xy))
    item.SetWidth(MM(0.5))
    item.SetDrill(MM(0.3))
    item.SetNet(net_item)
    board.Add(item)


def polyline(board: pcbnew.BOARD, net_item: pcbnew.NETINFO_ITEM, layer: int,
             coordinates: list[tuple[float, float]], width: float = 0.2) -> None:
    for start, end in zip(coordinates, coordinates[1:]):
        track(board, point(*start), point(*end), net_item, layer, width)


def manual_routes(board: pcbnew.BOARD, refs: dict[str, pcbnew.FOOTPRINT]) -> None:
    """Deterministic orthogonal routes with dedicated B.Cu vertical lanes."""
    def pxy(reference: str, number: str) -> tuple[float, float]:
        return mm_pos(pad(refs[reference], number))

    def lane(net_name: str, source: tuple[float, float], destination: tuple[float, float],
             lane_x: float) -> None:
        ni = net(board, net_name)
        polyline(board, ni, pcbnew.F_Cu, [source, (lane_x, source[1])])
        add_via(board, (lane_x, source[1]), ni)
        polyline(board, ni, pcbnew.B_Cu, [(lane_x, source[1]), (lane_x, destination[1])])
        add_via(board, (lane_x, destination[1]), ni)
        polyline(board, ni, pcbnew.F_Cu, [(lane_x, destination[1]), destination])

    lane("/R6_PULL", pxy("U1", "2"), pxy("SW2", "1"), 94.0)
    lane("/R5_ARM", pxy("U1", "3"), pxy("SW1", "1"), 24.0)
    lane("/R4_SELECT", pxy("U1", "4"), pxy("SW3", "6"), 116.0)
    lane("/R3_DOWN", pxy("U1", "5"), pxy("SW3", "5"), 93.0)
    lane("/R2_UP", pxy("U1", "6"), pxy("SW3", "4"), 91.0)

    # Bottom-side QFN pins approach the navigation switch at distinct heights.
    for name, number, via_y, b_x, y_lane, target in (
        ("/R1_RIGHT", "7", 82.0, 122.0, 61.0, (110.0, 63.5)),
        ("/R0_LEFT", "8", 83.0, 120.0, 66.0, (100.0, 63.5)),
    ):
        ni = net(board, name)
        sx, sy = pxy("U1", number)
        polyline(board, ni, pcbnew.F_Cu, [(sx, sy), (sx, via_y)])
        add_via(board, (sx, via_y), ni)
        polyline(board, ni, pcbnew.B_Cu, [(sx, via_y), (b_x, via_y), (b_x, y_lane)])
        add_via(board, (b_x, y_lane), ni)
        polyline(board, ni, pcbnew.F_Cu, [(b_x, y_lane), (target[0], y_lane), target])

    # Shared C0 return uses a low B.Cu bus beneath the two tactile switches.
    common = net(board, "/C0")
    sx, sy = pxy("U1", "9")
    polyline(board, common, pcbnew.F_Cu, [(sx, sy), (sx, 84.0)])
    add_via(board, (sx, 84.0), common)
    polyline(board, common, pcbnew.B_Cu,
             [(sx, 84.0), (108.0, 84.0), (108.0, 15.0), (39.75, 15.0), (39.75, 18.25)])
    polyline(board, common, pcbnew.B_Cu,
             [(108.0, 15.0), (109.75, 15.0), (109.75, 18.25)])
    add_via(board, (108.0, 70.5), common)
    polyline(board, common, pcbnew.F_Cu, [(108.0, 70.5), (105.0, 70.5), (105.0, 68.5)])

    # RGB GPIO channels use separated B.Cu levels before arriving at the SMD resistors.
    for name, pin_no, exit_x, level_y, resistor in (
        ("/RGB_R_GPIO", "15", 137.0, 38.0, "R2"),
        ("/RGB_G_GPIO", "16", 139.0, 40.0, "R3"),
        ("/RGB_B_GPIO", "17", 141.0, 42.0, "R4"),
    ):
        ni = net(board, name)
        source = pxy("U1", pin_no)
        destination = pxy(resistor, "1")
        polyline(board, ni, pcbnew.F_Cu, [source, (exit_x, source[1])])
        add_via(board, (exit_x, source[1]), ni)
        polyline(board, ni, pcbnew.B_Cu, [(exit_x, source[1]), (exit_x, level_y)])
        add_via(board, (exit_x, level_y), ni)
        polyline(board, ni, pcbnew.F_Cu,
                 [(exit_x, level_y), (destination[0], level_y)])
        add_via(board, (destination[0], level_y), ni)
        polyline(board, ni, pcbnew.B_Cu, [(destination[0], level_y), destination])
        add_via(board, destination, ni)

    for net_name, resistor, led_pin in (
        ("/RGB_R_K", "R2", "1"), ("/RGB_G_K", "R3", "3"), ("/RGB_B_K", "R4", "4"),
    ):
        track(board, pad(refs[resistor], "2").GetPosition(), pad(refs["D1"], led_pin).GetPosition(),
              net(board, net_name), pcbnew.F_Cu)

    # Local controller support and the four-wire IPC-100 interface.
    reset = net(board, "/RESET")
    polyline(board, reset, pcbnew.F_Cu,
             [pxy("U1", "20"), (124.75, 69.0), (117.0, 69.0), pxy("R1", "2")])
    for net_name, pin_no, trunk_x, header_pin, testpoint in (
        ("/SCL", "23", 132.0, "4", "TP4"),
        ("/SDA", "22", 134.0, "3", "TP3"),
    ):
        ni = net(board, net_name)
        source = pxy("U1", pin_no)
        top_y = 74.5 if net_name == "/SCL" else 73.5
        polyline(board, ni, pcbnew.F_Cu, [source, (source[0], top_y)])
        add_via(board, (source[0], top_y), ni)
        polyline(board, ni, pcbnew.B_Cu, [(source[0], top_y), (127.0, top_y)])
        add_via(board, (127.0, top_y), ni)
        polyline(board, ni, pcbnew.F_Cu, [(127.0, top_y), (129.0, top_y)])
        add_via(board, (129.0, top_y), ni)
        polyline(board, ni, pcbnew.B_Cu, [(129.0, top_y), (trunk_x, top_y)])
        hx, hy = pxy("J1", header_pin)
        header_y = 93.0 if net_name == "/SCL" else 97.0
        polyline(board, ni, pcbnew.B_Cu, [(trunk_x, top_y), (trunk_x, header_y), (hx, header_y)])
        add_via(board, (hx, header_y), ni)
        polyline(board, ni, pcbnew.F_Cu, [(hx, header_y), (hx, hy)])
        tx, ty = pxy(testpoint, "1")
        add_via(board, (trunk_x, ty), ni)
        polyline(board, ni, pcbnew.F_Cu, [(trunk_x, ty), (tx, ty)])

    for reference in ("SW1", "SW2"):
        for number in ("1", "2"):
            lands = [p for p in refs[reference].Pads() if p.GetNumber() == number]
            track(board, lands[0].GetPosition(), lands[1].GetPosition(), lands[0].GetNet(), pcbnew.B_Cu)

    ground = net(board, "/GND")
    polyline(board, ground, pcbnew.F_Cu, [pxy("J1", "2"), (127.0, 91.0)])

    # The display remains on IPC-100's dedicated J6 electrical branch, but both
    # ends now terminate on IPC-101 so the complete operator panel is removable.
    # The two keyed connectors sit together at the rear edge, allowing a short,
    # ordered fanout with no electrical connection to the J10 keypad branch.
    oled_routes = (
        ("/OLED_VCC", "1", "1", 0.20),
        ("/OLED_GND", "2", "2", 0.20),
        ("/OLED_SDA", "3", "3", 0.20),
        ("/OLED_SCL", "4", "4", 0.20),
        ("/OLED_RESET", "5", "5", 0.20),
    )
    for net_name, j2_pin, j4_pin, width in oled_routes:
        ni = net(board, net_name)
        j2_xy = pxy("J2", j2_pin)
        j4_xy = pxy("J4", j4_pin)
        via_xy = (j4_xy[0], 91.0)
        route = [j2_xy, via_xy]
        if j2_pin == "4":
            route = [j2_xy, (85.5, 79.0), (86.0, 86.0), via_xy]
        elif j2_pin == "5":
            route = [j2_xy, (87.0, 78.0), (87.5, 87.0), via_xy]
        polyline(board, ni, pcbnew.B_Cu, route, width)
        add_via(board, via_xy, ni)
        polyline(board, ni, pcbnew.F_Cu, [via_xy, j4_xy], width)

    # Short spokes bridge QFN power-pad islands into the surrounding F.Cu plane.
    power = net(board, "/+3V3")
    for number, endpoint in (("1", (112.0, 76.75)), ("21", (124.25, 71.5)),
                             ("18", (128.0, 76.75)), ("14", (128.0, 78.75)),
                             ("10", (124.25, 82.0))):
        polyline(board, power, pcbnew.F_Cu, [pxy("U1", number), endpoint])
        add_via(board, endpoint, power)
    polyline(board, power, pcbnew.F_Cu, [pxy("U1", "10"), pxy("U1", "12")])
    polyline(board, power, pcbnew.F_Cu, [pxy("U1", "13"), pxy("U1", "14")])
    polyline(board, power, pcbnew.B_Cu,
             [(124.25, 71.5), (128.0, 71.5),
              (128.0, 78.75), (128.0, 82.0), (124.25, 82.0)])
    polyline(board, power, pcbnew.B_Cu,
             [(112.0, 76.75), (112.0, 10.0), (130.0, 10.0),
              (130.0, 71.5), (124.25, 71.5)])


GRID = 0.5
LAYERS = (pcbnew.F_Cu, pcbnew.B_Cu)


def mm_pos(item) -> tuple[float, float]:
    p = item.GetPosition()
    return pcbnew.ToMM(p.x), pcbnew.ToMM(p.y)


def grid_xy(x: float, y: float) -> tuple[int, int]:
    return round(x / GRID), round(y / GRID)


def route_board(board: pcbnew.BOARD) -> None:
    """Route every net with a deterministic two-layer clearance-aware grid router."""
    all_pads = [p for fp in board.GetFootprints() for p in fp.Pads() if p.GetNetname()]
    by_net: dict[str, list[pcbnew.PAD]] = defaultdict(list)
    for p in all_pads:
        # Duplicate switch lands with the same pin number are internally common.
        key = (p.GetParentFootprint().GetReference(), p.GetNumber())
        if not any((q.GetParentFootprint().GetReference(), q.GetNumber()) == key for q in by_net[p.GetNetname()]):
            by_net[p.GetNetname()].append(p)

    occupied = {layer: {} for layer in LAYERS}
    vias: dict[tuple[int, int], str] = {}

    def pad_blocked(net_name: str, ix: int, iy: int) -> bool:
        x, y = ix * GRID, iy * GRID
        for p in all_pads:
            if p.GetNetname() == net_name:
                continue
            px, py = mm_pos(p)
            sx, sy = pcbnew.ToMM(p.GetSize().x) / 2 + 0.38, pcbnew.ToMM(p.GetSize().y) / 2 + 0.38
            if abs(x - px) <= sx and abs(y - py) <= sy:
                return True
        return False

    def free(net_name: str, state: tuple[int, int, int], goals: set[tuple[int, int]]) -> bool:
        ix, iy, layer = state
        if not (3 <= ix * GRID <= 147 and 3 <= iy * GRID <= 97):
            return False
        if (ix, iy) in goals:
            return True
        if pad_blocked(net_name, ix, iy):
            return False
        if occupied[layer].get((ix, iy), net_name) != net_name:
            return False
        if vias.get((ix, iy), net_name) != net_name:
            return False
        # Keep copper well clear of the four mounting holes.
        return all(math.hypot(ix * GRID - hx, iy * GRID - hy) >= 3.0
                   for hx, hy in ((5, 5), (145, 5), (5, 95), (145, 95)))

    def nearest_ports(p: pcbnew.PAD, net_name: str) -> list[tuple[int, int, int]]:
        x, y = mm_pos(p)
        cx, cy = grid_xy(x, y)
        candidates = []
        for radius in range(0, 7):
            for dx in range(-radius, radius + 1):
                for dy in range(-radius, radius + 1):
                    if max(abs(dx), abs(dy)) != radius:
                        continue
                    for layer in LAYERS:
                        s = (cx + dx, cy + dy, layer)
                        if free(net_name, s, set()):
                            candidates.append(s)
            if candidates:
                return candidates
        raise RuntimeError(f"No routing port for {p.GetParentFootprint().GetReference()}.{p.GetNumber()}")

    def astar(net_name: str, starts, goals):
        goal_xy = {(g[0], g[1]) for g in goals}
        queue = []
        distance = {}
        previous = {}
        for s in starts:
            distance[s] = 0
            heappush(queue, (0, s))
        while queue:
            _, current = heappop(queue)
            if (current[0], current[1]) in goal_xy:
                path = [current]
                while current in previous:
                    current = previous[current]
                    path.append(current)
                return list(reversed(path))
            ix, iy, layer = current
            neighbours = [(ix + 1, iy, layer), (ix - 1, iy, layer),
                          (ix, iy + 1, layer), (ix, iy - 1, layer),
                          (ix, iy, LAYERS[1] if layer == LAYERS[0] else LAYERS[0])]
            for nxt in neighbours:
                if not free(net_name, nxt, goal_xy):
                    continue
                step = 18 if nxt[2] != layer else 1
                candidate = distance[current] + step
                if candidate >= distance.get(nxt, 10**9):
                    continue
                distance[nxt] = candidate
                previous[nxt] = current
                h = min(abs(nxt[0] - gx) + abs(nxt[1] - gy) for gx, gy in goal_xy)
                heappush(queue, (candidate + h, nxt))
        raise RuntimeError(f"Unable to route {net_name}")

    def add_path(net_item, path):
        # Compress collinear grid moves and install vias at layer changes.
        segment = [path[0]]
        for state in path[1:]:
            if state[2] != segment[-1][2]:
                if len(segment) > 1:
                    track(board, point(segment[0][0] * GRID, segment[0][1] * GRID),
                          point(segment[-1][0] * GRID, segment[-1][1] * GRID), net_item, segment[0][2])
                via = pcbnew.PCB_VIA(board)
                via.SetPosition(point(state[0] * GRID, state[1] * GRID))
                via.SetWidth(MM(0.7)); via.SetDrill(MM(0.35)); via.SetNet(net_item)
                board.Add(via); vias[(state[0], state[1])] = net_item.GetNetname()
                segment = [state]
                continue
            if len(segment) >= 2:
                a, b = segment[-2], segment[-1]
                if (b[0] - a[0], b[1] - a[1]) != (state[0] - b[0], state[1] - b[1]):
                    track(board, point(segment[0][0] * GRID, segment[0][1] * GRID),
                          point(b[0] * GRID, b[1] * GRID), net_item, b[2])
                    segment = [b]
            segment.append(state)
        if len(segment) > 1:
            track(board, point(segment[0][0] * GRID, segment[0][1] * GRID),
                  point(segment[-1][0] * GRID, segment[-1][1] * GRID), net_item, segment[0][2])
        for ix, iy, layer in path:
            occupied[layer][(ix, iy)] = net_item.GetNetname()

    # Escape the dense QFN support pins first, then route panel controls. Power is
    # deliberately last because its many branches otherwise form routing walls.
    nets = [(name, pads) for name, pads in by_net.items()
            if len(pads) > 1 and name not in ("/GND", "/+3V3")]
    priority = {name: rank for rank, name in enumerate((
        "/SCL", "/SDA", "/RESET", "/INT_TEST",
        "/RGB_R_GPIO", "/RGB_G_GPIO", "/RGB_B_GPIO",
        "/RGB_R_K", "/RGB_G_K", "/RGB_B_K",
        "/R6_PULL", "/R5_ARM", "/R4_SELECT", "/R3_DOWN",
        "/R2_UP", "/R1_RIGHT", "/R0_LEFT", "/C0", "/GND", "/+3V3",
    ))}
    nets.sort(key=lambda pair: priority.get(pair[0], 100))
    for net_name, pads in nets:
        print(f"  {net_name}: {len(pads)} pads", flush=True)
        connected = [pads[0]]
        remaining = pads[1:]
        while remaining:
            target = min(remaining, key=lambda p: min(math.dist(mm_pos(p), mm_pos(q)) for q in connected))
            source = min(connected, key=lambda p: math.dist(mm_pos(p), mm_pos(target)))
            starts = nearest_ports(source, net_name)
            goals = nearest_ports(target, net_name)
            print(f"    {source.GetParentFootprint().GetReference()}.{source.GetNumber()} {starts[:2]} -> {target.GetParentFootprint().GetReference()}.{target.GetNumber()} {goals[:2]}", flush=True)
            path = astar(net_name, starts, goals)
            add_path(source.GetNet(), path)
            # Short pad-to-grid escape stubs are safe because the selected port is nearby.
            sp, ep = path[0], path[-1]
            track(board, source.GetPosition(), point(sp[0] * GRID, sp[1] * GRID), source.GetNet(), sp[2])
            track(board, point(ep[0] * GRID, ep[1] * GRID), target.GetPosition(), target.GetNet(), ep[2])
            connected.append(target)
            remaining.remove(target)


def add_plane(board: pcbnew.BOARD, net_name: str, layer: int) -> None:
    zone = pcbnew.ZONE(board)
    zone.SetLayer(layer)
    zone.SetNet(net(board, net_name))
    zone.SetPadConnection(pcbnew.ZONE_CONNECTION_FULL)
    outline = zone.Outline().NewOutline()
    for x, y in ((2, 2), (148, 2), (148, 98), (2, 98)):
        zone.Outline().Append(point(x, y), outline)
    board.Add(zone)


def add_ground_fanout(board: pcbnew.BOARD, refs: dict[str, pcbnew.FOOTPRINT]) -> None:
    ground = net(board, "/GND")
    for reference, number, dx, dy in (("U1", "19", 0, -5.8), ("C1", "2", 2, 0), ("C2", "2", 2, 0)):
        source = pad(refs[reference], number)
        x, y = mm_pos(source)
        destination = point(x + dx, y + dy)
        track(board, source.GetPosition(), destination, ground, pcbnew.F_Cu)
        add_via(board, (x + dx, y + dy), ground)
    add_via(board, mm_pos(pad(refs["U1"], "25")), ground)
    polyline(board, ground, pcbnew.F_Cu,
             [mm_pos(pad(refs["U1"], "25")), (125.25, 76.5), mm_pos(pad(refs["U1"], "19"))])
    polyline(board, ground, pcbnew.B_Cu, [(125.25, 70.0), (126.0, 68.0)])
    add_via(board, (126.0, 68.0), ground)
    polyline(board, ground, pcbnew.F_Cu, [(126.0, 68.0), (134.0, 68.0)])
    add_via(board, (134.0, 68.0), ground)
    polyline(board, ground, pcbnew.B_Cu, [(134.0, 68.0), (135.0, 68.0), (135.0, 84.0)])
    add_via(board, (135.0, 84.0), ground)
    polyline(board, ground, pcbnew.F_Cu, [(135.0, 84.0), (130.0, 84.0)])
    add_via(board, (130.0, 84.0), ground)
    polyline(board, ground, pcbnew.B_Cu,
             [(130.0, 84.0), (130.0, 91.0), (127.0, 91.0)])


def add_outline(board: pcbnew.BOARD) -> None:
    for item in list(board.Drawings()):
        if item.GetLayer() == pcbnew.Edge_Cuts:
            board.RemoveNative(item)
    corners = ((0, 0), (150, 0), (150, 100), (0, 100), (0, 0))
    for start, end in zip(corners, corners[1:]):
        edge = pcbnew.PCB_SHAPE(board)
        edge.SetShape(pcbnew.SHAPE_T_SEGMENT)
        edge.SetStart(point(*start))
        edge.SetEnd(point(*end))
        edge.SetLayer(pcbnew.Edge_Cuts)
        edge.SetWidth(MM(0.05))
        board.Add(edge)


def make_footprint_self_contained(footprint: pcbnew.FOOTPRINT) -> None:
    """Keep embedded geometry authoritative and move assembly markings to F.Fab."""
    footprint.SetFPID(pcbnew.LIB_ID())
    footprint.Reference().SetLayer(pcbnew.F_Fab)
    footprint.Value().SetLayer(pcbnew.F_Fab)
    for item in footprint.GraphicalItems():
        if item.GetLayer() == pcbnew.F_SilkS:
            item.SetLayer(pcbnew.F_Fab)


def main() -> None:
    print("load source", flush=True)
    source_board = pcbnew.LoadBoard(str(BOARD_PATH))
    board = pcbnew.BOARD()
    settings = board.GetDesignSettings()
    settings.m_MinClearance = MM(0.15)
    settings.m_MinThroughDrill = MM(0.3)
    settings.m_ViasMinSize = MM(0.5)
    default_class = board.GetAllNetClasses()["Default"]
    default_class.SetClearance(MM(0.15))
    default_class.SetTrackWidth(MM(0.2))
    default_class.SetViaDiameter(MM(0.5))
    default_class.SetViaDrill(MM(0.3))
    references = ("H1", "H2", "H3", "H4", "SW1", "SW2", "SW3", "U1", "J1", "J3",
                  "R1", "C1", "C2", "TP1", "TP2", "TP3", "TP4", "DS1")
    existing = {}
    for reference in references:
        source = source_board.FindFootprintByReference(reference)
        if source is None:
            raise KeyError(reference)
        footprint = pcbnew.FOOTPRINT(source)
        make_footprint_self_contained(footprint)
        for item in footprint.Pads():
            old_name = item.GetNetname()
            if old_name:
                item.SetNet(net(board, old_name))
        board.Add(footprint)
        existing[reference] = footprint
    print("cloned footprints", flush=True)
    add_outline(board)
    placements = {
        "H1": (5, 5, 0), "H2": (145, 5, 0), "H3": (5, 95, 0), "H4": (145, 95, 0),
        "SW1": (33.5, 20.75, 0), "SW2": (103.5, 20.75, 0), "SW3": (105, 63.5, 0),
        "U1": (124, 78, 0), "J1": (128, 95, 0), "J3": (139, 92, 0),
        "R1": (116, 67, 0), "C1": (138, 86, 0), "C2": (124, 91, 0),
        "TP1": (110, 90, 0), "TP2": (106, 90, 0), "TP3": (102, 88, 0), "TP4": (98, 86, 0),
        "DS1": (46.5, 63.5, 0),
    }
    for reference, (x, y, angle) in placements.items():
        footprint = existing[reference]
        footprint.SetPosition(point(x, y))
        footprint.SetOrientationDegrees(angle)
    print("placed footprints", flush=True)
    sw1 = existing["SW1"]
    sw1.SetValue("ARM B3F-4055")
    arm_net = net(board, "/R5_ARM")
    for item in sw1.Pads():
        if item.GetNumber() == "1":
            item.SetNet(arm_net)

    u1 = existing["U1"]
    pad(u1, "3").SetNet(arm_net)
    rgb_gpio = ("/RGB_R_GPIO", "/RGB_G_GPIO", "/RGB_B_GPIO")
    for number, name in zip(("15", "16", "17"), rgb_gpio):
        pad(u1, number).SetNet(net(board, name))

    source_resistor = existing["R1"]
    resistors = (
        clone_resistor(board, source_resistor, "R2", "1k RED", 65.0, 35.5, "/RGB_R_GPIO", "/RGB_R_K"),
        clone_resistor(board, source_resistor, "R3", "1k GREEN", 68.5, 35.5, "/RGB_G_GPIO", "/RGB_G_K"),
        clone_resistor(board, source_resistor, "R4", "1k BLUE", 72.0, 35.5, "/RGB_B_GPIO", "/RGB_B_K"),
    )
    led = add_rgb_led(board)
    oled_nets = {
        "1": "/OLED_VCC", "2": "/OLED_GND", "3": "/OLED_SDA",
        "4": "/OLED_SCL", "5": "/OLED_RESET",
    }
    j2 = load_connector(
        board, "Connector_JST", "JST_XH_B5B-XH-A_1x05_P2.50mm_Vertical",
        "J2", "OLED HARNESS OUTPUT", 65.0, 70.0, 0, oled_nets,
    )
    j4 = load_connector(
        board, "Connector_JST", "JST_GH_SM05B-GHS-TB_1x05-1MP_P1.25mm_Horizontal",
        "J4", "IPC-100 J6 OLED INPUT", 82.0, 95.0, 0,
        {"1": "/OLED_VCC", "2": "/OLED_GND", "3": "/OLED_SDA",
         "4": "/OLED_SCL", "5": "/OLED_RESET"},
    )
    print("added RGB", flush=True)

    refs = existing | {fp.GetReference(): fp for fp in resistors} | {"D1": led, "J2": j2, "J4": j4}
    print("routing", flush=True)
    manual_routes(board, refs)
    add_ground_fanout(board, refs)
    add_plane(board, "/+3V3", pcbnew.F_Cu)
    add_plane(board, "/GND", pcbnew.B_Cu)
    pcbnew.ZONE_FILLER(board).Fill(board.Zones())

    print("saving board", flush=True)
    pcbnew.SaveBoard(str(BOARD_PATH), board)
    print(f"Saved {BOARD_PATH}")


if __name__ == "__main__":
    main()
