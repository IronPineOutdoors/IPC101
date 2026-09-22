"""Rear tunnel R1: stationary bracket and collar for nominal 12.7 mm plywood."""
from functools import lru_cache
import json
import numpy as np
import trimesh
import generate_top_stop_r1 as roof
from generate_crosswind_control_box import write_binary_stl
g=roof.g
OUT=g.ROOT/'mounting'/'rear-tunnel-r1'
CX,CZ=78,50
WALL=12.7
BORE,OD=50,56
WALL_HOLE=58
SCREWS=[(CX+dx,CZ+dz) for dx in (-25,25) for dz in (-25,25)]

def along_y(d,length,x,y,z,segments=96):
    return g.m.Manifold.cylinder(length,d/2,circular_segments=segments).rotate((-90,0,0)).translate((x,y,z))

def pin_relief():
    # Existing 3.4 mm pin bore is tangent to the rail edge; 0.1 mm radial relief
    # opens the notch cleanly and avoids a non-manifold STL seam.
    return g.m.Manifold.cylinder(30,1.8,circular_segments=48).rotate((0,90,0)).translate((10,-7,40))

def annulus(od,id,y,length):
    return along_y(od,length,CX,y,CZ)-along_y(id,length+2,CX,y-1,CZ)

@lru_cache(None)
def bracket():
    p=g.h.build_bracket()+annulus(OD,BORE,-39,28.5)
    p-=along_y(BORE,32,CX,-40,CZ)
    # Slight entry relief, keeping a minimum 50 mm bore through the entire sleeve.
    p-=along_y(52,1,CX,-39,CZ)
    p-=along_y(52,1,CX,-11.5,CZ)
    for x,z in SCREWS:
        p+=along_y(9,3.2,x,-12,z)
        p-=along_y(3.4,9,x,-16,z)
        # M3 hex nut, 5.8 mm across flats, loaded from the box-facing side.
        p-=along_y(5.8/np.cos(np.pi/6),2.8,x,-11.4,z,6)
    return p-pin_relief()

@lru_cache(None)
def collar():
    # Rear flange bears on the inside plywood face at Y=-27.7.
    p=annulus(78,56.6,-31.7,4)+annulus(62,56.6,-38,10.3)
    for x,z in SCREWS:p-=along_y(3.4,6,x,-32.7,z)
    return p

def fit_ring():
    return g.cyl(56,6,(0,0,0))-g.cyl(50,8,(0,0,-1))

def wall_template():
    # A shallow stencil: center hole establishes the bore, four holes locate screws.
    p=g.cyl(78,2,(0,0,0))-g.cyl(WALL_HOLE,4,(0,0,-1))
    for x,z in SCREWS:p-=g.cyl(3.4,4,(x-CX,z-CZ,-1))
    return p

def shell():
    # Close the old floor port and its blind plate-fastener holes in one flat floor.
    p=roof.base()+g.cube((66,36,3),(45,3,0))
    for x in (50,106):
        for y in (9,33):p+=g.cyl(4.22,6.2,(x,y,0))
    # Rear passage only; the stationary tunnel does not project into the box.
    return p-along_y(52,6,CX,-1,CZ)

def print_part(name,p):
    if name in ('Bracket','Collar'):p=p.rotate((-90,0,0))
    lo=p.bounding_box()[:3]
    return p.translate(tuple(-v for v in lo))

def verify():
    checks={}
    def clear(name,a,b):
        v=max(0,(a^b).volume());assert v<.001,(name,v);checks[name]=round(v,7)
    b=bracket();c=collar();s=shell()
    clear('bracket/collar',b,c)
    wood=g.cube((180,WALL,110),(-12,-27.7,-5))-along_y(WALL_HOLE,15,CX,-29,CZ)
    for x,z in SCREWS:wood-=along_y(4,15,x,-29,z)
    clear('bracket/plywood',b,wood);clear('collar/plywood',c,wood)
    for d in range(71):clear('box rail lift '+str(d),(s+roof.roof()).translate((0,0,d)),b+c)
    cassette=g.cradle_local()+g.bezel_local()+g.r3_local()+g.pcb_local()+g.plate_local()
    for d in range(66):clear('cassette withdrawal '+str(d),g.face(cassette.translate((0,0,-d))),s)
    for d in range(51):clear('roof withdrawal '+str(d),roof.roof().translate((0,0,d)),s)
    # Measured connector bounding prism, centered and drawn axially through the bore.
    connector=g.cube((41,73,22.16),(CX-20.5,-70,CZ-11.08))
    clear('connector straight passage',connector,b+c+wood)
    for x,z in SCREWS:
        screw=along_y(3,25,x,-31.7,z)+along_y(5.5,3,x,-34.7,z)
        clear('screw/bracket '+str((x,z)),screw,b)
        clear('screw/collar '+str((x,z)),screw,c)
        clear('screw/box '+str((x,z)),screw,s)
    # Verify the rail tongues are unchanged inside their original envelopes.
    for x in (30,126):
        witness=g.cube((16,12,56),(x-8,-12,29))
        a=b^witness;original=(g.h.build_bracket()-pin_relief())^witness
        assert (a-original).volume()+(original-a).volume()<.001,'rail geometry changed'
    return {'revision':'REAR-TUNNEL-R1','status':'Fit prototype; flexible harness routing and sealing unverified','wall_mm':WALL,'pin_bore_radial_relief_mm':.1,'clear_bore_mm':BORE,'sleeve_od_mm':OD,'provisional_wall_hole_mm':WALL_HOLE,'connector_measured_mm':[41,22.16,73],'connector_length_basis':'connected pair; rectangular envelope assumes width/height include latch','connector_diagonal_mm':round(float(np.hypot(41,22.16)),3),'collar_radial_clearance_mm':.3,'rear_fastener_centers_xz_mm':SCREWS,'fasteners':'4 x M3x25 socket screws and M3 hex nuts; verify actual stack','checks_passed':len(checks),'clearance_checks_mm3':checks,'limitations':['Print bore ring and verify connector including latch first','No flexible cable sweep or minimum bend radius is modeled','Confirm actual bundle slides through the rear gap throughout the 70 mm lift without pinching','Service-loop length must be established on physical assembly; anchor deeper inside base','Wall flange, rear port and fasteners are not weather sealed','No final harness wire/contact compatibility or pin assignment released']}

def run():
    OUT.mkdir(parents=True,exist_ok=True)
    report=verify();exports={}
    for name,p in {'Bracket':bracket(),'Collar':collar(),'Base':shell(),'Bore_Ring':fit_ring(),'Wall_Template':wall_template()}.items():
        assert p.status()==g.m.Error.NoError and len(p.decompose())==1,(name,len(p.decompose()))
        orientations=[('PRINT',print_part(name,p))]
        if name in ('Bracket','Collar','Base'):orientations.insert(0,('INSTALLED',p))
        for orientation,solid in orientations:
            path=OUT/f'CrossWind_IPC101_Rear_Tunnel_{name}_R1_{orientation}.stl'
            write_binary_stl(path,solid)
            mesh=trimesh.load_mesh(path)
            assert mesh.is_watertight and mesh.is_winding_consistent and len(mesh.split())==1,path.name
            assert np.all(mesh.extents<256),path.name
            if orientation=='PRINT':assert abs(mesh.bounds[0,2])<1e-4,path.name
            exports[path.name]=np.round(mesh.extents,3).tolist()
    report['export_extents_mm']=exports
    (OUT/'REAR_TUNNEL_R1_verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='clearance_checks_mm3'},indent=2))
if __name__=='__main__':run()
