"""Actual N1.4 export and same-scale old/new P504 opening close-ups."""
from pathlib import Path
from verify_button_caps_r1 import load,installed
source=Path(__file__).with_name('preview_rev_i1.py').read_text()
header,body=source.split('for index,(title,eye,solids) in enumerate(views):',1)
exec(header)
g.FONT.update({'0':('01110','10001','10011','10101','11001','10001','01110'),
               '2':('01110','10001','00001','00010','00100','01000','11111'),
               '8':('01110','10001','10001','01110','10001','10001','01110')})
front=(0,g.h.C,g.h.S)
def plate(rev):
    return [(color,g.face(load(f'CrossWind_IPC101_Faceplate_Rev{rev}_{mat}.stl').translate((0,0,-2)))) for color,mat in [('Faceplate','WHITE_PETGHF'),('Inlay','BLACK_AMS')]]
new=plate('N14');old=plate('N13')
clip=g.face(g.cube((22,22,7),(94,52.5,-3)))
caps=[(color,g.face(installed(label,mat))) for label in ('ARM','PULL') for color,mat in [('Faceplate','WHITE_PETGHF'),('Inlay','BLACK_AMS')]]
current=[(name,s) for name,s in assembly if name not in ('Faceplate','Inlay')]+new+caps
views=[('N1.4 ENLARGED P504 OPENING',front,new+caps),
       ('PRIOR 6.2 MM OPENING',front,[(n,s^clip) for n,s in old]),
       ('NEW 8 MM OPENING',front,[(n,s^clip) for n,s in new]),
       ('REAR CRADLE UNCHANGED',(1,-2,-1),[(n,s^clip) for n,s in new]),
       ('N1.4 ON CURRENT ASSEMBLY',(-1,2,1.8),current),
       ('P504 OPENING AND FRONT LAND',(-1,2,1.8),[(n,s^clip) for n,s in new])]
body='for index,(title,eye,solids) in enumerate(views):'+body
body=body.replace('GREY SHELL   TAN CRADLE   DARK R3   GREEN PCB   IVORY BEZEL AND FACEPLATE','N1.4   P504 APERTURE 8 MM   SAME REAR CRADLE AND CORRECTED BUTTON POSITIONS')
body=body.replace('N1 FACEPLATE   MEASURED BUTTON X   REPRINT FIT PENDING','ACTUAL DIRECTIONAL TRAVEL STILL NEEDS PHYSICAL CHECK')
body=body.replace('RevI1_preview.png','N14_faceplate_preview.png')
exec(body)
