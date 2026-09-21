"""Rev I.1: unchanged R3 carrier in a removable cradle and separate face bezel.
All dimensions mm. Rev I and Rev H sources/exports remain historical baselines.
"""
from pathlib import Path
import numpy as np
import trimesh
import generate_rev_i as previous
from generate_rev_i import h, m, cube, cyl, ring, face, mark, rear_interface
from generate_crosswind_control_box import write_binary_stl

ROOT=Path(__file__).resolve().parent
FACEPLATE_TO_PCB_TOP=16.5  # provisional, adjustable after assembled fit test
PCB_THICKNESS=1.56
PCB_BACK=FACEPLATE_TO_PCB_TOP+PCB_THICKNESS
R3_HEIGHT=7.4
R3_BACK=PCB_BACK+R3_HEIGHT
CRADLE_BACK=R3_BACK+4
SEAT=R3_BACK
BEZEL_POST_END=SEAT-3
ATTACH=previous.ATTACH
FACE_FORWARD=previous.FACE_FORWARD
NUT_AF=5.8  # provisional slip pocket for nominal 5.5 mm AF M3 hex nut
NUT_DEPTH=2.6

def r3_local():
    mesh=trimesh.load_mesh(ROOT/'IPC101_RevA_RearCarrier_R3.stl')
    solid=m.Manifold(m.Mesh(np.asarray(mesh.vertices,dtype=np.float32),np.asarray(mesh.faces,dtype=np.uint32)))
    assert solid.status()==m.Error.NoError
    return solid.scale((1,1,-1)).translate((0,0,R3_BACK))

def pcb_local():
    p=cube((150,100,PCB_THICKNESS),(0,0,FACEPLATE_TO_PCB_TOP))
    for x,y in h.HOLES:p-=cyl(3.2,PCB_THICKNESS+2,(x,y,FACEPLATE_TO_PCB_TOP-1))
    return p

plate_local=previous.plate_local

def build_box():
    # Same external hull as corrected Rev I; only interior seating/relief changes.
    outer=m.Manifold.batch_hull([face(cube((174,124,32),(-12,-12,0))),cube((156,3,105),(0,0,0))])
    cavity=face(cube((170,120,32),(-10,-10,-1)))
    cavity=cavity^cube((240,180,160),(-40,3,3))
    cavity+=h.prism([(3,3),(h.BOTTOM_Y-3,3),(h.BOTTOM_Y-3,26),(31,96),(3,100)],(3,153))
    box=outer-cavity-face(cube((220,170,80),(-35,-35,-80)))
    for x,y in ATTACH:
        box+=face(cube((10,12.2,32-SEAT),(x-5,y-6.1,SEAT)))
        box-=face(cyl(4.2,6.1,(x,y,SEAT-.1)))
    box+=rear_interface()
    box-=cube((44,18,12),(56,12,-1))
    for x in (50,106):
        for y in (9,33):
            box+=cube((10,10,9),(x-5,y-5,0))
            box-=cyl(4.2,6.1,(x,y,-.1))
    return box-mark('IPC101-ENC-RI1 TEST',48,45,0)

def cradle_local():
    # Peripheral nest accepts the original R3 print with 0.30 mm side clearance.
    # Rear shelves support R3; four nuts secure board, R3 and cradle together.
    p=ring(-9,-9,168,118,5.7,CRADLE_BACK-BEZEL_POST_END,BEZEL_POST_END)
    p+=ring(-9,-9,168,118,12,4,R3_BACK)
    for x,y in h.HOLES:
        p+=cyl(10,4,(x,y,R3_BACK))
        p-=cyl(3.4,6,(x,y,R3_BACK-1))
        nut=m.Manifold.cylinder(NUT_DEPTH+.1,NUT_AF/np.sqrt(3),circular_segments=6)
        p-=nut.translate((x,y,CRADLE_BACK-NUT_DEPTH))
    for x,y in ATTACH:
        # Front 3 mm ring lands on shell seats; relieve everything behind them.
        p-=cube((10.6,12.8,10),(x-5.3,y-6.4,SEAT))
        p-=cyl(3.4,10,(x,y,BEZEL_POST_END-1))
        # Open inward U-slot avoids a bore tangent to the R3 nest edge.
        start=x if x<75 else x-2.2
        p-=cube((2.2,3.4,10),(start,y-1.7,BEZEL_POST_END-1))
    p-=mark('IPC101-CRADLE-RI1 TEST',35,-7,CRADLE_BACK-.4)
    return p

def bezel_local():
    # Removable front support: taking it off exposes every PCB screw axially.
    # Nominal 3 mm overlap under the faceplate perimeter leaves a future
    # gasket seating land; no unselected gasket thickness enters the stack.
    p=ring(-9,-9,168,118,12,3,0)
    for x,y in ATTACH:
        p+=cube((8,10,BEZEL_POST_END),(x-4,y-5,0))
        p-=cyl(3.4,BEZEL_POST_END+2,(x,y,-1))
    for x,y in h.HOLES:
        start=-2 if x<75 else x
        width=x+2 if x<75 else 152-x
        p+=cube((width,8,6),(start,y-4,0))
        p+=cyl(10,6,(x,y,0))
        p-=cyl(4.2,6.2,(x,y,-.1))
    p-=mark('IPC101-RIM-RI1 TEST',40,-7,2.6)
    return p

def models():
    return {'Box':build_box(),'Cradle':face(cradle_local()),'Bezel':face(bezel_local())}

def print_part(name,solid):
    if name=='Cradle':solid=cradle_local().rotate((180,0,0))
    elif name=='Bezel':solid=bezel_local()
    return h.print_orientation(solid)

if __name__=='__main__':
    for name,solid in models().items():
        assert solid.status()==m.Error.NoError and len(solid.decompose())==1,(name,'invalid/disconnected')
        for orientation,part in [('INSTALLED',solid),('PRINT',print_part(name,solid))]:
            write_binary_stl(ROOT/f'CrossWind_IPC101_{name}_RevI1_{orientation}.stl',part)
        print(name,solid.bounding_box(),round(solid.volume(),3))
