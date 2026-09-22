"""Read-only assembly references from the supplied Rev M.4 two-material exports.
Raw STL Z=0 is operator face; Z=2 is panel back; rear cradle ends at Z=4.8.
Keep exported XY (SCAD already applies its whole_mirror); only subtract 2 in Z.
PCB registration is a 180-degree rotation about Y: X=150-Xpcb, Y=Ypcb,
Z=PCB_BACK-Zpcb. This puts the component side toward the faceplate and aligns
ARM/PULL. The symmetric bare-board outline itself is unchanged.
"""
from enclosure_paths import asset
from functools import lru_cache
from pathlib import Path
import numpy as np
import trimesh
import manifold3d as m

ROOT=Path(__file__).resolve().parent.parent
THICKNESS=2.0
MOUNTS=((5,5),(145,5),(5,95),(145,95))
# SCAD positions AFTER whole_mirror(), i.e. exported STL coordinates.
CENTRES={'ARM':(116.5,20.75),'PULL':(46.5,20.75),'LED':(81.5,31),
         'NAV':(105,63.5),'OLED':(46.5,63.5)}

@lru_cache(maxsize=2)
def material_local(material):
    if material not in ('WHITE_PETGHF','BLACK_AMS'):raise ValueError(material)
    mesh=trimesh.load_mesh(asset(ROOT, f'CrossWind_IPC101_Faceplate_RevM4_{material}.stl'))
    assert mesh.is_watertight and mesh.is_winding_consistent,material
    solid=m.Manifold(m.Mesh(np.asarray(mesh.vertices,dtype=np.float32),np.asarray(mesh.faces,dtype=np.uint32)))
    assert solid.status()==m.Error.NoError,material
    return solid.translate((0,0,-THICKNESS))

@lru_cache(maxsize=1)
def plate_local():
    return material_local('WHITE_PETGHF')+material_local('BLACK_AMS')


def control_registration():
    """Compare current exported-XY placement against actual repository PCB file.
    Explicitly register PCB component-side-out; do not mirror the faceplate.
    """
    import re
    board=(ROOT.parents[1]/'hardware/kicad/IPC101.kicad_pcb').read_text(encoding='utf-8')
    refs={'SW1':'ARM','SW2':'PULL','SW3':'NAV','DS1':'OLED','D1':'LED'}
    result={}
    for block in board.split('\n\t(footprint ')[1:]:
        ref=re.search(r'\(property "Reference" "(SW1|SW2|SW3|DS1|D1)"',block)
        if not ref:continue
        at=re.search(r'\n\t\t\(at ([^)]+)\)',block)
        x,y=map(float,at.group(1).split()[:2]);name=refs[ref.group(1)]
        actual=CENTRES[name]
        result[name]={'pcb_file_xy':[x,y],'pcb_installed_xy':[150-x,y],
                      'faceplate_export_xy':list(actual),
                      'delta_xy':[round(actual[0]-(150-x),4),round(actual[1]-y,4)],
                      'role':'wired faceplate assembly' if name in ('NAV','OLED') else 'aligned control reference'}
    assert set(result)==set(refs.values()),'Missing PCB references'
    return result
