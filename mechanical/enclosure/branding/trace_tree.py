"""Trace the supplied transparent wordmark into CAD polygons; no redrawing.

Uses the alpha silhouette, not the shaded RGB channels. The fixed crop excludes
OUTDOORS. Seed pixels select only the main tree and its detached center triangle,
excluding neighboring IRON/PINE glyphs. Units in generated SCAD: tree height=1.
"""
from pathlib import Path
import hashlib,json,sys
import manifold3d as m
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from generate_crosswind_control_box import write_binary_stl
import numpy as np
import pymupdf
from scipy import ndimage
from shapely.geometry import box,Polygon,MultiPolygon
from shapely.ops import unary_union

ROOT=Path(__file__).resolve().parent
source=ROOT/'iron_pine_transparent_wordmark.png'
pix=pymupdf.Pixmap(str(source))
assert pix.alpha and pix.width==1536 and pix.height==1024
rgba=np.frombuffer(pix.samples,dtype=np.uint8).reshape(pix.height,pix.width,pix.n)
x0,y0,x1,y1=630,280,906,516
mask=rgba[y0:y1,x0:x1,-1]>180
labels,_=ndimage.label(mask)
chosen={int(labels[y-y0,x-x0]) for x,y in [(768,300),(768,490)]}
assert 0 not in chosen and len(chosen)==2
selected=np.isin(labels,list(chosen))
rects=[]
for y,row in enumerate(selected):
    edges=np.diff(np.r_[False,row,False].astype(int))
    for start,end in zip(np.flatnonzero(edges==1),np.flatnonzero(edges==-1)):
        rects.append(box(x0+start,y0+y,x0+end,y0+y+1))
original=unary_union(rects)
cleaned=MultiPolygon([Polygon(poly.exterior,[ring for ring in poly.interiors if Polygon(ring).area>4]) for poly in original.geoms])
trace=cleaned.simplify(.7,preserve_topology=True)
assert trace.is_valid and len(trace.geoms)==2
assert original.intersection(trace).area/original.union(trace).area>.985
minx,miny,maxx,maxy=original.bounds
height=maxy-miny;cx=(minx+maxx)/2
polygons=sorted(trace.geoms,key=lambda p:p.area,reverse=True)
lines=['// Generated from the alpha silhouette of the user-provided wordmark.',
       '// Unit height, centered X, bottom Y=0. Two original black components.',
       'module iron_pine_tree_2d(){ union(){']
svg_paths=[]
solids=[]
for poly in polygons:
    rings=[poly.exterior,*poly.interiors];points=[];paths=[]
    for ring in rings:
        path=[]
        coords=list(ring.coords)[:-1]
        svg_paths.append('M '+' L '.join(f'{x:.3f},{y:.3f}' for x,y in coords)+' Z')
        for x,y in coords:
            path.append(len(points));points.append([(x-cx)/height,(maxy-y)/height])
        paths.append(path)
    solids.append(m.CrossSection([np.array([points[i] for i in path]) for path in paths]).extrude(.55))
    lines.append('polygon(points='+json.dumps([[round(x,7),round(y,7)] for x,y in points])+',paths='+json.dumps(paths)+');')
lines.append('}}')
solid=m.Manifold.batch_boolean(solids,m.OpType.Add)
assert solid.status()==m.Error.NoError and len(solid.decompose())==2
write_binary_stl(ROOT/'iron_pine_tree_unit.stl',solid)
(ROOT/'iron_pine_tree_trace.scad').write_text('\n'.join(lines)+'\n')
(ROOT/'iron_pine_tree_trace.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{minx-5} {miny-5} {maxx-minx+10} {height+10}"><path fill="black" fill-rule="evenodd" d="'+ ' '.join(svg_paths)+'"/></svg>\n')
report={'source':source.name,'sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
        'alpha_threshold':180,'crop_xyxy':[x0,y0,x1,y1],'seed_pixels_xy':[[768,300],[768,490]],
        'original_pixel_bounds':list(original.bounds),'selected_components':2,
        'simplification_tolerance_pixels':.7,'removed_raster_pinholes_max_area_pixels':4,'hausdorff_error_pixels':original.hausdorff_distance(trace),
        'silhouette_iou':original.intersection(trace).area/original.union(trace).area,
        'faceplate_tree_height_mm':13.26,'faceplate_tree_width_mm':(maxx-minx)/height*13.26,
        'maximum_trace_error_mm':original.hausdorff_distance(trace)/height*13.26}
assert report['silhouette_iou']>.985
(ROOT/'tree_trace_verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
