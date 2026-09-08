"""Bench-only TPU button diaphragms and rigid clamp frames; millimetres.

Flat skin prints on the bed. Central reinforcement faces upward in print;
install it toward the actuator. No final actuator length or waterproof claim.
"""
from pathlib import Path
import sys
import math
import manifold3d as m
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from generate_ipc101_rev_c import rounded_box, write_binary_stl

HOLES = ((4,4),(40,4),(4,34),(40,34))

def rounded(w,h,r,z):
    return rounded_box(w,h,r,z).translate(((44-w)/2,(38-h)/2,0))

def holes(solid):
    for x,y in HOLES:
        solid -= m.Manifold.cylinder(12,1.7,circular_segments=48).translate((x,y,-2))
    return solid

def opening(kind,depth):
    if kind=='ARM_PULL':
        return rounded(26,20,3,depth)
    return m.Manifold.cylinder(depth,13,circular_segments=96).translate((22,19,0))

def membrane(kind, thickness):
    # 1.2 mm thick peripheral clamping flange, thin central continuous web.
    flange=rounded(44,38,3,1.2)-opening(kind,3).translate((0,0,-1))
    web=rounded(44,38,3,thickness)
    if kind=='ARM_PULL':
        centre=rounded(15.2,10,1.8,1).translate((0,0,thickness))
    else:
        centre=(rounded(18,7.2,1.8,1)+rounded(7.2,18,1.8,1)).translate((0,0,thickness))
    return holes(flange+web+centre)

def frame(kind):
    return holes(rounded(44,38,3,3)-opening(kind,5).translate((0,0,-1)))

if __name__=='__main__':
    root=Path(__file__).resolve().parent
    for kind in ('ARM_PULL','P504'):
        parts={f'{kind}_CLAMP_FRAME_RIGID.stl':frame(kind)}
        for thickness in (.4,.6,.8):
            parts[f'{kind}_TPU_WEB_{thickness:.1f}mm.stl']=membrane(kind,thickness)
        for filename,solid in parts.items():
            assert solid.status()==m.Error.NoError and len(solid.decompose())==1
            assert solid.volume()>0
            for x,y in HOLES:
                probe=m.Manifold.cylinder(10,1.6,circular_segments=48).translate((x,y,-1))
                assert (probe ^ solid).volume()<1e-6
            write_binary_stl(root/filename,solid,filename.encode())
            print(filename,solid.num_tri(),'triangles; valid connected solid, clear bolt bores')
