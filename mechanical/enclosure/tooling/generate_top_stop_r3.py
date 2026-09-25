"""R3 adds opposed underside access for the push-up contact-block release."""
import json
import numpy as np
import trimesh
import generate_top_stop_r2 as r2
from generate_crosswind_control_box import write_binary_stl
g,r1=r2.g,r2.r1
OUT,X,Y,LAND=r2.OUT,r2.X,r2.Y,r2.LAND

def relief():
    # Two opposed X-side approaches, perpendicular to the +Y panel key.
    # The central overlap is already empty; leave 2 mm below the mounting land.
    return g.cube((66,14,71.5),(X-33,Y-7,65))

def roof():return r2.roof()-relief()

def coupon():
    # Standalone service pocket; no inherited roof skirts, tie tab or ledges.
    p=g.cyl(47,32,(X,Y,109))
    p-=g.cyl(41,LAND-65,(X,Y,65))
    p-=g.cyl(16.3,5,(X,Y,137.5))+g.cube((1.8,3,5),(X-.9,Y+6.85,137.5))
    return p-relief()

def verify():
    # Reuse all R2 insertion, mounting and service checks on the R3 roof.
    original=r2.roof
    try:
        r2.roof=roof_for_checks
        report=r2.verify()
    finally:r2.roof=original
    p=roof_for_checks();c=coupon()
    assert (p^relief()).volume()<.001
    assert (c^relief()).volume()<.001
    assert len(p.decompose())==len(c.decompose())==1
    assert (p-r2_original()).volume()<.001,'R3 must only remove material'
    # Every higher layer of the print-oriented coupon is supported by the layer below.
    # Check downward-closed XY sections at 0.2 mm intervals using manifold cross sections.
    printed=r1.print_part('Roof',c)
    previous=printed.slice(.1)
    for z in np.arange(.3,32,.2):
        current=printed.slice(float(z))
        assert (current-previous).area()<.001,('unsupported coupon section',float(z))
        previous=current
    report.update(revision='TOP-STOP-R3',status='R2 insertion fit physically confirmed; R3 release access awaiting test',release_slot_width_mm=14,release_slot_top_z_mm=136.5,remaining_material_above_slot_mm=4.5,coupon_support='No expanding XY sections at 0.2 mm layers in exported orientation',limitations=['Actual latch stroke and finger/tool envelope are not dimensioned; physical release test required','Coupon reproduces central pocket and release slots, not surrounding roof or wire tab','Full roof support and weather sealing remain unqualified'])
    return report

# Keep an immutable reference because the reused R2 checker calls its module roof().
r2_original=r2.roof
def roof_for_checks():return r2_original()-relief()

def run():
    report=verify()
    for name,p in [('Roof',roof()),('Release_Coupon',coupon())]:
        for orientation,s in [('INSTALLED',p),('PRINT',r1.print_part('Roof',p))]:
            path=OUT/f'CrossWind_IPC101_Top_STOP_{name}_R3_{orientation}.stl'
            write_binary_stl(path,s)
            mesh=trimesh.load_mesh(path)
            assert mesh.is_watertight and mesh.is_winding_consistent and len(mesh.split())==1,path.name
            assert np.all(mesh.extents<256)
    (OUT/'TOP_STOP_R3_verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='clearance_checks_mm3'},indent=2))
if __name__=='__main__':run()
