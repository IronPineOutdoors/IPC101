// CrossWind IPC-101 Control Box Rev H2 TESTFIT
// STATUS: TEST-FIT / NOT FABRICATION-FROZEN
// Corrects Rev H1: removes the temporary external connector cassette; keeps closed shell and clean exterior.
// Rev G rear wood-mount interface is preserved.

$fn=48;

PANEL_W=150;
PANEL_H=100;
BODY_W=156;
WOOD_H=101.6;
TILT=47;
WALL=3;
FACE_RIM=7;
SIDE_MARGIN=3;

// Rev H/H1/H2 working stack target only; carrier will set this later.
FACE_TO_PCB_TOP=16.5;
PCB_T=1.56;

// More upper depth than Rev G so the IPC-101 parallel stack has room.
TOP_PROJECTION=24;
LOWER_Z=12;

// Rev G preserved wood-mount interface.
WOOD_HOLE_X=[16,140];
WOOD_HOLE_Z=[28,70];
WOOD_PAD_W=24;
WOOD_PAD_H=20;
WOOD_PAD_DEPTH=4;
WOOD_CLEARANCE=4.5;
WOOD_HEAD_D=9.5;
DRIVER_ACCESS_D=11;

// Rear IPC-101-to-Alpha connector is intentionally NOT cut in Rev H2.
// Add the exact flush panel-mount cutout only after connector selection.

MARK="IPC101-ENC-RH2 TEST";

run=PANEL_H*sin(TILT);
rise=PANEL_H*cos(TILT);
bot_y=TOP_PROJECTION+run;
bot_z=LOWER_Z;
top_y=TOP_PROJECTION;
top_z=LOWER_Z+rise;

// Face-local coordinates: X across panel, V bottom->top, N inward.
module on_face(){
    multmatrix([
        [1,0,0,SIDE_MARGIN],
        [0,-sin(TILT),-cos(TILT),bot_y],
        [0, cos(TILT),-sin(TILT),bot_z],
        [0,0,0,1]
    ]) children();
}

module beam(width,y,z){
    translate([0,y,z]) cube([width,0.2,0.2]);
}

module wedge(width,xoff,profile){
    translate([xoff,0,0])
    hull(){ for(p=profile) beam(width,p[0],p[1]); }
}

module shell(){
    outer_profile=[
        [0,0],
        [bot_y,bot_z],
        [top_y,top_z],
        [0,WOOD_H-0.2]
    ];

    // Inset cavity deliberately leaves a continuous lower/underside wall.
    inset_run=FACE_RIM*sin(TILT);
    inset_rise=FACE_RIM*cos(TILT);
    cavity_profile=[
        [WALL,WALL],
        [bot_y-5-inset_run,bot_z+inset_rise+WALL],
        [top_y-5+inset_run,top_z-inset_rise-WALL],
        [WALL,WOOD_H-WALL]
    ];

    difference(){
        wedge(BODY_W,0,outer_profile);
        wedge(BODY_W-2*WALL,WALL,cavity_profile);

        // Front service opening only through the inclined front wall.
        on_face()
            translate([FACE_RIM,FACE_RIM,-2])
                cube([PANEL_W-2*FACE_RIM,PANEL_H-2*FACE_RIM,WALL+5]);
    }
}

module y_cyl(len,d,x,y,z){
    translate([x,y,z]) rotate([-90,0,0]) cylinder(h=len,d=d);
}

module rear_mount_reinforcement(){
    for(x=WOOD_HOLE_X) for(z=WOOD_HOLE_Z)
        translate([x-WOOD_PAD_W/2,0,z-WOOD_PAD_H/2])
            cube([WOOD_PAD_W,WOOD_PAD_DEPTH,WOOD_PAD_H]);
}

module rear_mount_cuts(){
    for(x=WOOD_HOLE_X) for(z=WOOD_HOLE_Z){
        y_cyl(WOOD_PAD_DEPTH+2,WOOD_CLEARANCE,x,-1,z);
        y_cyl(WOOD_PAD_DEPTH,WOOD_HEAD_D,x,1.4,z);
        y_cyl(120,DRIVER_ACCESS_D,x,1.4,z);
    }
}

module revision_mark(){
    // Recessed on the inside rear wall; hidden after assembly.
    translate([BODY_W/2,0.7,88]) rotate([90,0,0])
        linear_extrude(height=0.45)
            text(MARK,size=4,halign="center",valign="center",font="Liberation Sans:style=Bold");
}

module rev_h2(){
    difference(){
        union(){
            shell();
            rear_mount_reinforcement();
        }
        rear_mount_cuts();
        revision_mark();
    }
}

rev_h2();
