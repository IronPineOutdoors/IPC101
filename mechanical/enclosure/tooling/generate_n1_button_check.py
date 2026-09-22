"""Measured button-alignment strip, not the finished N1 faceplate.

Operator-facing X runs left to right. Existing face-down material exports use
Xexport=150-Xoperator, preserving M4's print/assembly coordinate convention.
"""
from enclosure_paths import asset
import json
import numpy as np
import trimesh
import generate_rev_i1 as g
from generate_crosswind_control_box import write_binary_stl

LEFT_FROM_LEFT=46.88
RIGHT_FROM_RIGHT=34.33
WIDTH=150.0
Y=20.75 # existing vertical coordinate; not remeasured by user
CENTRES=(LEFT_FROM_LEFT,WIDTH-RIGHT_FROM_RIGHT)

def opening(x):
    return g.m.Manifold.batch_hull([
        g.cyl(4,4,(x+dx,Y+dy,-1))
        for dx in (-6,6) for dy in (-3.4,3.4)])

def strip():
    p=g.cube((WIDTH,35,2),(0,0,0))
    for x in CENTRES:p-=opening(WIDTH-x)
    for x in (5,145):p-=g.cyl(3.2,4,(x,5,-1))
    return p-g.mark('N1 TEST',60,6,1.6)

if __name__=='__main__':
    p=strip()
    assert p.status()==g.m.Error.NoError and len(p.decompose())==1
    for x in CENTRES:
        assert (p ^ opening(WIDTH-x)).volume()<1e-5
    for name,s in [('Bezel',g.bezel_local()),('Cradle',g.cradle_local()),('PCB',g.pcb_local())]:
        assert (p.translate((0,0,-2)) ^ s).volume()<1e-5,name
    path=asset(g.ROOT, 'CrossWind_IPC101_Button_Check_N1_PRINT.stl')
    write_binary_stl(path,p)
    mesh=trimesh.load_mesh(path)
    assert mesh.is_watertight and mesh.is_winding_consistent and len(mesh.split())==1
    report={'status':'measured XY check only; finished faceplate and function labels pending',
        'operator_centres_mm':[[x,Y] for x in CENTRES],
        'export_centres_mm':[[WIDTH-x,Y] for x in CENTRES],
        'measurement_note':'150 mm PCB width assumed; vertical positions and opening sizes unchanged from M4',
        'size_mm':mesh.extents.tolist(),'watertight':True,'bezel_cradle_bare_pcb_clear':True}
    (asset(g.ROOT, 'N1_button_check.json')).write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
