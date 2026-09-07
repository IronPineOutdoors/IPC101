"""Fail fabrication export if solderable pads or archived mask flashes are missing.

Run with KiCad's bundled Python. Checks the actual PCB and optionally Gerbers/ZIP.
"""
import argparse
from collections import Counter
from pathlib import Path
import re
import zipfile
import pcbnew

ROOT = Path(__file__).resolve().parents[3]


def validate(board_path, read=None):
    board = pcbnew.LoadBoard(str(board_path))
    expected = {'F': set(), 'B': set()}
    counts = Counter()
    for footprint in board.GetFootprints():
        for pad in footprint.Pads():
            attribute = pad.GetAttribute()
            if attribute == pcbnew.PAD_ATTRIB_PTH:
                sides = ('F', 'B')
                counts['PTH'] += 1
            elif attribute == pcbnew.PAD_ATTRIB_SMD:
                sides = ('F',) if pad.IsOnLayer(pcbnew.F_Cu) else ('B',)
                counts['SMD'] += 1
            else:
                continue
            for side in sides:
                layer = pcbnew.F_Mask if side == 'F' else pcbnew.B_Mask
                if not pad.IsOnLayer(layer):
                    raise ValueError(f'{footprint.GetReference()} pad {pad.GetNumber()}: missing {side}.Mask')
                pos = pad.GetPosition()
                expected[side].add((pos.x, -pos.y))
    if not counts['PTH'] or not counts['SMD']:
        raise ValueError('Expected both PTH and SMD assembly pads')
    if read is not None:
        for side, extension, function in [('F', 'gts', 'Top'), ('B', 'gbs', 'Bot')]:
            name = f'IPC101-{side}_Mask.{extension}'
            content = read(name).decode('utf-8')
            if f'%TF.FileFunction,Soldermask,{function}*%' not in content:
                raise ValueError(f'{name}: missing mask layer identification')
            if '%FSLAX46Y46*%' not in content or '%MOMM*%' not in content:
                raise ValueError(f'{name}: unexpected coordinate format')
            flashes = {(int(x), int(y)) for x, y in re.findall(r'X(-?\d+)Y(-?\d+)D03\*', content)}
            missing = expected[side] - flashes
            if missing:
                raise ValueError(f'{name}: missing {len(missing)} solderable pad openings: {sorted(missing)}')
            if not content.rstrip().endswith('M02*'):
                raise ValueError(f'{name}: incomplete Gerber')
            print(f'{name}: {len(flashes)} flashed openings; all {len(expected[side])} solderable pad centres present')
    print(f'PASS: {counts["PTH"]} PTH pads open on both sides; {counts["SMD"]} SMD pads open on assembly side')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--board', type=Path, default=ROOT/'hardware/kicad/IPC101.kicad_pcb')
    parser.add_argument('--gerbers', type=Path)
    parser.add_argument('--zip', type=Path)
    args = parser.parse_args()
    validate(args.board, (lambda name: (args.gerbers/name).read_bytes()) if args.gerbers else None)
    if args.zip:
        with zipfile.ZipFile(args.zip) as archive:
            if archive.testzip() is not None:
                raise ValueError('Corrupt ZIP member')
            required = {f'IPC101-{suffix}' for suffix in ('F_Cu.gtl','B_Cu.gbl','F_Mask.gts','B_Mask.gbs','Edge_Cuts.gm1','PTH.drl','NPTH.drl')}
            if not required.issubset(archive.namelist()):
                raise ValueError(f'Missing fabrication files: {required-set(archive.namelist())}')
            validate(args.board, archive.read)
            if args.gerbers:
                for name in archive.namelist():
                    if archive.read(name) != (args.gerbers/name).read_bytes():
                        raise ValueError(f'ZIP differs from generated Gerber: {name}')
        print(f'PASS: archived fabrication files verified: {args.zip.name}')
