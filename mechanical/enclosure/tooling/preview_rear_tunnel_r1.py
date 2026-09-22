"""Engineering views of the stationary rear tunnel and plywood collar."""
from pathlib import Path
import generate_rear_tunnel_r1 as t
source=Path(__file__).with_name('preview_rev_i1.py').read_text()
header,body=source.split('for index,(title,eye,solids) in enumerate(views):',1)
exec(header)
g.FONT.update({'0':('01110','10001','10011','10101','11001','10001','01110'),
               '8':('01110','10001','10001','01110','10001','10001','01110'),
               'K':('10001','10010','10100','11000','10100','10010','10001')})
colors.update({'Tunnel':(124,147,164),'Collar':(187,147,67),'Wood':(205,179,139),'Roof':(150,160,168),'Connector':(80,87,91)})
wood=g.cube((140,12.7,92),(8,-27.7,5))-t.along_y(58,15,78,-29,50)
for x,z in t.SCREWS:wood-=t.along_y(4,15,x,-29,z)
cut=g.cube((170,230,220),(78,-70,-10))
context=[('Box',t.shell()),('Roof',t.roof.roof()),('Tunnel',t.bracket()),('Collar',t.collar()),('Wood',wood)]
views=[('STATIONARY TUNNEL BETWEEN RAILS',(-1,2,1),[('Tunnel',t.bracket())]),
       ('SECTION  HALF INCH PLYWOOD',(1,.1,.2),[(n,s-cut) for n,s in context]),
       ('REAR COLLAR AND CLAMP HOLES',(1,-2,1),[('Tunnel',t.bracket()),('Collar',t.collar()),('Wood',wood)])]
height=550
pixels=np.full((height,width,3),246,dtype=np.uint8)
body='for index,(title,eye,solids) in enumerate(views):'+body
body=body.replace("label('GREY SHELL   TAN CRADLE   DARK R3   GREEN PCB   IVORY BEZEL AND FACEPLATE',20,978)","label('50 MM CLEAR BORE   56 MM SLEEVE   58 MM WALL HOLE PROVISIONAL',20,496)")
body=body.replace("label('N1 FACEPLATE   MEASURED BUTTON X   REPRINT FIT PENDING',20,1005)","label('FIT RING FIRST   HARNESS MOTION AND SEALING REQUIRE PHYSICAL CHECK',20,524)")
body=body.replace("asset(g.ROOT, 'RevI1_preview.png')","t.OUT/'REAR_TUNNEL_R1_preview.png'")
exec(body)
