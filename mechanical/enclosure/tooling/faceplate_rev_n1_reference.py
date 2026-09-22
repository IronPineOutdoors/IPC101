"""N1 uses user-confirmed operator-view positions, not an assumed PCB flip."""
from enclosure_paths import asset
from functools import lru_cache
from pathlib import Path
import numpy as np
import trimesh
import manifold3d as m

ROOT=Path(__file__).resolve().parent.parent
THICKNESS=2.0
MOUNTS=((5,5),(145,5),(5,95),(145,95))
OPERATOR_CENTRES={'ARM':(46.88,20.75),'PULL':(115.67,20.75),
                  'LED':(68.5,31),'NAV':(45,63.5),'OLED':(103.5,63.5)}
CENTRES={name:(150-x,y) for name,(x,y) in OPERATOR_CENTRES.items()}

@lru_cache(maxsize=2)
def material_local(material):
    if material not in ('WHITE_PETGHF','BLACK_AMS'):raise ValueError(material)
    mesh=trimesh.load_mesh(asset(ROOT, f'CrossWind_IPC101_Faceplate_RevN1_{material}.stl'))
    assert mesh.is_watertight and mesh.is_winding_consistent,material
    solid=m.Manifold(m.Mesh(np.asarray(mesh.vertices,dtype=np.float32),np.asarray(mesh.faces,dtype=np.uint32)))
    assert solid.status()==m.Error.NoError,material
    return solid.translate((0,0,-THICKNESS))

def plate_local():return material_local('WHITE_PETGHF')+material_local('BLACK_AMS')

def control_registration():
    result={}
    for name,xy in OPERATOR_CENTRES.items():
        result[name]={'operator_view_xy':list(xy),'faceplate_export_xy':list(CENTRES[name]),
            'basis':'User physical X measurements and confirmed ARM-left/PULL-right; Y retained from M4' if name in ('ARM','PULL') else 'Retained M4 wired faceplate location',
            'physical_validation':'Replacement print pending'}
    return result
