"""Verify R3 reuse, hardware access, service paths and all Rev I.1 exports."""
import itertools,json
import numpy as np
import trimesh
import generate_rev_i1 as g
from verify_rev_i import clear,same

def hardware():
    board=[]; nuts=[]; attachment=[]
    for x,y in g.h.HOLES:
        # Provisional M3x14 socket screw: 5.5 diameter x 3 head; 3 mm shank.
        board.append(g.cyl(5.5,3,(x,y,g.FACEPLATE_TO_PCB_TOP-3))+g.cyl(3,14,(x,y,g.FACEPLATE_TO_PCB_TOP)))
        nut=g.m.Manifold.cylinder(2.4,5.5/np.sqrt(3),circular_segments=6).translate((x,y,g.CRADLE_BACK-2.4))
        nuts.append(nut-g.cyl(3,4,(x,y,g.CRADLE_BACK-3)))
    for x,y in g.ATTACH:
        attachment.append(g.cyl(5.5,3,(x,y,-3))+g.cyl(3,30,(x,y,0)))
    faceplate=[]
    for x,y in g.h.HOLES:
        faceplate.append(g.cyl(5.5,3,(x,y,-5))+g.cyl(3,6,(x,y,-2)))
    return board,nuts,attachment,faceplate

def exported_checks(parts):
    report={}
    for name,part in parts.items():
        assert part.status()==g.m.Error.NoError and len(part.decompose())==1,name
        for orientation in ('INSTALLED','PRINT'):
            mesh=trimesh.load_mesh(g.ROOT/f'CrossWind_IPC101_{name}_RevI1_{orientation}.stl')
            assert mesh.is_watertight and mesh.is_winding_consistent and len(mesh.split())==1,(name,orientation)
            expected=part if orientation=='INSTALLED' else g.print_part(name,part)
            assert np.allclose(mesh.bounds.flatten(),expected.bounding_box(),atol=1e-4)
            assert abs(mesh.volume-expected.volume())<.1
            if orientation=='PRINT':
                assert np.all(mesh.extents<256) and abs(mesh.bounds[0,2])<1e-4
            if name=='Box':
                v=mesh.vertices.copy()
                if orientation=='PRINT':v+=np.asarray(part.bounding_box()[:3])
                v-=[3,g.h.BOTTOM_Y+g.FACE_FORWARD,g.h.BOTTOM_Z]
                a=np.radians(90+g.h.ANGLE)
                t=(v@np.array([[1,0,0],[0,np.cos(a),-np.sin(a)],[0,np.sin(a),np.cos(a)]]))[mesh.faces]
                c=t.mean(axis=1)
                cap=(np.max(abs(t[:,:,2]),axis=1)<.001)&(c[:,0]>-9.9)&(c[:,0]<159.9)&(c[:,1]>-9.9)&(c[:,1]<109.9)
                assert not np.any(cap),'Front membrane regression'
            report[name+'_'+orientation]=np.round(mesh.extents,3).tolist()
    return report

