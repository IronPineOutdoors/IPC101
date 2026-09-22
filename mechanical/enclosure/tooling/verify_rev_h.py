"""Geometric fit checks and an orthographic preview for the Rev H prototype."""
from enclosure_paths import asset
import sys
from pathlib import Path
import numpy as np
import generate_rev_h as g
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'panel'))
from generate_ipc101_rev_c import build_faceplate, MOUNT_CENTRES

parts=g.models()
plate=g.face(build_faceplate().scale((1,1,-1)))
assert tuple(MOUNT_CENTRES)==g.HOLES
assert (plate ^ parts['Box']).volume()<1e-5, 'Faceplate collides with enclosure'
for lift in np.linspace(0,70,71):
    assert (parts['Box'].translate((0,0,float(lift))) ^ parts['Bracket']).volume()<1e-5, f'Rail interference at {lift}'
# Full annular support at every screw seat, immediately inside the datum.
for x,y in g.HOLES:
    witness=g.face(g.cyl(8,.1,(x,y,0))-g.cyl(4.4,.3,(x,y,-.1)))
    assert abs((witness ^ parts['Box']).volume()-witness.volume())<1e-5, 'Unsupported screw seat'
for name,solid in parts.items():
    assert len(solid.decompose())==1
    mesh=solid.to_mesh()
    edges=np.concatenate([mesh.tri_verts[:,[0,1]],mesh.tri_verts[:,[1,2]],mesh.tri_verts[:,[2,0]]])
    _,counts=np.unique(np.sort(edges,axis=1),axis=0,return_counts=True)
    assert np.all(counts==2), f'Nonclosed mesh: {name}'


# Dependency-free orthographic raster preview: front, rear, fitted side.
import struct, zlib
width,height=1500,600
pixels=np.full((height,width,3),244,dtype=np.uint8)
for index,(eye,fitted) in enumerate([((1,2,1.4),False),((-1,-2,1.2),False),((1,0,0),True)]):
    forward=np.array(eye,dtype=float); forward/=np.linalg.norm(forward)
    right=np.cross((0,0,1),forward); right/=np.linalg.norm(right)
    up=np.cross(forward,right)
    rotation=np.array([right,up,forward]).T
    depth=np.full((height,500),-np.inf)
    for name,solid in [*parts.items(),*([('Faceplate',plate)] if fitted else [])]:
        mesh=solid.to_mesh(); vertices=mesh.vert_properties[:,:3]
        projected=(vertices-np.array([78,45,52]))@rotation
        projected[:,:2]*=2.5; projected[:,0]+=250; projected[:,1]=300-projected[:,1]
        color=np.array({'Box':(82,127,152),'Bracket':(232,165,76),'Wiring_Plate':(132,170,131),'Faceplate':(216,226,232)}[name])
        for triangle in mesh.tri_verts:
            pts=projected[triangle]; a,b,c=pts
            lo=np.maximum(np.floor(pts[:,:2].min(axis=0)).astype(int),(0,0))
            hi=np.minimum(np.ceil(pts[:,:2].max(axis=0)).astype(int),(499,599))
            if np.any(lo>hi): continue
            xx,yy=np.meshgrid(np.arange(lo[0],hi[0]+1)+.5,np.arange(lo[1],hi[1]+1)+.5)
            denom=(b[1]-c[1])*(a[0]-c[0])+(c[0]-b[0])*(a[1]-c[1])
            if abs(denom)<1e-9: continue
            u=((b[1]-c[1])*(xx-c[0])+(c[0]-b[0])*(yy-c[1]))/denom
            v=((c[1]-a[1])*(xx-c[0])+(a[0]-c[0])*(yy-c[1]))/denom
            w=1-u-v; zz=u*a[2]+v*b[2]+w*c[2]
            region=depth[lo[1]:hi[1]+1,lo[0]:hi[0]+1]
            mask=(u>=0)&(v>=0)&(w>=0)&(zz>region)
            region[mask]=zz[mask]
            original=vertices[triangle]; normal=np.cross(original[1]-original[0],original[2]-original[0])
            normal/=max(np.linalg.norm(normal),1e-12)
            shade=.45+.55*abs(np.dot(normal,np.array([.3,.4,.866])))
            target=pixels[lo[1]:hi[1]+1,index*500+lo[0]:index*500+hi[0]+1]
            target[mask]=(color*shade).astype(np.uint8)
def chunk(kind,data):
    return struct.pack('>I',len(data))+kind+data+struct.pack('>I',zlib.crc32(kind+data)&0xffffffff)
raw=b''.join(b'\0'+row.tobytes() for row in pixels)
asset(Path(__file__).resolve().parent.parent, 'RevH_preview.png').write_bytes(b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>2I5B',width,height,8,2,0,0,0))+chunk(b'IDAT',zlib.compress(raw))+chunk(b'IEND',b''))
print('PASS: faceplate clearance, four seating annuli, 71 slide positions, closed connected meshes.')
