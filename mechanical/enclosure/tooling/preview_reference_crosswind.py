"""Trace supplied CrossWind alpha silhouette and render a panel visual study."""
from enclosure_paths import asset
from pathlib import Path
import hashlib,json,re,shutil
import numpy as np
import pymupdf as fitz
from scipy import ndimage
from shapely.geometry import box,Polygon,MultiPolygon
from shapely.ops import unary_union
ROOT=Path(__file__).resolve().parent.parent
out=asset(ROOT, 'branding')/'reference_crosswind_concept'
out.mkdir(exist_ok=True)
source=out/'crosswind_transparent_logo.png'
if not source.exists():
    shutil.copy2(Path('C:/Users/DAVID/OneDrive/Documents/Projects/IronPine/Crosswind/branding/crosswind/crosswind_transparent_logo.png'),source)
pix=fitz.Pixmap(str(source))
a=np.frombuffer(pix.samples,dtype=np.uint8).reshape(pix.height,pix.width,pix.n)
assert pix.alpha
labels,n=ndimage.label(a[:,:,-1]>180)
counts=np.bincount(labels.ravel()); chosen=np.flatnonzero(counts>=100); chosen=chosen[chosen!=0]
mask=np.isin(labels,chosen)
rects=[]
for y,row in enumerate(mask):
    edges=np.diff(np.r_[False,row,False].astype(int))
    rects.extend(box(s,y,e,y+1) for s,e in zip(np.flatnonzero(edges==1),np.flatnonzero(edges==-1)))
original=unary_union(rects)
clean=MultiPolygon([Polygon(poly.exterior,[r for r in poly.interiors if Polygon(r).area>4]) for poly in original.geoms])
trace=clean.simplify(.7,preserve_topology=True)
paths=[]
for poly in trace.geoms:
    for ring in [poly.exterior,*poly.interiors]:
        paths.append('M '+' L '.join(f'{x:.3f},{y:.3f}' for x,y in list(ring.coords)[:-1])+' Z')
x0,y0,x1,y1=original.bounds
path='<path fill="#28282a" fill-rule="evenodd" d="'+' '.join(paths)+'"/>'
(out/'crosswind_trace.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0} {y0} {x1-x0} {y1-y0}">{path}</svg>')
# Reuse the preferred tree layout and exact panel cutout coordinates.
base=(asset(ROOT, 'branding')/'stacked_brand_wind_concept'/'faceplate.svg').read_text()
base=re.sub(r'<g fill="none" stroke="#28282a".*?</g>','',base)
base=re.sub(r'<text x="112".*?</text>','',base)
scale=58/(x1-x0)
logo=f'<g transform="translate(78 3) scale({scale}) translate({-x0} {-y0})">{path}</g>'
base=base.replace('</svg>',logo+'</svg>')
for name,view,w,h in [('faceplate','-3 -3 156 106',1560,1060),('crosswind_detail','74 0 66 21',1584,504)]:
    svg=re.sub(r'<svg[^>]*>',f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="{view}">',base,count=1)
    (out/f'{name}.svg').write_text(svg)
    fitz.open(stream=svg.encode(),filetype='svg')[0].get_pixmap(alpha=False).save(str(out/f'{name}.png'))
iou=original.intersection(trace).area/original.union(trace).area
assert iou>.98
report={'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'alpha_threshold':180,'minimum_component_pixels':100,'components':len(chosen),'source_bounds':list(original.bounds),'silhouette_iou':iou,'width_mm':58,'height_mm':(y1-y0)*scale,'position_from_top_left_mm':[78,3],'status':'visual concept; print detail and production CAD pending'}
(out/'trace_report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
