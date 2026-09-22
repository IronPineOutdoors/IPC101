"""Top STOP packaging study; no production or print-ready geometry released."""
from enclosure_paths import asset
import json
import generate_rev_i1 as g
X,Y=78,10
TOP=141

def base():
    # Cable opening only; retain the existing rear mounting interface.
    return g.build_box()-g.cube((24,24,15),(66,3.1,95))

def rounded_layer(x0,x1,y0,y1,z,h,r):
    return g.m.Manifold.batch_hull([g.cyl(2*r,h,(x,y,z)) for x in (x0+r,x1-r) for y in (y0+r,y1-r)])

def roof():
    # Rounded full-width upper housing; front grows smoothly toward the top.
    outer=g.m.Manifold.batch_hull([rounded_layer(-9,165,-12,30,105,1,8),rounded_layer(-9,165,-12,40,135,6,8)])
    inner=g.m.Manifold.batch_hull([rounded_layer(-6,162,-9,27,107.5,1,5),rounded_layer(-6,162,-9,37,132,6.5,5)])
    p=outer-inner
    p-=g.cube((24,24,10),(66,3.1,100))
    p-=g.build_box()
    p-=g.cyl(16.3,5,(X,Y,137.5))+g.cube((1.8,3,5),(X-.9,Y+6.85,137.5))
    return p

def candidate():return base()+roof()

def body(top):
    # Same conservative 32 mm-wide / 33 mm-deep package used for S1.
    return g.cube((32,32,30.5),(X-16,Y-16,top-33))

def neck(top):return g.cyl(16.2,4,(X,Y,top-3))
def button(top):return g.cyl(29,16,(X,Y,top+5))
def collar(top):return g.cyl(24,5,(X,Y,top))

def run():
    shell=candidate()
    parts={'PCB':g.face(g.pcb_local()),'R3':g.face(g.r3_local()),'Cradle':g.face(g.cradle_local()),'Bezel':g.face(g.bezel_local()),'Faceplate':g.face(g.plate_local())}
    flush=106.08
    report={'status':'Packaging study only; raised concept not print-ready', 'flush_mount_surface_z_mm':flush,'candidate_surface_z_mm':TOP,'old_shell_top_z_mm':g.build_box().bounding_box()[5], 'roof_height_increase_mm':TOP-g.build_box().bounding_box()[5], 'flush_body_intersections_mm3':{n:max(0,(body(flush)^s).volume()) for n,s in parts.items()},'candidate_static_intersections_mm3':{n:max(0,(shell^s).volume()) for n,s in parts.items()}}
    assert all(v<.001 for v in report['candidate_static_intersections_mm3'].values())
    wire=g.cube((20,20,10),(68,5,TOP-43))
    for n,s in {'Shell':shell,**parts}.items():
        assert (body(TOP)^s).volume()<.001,n
        assert (wire^s).volume()<.001,n
    rear=g.cube((250,10,150),(-40,-10,0))
    a=base()^rear;b=g.build_box()^rear
    assert (a-b).volume()+(b-a).volume()<.001
    report['rear_mount_unchanged']=True
    for d in range(71):assert (shell.translate((0,0,d))^g.h.build_bracket()).volume()<.001
    report['service_path_collisions_mm']=[]
    for d in range(66):
        moving=g.face(g.bezel_local().translate((0,0,-d)))
        if (moving^base()).volume()>.001:report['service_path_collisions_mm'].append(d)
    assert not report['service_path_collisions_mm']
    report['roof_removed_for_cassette_service']=True
    for d in range(51):
        lifted=roof().translate((0,0,d))+body(TOP).translate((0,0,d))
        for n,s in {'Base':base(),**parts}.items():assert (lifted^s).volume()<.001,(n,d)
    report['limitation']='Static and service envelope checks pass with removable upper housing. Roof fasteners, gasket, populated-board components and actual soldered harness remain to be designed/checked; no print release.'
    (asset(g.ROOT, 'TOP_STOP_study.json')).write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
if __name__=='__main__':run()