def run():
    parts=g.models(); box=parts['Box']; cradle=g.cradle_local(); bezel=g.bezel_local(); r3=g.r3_local(); pcb=g.pcb_local(); plate=g.plate_local()
    local={'Cradle':cradle,'Bezel':bezel,'R3':r3,'PCB':pcb,'Faceplate':plate}
    for (a,s),(b,t) in itertools.combinations(local.items(),2):clear(s,t,a+'/'+b)
    for name,solid in local.items():clear(g.face(solid),box,name+'/shell')
    bracket=g.h.build_bracket()
    for lift in range(71):clear(box.translate((0,0,lift)),bracket,f'rail lift {lift}')
    rear=g.cube((250,10,150),(-40,-10,0))
    same(box^rear,g.h.build_box()^rear,'Rev H interface')
    same(box^g.cube((300,30,180),(-60,-30,-10)),g.rear_interface(),'Rear projection')
    clear(box,g.h.pin_hole(),'Pin access')
    assert np.allclose(box.bounding_box(),g.previous.build_box().bounding_box()),'Shell exterior bounds'
    clear(box,g.h.build_port_plate(),'Wiring plate')
    clear(box,g.cube((44,18,11),(56,12,-1)),'Service port')
    floor=g.cube((148,90,2.5),(4,4,.5))-g.cube((44,18,5),(56,12,0))
    for x in (50,106):
        for y in (9,33):floor-=g.cyl(4.2,5,(x,y,0))
    same(floor,box^floor,'Floor')
    rearwall=g.cube((150,2.5,98),(3,.25,3));same(rearwall,box^rearwall,'Rear wall')
    lip=g.ring(0,0,150,100,2.5,.1,0)
    same(lip,bezel^lip,'Continuous faceplate seating land')
    # Actual R3 STL, not a redrawn approximation. Only rigid reflection/placement.
    original=trimesh.load_mesh(g.ROOT/'IPC101_RevA_RearCarrier_R3.stl')
    assert original.is_watertight and len(original.split())==1
    assert abs(r3.volume()-original.volume)<.02
    assert abs(r3.bounding_box()[2]-g.PCB_BACK)<1e-5
    assert abs(pcb.bounding_box()[2]-g.FACEPLATE_TO_PCB_TOP)<1e-8
    board,nuts,attachment,faceplate_bolts=hardware()
    for bolt,nut in zip(board,nuts):
        for name,solid in local.items():clear(bolt,solid,'PCB screw/'+name);clear(nut,solid,'PCB nut/'+name)
        clear(g.face(bolt+nut),box,'PCB hardware/shell')
    for bolt in attachment+faceplate_bolts:
        for name,solid in local.items():clear(bolt,solid,'Cassette screw/'+name)
        clear(g.face(bolt),box,'Cassette screw/shell')
    for x,y in g.h.HOLES:
        # With bezel removed, driver and screw head approach axially unobstructed.
        tool=g.cyl(6.5,g.FACEPLATE_TO_PCB_TOP-3+20,(x,y,-20))
        clear(tool,cradle+r3+pcb,'PCB driver')
        clear(g.face(tool),box,'PCB driver/shell')
        face_tool=g.cyl(6.5,20,(x,y,-25));clear(face_tool,plate+bezel,'Faceplate driver')
        bore=g.cyl(3,20,(x,y,g.PCB_BACK-1));clear(bore,r3+cradle,'R3/board hole alignment')
        seat=g.cyl(7.5,.1,(x,y,g.PCB_BACK+.001))-g.cyl(3.8,.3,(x,y,g.PCB_BACK-.1))
        same(seat,r3^seat,'R3 post seating annulus')
    for x,y in g.ATTACH:
        tool=g.cyl(6.5,20,(x,y,-23));clear(tool,plate+bezel,'Cassette driver/faceplate')
    clamp_areas=[]
    for x,y in g.ATTACH:
        witness=g.cube((8,10,.1),(x-4,y-5,g.BEZEL_POST_END))
        area=(cradle^witness).volume()/.1
        assert area>0,'Bezel post lacks cradle contact'
        clamp_areas.append(round(area,3))
        underside=(cradle^g.cube((10,12.2,.1),(x-5,y-6.1,g.SEAT-.1)))
        assert underside.volume()>0,'Cradle lacks seat contact'
    # Fasteners removed: whole cassette, bezel alone, PCB alone and R3 lift out.
    cassette=cradle+bezel+r3+pcb+plate
    for travel in np.linspace(0,65,66):
        delta=(0,0,-float(travel))
        clear(g.face(cassette.translate(delta)),box,'Cassette withdrawal')
        clear((bezel+plate).translate(delta),cradle+r3+pcb,'Bezel removal')
        clear(pcb.translate(delta),cradle+r3,'PCB removal with bezel off')
        clear(r3.translate(delta),cradle,'R3 insertion/removal')
    report=exported_checks(parts)
    report['bezel_to_cradle_contact_mm2']=clamp_areas
    report['status']='TEST-FIT / PHYSICAL VALIDATION PENDING'
    report['checks']='PASS: 6 closed connected exports; R3 placement/posts; hardware envelopes and driver access; 71 rail and 66 service positions; exact Rev H interface; front membrane; floor/rear/port; spacing'
    report['limitations']=['N/M.4 rear features absent','Hardware dimensions provisional','Populated PCB and harness not modeled','Seals and structural loads unqualified','Inherited Rev H bracket pin tangency documented in README']
    (g.ROOT/'RevI1_verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':run()
