"""Check compact IPO badge and preserve the N1.2 mechanical interface."""
import json
import generate_rev_i1 as g
from verify_button_caps_r1 import load,installed

def material_local(material):
    return load(f'CrossWind_IPC101_Faceplate_RevN13_{material}.stl').translate((0,0,-2))

def plate_local():return material_local('WHITE_PETGHF')+material_local('BLACK_AMS')

def run():
    w=material_local('WHITE_PETGHF');b=material_local('BLACK_AMS')
    assert len(w.decompose())==1 and (w^b).volume()<.001
    ow=load('CrossWind_IPC101_Faceplate_RevN12_WHITE_PETGHF.stl').translate((0,0,-2))
    ob=load('CrossWind_IPC101_Faceplate_RevN12_BLACK_AMS.stl').translate((0,0,-2))
    mark=g.cube((70,8,4),(40,9,-2))
    new=w+b-mark;old=ow+ob-mark
    delta=(new-old).volume()+(old-new).volume()
    assert delta<.01,('Mechanical change',delta)
    brand=g.cube((65,21,1),(86,78,-2.1))
    other=(b-brand);oldother=(ob-brand)
    assert (other-oldother).volume()+(oldother-other).volume()<.01,'CrossWind artwork changed'
    tree=b^g.cube((16,13,1),(108,84,-2.1))
    expected=load('branding/iron_pine_tree_unit.stl').scale((-12.5,12.5,1)).translate((116,84.3,-2))
    assert (tree-expected).volume()+(expected-tree).volume()<.01
    assert len(tree.decompose())==2
    ipo=b^g.cube((16,5,1),(108,79,-2.1))
    assert len(ipo.decompose())==3,'IPO must contain three separate glyphs'
    gap=tree.bounding_box()[1]-ipo.bounding_box()[4]
    assert gap>.9
    badge=b^brand;bounds=badge.bounding_box()
    motion_checks=0
    for label in ('ARM','PULL'):
        for step in range(21):
            assert (installed(label,travel=step*.05)^(w+b)).volume()<.001
            motion_checks+=1
    report={'revision':'N1.3','status':'CAD verified compact branding option; print legibility pending',
        'badge_width_mm':bounds[3]-bounds[0],'badge_height_mm':bounds[4]-bounds[1],
        'tree_height_mm':12.5,'IPO_font_size_mm':3.2,
        'IPO_glyph_height_mm':ipo.bounding_box()[4]-ipo.bounding_box()[1],
        'tree_to_IPO_gap_mm':gap,'white_components':len(w.decompose()),'black_components':len(b.decompose()),
        'mechanical_change_outside_revision_mark_mm3':delta,'cap_motion_checks':motion_checks,
        'preserved':'Actual traced tree, CrossWind artwork, all N1.2 mechanical interfaces and R1 caps'}
    (g.ROOT/'N13_faceplate_verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':run()
