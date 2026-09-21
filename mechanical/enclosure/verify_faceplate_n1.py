"""Verify N1 manufacturing geometry, preserved interfaces and artwork."""
import json
import numpy as np
import trimesh
import generate_rev_i1 as g
import faceplate_rev_m4_reference as old
import faceplate_rev_n1_reference as new

def run():
    white=new.material_local('WHITE_PETGHF'); black=new.material_local('BLACK_AMS')
    combined=white+black
    checks={}
    def clear(name,a,b):
        v=(a^b).volume();checks[name]=round(v,7);assert v<.001,(name,v)
    clear('white and black have no volume overlap',white,black)
    exports={}
    for material,p in [('WHITE_PETGHF',white),('BLACK_AMS',black)]:
        mesh=trimesh.load_mesh(g.ROOT/f'CrossWind_IPC101_Faceplate_RevN1_{material}.stl')
        assert mesh.is_watertight and mesh.is_winding_consistent,material
        assert len(mesh.split())==1 if material=='WHITE_PETGHF' else len(mesh.split())>1
        exports[material]={'bounds_mm':mesh.bounds.tolist(),'watertight':True,'components':len(mesh.split())}
    for name in ('ARM','PULL'):
        x,y=new.CENTRES[name]
        aperture=g.m.Manifold.batch_hull([g.cyl(4,4,(x+dx,y+dy,-3)) for dx in (-6,6) for dy in (-3.4,3.4)])
        clear(name+' full rounded opening',combined,aperture)
    # Outside changed button regions and hidden revision mark, keep M4's body.
    changed=g.cube((150,13,5),(0,14,-3))+g.cube((90,5,5),(30,11,-3))
    before=old.plate_local()-changed;after=combined-changed
    difference=(before-after).volume()+(after-before).volume()
    assert difference<.05,('Unplanned body/interface change',difference)
    checks['body difference outside edited regions_mm3']=round(difference,7)
    tree_region=g.cube((12,14,1),(110,83.2,-2.1))
    tree=black^tree_region
    assert len(tree.decompose())==1 and tree.volume()>1,'Tree must be connected'
    assert abs(tree.bounding_box()[1]-83.54)<.01,'Flat trunk bottom'
    lettering=black^g.cube((20,3,1),(106,80,-2.1))
    gap=tree.bounding_box()[1]-lettering.bounding_box()[4]
    assert gap>.9,('Tree touches OUTDOORS',gap)
    checks['tree_to_OUTDOORS_gap_mm']=round(gap,4)
    # True old/new equality of rear protrusions (revision engraving is inward).
    rear=g.cube((150,100,4),(0,0,0))
    a=white^rear;b=old.material_local('WHITE_PETGHF')^rear
    assert (a-b).volume()+(b-a).volume()<.01,'Rear P504 cradle changed'
    report={'revision':'N1','status':'CAD passed; reprint physical alignment pending',
            'controls':new.control_registration(),'exports':exports,'checks':checks,
            'physical_notes':['ARM left, PULL right confirmed by user','Y=20.75 retained, not remeasured','Measured spacing68.79 differs from PCB-file nominal70; verify without preload','OLED/D-pad PCB locations reported swapped; wired faceplate locations retained']}
    (g.ROOT/'N1_faceplate_verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':run()
