"""Reuse the project's deterministic mesh rasterizer for the S1 accessory."""
from pathlib import Path
import generate_stop_s1 as stop
source=Path(__file__).with_name('preview_rev_i1.py').read_text()
header,body=source.split('for index,(title,eye,solids) in enumerate(views):',1)
exec(header)
colors.update(Pod=(217,177,61),Cover=(190,150,50),Switch=(194,46,38))
accessory=[('Pod',g.face(stop.pod())),('Cover',g.face(stop.cover())),('Switch',g.face(stop.envelope()))]
views=[('S1 STOP POD ON CURRENT PANEL',(-1,2,1.8),assembly+accessory),
 ('FRONT VIEW', (0, g.h.C, g.h.S),assembly+accessory),
 ('POD FRONT PRINT DOWN',(-1,2,1),[('Pod',stop.pod().rotate((180,0,0)))]),
 ('REAR COVER REMOVED',(1,1,2),[('Pod',stop.pod()),('Cover',stop.cover().translate((0,0,25))),('Switch',stop.envelope())]),
 ('SWITCH CLEARANCE SECTION',(1,0,0),[(n,s-g.cube((50,100,100),(-42,0,-40))) for n,s in [('Pod',stop.pod()),('Cover',stop.cover()),('Switch',stop.envelope())]]),
 ('PRINT CUTOUT COUPON FIRST',(0,1,3),[('Pod',stop.coupon())])]
body='for index,(title,eye,solids) in enumerate(views):'+body
body=body.replace('GREY SHELL   TAN CRADLE   DARK R3   GREEN PCB   IVORY BEZEL AND FACEPLATE','GOLD S1 POD   RED SWITCH ENVELOPE   I1 ASSEMBLY WITH N1 FACEPLATE')
body=body.replace('N1 FACEPLATE   MEASURED BUTTON X   REPRINT FIT PENDING','SWITCH IS A CLEARANCE ENVELOPE   PHYSICAL FIT AND STIFFNESS PENDING')
body=body.replace('RevI1_preview.png','STOP_S1_preview.png')
exec(body)
