"""Rev I geometric and exported-mesh regression checks (no physical claims)."""
import json
import numpy as np
import trimesh
import generate_rev_i as g
import generate_rev_h as h

EPS=1e-4

def clear(a,b,label):
    overlap=(a^b).volume()
    assert overlap<EPS,(label,overlap)

def same(a,b,label):
    assert (a-b).volume()+(b-a).volume()<EPS,label

def run():
    parts=g.models(); box=parts['Box']; carrier=parts['Carrier']
    bracket=h.build_bracket(); plate=g.face(g.plate_local()); pcb=g.face(g.pcb_local())
    for name,a,b in [('carrier/shell',carrier,box),('PCB/shell',pcb,box),
                     ('plate/shell',plate,box),('PCB/carrier',pcb,carrier),
                     ('plate/carrier',plate,carrier),('wiring plate',box,h.build_port_plate())]: clear(a,b,name)
    for lift in np.linspace(0,70,71): clear(box.translate((0,0,float(lift))),bracket,f'slide {lift}')
    rear=g.cube((250,10,150),(-40,-10,0))
    same(box^rear,h.build_box()^rear,'Frozen rear interface changed')
    clear(box,h.pin_hole(),'Retaining pin')
    # New shell cannot penetrate rear datum; only the inherited receivers do.
    same(box^g.cube((300,30,180),(-60,-30,-10)),g.rear_interface(),'Unexpected rear projections')
    # Whole panel cassette lifts straight out, normal to face, after removing screws.
    for distance in np.linspace(0,65,66):
        moving=g.face((g.carrier_local()+g.pcb_local()+g.plate_local()).translate((0,0,-float(distance))))
        clear(moving,box,f'Front service removal {distance}')
    for x,y in h.HOLES:
        bore=g.cyl(3.2,6,(x,y,g.PCB_BACK))
        clear(g.carrier_local(),bore,'PCB fastener alignment')
        seat=g.cyl(8,.1,(x,y,g.PCB_BACK))-g.cyl(4.4,.3,(x,y,g.PCB_BACK-.1))
        same(seat,g.carrier_local()^seat,'PCB seating annulus')
    for travel in np.linspace(0,115,24):
        clear(g.pcb_local().translate((0,float(travel),0)),g.carrier_local(),'PCB side insertion')
    assert abs(g.pcb_local().bounding_box()[2]-g.FACEPLATE_TO_PCB_TOP)<1e-8
    assert abs(g.PCB_BACK-g.PCB_THICKNESS-g.FACEPLATE_TO_PCB_TOP)<1e-8
    clear(box,g.cube((44,18,11),(56,12,-1)),'Service port blocked')
    floor=g.cube((148,90,2.5),(4,4,.5))-g.cube((44,18,5),(56,12,0))
    for x in (50,106):
        for y in (9,33): floor-=g.cyl(4.2,5,(x,y,0))
    same(floor,box^floor,'Floor continuity')
    rearwall=g.cube((150,2.5,98),(3,.25,3))
    same(rearwall,box^rearwall,'Rear wall continuity')
    report={}
    # Inspect ALL actual authoritative Rev H exported parts, including print files.
    for name in ('Box','Bracket','Wiring_Plate'):
        for orientation in ('INSTALLED','PRINT'):
            mesh=trimesh.load_mesh(g.SOURCE_ROOT/f'CrossWind_IPC101_{name}_RevH_{orientation}.stl')
            if name=='Bracket':
                # Frozen STL has a pin tangent seam at Y=-5.3, Z=40.
                assert len(mesh.split(only_watertight=False))==1
                print('KNOWN REV H STL LIMITATION:', orientation, 'pin tangent edge; unchanged')
            else:
                assert mesh.is_watertight and len(mesh.split())==1
            expected=h.models()[name]
            if orientation=='PRINT': expected=h.print_orientation(expected,name=='Bracket')
            assert np.allclose(mesh.bounds.flatten(),expected.bounding_box(),atol=1e-4)
            assert abs(mesh.volume-expected.volume())<.1
    for name,part in parts.items():
        assert part.status()==g.m.Error.NoError and len(part.decompose())==1
        for orientation in ('INSTALLED','PRINT'):
            mesh=trimesh.load_mesh(g.ROOT/f'CrossWind_IPC101_{name}_RevI_{orientation}.stl')
            assert mesh.is_watertight and mesh.is_winding_consistent and len(mesh.split())==1
            if name=='Box':
                # Test actual exported triangles, not just Boolean volume: opposite
                # coincident faces can enclose no volume yet cap the aperture.
                vertices=mesh.vertices.copy()
                if orientation=='PRINT':
                    vertices+=np.asarray(part.bounding_box()[:3])
                vertices-=np.array([3,h.BOTTOM_Y+g.FACE_FORWARD,h.BOTTOM_Z])
                angle=np.radians(90+h.ANGLE)
                rotation=np.array([[1,0,0],[0,np.cos(angle),-np.sin(angle)],
                                   [0,np.sin(angle),np.cos(angle)]])
                local=vertices@rotation
                tris=local[mesh.faces]
                centre=tris.mean(axis=1)
                caps=(np.max(np.abs(tris[:,:,2]),axis=1)<.001)
                caps&=(centre[:,0]>-9.9)&(centre[:,0]<159.9)
                caps&=(centre[:,1]>-9.9)&(centre[:,1]<109.9)
                assert not np.any(caps), 'Exported front opening has coplanar membrane triangles'
            expected=part if orientation=='INSTALLED' else g.print_part(name,part)
            assert np.allclose(mesh.bounds.flatten(),expected.bounding_box(),atol=1e-4)
            assert abs(mesh.volume-expected.volume())<.1
            if orientation=='PRINT':
                assert np.all(mesh.extents<256),('A1 build envelope',mesh.extents)
                assert abs(mesh.bounds[0,2])<1e-4
            report[f'{name}_{orientation}']=np.round(mesh.extents,3).tolist()
    print(json.dumps(report,indent=2))
    print('PASS: closed connected exports; inherited interface; pin; 71 slide positions; 66 front withdrawal positions; plate/PCB/carrier clearance; four PCB seats; stack; service port; rear/floor continuity; print bounds.')
    return parts

if __name__=='__main__': run()
