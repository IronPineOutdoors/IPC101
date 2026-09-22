"""N1 front, logo detail, rear and installed views from actual exported meshes."""
from pathlib import Path
source=Path(__file__).with_name('preview_rev_i1.py').read_text()
header,body=source.split('for index,(title,eye,solids) in enumerate(views):',1)
exec(header)
g.FONT.update({'7':('11111','00001','00010','00100','01000','01000','01000'),
               '8':('01110','10001','10001','01110','10001','10001','01110')})
front=(0,g.h.C,g.h.S)
faceparts=[('Faceplate',g.face(material_local('WHITE_PETGHF'))),('Inlay',g.face(material_local('BLACK_AMS')))]
logo_clip=g.face(g.cube((65,22,8),(88,77,-3)))
buttons_clip=g.face(g.cube((100,23,8),(23,12,-3)))
mark_clip=g.face(g.cube((45,10,2),(52.5,9,-1)))
views=[('N1 OPERATOR VIEW',front,faceparts),
 ('TREE AND OUTDOORS SEPARATED',front,[(n,s^logo_clip) for n,s in faceparts]),
 ('ARM LEFT   PULL RIGHT',front,[(n,s^buttons_clip) for n,s in faceparts]),
 ('REAR REVISION MARK',(1,-2,-1),[(n,s^mark_clip) for n,s in faceparts if n=='Faceplate']),
 ('N1 ON I1 ASSEMBLY',(-1,2,1.8),assembly),
 ('REAR CRADLE UNCHANGED',(1,-2,1.5),faceparts)]
body='for index,(title,eye,solids) in enumerate(views):'+body
body=body.replace('GREY SHELL   TAN CRADLE   DARK R3   GREEN PCB   IVORY BEZEL AND FACEPLATE','N1   ARM X46.88   PULL X115.67   OPERATOR LEFT EDGE DATUM')
body=body.replace('N1 FACEPLATE   MEASURED BUTTON X   REPRINT FIT PENDING','MEASURED BUTTON CENTERS   ACTUAL TWO MATERIAL EXPORTS   PHYSICAL FIT PENDING')
body=body.replace('RevI1_preview.png','N1_faceplate_preview.png')
exec(body)
