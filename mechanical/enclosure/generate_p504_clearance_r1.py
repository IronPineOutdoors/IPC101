"""Small P504 fit coupon: existing N1.3 rear cradle, 8 mm front aperture."""
import json
import trimesh
import generate_rev_i1 as g
from verify_button_caps_r1 import load
from generate_crosswind_control_box import write_binary_stl

g.previous.FONT.update({'4':('00010','00110','01010','10010','11111','00010','00010'),
                        '5':('11111','10000','10000','11110','00001','00001','11110')})
DIAMETER=8.0

if __name__=='__main__':
    old=load('CrossWind_IPC101_Faceplate_RevN13_WHITE_PETGHF.stl')
    crop=g.cube((30,30,6),(90,48.5,0))
    original=old^crop
    coupon=original-g.cyl(DIAMETER,2.2,(105,63.5,-.1))
    coupon-=g.mark('P504-R1',94,50,1.6)
    rear=g.cube((30,30,4),(90,48.5,2))
    a=coupon^rear;b=original^rear
    assert (a-b).volume()+(b-a).volume()<.001,'Rear cradle changed'
    assert (coupon^g.cyl(7.9,2.1,(105,63.5,-.05))).volume()<.001
    assert coupon.status()==g.m.Error.NoError and len(coupon.decompose())==1
    path=g.ROOT/'CrossWind_IPC101_P504_Clearance_R1_8mm_PRINT.stl'
    write_binary_stl(path,g.h.print_orientation(coupon))
    mesh=trimesh.load_mesh(path)
    assert mesh.is_watertight and mesh.is_winding_consistent and len(mesh.split())==1
    report={'status':'Fit coupon only; directional travel not physically verified',
        'aperture_mm':DIAMETER,'prior_aperture_mm':6.2,'size_mm':mesh.extents.tolist(),
        'rear_cradle':'Exact N1.3 geometry retained','watertight':True,
        'purpose':'Distinguish cap/hub aperture interference from rear mounting or switch restriction'}
    (g.ROOT/'P504_clearance_R1_verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
