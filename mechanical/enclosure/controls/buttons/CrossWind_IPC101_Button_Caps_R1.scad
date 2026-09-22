// R1 measured-stack push caps. Units mm. Import each label's two materials together.
// Front/lettering is at Z=0 on the bed; +Z points inward when assembled.
$fn=64;
label="ARM"; // ARM or PULL
part="white"; // white or black
front_to_button=12.82;
plate_thickness=2.05;
rest_clearance=0.20; // provisional free play; confirm no preload in the real assembly
protrusion=1.50;
guide_depth=plate_thickness+protrusion; // 3.55, face to rear retaining flange
flange_depth=1.0;
button_from_back=front_to_button-plate_thickness; // 10.77
tip_from_back=button_from_back-rest_clearance; // 10.57
tip_z=guide_depth+tip_from_back; // 14.12 from cap face
stem_length=tip_from_back-flange_depth; // 9.57 from flange rear to tip
inlay_depth=.6;

assert(label=="ARM" || label=="PULL");
assert(stem_length>0);
module rounded(w,h,r,d){
 hull()for(x=[-w/2+r,w/2-r])for(y=[-h/2+r,h/2-r])
 translate([x,y,0])cylinder(h=d,r=r);
}
module graphics(){
 // Mirror the COMPLETE word once so it reads correctly from the front (-Z).
 mirror([1,0,0])linear_extrude(inlay_depth)
 text(label,size=3.2,font="Liberation Sans:style=Bold",halign="center",valign="center");
}
module shape(){
 union(){
 rounded(15.2,10.0,2.0,guide_depth+.01);
 translate([0,0,guide_depth])rounded(18.0,12.8,2.3,flange_depth);
 translate([0,0,guide_depth+flange_depth-.01])cylinder(h=stem_length+.01,d=5.5);
 }
}
module revision(){
 // Hidden rear flange marking, clear of the central stem and guide faces.
 translate([0,4.35,guide_depth+flange_depth-.3])linear_extrude(.4)
 text(label=="ARM"?"A-R1":"P-R1",size=1.3,font="Liberation Sans:style=Bold",halign="center",valign="center");
}
if(part=="white")difference(){shape();graphics();revision();}
if(part=="black")graphics();
