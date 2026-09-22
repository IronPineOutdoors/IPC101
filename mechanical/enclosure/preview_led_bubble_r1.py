from pathlib import Path
from generate_led_bubble_r1 import bubble,coupon
source=Path(__file__).with_name('preview_rev_i1.py').read_text()
header,body=source.split('for index,(title,eye,solids) in enumerate(views):',1)
exec(header)
height=480
pixels=np.full((height,width,3),246,dtype=np.uint8)
lens=bubble(5.5,2)
section=lens-g.cube((20,30,20),(0,-15,-1))
views=[('LED BUBBLE R1 SAMPLE',(1,-2,1.5),[('Faceplate',lens)]),('HOLLOW LED POCKET SECTION',(1,-2,1),[('Faceplate',section)]),('PANEL HOLE FIT STRIP',(0,-1,3),[('Faceplate',coupon())])]
body='for index,(title,eye,solids) in enumerate(views):'+body
body='\n'.join(line for line in body.splitlines() if not line.startswith("label('"))
body=body.replace('RevI1_preview.png','LED_R1_preview.png')
exec(body)
