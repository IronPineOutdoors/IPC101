"""Rev H fit prototype; installed X across, Y outward, Z up, millimetres."""
from enclosure_paths import asset
from pathlib import Path
import math
import manifold3d as m
from generate_crosswind_control_box import write_binary_stl

W, H = 150., 100.
ANGLE = 47.
BOTTOM_Z = 32.
TOP_Y = 32.
S, C = math.sin(math.radians(ANGLE)), math.cos(math.radians(ANGLE))
BOTTOM_Y = TOP_Y + H*S
HOLES = ((5,5),(145,5),(5,95),(145,95))

def cube(size, pos):
    return m.Manifold.cube(size).translate(pos)

def face(solid):
    # Local +Z is inward; local Z=0 is the common plate/boss seating plane.
    return solid.rotate((90+ANGLE,0,0)).translate((3,BOTTOM_Y,BOTTOM_Z))

def cyl(d,h,pos):
    return m.Manifold.cylinder(h,d/2,circular_segments=64).translate(pos)

def ring(x,y,w,h,b,depth,z=0):
    return cube((w,h,depth),(x,y,z))-cube((w-2*b,h-2*b,depth+2),(x+b,y+b,z-1))

def prism(profile, xs=(0,156)):
    return m.Manifold.hull_points([(x,y,z) for x in xs for y,z in profile])

def pin_hole():
    return m.Manifold.cylinder(30,1.7,circular_segments=48).rotate((0,90,0)).translate((10,-7,40))

def build_box():
    top_z=BOTTOM_Z+H*C
    outer=prism([(0,0),(BOTTOM_Y,0),(BOTTOM_Y,BOTTOM_Z),(TOP_Y,top_z),(0,top_z+4)])
    # Exact planar face rim extends beyond all four edges of the existing plate.
    outer += face(cube((156,106,5),(-3,-3,0)))
    # Clip the cavity to retain a continuous 3 mm back and floor.
    interior=prism([(3,3),(BOTTOM_Y-3,3),(BOTTOM_Y-3,BOTTOM_Z-6),
                    (TOP_Y-1,top_z-6),(3,top_z)], (3,153))
    interior=interior ^ face(cube((180,250,180),(-15,-75,5)))
    opening=face(cube((128,78,24),(11,11,-2)))
    box=outer-interior-opening
    for x,y in HOLES:
        box+=face(cyl(11,10,(x,y,0)))
    # Cut all front material flush to the exact shared datum, including top rim.
    box-=face(cube((180,140,60),(-15,-20,-60)))
    # Gasket inside the fasteners: 2 mm wide x 0.8 mm deep continuous groove.
    box-=face(ring(8,8,134,84,2,.8))
    for x,y in HOLES:
        box-=face(cyl(4.2,6.1,(x,y,-.1)))
        box-=face(cyl(3.2,8,(x,y,5.9)))
    # External T-slot receivers; no mounting fastener breaches the rear wall.
    for x in (30,126):
        receiver=cube((20,10,64),(x-10,-10,24))
        receiver-=cube((6.8,8,61),(x-3.4,-12,24))
        receiver-=cube((12.8,4,61),(x-6.4,-9,24))
        box+=receiver
    box-=pin_hole()
    # Underside service port and blind insert pockets, sealed by a separate plate.
    box-=cube((44,18,12),(56,12,-1))
    for x in (50,106):
        for y in (9,33):
            box+=cube((10,10,9),(x-5,y-5,0))
            box-=cyl(4.2,6.1,(x,y,-.1))
    return box

def build_bracket():
    bracket=cube((140,3,92),(8,-15,5))
    for x in (30,126):
        bracket+=cube((6,6.7,54),(x-3,-12,30))
        bracket+=cube((12,3.3,54),(x-6,-8.65,30))
    for x in (14,142):
        for z in (15,90):
            hole=m.Manifold.cylinder(6,2.25,circular_segments=48).rotate((-90,0,0)).translate((x,-16,z))
            bracket-=hole
    return bracket-pin_hole()

def build_port_plate():
    plate=cube((66,36,3),(45,3,-3))
    # Blank centre intentionally awaits actual connector geometry.
    for x in (50,106):
        for y in (9,33):
            plate-=cyl(3.4,5,(x,y,-4))
    plate-=ring(53,9,50,24,2,.8,-.8)
    return plate

def print_orientation(solid, rear=False):
    if rear: solid=solid.rotate((90,0,0))
    b=solid.bounding_box()
    return solid.translate((-b[0],-b[1],-b[2]))

def models():
    return {'Box':build_box(),'Bracket':build_bracket(),'Wiring_Plate':build_port_plate()}

if __name__=='__main__':
    root=Path(__file__).resolve().parent.parent
    parts=models()
    for name,part in parts.items():
        assert part.status()==m.Error.NoError and part.volume()>0
        assert len(part.decompose())==1, (name,'disconnected geometry')
        for orientation,solid in [('INSTALLED',part),('PRINT',print_orientation(part,name=='Bracket'))]:
            path=asset(root, f'CrossWind_IPC101_{name}_RevH_{orientation}.stl')
            write_binary_stl(path,solid)
            with path.open('r+b') as out:
                out.write(b'Crosswind IPC-101 Rev H fit prototype'.ljust(80,b'\0'))
        print(name,part.num_tri(),round(part.volume(),1),part.bounding_box())
    assert (parts['Box'] ^ parts['Bracket']).volume()<.001, 'Bracket interference'
    assert (parts['Box'] ^ parts['Wiring_Plate']).volume()<.001, 'Wiring plate interference'
