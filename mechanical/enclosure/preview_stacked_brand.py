"""Vector layout study on N1.4 dimensions; does not replace production STLs."""
from pathlib import Path
import re
import pymupdf as fitz
ROOT=Path(__file__).resolve().parent
out=ROOT/'branding'/'stacked_brand_concept'
out.mkdir(exist_ok=True)
tree=re.search(r'<path.*?/>',(ROOT/'branding'/'iron_pine_tree_trace.svg').read_text()).group()
# Trace bounds 645..886,288..511. Preserve exact supplied tree silhouette.
scale=18/223
art=f'<g transform="translate(14 3) scale({scale}) translate(-768 -288)">{tree}</g>'
for word,x,y in [('Iron',18,7.3),('Pine',20.4,13.1),('Outdoors',24.6,19.0)]:
    art+=f'<text x="{x}" y="{y}" font-family="Arial" font-weight="bold" font-size="4">{word}</text>'
base='<rect width="150" height="100" rx="0.4" fill="#e8e1d1" stroke="#aca799" stroke-width="0.25"/>'
for x,y,d in [(5,5,3.2),(145,5,3.2),(5,95,3.2),(145,95,3.2),(45,36.5,8),(68.5,69,5.2)]+[(103.5+dx,36.5+dy,3.2) for dx in (-34.4,34.4) for dy in (-19.4,19.4)]:
    base+=f'<circle cx="{x}" cy="{y}" r="{d/2}" fill="#f6f6f6"/>'
base+='<rect x="75" y="22.5" width="57" height="28" fill="#f6f6f6"/>'
base+='<g fill="none" stroke="#28282a" stroke-width="0.9" stroke-linecap="round"><polyline points="86,7 99,4.7 124,3.5 139,7"/><polyline points="89,17.5 104,19.3 126,19.7 138,17"/></g>'
base+='<text x="112" y="13.6" text-anchor="middle" font-family="Arial" font-size="4.3" font-weight="bold">CROSSWIND</text>'
for word,x in [('ARM',46.88),('PULL',115.67)]:
    base+=f'<rect x="{x-7.6}" y="74.25" width="15.2" height="10" rx="2" fill="#e8e1d1" stroke="#b9b2a4" stroke-width="0.25"/><text x="{x}" y="80.4" text-anchor="middle" font-family="Arial" font-size="3.2" font-weight="bold">{word}</text>'
for name,view,w,h in [('faceplate','-3 -3 156 106',1560,1060),('logo_detail','0 0 52 25',1560,750)]:
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="{view}"><rect x="-3" y="-3" width="156" height="106" fill="#f6f6f6"/><g fill="#28282a">{base}{art}</g></svg>'
    (out/f'{name}.svg').write_text(svg)
    doc=fitz.open(stream=svg.encode(),filetype='svg')
    doc[0].get_pixmap(alpha=False).save(str(out/f'{name}.png'))
print(out)
