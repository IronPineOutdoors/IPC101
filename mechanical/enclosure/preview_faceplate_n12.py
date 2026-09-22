"""Use the actual N1.2 exports for the close-up and assembly preview."""
from pathlib import Path
import verify_faceplate_n12 as n12
source=Path(__file__).with_name('preview_faceplate_n1.py').read_text()
# The nested renderer's initial assembly is N1; replace only its faceplate solids.
source=source.replace('exec(header)', '''exec(header)
g.FONT['2']=('01110','10001','00001','00010','00100','01000','11111')
material_local=n12.material_local
assembly=[(n,s) for n,s in assembly if n not in ('Faceplate','Inlay')]+[
 ('Faceplate',g.face(material_local('WHITE_PETGHF'))),('Inlay',g.face(material_local('BLACK_AMS')))]''')
source=source.replace('N1 OPERATOR VIEW','N1.2 OPERATOR VIEW').replace('TREE AND OUTDOORS SEPARATED','TREE TRACED FROM YOUR WORDMARK').replace('ARM LEFT   PULL RIGHT','MEASURED BUTTON OPENINGS').replace('N1 ON I1 ASSEMBLY','N1.2 ON I1 ASSEMBLY')
source=source.replace('N1   ARM X46.88','N1.2 ARM X46.88')
source=source.replace('N1_faceplate_preview.png','N12_faceplate_preview.png')
exec(source)
