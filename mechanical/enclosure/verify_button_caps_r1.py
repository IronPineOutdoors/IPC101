"""R1 cap geometry, measured release clearance and current N1.2 interface checks."""
from functools import lru_cache
import json
import numpy as np
import trimesh
import generate_rev_i1 as g
import faceplate_rev_n1_reference as fp
from verify_rev_i1 import hardware

GUIDE_DEPTH=3.55
BUTTON_BACK=10.77
REST_GAP=.20

@lru_cache(maxsize=None)
def load(name):
    mesh=trimesh.load_mesh(g.ROOT/name)
    assert mesh.is_watertight and mesh.is_winding_consistent,name
    solid=g.m.Manifold(g.m.Mesh(np.asarray(mesh.vertices,dtype=np.float32),np.asarray(mesh.faces,dtype=np.uint32)))
    assert solid.status()==g.m.Error.NoError,name
    return solid

def cap(label,material=None):
    if material:return load(f'CrossWind_IPC101_{label}_Cap_R1_{material}.stl')
    return cap(label,'WHITE_PETGHF')+cap(label,'BLACK_AMS')

def installed(label,material=None,travel=0):
    x,y=fp.CENTRES[label]
    return cap(label,material).translate((x,y,-GUIDE_DEPTH+travel))

def n11(material=None):
    # Retained helper name for existing preview imports; now loads current N1.2.
    if material:return load(f'CrossWind_IPC101_Faceplate_RevN12_{material}.stl').translate((0,0,-2))
    return n11('WHITE_PETGHF')+n11('BLACK_AMS')

def run():
    checks={};exports={}
    fixed=[('N12',n11()),('N1',fp.plate_local()),('Bezel',g.bezel_local()),('Cradle',g.cradle_local()),('R3',g.r3_local()),('PCB',g.pcb_local())]
    shell=g.build_box()
    def clear(name,a,b):
        v=(a^b).volume();checks[name]=round(v,7);assert v<.001,(name,v)
    for label in ('ARM','PULL'):
        w=cap(label,'WHITE_PETGHF');b=cap(label,'BLACK_AMS')
        assert len(w.decompose())==1,label
        clear(label+' body/inlay',w,b)
        assert np.allclose(cap(label).bounding_box(),[-9,-6.4,0,9,6.4,14.12],atol=.0001)
        assert np.all(np.array(b.bounding_box()[:2])>[-7.6,-5]) and np.all(np.array(b.bounding_box()[3:5])<[7.6,5])
        tip=installed(label).bounding_box()[5]
        assert abs(BUTTON_BACK-tip-REST_GAP)<.0001
        x,y=fp.CENTRES[label]
        actuator=g.cyl(6,g.FACEPLATE_TO_PCB_TOP-BUTTON_BACK,(x,y,BUTTON_BACK))
        clear(label+' released switch face',installed(label),actuator)
        assert (installed(label,travel=-.1)^n11()).volume()>.1,'Flange must catch rear faceplate'
        for travel in np.linspace(0,1,21):
            p=installed(label,travel=float(travel))
            for name,s in fixed:
                clear(f'{label} travel{travel:.2f} / {name}',p,s)
            clear(f'{label} travel{travel:.2f} / shell',g.face(p),shell)
        for i,bolts in enumerate(hardware()):
            for j,bolt in enumerate(bolts):clear(f'{label} / hardware{i}-{j}',installed(label),bolt)
        for material in ('WHITE_PETGHF','BLACK_AMS'):
            name=f'CrossWind_IPC101_{label}_Cap_R1_{material}.stl'
            mesh=trimesh.load_mesh(g.ROOT/name)
            exports[name]={'bounds_mm':mesh.bounds.tolist(),'components':len(mesh.split()),'watertight':True}
    clear('ARM / PULL',installed('ARM'),installed('PULL'))
    # Variant removes redundant artwork only; preserve all N1 apertures/interfaces.
    mark_zone=g.cube((70,8,4),(40,9,-2))
    a=n11()-mark_zone;b=fp.plate_local()-mark_zone
    assert (a-b).volume()+(b-a).volume()<.01,'N1.2 structural geometry changed'
    clear('N12 body/inlay',n11('WHITE_PETGHF'),n11('BLACK_AMS'))
    assert len(n11('WHITE_PETGHF').decompose())==1
    for material in ('WHITE_PETGHF','BLACK_AMS'):
        name=f'CrossWind_IPC101_Faceplate_RevN12_{material}.stl'
        mesh=trimesh.load_mesh(g.ROOT/name)
        exports[name]={'bounds_mm':mesh.bounds.tolist(),'components':len(mesh.split()),'watertight':True}
    report={'status':'CAD verified; physical fit, free return and switch travel pending',
            'user_front_face_to_button_mm':12.82,'user_plate_thickness_mm':2.05,
            'button_from_plate_back_mm':BUTTON_BACK,'rest_clearance_mm':REST_GAP,
            'stem_from_flange_rear_mm':9.57,'overall_cap_height_mm':14.12,
            'guide_size_mm':[15.2,10.0],'flange_size_mm':[18,12.8,1],
            'geometric_motion_checked_mm':1.0,'checks':checks,'exports':exports,
            'limitations':['Shared measurement applied to both buttons; verify each','21 geometric positions do not establish switch rated travel or force','Floating flange-retained plunger; not a press-fit socket or spring','No positive overtravel stop or environmental seal added','PCB remains nominal16.5; cap reach uses measured10.77 from plate back']}
    (g.ROOT/'R1_button_caps_verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PASS',len(checks),'checks; labeled caps and N1.2 compatible')

if __name__=='__main__':run()
