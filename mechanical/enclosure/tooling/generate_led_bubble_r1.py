"""LED bubble R1 optical/fit samples, not a final retained LED assembly."""
from enclosure_paths import asset
import json
import trimesh
import generate_rev_i1 as g
from generate_crosswind_control_box import write_binary_stl
OUTER=7.8
PLATE=2.05
BORES=(5.3,5.5,5.7)
HOLES=(8.0,8.2,8.4)
g.previous.FONT.update({'2':('01110','10001','00001','00010','00100','01000','11111'), '3':('11110','00001','00001','01110','00001','00001','11110')})
def sphere(r,z):
    return g.m.Manifold.sphere(r,64).translate((0,0,z))
def bubble(bore,index):
    # Rear flange on bed, dome upward. Panel back at z1, front at z3.05.
    neck=1+PLATE
    outer=g.cyl(OUTER,neck,(0,0,0))+sphere(OUTER/2,neck)
    outer=outer-g.cube((40,40,10),(-20,-20,-10))
    outer+=g.cyl(10,1,(0,0,0))+g.cube((11,6,1),(3,-3,0))
    cavity=g.cyl(bore,neck+.2,(0,0,-.2))+sphere(bore/2,neck)
    return outer-cavity-g.mark(str(index),7,-1.5,.6)
def coupon():
    part=g.cube((72,25,PLATE),(0,0,0))
    for index,d in enumerate(HOLES,1):
        x=12+24*(index-1)
        part-=g.cyl(d,PLATE+.2,(x,15,-.1))
        part-=g.mark(str(index),x-1,3,PLATE-.4)
    return part
if __name__=='__main__':
    records=[]
    samples={f'Bubble_{i}_Bore{d:.1f}':bubble(d,i) for i,d in enumerate(BORES,1)}
    samples['Hole_Strip']=coupon()
    for name,solid in samples.items():
        assert solid.status()==g.m.Error.NoError and len(solid.decompose())==1
        path=asset(g.ROOT, f'CrossWind_IPC101_LED_R1_{name}_PRINT.stl')
        write_binary_stl(path,solid)
        mesh=trimesh.load_mesh(path)
        assert mesh.is_watertight and mesh.is_winding_consistent and len(mesh.split())==1
        assert abs(mesh.bounds[0,2])<.001
        records.append({'file':path.name,'size_mm':mesh.extents.tolist(),'watertight':True})
    # Fit is checked at the panel slab only: the flange deliberately retains from behind.
    for d in BORES:
        lens=bubble(d,1)
        for h in HOLES:
            panel=g.cube((30,30,PLATE),(-15,-15,1))-g.cyl(h,PLATE+.2,(0,0,.9))
            assert (lens^panel).volume()<.001
    report={'status':'Test samples only; optical quality, actual fit and final retention pending',
        'recorded_LED_body_mm':[5.10,8.88],'bubble_outer_diameter_mm':OUTER,
        'sample_bores_mm':BORES,'strip_holes_mm':HOLES,'plate_thickness_mm':PLATE,
        'bubble_wall_mm':[(OUTER-d)/2 for d in BORES], 'panel_fit_checks':9,'files':records}
    (asset(g.ROOT, 'LED_R1_verification.json')).write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
