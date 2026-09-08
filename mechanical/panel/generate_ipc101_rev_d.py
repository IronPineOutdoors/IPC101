"""Rev D faceplate fit correction: OLED shifted 8 mm right, operator/front view."""
from pathlib import Path
import csv
import manifold3d as m
import generate_ipc101_rev_c as base

OLED_CENTRE = (54.5, 63.5)

if __name__ == '__main__':
    root = Path(__file__).resolve().parent
    plate = base.build_faceplate(oled_centre=OLED_CENTRE)
    assert plate.status() == m.Error.NoError and len(plate.decompose()) == 1
    assert plate.bounding_box() == (0., 0., 0., 150., 100., 2.)
    # Every new display bore/window and every unchanged control bore stays open.
    for dx in (-34.4, 34.4):
        for dy in (-19.4, 19.4):
            hole = base.cylinder(3.1, 3, (OLED_CENTRE[0]+dx, OLED_CENTRE[1]+dy))
            assert (plate ^ hole).volume() < 1e-5
    for centre in base.MOUNT_CENTRES:
        assert (plate ^ base.cylinder(3.1, 3, centre)).volume() < 1e-5
    window = m.Manifold.cube((56.9,27.9,3)).translate((26.05,49.55,-.5))
    assert (plate ^ window).volume() < 1e-5
    # 73 x 43 mm OLED PCB envelope ends at X=91; 18 mm navigation cap starts X=96.
    assert base.NAV_CENTRE[0]-9-(OLED_CENTRE[0]+73/2) == 5.0
    base.write_binary_stl(root/'CrossWind_ControlPanel_RevD_OLED_8mm_Right_IPC101.stl', plate,
                          b'IPC101 Rev D faceplate OLED right 8mm; no STOP cutout')
    # Keep Rev C coordinates as historical PCB data. Rev D file is faceplate-only.
    with (root/'IPC101_P0_PANEL_COORDINATES.csv').open(newline='') as source:
        rows = list(csv.DictReader(source))
    rows = [r for r in rows if r['feature'] != 'PCB_OUTLINE']
    for row in rows:
        if row['feature'] == 'OLED_CENTER' or row['feature'].startswith('OLED_MH_'):
            row['x_mm'] = f"{float(row['x_mm'])+8:.1f}"
            row['status'] = 'REV_D_FACEPLATE_ONLY_SHIFT_RIGHT_8MM'
    with (root/'IPC101_RevD_FACEPLATE_COORDINATES.csv').open('w', newline='') as output:
        writer = csv.DictWriter(output, fieldnames=rows[0].keys()); writer.writeheader(); writer.writerows(rows)
    print('PASS: connected solid, 150x100x2 mm, OLED window and eight mounting bores verified.')
    print('OLED centre 54.5,63.5; mounting X=20.1/88.9, Y=44.1/82.9 mm.')
    print('Nominal lateral gap: OLED PCB envelope to navigation cap envelope = 5 mm.')
