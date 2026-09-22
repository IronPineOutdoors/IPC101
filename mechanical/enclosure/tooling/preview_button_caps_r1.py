"""Actual R1 two-color cap meshes on the matching N1.2 faceplate."""
from pathlib import Path
import verify_button_caps_r1 as caps
source=Path(__file__).with_name('preview_rev_i1.py').read_text()
header,body=source.split('for index,(title,eye,solids) in enumerate(views):',1)
exec(header)
g.FONT['2']=('01110','10001','00001','00010','00100','01000','11111')
front=(0,g.h.C,g.h.S)
cap_parts=[(color,g.face(caps.installed(label,material))) for label in ('ARM','PULL') for color,material in [('Faceplate','WHITE_PETGHF'),('Inlay','BLACK_AMS')]]
plate_parts=[(color,g.face(caps.n11(material))) for color,material in [('Faceplate','WHITE_PETGHF'),('Inlay','BLACK_AMS')]]
assembly=[(n,s) for n,s in assembly if n not in ('Faceplate','Inlay')]+plate_parts+cap_parts
def single(label):
    return [(color,g.face(caps.cap(label,material))) for color,material in [('Faceplate','WHITE_PETGHF'),('Inlay','BLACK_AMS')]]
x,y=caps.fp.CENTRES['ARM']
section_cut=g.cube((30,50,40),(x,y-25,-10))
section=[('Faceplate',g.face((caps.n11()+caps.installed('ARM'))-section_cut)),
         ('PCB',g.face(g.cyl(6,g.FACEPLATE_TO_PCB_TOP-10.77,(x,y,10.77))-section_cut))]
section_clip=g.face(g.cube((20,20,22),(x-10,y-10,-5)))
views=[('R1 ARM FACE LABEL',front,single('ARM')),
       ('R1 PULL FACE LABEL',front,single('PULL')),
       ('REAR FLANGE AND STEM',(1,-2,-1),single('ARM')),
       ('N1.2 PANEL WITH LABELED CAPS',front,plate_parts+cap_parts),
       ('MEASURED RELEASE GAP SECTION',(1,0,0),[(n,s^section_clip) for n,s in section]),
       ('CURRENT CONTROL PANEL',(-1,2,1.8),assembly)]
body='for index,(title,eye,solids) in enumerate(views):'+body
body=body.replace('GREY SHELL   TAN CRADLE   DARK R3   GREEN PCB   IVORY BEZEL AND FACEPLATE','R1 CAPS   FLUSH TWO COLOR LABELS   N1.2 FACEPLATE HAS NO DUPLICATE BUTTON TEXT')
body=body.replace('N1 FACEPLATE   MEASURED BUTTON X   REPRINT FIT PENDING','STEM FIT BASED ON USER MEASUREMENTS   PHYSICAL FREE RETURN AND TRAVEL PENDING')
body=body.replace('RevI1_preview.png','R1_button_caps_preview.png')
exec(body)
