"""Removable top STOP housing R1; engineering fit prototype, dimensions mm."""
from functools import lru_cache
import json
import numpy as np
import trimesh
import study_top_stop as study
from generate_crosswind_control_box import write_binary_stl
g=study.g
OUT=g.ROOT/'controls'/'stop'/'top-mounted'
TOP=study.TOP
HOLES=[(x,y) for x in (-3,159) for y in (5,17)]
SEAT=117

@lru_cache(None)
def base():
    p=study.base()
    for x,y in HOLES:
        p+=g.cyl(10,18,(x,y,99))
        p+=g.cyl(7,2,(x,y,SEAT))
        p-=g.cyl(2.7,12,(x,y,107))
    return p

@lru_cache(None)
def roof():
    p=study.roof()
    # Relieve the inherited shell contact in all axes for printed-part clearance.
    original=g.build_box()
    for axis in range(3):
        for amount in (-.3,.3):
            delta=[0,0,0];delta[axis]=amount
            p-=original.translate(tuple(delta))
    # Underside tie tab anchored in the rear wall, clear of the switch envelope.
    tab=g.cube((18,16,3),(99,-10,112))
    for x in (102,111):tab-=g.cube((3,7,5),(x,-5,111))
    p+=tab
    for x,y in HOLES:
        p+=g.cyl(10,TOP-SEAT,(x,y,SEAT))
        p-=g.cyl(10.6,19,(x,y,98))
        p-=g.cyl(7.6,2.4,(x,y,SEAT))
        p-=g.cyl(3.4,25,(x,y,SEAT))
        p-=g.cyl(6.4,4,(x,y,138))
    return p

def screw(x,y):
    return g.cyl(3,30,(x,y,108))+g.cyl(5.5,3,(x,y,138))

def coupons():
    lower=g.cyl(10,18,(0,0,99))+g.cyl(7,2,(0,0,117))
    lower+=g.cube((20,20,2),(-10,-10,99))
    lower-=g.cyl(2.7,12,(0,0,107))
    upper=g.cyl(10,24,(0,0,117))
    upper-=g.cyl(7.6,2.4,(0,0,117))+g.cyl(3.4,25,(0,0,117))+g.cyl(6.4,4,(0,0,138))
    return {'Pilot_Coupon':lower,'Roof_Coupon':upper}

def print_part(name,p):
    if name in ('Roof','Roof_Coupon'):p=p.rotate((180,0,0))
    lo=p.bounding_box()[:3]
    return p.translate(tuple(-v for v in lo))

def verify():
    parts={'Base':base(),'Roof':roof()}
    fixed={'PCB':g.face(g.pcb_local()),'R3':g.face(g.r3_local()),'Cradle':g.face(g.cradle_local()),'Bezel':g.face(g.bezel_local()),'Faceplate':g.face(g.plate_local())}
    checks={}
    def clear(name,a,b):
        volume=max(0,(a^b).volume())
        assert volume<.001,(name,volume)
        checks[name]=round(volume,7)
    for n,p in parts.items():
        assert p.status()==g.m.Error.NoError and len(p.decompose())==1,(n,len(p.decompose()))
        for k,s in fixed.items():clear(n+'/'+k,p,s)
        clear(n+'/switch',p,study.body(TOP)+study.neck(TOP))
        clear(n+'/mounting nut access',p,g.cyl(36,4,(study.X,study.Y,134.5)))
        clear(n+'/wire reserve',p,g.cube((20,20,10),(68,5,TOP-43)))
    clear('base/roof',base(),roof())
    for x,y in HOLES:
        clear('screw/roof '+str((x,y)),screw(x,y),roof())
        # The screw engages the base pilot intentionally; verify exposed hardware only.
        for k,s in fixed.items():clear('screw/'+k+str((x,y)),screw(x,y),s)
        clear('driver access '+str((x,y)),g.cyl(7,35,(x,y,141)),roof()+study.button(TOP)+study.collar(TOP))
    rear=g.cube((250,10,150),(-40,-10,0))
    a=base()^rear;b=g.build_box()^rear
    assert (a-b).volume()+(b-a).volume()<.001,'rear interface changed'
    shell=base()+roof();bracket=g.h.build_bracket()
    cassette=g.cradle_local()+g.bezel_local()+g.r3_local()+g.pcb_local()+g.plate_local()
    for d in range(71):clear('bracket slide '+str(d),shell.translate((0,0,d)),bracket)
    for d in range(66):
        moving=g.face(cassette.translate((0,0,-d)))
        clear('cassette withdrawal '+str(d),moving,base())
    for d in range(51):
        moving=(roof()+study.body(TOP)+study.neck(TOP)).translate((0,0,d))
        for k,s in {'Base':base(),**fixed}.items():clear('roof lift '+str(d)+'/'+k,moving,s)
    return {'revision':'TOP-STOP-R1','status':'Engineering fit prototype; physical fit and sealing unqualified','fastener_centers_xy_mm':HOLES,'fasteners':'4 x M3x30 socket screws, 2.7 mm printed blind pilots; trial fit required','seat_z_mm':SEAT,'locator_diametral_clearance_mm':.6,'switch_mount_surface_z_mm':TOP,'rear_mount_unchanged':True,'checks_passed':len(checks),'clearance_checks_mm3':checks,'limitations':['Actual populated PCB and soldered harness not modeled','Roof seam and screw wells are not weather sealed','Pilot retention and print tolerances require coupon trial','Switch body represented by conservative envelope']}

def run():
    report=verify()
    for name,p in {'Base':base(),'Roof':roof(),**coupons()}.items():
        for orientation,solid in [('INSTALLED',p),('PRINT',print_part(name,p))]:
            path=OUT/f'CrossWind_IPC101_Top_STOP_{name}_R1_{orientation}.stl'
            write_binary_stl(path,solid)
            mesh=trimesh.load_mesh(path)
            assert mesh.is_watertight and mesh.is_winding_consistent and len(mesh.split())==1,path.name
            assert np.all(mesh.extents<256),path.name
    (OUT/'TOP_STOP_R1_verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
if __name__=='__main__':run()
