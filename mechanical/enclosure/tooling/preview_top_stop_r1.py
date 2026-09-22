"""R1 engineering preview: fastened removable roof; physical fit/sealing pending."""
from pathlib import Path
import generate_top_stop_r1 as design
import study_top_stop as study
from verify_button_caps_r1 import load,installed
source=Path(__file__).with_name('preview_rev_i1.py').read_text()
header,body=source.split('for index,(title,eye,solids) in enumerate(views):',1)
exec(header)
colors.update({'Roof':(150,160,168),'Red':(212,36,28),'Yellow':(242,191,35),'Switch':(48,49,52),'Wire':(189,106,53)})
plateparts=[(n,g.face(load('CrossWind_IPC101_Faceplate_RevN14_'+mat+'.stl').translate((0,0,-2)))) for n,mat in [('Faceplate','WHITE_PETGHF'),('Inlay','BLACK_AMS')]]
caps=[(n,g.face(installed(label,mat))) for label in ('ARM','PULL') for n,mat in [('Faceplate','WHITE_PETGHF'),('Inlay','BLACK_AMS')]]
fixed=[(n,s) for n,s in assembly if n not in ('Box','Faceplate','Inlay')]+[('Box',design.base())]+plateparts+caps
upper=[('Roof',design.roof()),('Switch',study.body(study.TOP)+study.neck(study.TOP)),('Red',study.button(study.TOP)),('Yellow',study.collar(study.TOP))]
full=fixed+upper+[('Hardware',design.screw(x,y)) for x,y in design.HOLES]
cut=g.cube((160,220,220),(78,-40,-10))
views=[('TOP STOP R1  REMOVABLE ROOF',(-1,2,1.7),full),('SIDE SECTION THROUGH SWITCH',(1,.1,.15),[(n,s-cut) for n,s in full]),('UPPER HOUSING REMOVES FIRST',(-1,2,1.3),fixed+[(n,s.translate((0,0,45))) for n,s in upper])]
height=550
pixels=np.full((height,width,3),246,dtype=np.uint8)
body='for index,(title,eye,solids) in enumerate(views):'+body
body=body.replace("label('GREY SHELL   TAN CRADLE   DARK R3   GREEN PCB   IVORY BEZEL AND FACEPLATE',20,978)","label('R1 FIT PROTOTYPE   FOUR M3 SCREWS   LOCATING SHOULDERS   HARNESS TIE TAB',20,496)")
body=body.replace("label('N1 FACEPLATE   MEASURED BUTTON X   REPRINT FIT PENDING',20,1005)","label('N1.4 GEOMETRY SHOWN   FINAL ARTWORK AND WEATHER SEALING PENDING',20,524)")
body=body.replace("asset(g.ROOT, 'RevI1_preview.png')","design.OUT/'TOP_STOP_R1_preview.png'")
exec(body)
