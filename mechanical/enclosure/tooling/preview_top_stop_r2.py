"""Show corrected underside access and the central fit coupon."""
from pathlib import Path
import generate_top_stop_r2 as design
source=Path(__file__).with_name('preview_rev_i1.py').read_text()
header,body=source.split('for index,(title,eye,solids) in enumerate(views):',1)
exec(header)
g.FONT.update({'2':('01110','10001','00001','00010','00100','01000','11111'),'K':('10001','10010','10100','11000','10100','10010','10001')})
colors.update({'Roof':(150,160,168),'Block':(56,126,92)})
cut=g.cube((100,100,100),(78,-30,60))
views=[('R2 UNDERSIDE ACCESS',(-1,2,-1.8),[('Roof',design.roof())]),
       ('INSERT THEN TWIST WITH ROOF OFF',(1,.2,-.4),[('Roof',design.roof()-cut),('Block',design.block(45,8))]),
       ('CENTRAL ACCESS COUPON',(-1,2,-1.5),[('Roof',design.coupon())])]
height=550
pixels=np.full((height,width,3),246,dtype=np.uint8)
body='for index,(title,eye,solids) in enumerate(views):'+body
body=body.replace("label('GREY SHELL   TAN CRADLE   DARK R3   GREEN PCB   IVORY BEZEL AND FACEPLATE',20,978)","label('41 MM CLEAR ACCESS   TOP KEYED HOLE AND FOUR ROOF MOUNTS UNCHANGED',20,496)")
body=body.replace("label('N1 FACEPLATE   MEASURED BUTTON X   REPRINT FIT PENDING',20,1005)","label('PRINT CENTRAL COUPON FIRST   ACTUAL SWITCH INSERTION AND TWIST TEST PENDING',20,524)")
body=body.replace("asset(g.ROOT, 'RevI1_preview.png')","design.OUT/'TOP_STOP_R2_preview.png'")
exec(body)
