"""Verify N1.2 faithfully uses the traced tree while preserving N1.1 mechanics."""
from enclosure_paths import asset
import json,re
import numpy as np
import generate_rev_i1 as g
from verify_button_caps_r1 import load

def material_local(material):
    return load(f'CrossWind_IPC101_Faceplate_RevN12_{material}.stl').translate((0,0,-2))

def plate_local():return material_local('WHITE_PETGHF')+material_local('BLACK_AMS')

def run():
    white=material_local('WHITE_PETGHF');black=material_local('BLACK_AMS')
    assert len(white.decompose())==1
    assert (white^black).volume()<.001
    oldwhite=load('CrossWind_IPC101_Faceplate_RevN11_WHITE_PETGHF.stl').translate((0,0,-2))
    oldblack=load('CrossWind_IPC101_Faceplate_RevN11_BLACK_AMS.stl').translate((0,0,-2))
    mark_zone=g.cube((70,8,4),(40,9,-2))
    a=white+black-mark_zone;b=oldwhite+oldblack-mark_zone
    structural_delta=(a-b).volume()+(b-a).volume()
    assert structural_delta<.01,('Changed mechanical geometry',structural_delta)
    tree_zone=g.cube((16,14,1),(108,83,-2.1))
    actual=black^tree_zone
    assert len(actual.decompose())==2,'Preserve original main tree and center triangle'
    scad=(asset(g.ROOT, 'branding/iron_pine_tree_trace.scad')).read_text()
    polys=[]
    for line in scad.splitlines():
        if line.startswith('polygon('):
            points=json.loads(re.search(r'points=(.*),paths=',line).group(1))
            paths=json.loads(re.search(r'paths=(.*)\);',line).group(1))
            contours=[np.array([points[i] for i in path]) for path in paths]
            polys.append(g.m.CrossSection(contours).extrude(.55))
    expected=g.m.Manifold.batch_boolean(polys,g.m.OpType.Add).scale((-13.26,13.26,1)).translate((116,83.54,-2))
    trace_delta=(expected-actual).volume()+(actual-expected).volume()
    assert trace_delta<.01,('Export differs from traced source',trace_delta)
    a=black-tree_zone;b=oldblack-tree_zone
    other_art_delta=(a-b).volume()+(b-a).volume()
    assert other_art_delta<.01,'Unrequested artwork change'
    letters=black^g.cube((20,3,1),(106,80,-2.1))
    gap=actual.bounding_box()[1]-letters.bounding_box()[4]
    assert gap>.9,'Tree/OUTDOORS overlap'
    report={'revision':'N1.2','status':'CAD verified; physical print pending',
        'tree_source':'branding/iron_pine_transparent_wordmark.png',
        'trace':json.loads((asset(g.ROOT, 'branding/tree_trace_verification.json')).read_text()),
        'white_components':len(white.decompose()),'black_components':len(black.decompose()),
        'tree_components':2,'tree_OUTDOORS_gap_mm':gap,
        'mechanical_change_outside_rear_mark_mm3':structural_delta,
        'export_to_vector_trace_difference_mm3':trace_delta,
        'other_front_artwork_change_mm3':other_art_delta,
        'preserved':'Button centers, apertures, panel thickness, rear P504 cradle, mount holes, R1 cap fit; no panel ARM/PULL text'}
    (asset(g.ROOT, 'N12_faceplate_verification.json')).write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':run()
