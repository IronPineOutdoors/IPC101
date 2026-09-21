$fn=48;
pcb_x=150; pcb_y=100; margin=3; base_t=2.4; rim_w=6; rib_w=5;
post_d=8; post_h=5; hole_d=3.4;
module beam(x,y,w,d){translate([x,y,0]) cube([w,d,base_t]);}
module post(x,y){difference(){translate([x,y,base_t-0.2]) cylinder(d=post_d,h=post_h+0.2);translate([x,y,-0.1]) cylinder(d=hole_d,h=base_t+post_h+0.4);}}
union(){
 beam(-margin,-margin,pcb_x+2*margin,rim_w);
 beam(-margin,pcb_y+margin-rim_w,pcb_x+2*margin,rim_w);
 beam(-margin,-margin,rim_w,pcb_y+2*margin);
 beam(pcb_x+margin-rim_w,-margin,rim_w,pcb_y+2*margin);
 beam(0,12,pcb_x,rib_w);
 beam(0,83,pcb_x,rib_w);
 beam(72.5,0,rib_w,pcb_y);
 post(5,5); post(145,5); post(5,95); post(145,95);
}