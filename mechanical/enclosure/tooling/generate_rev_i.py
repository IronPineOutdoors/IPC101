"""Rev I fit-validation shell/carrier; mm, Rev H installed coordinate system."""
from enclosure_paths import asset
from pathlib import Path
import sys
import manifold3d as m
import generate_rev_h as h
from generate_rev_h import cube, cyl, ring
from generate_crosswind_control_box import write_binary_stl
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'panel'))
from generate_ipc101_rev_c import FONT

FACEPLATE_TO_PCB_TOP = 16.5  # physical prototype target, NOT frozen
PCB_THICKNESS = 1.56  # measured/user-confirmed; KiCad nominal is 1.60
PCB_BACK = FACEPLATE_TO_PCB_TOP + PCB_THICKNESS
CARRIER_BACK = PCB_BACK + 7
FACE_FORWARD = 8.0  # shell development allowance; does not move docking geometry
ATTACH = ((-5,20),(-5,80),(155,20),(155,80))
SOURCE_ROOT = Path(__file__).resolve().parent.parent
ROOT = SOURCE_ROOT / "archive" / "superseded-rev-i"

def face(s):
    return h.face(s).translate((0,FACE_FORWARD,0))

def mark(text, x, y, z):
    font = dict(FONT)
    font.update({'0':('01110','10001','10011','10101','11001','10001','01110'),
                 '1':('00100','01100','00100','00100','00100','00100','01110'),
                 '-':('00000','00000','00000','11111','00000','00000','00000')})
    cells=[]
    for i,ch in enumerate(text):
        if ch==' ': continue
        for r,row in enumerate(font[ch]):
            for c,on in enumerate(row):
                if on=='1': cells.append(cube((.42,.42,.4),(x+i*3+c*.5,y+(6-r)*.5,z)))
    return m.Manifold.batch_boolean(cells,m.OpType.Add)

def rear_interface():
    # Extract the actual authoritative geometry; no retyped rail dimensions.
    return h.build_box() ^ cube((250,10,150),(-40,-10,0))

def build_box():
    front=face(cube((174,124,32),(-12,-12,0)))
    back=cube((156,3,105),(0,0,0))
    outer=m.Manifold.batch_hull([front,back])
    # Cross the front datum: a coplanar cut can leave zero-volume sheets
    # that pass Boolean volume checks but obstruct the exported opening.
    cavity=face(cube((170,120,30),(-10,-10,-1)))
    cavity+=h.prism([(3,3),(h.BOTTOM_Y-3,3),(h.BOTTOM_Y-3,26),(31,96),(3,100)],(3,153))
    box=outer-cavity
    # Plane-cut the front opening and keep all new shell behind its datum.
    box-=face(cube((220,170,80),(-35,-35,-80)))
    # Integral structural rear seats, outside the PCB envelope.
    for x,y in ATTACH:
        box+=face(cube((10,12.2,32-CARRIER_BACK),(x-5,y-6.1,CARRIER_BACK)))
        box-=face(cyl(4.2,6.1,(x,y,CARRIER_BACK-.1)))
    box+=rear_interface()
    # Preserve the existing replaceable blank service plate and its fasteners.
    box-=cube((44,18,12),(56,12,-1))
    for x in (50,106):
        for y in (9,33):
            box+=cube((10,10,9),(x-5,y-5,0))
            box-=cyl(4.2,6.1,(x,y,-.1))
    box-=mark('IPC101-ENC-RI TEST',48,45,0)
    return box

def carrier_local():
    # Open perimeter frame; underside seats define board height independently
    # of the faceplate fasteners. Side access remains open between the rails.
    part=ring(-9,-9,168,118,8,3,CARRIER_BACK-3)
    part+=ring(-9,-9,168,118,8,3,0)
    for x,y in ATTACH:
        part+=cube((8,10,CARRIER_BACK),(x-4,y-5,0))
        part-=cyl(3.4,CARRIER_BACK+2,(x,y,-1))
        # Recess screw heads to the rear rail, leaving an unobstructed driver bore.
        part-=cyl(6.5,CARRIER_BACK-3,(x,y,0))
    for x,y in h.HOLES:
        # Narrow bridges reach only the mounting-hole corners.
        left=x<75
        start=-2 if left else x
        width=x+2 if left else 152-x
        part+=cube((width,8,6),(start,y-4,0))
        part+=cyl(10,6,(x,y,0))
        part-=cyl(4.2,6.2,(x,y,-.1))
        part+=cube((width,8,CARRIER_BACK-PCB_BACK),(start,y-4,PCB_BACK))
        part+=cyl(9,CARRIER_BACK-PCB_BACK,(x,y,PCB_BACK))
        part-=cyl(4.2,6,(x,y,PCB_BACK))
    part-=mark('IPC101-CARRIER-RI TEST',35,-7,CARRIER_BACK-.4)
    return part

def pcb_local():
    pcb=cube((150,100,PCB_THICKNESS),(0,0,FACEPLATE_TO_PCB_TOP))
    for x,y in h.HOLES: pcb-=cyl(3.2,PCB_THICKNESS+2,(x,y,FACEPLATE_TO_PCB_TOP-1))
    return pcb

def plate_local():
    # Envelope only: N/M.4 source is not present. Do not substitute Rev C layout.
    p=cube((150,100,2),(0,0,-2))
    for x,y in h.HOLES: p-=cyl(3.2,4,(x,y,-3))
    return p

def models():
    return {'Box':build_box(),'Carrier':face(carrier_local())}

def print_part(name,part):
    if name=='Carrier': return h.print_orientation(carrier_local().rotate((180,0,0)))
    return h.print_orientation(part)

if __name__=='__main__':
    ROOT.mkdir(parents=True, exist_ok=True)
    for name,part in models().items():
        assert part.status()==m.Error.NoError and len(part.decompose())==1
        for orientation,solid in [('INSTALLED',part),('PRINT',print_part(name,part))]:
            write_binary_stl(asset(ROOT, f'CrossWind_IPC101_{name}_RevI_{orientation}.stl'),solid)
        print(name,part.bounding_box(),part.volume())
