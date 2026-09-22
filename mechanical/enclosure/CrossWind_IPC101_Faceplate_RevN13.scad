// Tree traced from supplied transparent wordmark alpha, see branding/trace_tree.py.
include <branding/iron_pine_tree_trace.scad>
// N1.3: operator-view button positions measured on the physical PCB.
// ARM left, PULL right confirmed by user 2026-09-21.
// OLED and navigation remain wired faceplate assemblies at M4 positions.

$fn=64; part="white"; W=150;H=100;T=2;gd=.55;
mounts=[[5,5],[145,5],[5,95],[145,95]];
arm=[46.88,20.75]; pull=[115.67,20.75]; led=[68.5,31]; nav=[45,63.5]; oled=[103.5,63.5];

module rr(w,h,r,z){hull()for(x=[-w/2+r,w/2-r])for(y=[-h/2+r,h/2-r])translate([x,y,0])cylinder(h=z,r=r);}
module cuts(){
 for(p=mounts)translate([p[0],p[1],-.5])cylinder(h=3,d=3.2);
 translate([oled[0]-28.5,oled[1]-14,-.5])cube([57,28,3]);
 for(dx=[-34.4,34.4])for(dy=[-19.4,19.4])translate([oled[0]+dx,oled[1]+dy,-.5])cylinder(h=3,d=3.2);
 translate([nav[0],nav[1],-.5])cylinder(h=3,d=6.2);
 translate([led[0],led[1],-.5])cylinder(h=3,d=5.2);
 translate([arm[0],arm[1],-.5])rr(16,10.8,2,3);
 translate([pull[0],pull[1],-.5])rr(16,10.8,2,3);
}
module cradle(){p=10.70;w=2;o=p+2*w;ch=2.8;translate([nav[0],nav[1],T])difference(){
 translate([-o/2,-o/2,0])cube([o,o,ch]);
 translate([-p/2,-p/2,-.1])cube([p,p,ch+.2]);
 translate([-o/2-.2,-4.2,1])cube([o+.4,8.4,ch+1]);
 translate([-4.2,-o/2-.2,1])cube([8.4,o+.4,ch+1]);}}
module txt(s,x,y,sz,ha="center",font="Liberation Sans:style=Bold"){
 translate([x,y,0])linear_extrude(gd)text(s,size=sz,font=font,halign=ha,valign="center");
}
module line2d(x1,y1,x2,y2,w=.8){
 linear_extrude(gd) hull(){
  translate([x1,y1])circle(d=w);
  translate([x2,y2])circle(d=w);
 }
}
module pine(x,y,s=1){
 // Same top/bottom limits as N1.1, original traced aspect ratio and open center.
 translate([x,y-7*s,0])scale([17*s,17*s,gd/.55])import("branding/iron_pine_tree_unit.stl");
}
module swoosh(){
 // robust two-stroke CrossWind swoosh, ~0.9mm printable width
 line2d(86,93,99,95.3,.9); line2d(99,95.3,124,96.5,.9); line2d(124,96.5,139,93,.9);
 line2d(89,82.5,104,80.7,.9); line2d(104,80.7,126,80.3,.9); line2d(126,80.3,138,83,.9);
}

module desired_operator_graphics(){
 // Compact brand badge: original tree silhouette with bold IPO below.
 translate([34,84.3,0])scale([12.5,12.5,gd/.55])import("branding/iron_pine_tree_unit.stl");
 txt("IPO",34,81.5,3.2);

 txt("CROSSWIND",112,88,4.3);
 swoosh();

 // ARM label is on its R1 cap face.
 // PULL label is on its R1 cap face.
}

// Manufacturing conversion ONLY: all layout coordinates above are operator-view.
// Front prints at Z=0; Xexport=150-Xoperator. Do not mirror STLs in the slicer.
module whole_mirror(){translate([150,0,0])mirror([1,0,0])children();}
module raw_white(){
 difference(){union(){cube([W,H,T]);cradle();}cuts();desired_operator_graphics();
 // Hidden rear mark; pre-mirror text so it reads from the rear after conversion.
 translate([75,12,1.6]) mirror([1,0,0]) linear_extrude(.5)
 text("IPC101-FP-N1.3",size=3,font="Liberation Sans:style=Bold",halign="center");}
}
if(part=="white") whole_mirror() raw_white();
if(part=="black") whole_mirror() desired_operator_graphics();
