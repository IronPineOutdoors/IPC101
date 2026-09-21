"""Engineering preview of the R3-based Rev I.1 assembly; reference hardware only."""
import numpy as np
import struct,zlib
import generate_rev_i1 as g
from faceplate_rev_n1_reference import material_local
from verify_rev_i1 import hardware
parts=g.models()
box=parts['Box'];cradle=parts['Cradle'];bezel=parts['Bezel']
r3=g.face(g.r3_local());pcb=g.face(g.pcb_local());plate=g.face(g.plate_local());bracket=g.h.build_bracket()
g.FONT=dict(g.previous.FONT)
g.FONT.update({'B':('11110','10001','10001','11110','10001','10001','11110'),'G':('01111','10000','10000','10111','10001','10001','01111'),'H':('10001','10001','10001','11111','10001','10001','10001'),'V':('10001','10001','10001','10001','10001','01010','00100'),'X':('10001','10001','01010','00100','01010','10001','10001'),'F':('11111','10000','10000','11110','10000','10000','10000'),'Y':('10001','10001','01010','00100','00100','00100','00100')})
g.FONT.update({'1':('00100','01100','00100','00100','00100','00100','01110'),'6':('01110','10000','10000','11110','10001','10001','01110'),'5':('11111','10000','10000','11110','00001','00001','11110'),'.':('00000','00000','00000','00000','00000','00100','00100')})
g.FONT['4']=('00010','00110','01010','10010','11111','00010','00010')
g.FONT['3']=('11110','00001','00001','01110','00001','00001','11110')
g.FONT['Z']=('11111','00001','00010','00100','01000','10000','11111')
colors={'Box':(150,160,168),'Cradle':(180,151,114),'R3':(104,116,128),'PCB':(106,147,125),'Bezel':(215,206,186),'Faceplate':(232,225,209),'Inlay':(38,40,42),'Bracket':(103,111,124),'Wiring':(187,188,182),'Hardware':(73,78,83)}
board,nuts,attachment,faceplate_bolts=hardware()
bolts=g.m.Manifold.batch_boolean(board+nuts+attachment+faceplate_bolts,g.m.OpType.Add)
assembly=[('Box',box),('Cradle',cradle),('R3',r3),('Bezel',bezel),('PCB',pcb),('Faceplate',g.face(material_local('WHITE_PETGHF'))),('Inlay',g.face(material_local('BLACK_AMS'))),('Bracket',bracket),('Wiring',g.h.build_port_plate()),('Hardware',g.face(bolts))]
cut=g.cube((120,260,200),(78,-40,-20))
views=[('OPEN SHELL AND SEATS',(1,2,1.6),[('Box',box)]),
       ('REAR WITH REV H BRACKET',(-1,-2,1),assembly),
       ('ORIGINAL R3 IN CRADLE',(1,2,1.6),[('Cradle',cradle),('R3',r3)]),
       ('BEZEL OFF PCB SCREWS EXPOSED',(1,2,1.6),[('Cradle',cradle),('R3',r3),('PCB',pcb),('Hardware',g.face(g.m.Manifold.batch_boolean(board+nuts,g.m.OpType.Add)))]),
       ('EXPLODED FRONT SERVICE',(1.4,2,1.5),[('Box',box),('Bracket',bracket.translate((0,-25,0))),('Cradle',g.face(g.cradle_local().translate((0,0,-30)))),('R3',g.face(g.r3_local().translate((0,0,-50)))),('PCB',g.face(g.pcb_local().translate((0,0,-70)))),('Bezel',g.face(g.bezel_local().translate((0,0,-90)))),('Faceplate',g.face(material_local('WHITE_PETGHF').translate((0,0,-110)))),('Inlay',g.face(material_local('BLACK_AMS').translate((0,0,-110))))]),
       ('SECTION PCB TOP GAP 16.5 MM',(1,0,0),[(n,s-cut) for n,s in assembly])]
width,height=1800,1040
pixels=np.full((height,width,3),246,dtype=np.uint8)
def label(text,x,y,scale=2):
    for i,ch in enumerate(text):
        if ch==' ':continue
        for r,row in enumerate(g.FONT.get(ch,g.FONT['I'])):
            for c,on in enumerate(row):
                if on=='1': pixels[y+r*scale:y+(r+1)*scale,x+(i*6+c)*scale:x+(i*6+c+1)*scale]=(45,48,51)
for index,(title,eye,solids) in enumerate(views):
    ox=(index%3)*600; oy=(index//3)*480
    label(title,ox+20,oy+20)
    forward=np.array(eye,dtype=float);forward/=np.linalg.norm(forward)
    right=np.cross((0,0,1),forward);right/=np.linalg.norm(right)
    up=np.cross(forward,right);rotation=np.array([right,up,forward]).T
    allv=np.concatenate([s.to_mesh().vert_properties[:,:3] for _,s in solids])@rotation
    lo=allv.min(axis=0);hi=allv.max(axis=0);centre=(lo+hi)/2
    scale=min(550/(hi[0]-lo[0]),390/(hi[1]-lo[1]))
    depth=np.full((480,600),-np.inf)
    for name,solid in solids:
        mesh=solid.to_mesh(); vertices=mesh.vert_properties[:,:3]
        projected=vertices@rotation-centre
        projected[:,:2]*=scale;projected[:,0]+=300;projected[:,1]=260-projected[:,1]
        for triangle in mesh.tri_verts:
            pts=projected[triangle];a,b,c=pts
            lo=np.maximum(np.floor(pts[:,:2].min(axis=0)).astype(int),(0,45))
            hi=np.minimum(np.ceil(pts[:,:2].max(axis=0)).astype(int),(599,479))
            if np.any(lo>hi):continue
            xx,yy=np.meshgrid(np.arange(lo[0],hi[0]+1)+.5,np.arange(lo[1],hi[1]+1)+.5)
            denom=(b[1]-c[1])*(a[0]-c[0])+(c[0]-b[0])*(a[1]-c[1])
            if abs(denom)<1e-9:continue
            u=((b[1]-c[1])*(xx-c[0])+(c[0]-b[0])*(yy-c[1]))/denom
            v=((c[1]-a[1])*(xx-c[0])+(a[0]-c[0])*(yy-c[1]))/denom
            w=1-u-v;zz=u*a[2]+v*b[2]+w*c[2]
            region=depth[lo[1]:hi[1]+1,lo[0]:hi[0]+1]
            mask=(u>=0)&(v>=0)&(w>=0)&(zz>region);region[mask]=zz[mask]
            original=vertices[triangle];normal=np.cross(original[1]-original[0],original[2]-original[0]);normal/=max(np.linalg.norm(normal),1e-12)
            shade=.5+.5*abs(np.dot(normal,np.array([.3,.4,.866])))
            target=pixels[oy+lo[1]:oy+hi[1]+1,ox+lo[0]:ox+hi[0]+1]
            target[mask]=(np.array(colors[name])*shade).astype(np.uint8)
label('GREY SHELL   TAN CRADLE   DARK R3   GREEN PCB   IVORY BEZEL AND FACEPLATE',20,978)
label('N1 FACEPLATE   MEASURED BUTTON X   REPRINT FIT PENDING',20,1005)
def chunk(kind,data):return struct.pack('>I',len(data))+kind+data+struct.pack('>I',zlib.crc32(kind+data)&0xffffffff)
raw=b''.join(b'\0'+row.tobytes() for row in pixels)
(g.ROOT/'RevI1_preview.png').write_bytes(b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>2I5B',width,height,8,2,0,0,0))+chunk(b'IDAT',zlib.compress(raw))+chunk(b'IEND',b''))
