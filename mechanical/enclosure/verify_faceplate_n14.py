"""Verify enlarged P504 aperture against the previous complete faceplate."""
import json,math
import generate_rev_i1 as g
from verify_button_caps_r1 import load,installed

def material_local(material):
    return load(f'CrossWind_IPC101_Faceplate_RevN14_{material}.stl').translate((0,0,-2))

def plate_local():return material_local('WHITE_PETGHF')+material_local('BLACK_AMS')

def run():
    w=material_local('WHITE_PETGHF');b=material_local('BLACK_AMS');p=w+b
    ow=load('CrossWind_IPC101_Faceplate_RevN13_WHITE_PETGHF.stl').translate((0,0,-2))
    ob=load('CrossWind_IPC101_Faceplate_RevN13_BLACK_AMS.stl').translate((0,0,-2))
    assert len(w.decompose())==1 and (w^b).volume()<.001
    mark=g.cube((70,8,4),(40,9,-2))
    aperture=g.cyl(8,3,(105,63.5,-2.5))
    expected=ow+ob-aperture-mark;actual=p-mark
    delta=(actual-expected).volume()+(expected-actual).volume()
    assert delta<.01,('Unexpected change outside hole/revision',delta)
    assert (p^g.cyl(7.9,2.1,(105,63.5,-2.05))).volume()<.001
    assert (b-ob).volume()+(ob-b).volume()<.01,'Artwork changed'
    rear=g.cube((150,100,4),(0,0,0))
    a=w^rear;c=ow^rear
    assert (a-c).volume()+(c-a).volume()<.001,'Rear cradle changed'
    for angle in range(0,360,45):
        # Earlier reference cap has a 5 mm hub. Clearance envelope only.
        dx=1.4*math.cos(math.radians(angle));dy=1.4*math.sin(math.radians(angle))
        assert (p^g.cyl(5,2.2,(105+dx,63.5+dy,-2.1))).volume()<.001
    for label in ('ARM','PULL'):
        for i in range(21):assert (installed(label,travel=.05*i)^p).volume()<.001
    report={'revision':'N1.4','status':'CAD verified; actual P504 directional test pending',
        'P504_aperture_mm':8.0,'prior_aperture_mm':6.2,'added_radial_clearance_mm':.9,
        'only_allowed_change_difference_mm3':delta,'white_components':len(w.decompose()),
        'black_components':len(b.decompose()),'rear_cradle_unchanged':True,'artwork_unchanged':True,
        'reference_hub_mm':5,'reference_hub_radial_offset_checked_mm':1.4,
        'reference_hub_direction_checks':8,'ARM_PULL_motion_checks':42,
        'limitation':'Reference hub sweep is not a measurement of the installed cap or proof of physical switch travel'}
    (g.ROOT/'N14_faceplate_verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':run()
