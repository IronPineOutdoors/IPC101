"""Compare the compact IPO option with the prior full wordmark."""
from pathlib import Path
import verify_faceplate_n13 as n13
from verify_button_caps_r1 import load,installed
source=Path(__file__).with_name('preview_rev_i1.py').read_text()
header,body=source.split('for index,(title,eye,solids) in enumerate(views):',1)
exec(header)
front=(0,g.h.C,g.h.S)
def plate(rev):
    return [(color,g.face(load(f'CrossWind_IPC101_Faceplate_Rev{rev}_{mat}.stl').translate((0,0,-2)))) for color,mat in [('Faceplate','WHITE_PETGHF'),('Inlay','BLACK_AMS')]]
new=plate('N13');old=plate('N12')
caps=[(color,g.face(installed(label,mat))) for label in ('ARM','PULL') for color,mat in [('Faceplate','WHITE_PETGHF'),('Inlay','BLACK_AMS')]]
badge_clip=g.face(g.cube((20,20,4),(106,78,-3)))
top_clip=g.face(g.cube((145,24,4),(3,76,-3)))
body_assembly=[(name,s) for name,s in assembly if name not in ('Faceplate','Inlay')]+new+caps
views=[('PRIOR FULL WORDMARK',front,old+caps),
       ('N1.3 COMPACT TREE AND IPO',front,new+caps),
       ('COMPACT BADGE DETAIL',front,[(n,s^badge_clip) for n,s in new]),
       ('CROSSWIND AND COMPACT BRAND',front,[(n,s^top_clip) for n,s in new]),
       ('N1.3 ON CURRENT ASSEMBLY',(-1,2,1.8),body_assembly),
       ('REAR INTERFACE UNCHANGED',(1,-2,1.5),new)]
body='for index,(title,eye,solids) in enumerate(views):'+body
body=body.replace('GREY SHELL   TAN CRADLE   DARK R3   GREEN PCB   IVORY BEZEL AND FACEPLATE','ACTUAL TRACED TREE   BOLD IPO   CROSSWIND ARTWORK AND MECHANICAL FIT UNCHANGED')
body=body.replace('N1 FACEPLATE   MEASURED BUTTON X   REPRINT FIT PENDING','N1.3 COMPACT BRANDING OPTION   INSPECT SLICED LETTERING BEFORE PRINTING')
body=body.replace('RevI1_preview.png','N13_faceplate_preview.png')
exec(body)
