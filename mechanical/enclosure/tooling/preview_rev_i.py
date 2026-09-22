"""Engineering orthographic raster views; neutral part colors; no render dependencies."""
from enclosure_paths import asset
import numpy as np
import struct,zlib
import generate_rev_i as g
parts=g.models()
box=parts['Box']; carrier=parts['Carrier']; pcb=g.face(g.pcb_local()); plate=g.face(g.plate_local()); bracket=g.h.build_bracket()
g.FONT.update({'B':('11110','10001','10001','11110','10001','10001','11110'),'G':('01111','10000','10000','10111','10001','10001','01111'),'H':('10001','10001','10001','11111','10001','10001','10001'),'V':('10001','10001','10001','10001','10001','01010','00100'),'X':('10001','10001','01010','00100','01010','10001','10001'),'F':('11111','10000','10000','11110','10000','10000','10000'),'Y':('10001','10001','01010','00100','00100','00100','00100')})
g.FONT.update({'1':('00100','01100','00100','00100','00100','00100','01110'),'6':('01110','10000','10000','11110','10001','10001','01110'),'5':('11111','10000','10000','11110','00001','00001','11110'),'.':('00000','00000','00000','00000','00000','00100','00100')})
colors={'Box':(150,160,168),'Carrier':(170,151,119),'PCB':(106,137,125),'Faceplate':(222,220,207),'Bracket':(103,111,124),'Wiring':(187,188,182)}
assembly=[('Box',box),('Carrier',carrier),('PCB',pcb),('Faceplate',plate),('Bracket',bracket),('Wiring',g.h.build_port_plate())]
cut=g.cube((120,260,200),(78,-40,-20))
views=[('OPEN SHELL', (1,2,1.6),[('Box',box)]),
       ('REAR WITH REV H BRACKET',(-1,-2,1),assembly),
       ('SIDE ASSEMBLY',(1,0,0),assembly),
       ('CARRIER AND PCB',(1,2,1.6),[('Carrier',carrier),('PCB',pcb)]),
       ('EXPLODED STACK',(1.4,2,1.5),[('Box',box),('Bracket',bracket.translate((0,-25,0))),('Carrier',g.face(g.carrier_local().translate((0,0,-40)))),('PCB',g.face(g.pcb_local().translate((0,0,-65)))),('Faceplate',g.face(g.plate_local().translate((0,0,-90))))]),
       ('SECTION   PCB TOP GAP 16.5 MM',(1,0,0),[(n,s-cut) for n,s in assembly])]
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
label('GREY SHELL AND BRACKET   TAN CARRIER   GREEN PCB   IVORY FACEPLATE REFERENCE',20,978)
label('TEST FIT   PHYSICAL VALIDATION PENDING   FACEPLATE DETAIL NOT AVAILABLE',20,1005)
def chunk(kind,data):return struct.pack('>I',len(data))+kind+data+struct.pack('>I',zlib.crc32(kind+data)&0xffffffff)
raw=b''.join(b'\0'+row.tobytes() for row in pixels)
(asset(g.ROOT, 'RevI_preview.png')).write_bytes(b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>2I5B',width,height,8,2,0,0,0))+chunk(b'IDAT',zlib.compress(raw))+chunk(b'IEND',b''))
