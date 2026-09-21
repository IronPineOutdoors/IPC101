// CrossWind IPC-101 Control Box Rev H TESTFIT
// 2026-09-20
// STATUS: TEST-FIT / NOT FABRICATION-FROZEN
//
// Rev H preserves the Rev G wood mounting interface but redesigns the
// control-panel volume around IPC-101. The current 16.5 mm faceplate-back to
// PCB-top spacing is provisional and must be physically validated.

$fn=20;

PANEL_W=150;
PANEL_H=100;
BODY_W=156;
WOOD_H=101.6;
TILT=47;
WALL=3;

FACE_TO_PCB_TOP=16.5;
PCB_T=1.56;

// Rev G preserved wood mounting interface
WOOD_HOLE_X=[16,140];
WOOD_HOLE_Z=[28,70];
WOOD_CLEARANCE=4.5;
WOOD_HEAD_D=9.5;
DRIVER_D=11;
WOOD_PAD_W=24;
WOOD_PAD_H=20;
WOOD_PAD_DEPTH=4;

FACE_MARGIN=3;
FRONT_EXTENSION=24; // TEST-FIT value, not frozen

// Generic rear connector cassette bay. Connector-specific insert remains TBD.
CONN_BAY_W=34;
CONN_BAY_H=26;
CONN_BAY_Z=43;

MARK="IPC101-ENC-RH TEST";

run=PANEL_H*sin(TILT);
rise=PANEL_H*cos(TILT);
top_y=8+FRONT_EXTENSION;
bot_y=top_y+run;
bot_z=7.5;
top_z=bot_z+rise;

module outer_shell(){
    difference(){
        linear_extrude(height=BODY_W)
            polygon(points=[[0,0],[bot_y,bot_z],[top_y,top_z],[0,WOOD_H]]);
        translate([WALL,0,WALL])
            linear_extrude(height=BODY_W-2*WALL)
                polygon(points=[[0,0],[bot_y-WALL*1.5,bot_z+WALL],[top_y-WALL*1.5,top_z-WALL],[0,WOOD_H-2*WALL]]);
    }
}

module installed_shell(){
    multmatrix([[0,0,1,0],[1,0,0,0],[0,1,0,0],[0,0,0,1]]) outer_shell();
}

function face_pt(px,py,n=0)=[FACE_MARGIN+px,
    bot_y-py*sin(TILT)-n*cos(TILT),
    bot_z+py*cos(TILT)-n*sin(TILT)];

module rod_between(a,b,d){
    hull(){ translate(a) sphere(d=d); translate(b) sphere(d=d); }
}

module wood_mount_pads(){
    for(x=WOOD_HOLE_X) for(z=WOOD_HOLE_Z)
        translate([x-WOOD_PAD_W/2,0,z-WOOD_PAD_H/2])
            cube([WOOD_PAD_W,WOOD_PAD_DEPTH,WOOD_PAD_H]);
}

module wood_mount_cuts(){
    for(x=WOOD_HOLE_X) for(z=WOOD_HOLE_Z){
        translate([x,-1,z]) rotate([-90,0,0]) cylinder(h=WOOD_PAD_DEPTH+3,d=WOOD_CLEARANCE);
        translate([x,1.4,z]) rotate([-90,0,0]) cylinder(h=WOOD_PAD_DEPTH+2,d=WOOD_HEAD_D);
        translate([x,1.4,z]) rotate([-90,0,0]) cylinder(h=120,d=DRIVER_D);
    }
}

PANEL_HOLES=[[5,5],[145,5],[5,95],[145,95]];

module stack_bosses(){
    for(h=PANEL_HOLES){
        p0=face_pt(h[0],h[1],2.0);
        p1=face_pt(h[0],h[1],FACE_TO_PCB_TOP);
        p2=face_pt(h[0],h[1],FACE_TO_PCB_TOP+PCB_T+7.0);
        rod_between(p0,p1,8);
        rod_between(p1,p2,11);
    }
}

module stack_holes(){
    for(h=PANEL_HOLES){
        p0=face_pt(h[0],h[1],-2);
        p2=face_pt(h[0],h[1],FACE_TO_PCB_TOP+PCB_T+9);
        rod_between(p0,p2,3.3);
    }
}

module connector_bay_cut(){
    translate([(BODY_W-CONN_BAY_W)/2,-1,CONN_BAY_Z-CONN_BAY_H/2])
        cube([CONN_BAY_W,10,CONN_BAY_H]);
}

module connector_bay_lip(){
    translate([(BODY_W-CONN_BAY_W)/2-3,0.5,CONN_BAY_Z-CONN_BAY_H/2-3])
        difference(){
            cube([CONN_BAY_W+6,3,CONN_BAY_H+6]);
            translate([3,-1,3]) cube([CONN_BAY_W,5,CONN_BAY_H]);
        }
}

module rev_mark(){
    translate([BODY_W/2,0.6,82]) rotate([90,0,0])
        linear_extrude(height=0.45)
            text(MARK,size=4,halign="center",valign="center",font="Liberation Sans:style=Bold");
}

module rev_h(){
    difference(){
        union(){
            installed_shell();
            wood_mount_pads();
            stack_bosses();
            connector_bay_lip();
        }
        wood_mount_cuts();
        stack_holes();
        connector_bay_cut();
        rev_mark();

        // Generous first-pass control-panel service opening.
        hull(){
            for(px=[5,145],py=[5,95]){
                p=face_pt(px,py,-1);
                q=face_pt(px,py,35);
                translate(p) cube([1,1,1],center=true);
                translate(q) cube([1,1,1],center=true);
            }
        }
    }
}

rev_h();
