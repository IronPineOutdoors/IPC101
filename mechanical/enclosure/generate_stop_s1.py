"""XA1E side pod S1: additive accessory to the unchanged I1 cassette, mm.
Run from any cwd. Python/manifold3d is the editable manufacturing source.
"""
import json
import numpy as np
import trimesh
import generate_rev_i1 as g
from generate_rev_i1 import cube, cyl, face, m, ROOT
from generate_crosswind_control_box import write_binary_stl

CX,CY=-42,50
COVER_HOLES=[(x,y) for x in (-65,-19) for y in (24,76)]

def cutout(z=-6,depth=8):
    # Midpoints of IDEC tolerances: diameter16.3, key1.8, overall18.0.
    return cyl(16.3,depth,(CX,CY,z))+cube((1.8,3,depth),(CX-.9,CY+6.85,z))

def pod():
    p=cube((68,80,5),(-69,10,-5))
    p+=g.ring(-69,20,54,60,3,43,0)
    p-=cyl(36,3,(CX,CY,-2.5)) # 2.5 mm mounting land, nut access
    p-=cutout()
    for y in (20,80):p-=cyl(3.4,7,(-5,y,-6))
    for x,y in COVER_HOLES:
        p+=cyl(8,9,(x,y,34))
        p-=cyl(2.7,9,(x,y,35)) # pilot for M3x10; physical thread fit pending
    p-=cube((7,5,7),(CX-3.5,19,37)) # split cable exit, rear cover closes it
    # Two tie holes in lower wall, away from contact body, for strain relief.
    for x in (CX-7,CX+7):
        p-=cyl(3,5,(0,0,0)).rotate((90,0,0)).translate((x,24,35))
    return p-g.mark('STOP-S1',-54,13,-.4)

def cover():
    p=cube((54,60,3),(-69,20,43))
    for x,y in COVER_HOLES:p-=cyl(3.4,5,(x,y,42))
    return p-g.mark('STOP-S1',-53,32,45.6)

def coupon():
    return cube((40,40,2.5),(CX-20,CY-20,-5))-cutout()-g.mark('STOP-S1',-54,32,-2.9)

def envelope():
    # Conservative installation envelope, not an exact switch CAD model.
    return cube((32,32,25.5),(CX-16,CY-16,5))+cyl(32,7.5,(CX,CY,-2.5))+cyl(16.2,3,(CX,CY,-5.5))+cyl(29,21,(CX,CY,-26))

def verify(parts):
    checks={}
    def clear(name,a,b):
        v=(a^b).volume();checks[name]=round(v,8);assert v<1e-4,(name,v)
    fixed=g.models();fixed.update(PCB=face(g.pcb_local()),R3=face(g.r3_local()),N1=face(g.plate_local()))
    for n in ('Pod','Cover'):
        for k,s in fixed.items():clear(n+' / '+k,face(parts[n]),s)
    clear('pod / cover',parts['Pod'],parts['Cover'])
    for n in ('Pod','Cover'):
        clear('switch envelope / '+n,envelope(),parts[n])
        clear('contact block rotation / '+n,cyl(32*np.sqrt(2),25.5,(CX,CY,5)),parts[n])
    for d in range(71):
        for n in ('Pod','Cover'):clear(f'bracket slide {d} / {n}',face(parts[n]).translate((0,0,d)),g.h.build_bracket())
    for d in range(66):clear(f'pod front withdrawal {d}',face(parts['Pod'].translate((0,0,-d))),fixed['Box'])
    for d in range(41):clear(f'cover withdrawal {d}',cover().translate((0,0,d)),pod())
    # Replacement M3x35 starts at -5, ends at30: same engagement as old x30.
    for y in (20,80):
        bolt=cyl(3,35,(-5,y,-5))+cyl(5.5,3,(-5,y,-8))
        clear(f'bolt {y} / pod',bolt,pod())
        for k,s in fixed.items():clear(f'bolt {y} / '+k,face(bolt),s)
    report={'status':'CAD checks passed; physical fit and mounting stiffness pending','switch_envelope_mm':[32,32,33],'panel_thickness_mm':2.5,'cutout_diameter_mm':16.3,'checks':checks,'exports':{}}
    for n,p in parts.items():
        assert p.status()==m.Error.NoError and len(p.decompose())==1,n
        for orientation,s in [('INSTALLED',face(p)),('PRINT',g.h.print_orientation(p))]:
            path=ROOT/f'CrossWind_IPC101_STOP_{n}_S1_{orientation}.stl'
            write_binary_stl(path,s)
            mesh=trimesh.load_mesh(path)
            assert mesh.is_watertight and mesh.is_winding_consistent and len(mesh.split())==1,path
            report['exports'][path.name]={'size_mm':mesh.extents.tolist(),'watertight':True}
    (ROOT/'STOP_S1_verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PASS:',len(checks),'clearance checks; six watertight exports')

if __name__=='__main__':verify({'Pod':pod(),'Cover':cover(),'Coupon':coupon()})
