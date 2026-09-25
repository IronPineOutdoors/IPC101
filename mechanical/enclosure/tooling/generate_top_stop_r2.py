"""R2 roof: measured contact-block insertion and full central rotation clearance."""
from functools import lru_cache
import json
import numpy as np
import trimesh
import generate_top_stop_r1 as r1
import generate_rear_tunnel_r1 as rear
from generate_crosswind_control_box import write_binary_stl
g=r1.g
OUT=r1.OUT
X,Y=r1.study.X,r1.study.Y
WIDTH=27.3
BORE=41
LAND=138.5

@lru_cache(None)
def roof():
    # Reinforce the enlarged central pocket with a 3 mm cylindrical wall.
    p=r1.roof()+g.cyl(47,LAND-109,(X,Y,109))
    # Continuous access from outside the underside to the 2.5 mm top land.
    p-=g.cyl(BORE,LAND-65,(X,Y,65))
    # Preserve the existing lower mating relief around both compatible bases.
    original=g.build_box()
    p-=original
    for axis in range(3):
        for amount in (-.3,.3):
            delta=[0,0,0];delta[axis]=amount
            p-=original.translate(tuple(delta))
    return p

def block(angle=0,drop=0):
    # Depth retained from previous conservative package, not a user measurement.
    return g.cube((WIDTH,WIDTH,30.5),(-WIDTH/2,-WIDTH/2,0)).rotate((0,0,angle)).translate((X,Y,108-drop))

def coupon():
    # Central roof section preserves the complete pocket and keyed mounting land.
    return roof()^g.cube((51,60,45),(X-25.5,Y-30,100))

def verify():
    p=roof();checks={}
    def clear(name,a,b):
        v=max(0,(a^b).volume());assert v<.001,(name,v);checks[name]=round(v,7)
    # Continuous swept volume proves entry at every angle/depth for the stated envelope.
    clear('continuous 41 mm entry and rotation volume',p,g.cyl(BORE,LAND-65,(X,Y,65)))
    for angle in range(0,360,5):
        for drop in (0,5,15,30,45):clear(f'block angle {angle} drop {drop}',p,block(angle,drop))
    old_block=max((r1.roof()^block(0,d)).volume() for d in range(46))
    assert old_block>.001,'Regression must reproduce the R1 insertion obstruction'
    top=g.cube((200,100,3),(-20,-30,LAND))
    a=p^top;b=r1.roof()^top
    assert (a-b).volume()+(b-a).volume()<.001,'top mounting land changed'
    for x,y in r1.HOLES:
        region=g.cube((12,12,45),(x-6,y-6,100))
        a=p^region;b=r1.roof()^region
        assert (a-b).volume()+(b-a).volume()<.001,'attachment changed'
    fixed={'PCB':g.face(g.pcb_local()),'R3':g.face(g.r3_local()),'Cradle':g.face(g.cradle_local()),'Bezel':g.face(g.bezel_local()),'Faceplate':g.face(g.plate_local())}
    for name,s in fixed.items():clear(name,p,s)
    for name,base in [('original R1',r1.base()),('rear entry R1',rear.shell())]:
        for d in range(51):clear(name+' roof lift '+str(d),(p+block()).translate((0,0,d)),base)
    for d in range(71):clear('bracket lift '+str(d),(rear.shell()+p).translate((0,0,d)),rear.bracket()+rear.collar())
    assert len(p.decompose())==1 and p.status()==g.m.Error.NoError
    return {'revision':'TOP-STOP-R2','status':'CAD verified; physical insertion/twist test pending','measured_block_width_mm':WIDTH,'rotation_diagonal_mm':float(np.hypot(WIDTH,WIDTH)),'clear_pocket_diameter_mm':BORE,'conservative_block_depth_mm':30.5,'top_land_and_keyed_hole_unchanged':True,'roof_attachments_unchanged':True,'r1_insertion_intersection_mm3':old_block,'checks_passed':len(checks),'assembly':'Install contact block from underside with roof removed from base, then install roof','limitations':['Block depth remains a conservative inherited envelope; actual depth not measured','Wires, fingers and tools are not modeled','Sealing and support removal require physical checks'],'clearance_checks_mm3':checks}

def run():
    report=verify()
    for name,p in [('Roof',roof()),('Access_Coupon',coupon())]:
        assert len(p.decompose())==1,(name,len(p.decompose()))
        for orientation,s in [('INSTALLED',p),('PRINT',r1.print_part('Roof',p))]:
            path=OUT/f'CrossWind_IPC101_Top_STOP_{name}_R2_{orientation}.stl'
            write_binary_stl(path,s)
            mesh=trimesh.load_mesh(path)
            assert mesh.is_watertight and mesh.is_winding_consistent and len(mesh.split())==1,path.name
            assert np.all(mesh.extents<256)
    (OUT/'TOP_STOP_R2_verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='clearance_checks_mm3'},indent=2))
if __name__=='__main__':run()
