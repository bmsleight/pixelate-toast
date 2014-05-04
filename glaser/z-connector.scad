include <variables.scad>;
use <pully.scad>;
use <motor.scad>;
use <bearings.scad>;


translate([-13,52,-4])  rotate([180,180,90]) color("Blue") import("sc90.stl");

translate([0,linear_bearing_or*1.5,0]) bearing_LM6UU();
translate([0,-linear_bearing_or*1.5,0]) bearing_LM6UU();

//z_base();
!z_base();

//translate([0,linear_bearing_or*6,0]) z_motor_mount();

module z_base()
{
  translate([0,(linear_bearing_or*3)/2,0]) z_base_half();
  translate([0,-(linear_bearing_or*3)/2,0]) z_base_half();
  translate([0,linear_bearing_or*6,0]) z_motor_mount();
  translate([(linear_bearing_len+9)/2+(radius_bolt*4)/2,0,0]) screw_hole();
  translate([-(linear_bearing_len+9)/2-(radius_bolt*4)/2,0,0]) screw_hole();
}

module zip_hole(extra=0)
{
  translate([linear_bearing_len/3,linear_bearing_or+3+extra,4]) cube([gap_zip_tie_x,gap_zip_tie_y, 100], center=true);
}

module screw_hole() {
  translate([0,0,-4]) difference()
  {
    cube([radius_bolt*4, radius_bolt*5.5, 6], center=true);
    translate([0,0,0.75]) rotate([0,0,0])  cylinder(h=100, r=radius_bolt*1.1, center=true);
  }
}


module z_motor_mount() 
//Size WxHxD: 26mm x 24mm x 13mm
{
  translate([0,0,-4]) difference()
  {
    cube([linear_bearing_len+9,(linear_bearing_or*3)*2, 6], center=true);
//#  translate([-24/2-2,32/2,-13/2+5])  rotate([180,180,90]) import("sc90.stl");
//   translate([10,-4.5,4]) cube([10,15,6], center=true);
   translate([-1,0,7]) cube([26*1.05*2,24*1.025,13*1.05], center=true);
   translate([3,-0.5,7]) cube([3*1.05,31*1.1,13*1.05], center=true);

    mirror([0,0,0]) zip_hole(5);
    mirror([0,1,0]) zip_hole(5);
    mirror([0,1,0]) zip_hole(8);
    mirror([1,0,0]) zip_hole(5);
    rotate([0,0,180]) mirror([0,0,0]) zip_hole(5);
    rotate([0,0,180]) mirror([0,0,0]) zip_hole(8);

//    translate([-2.5,0,0]) cube([10,12.5,100], center=true);
   translate([15.81,5,7])  cube([15,30,100], center=true);
   translate([14.25,25.95,0])  cube([20,20,100], center=true);

  }
//color("grey")  translate([-24/2-2,32/2,-13/2+2.5])  rotate([180,180,90]) import("sc90.stl");
}

module z_base_half()
{
  translate([0,0,-4]) difference()
  {
    cube([linear_bearing_len+9,linear_bearing_or*3, 6], center=true);
    translate([0,0,4]) bearing_LM6UU();
    translate([0,0,4]) rotate([0,90,0])  cylinder(h=100,r=radius_tr*1.2, center=true);
    mirror([0,0,0]) zip_hole();
    mirror([0,1,0]) zip_hole();
    mirror([1,0,0]) zip_hole();
    rotate([0,0,180]) mirror([0,0,0]) zip_hole();

  }
}