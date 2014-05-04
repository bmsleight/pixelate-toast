
$fn=60;

rotate([0,90,0]) difference()
  {
    cube([12,12,6], center=true);
    translate([0,0,0]) rotate([0,0,0])  cylinder(h=100, r=3*1.1, center=true);

//    cube([12,24,6], center=true);
//    translate([0,6,0]) rotate([0,0,0])  cylinder(h=100, r=3*1.1, center=true);
//    translate([0,-6,0]) rotate([0,0,0])  cylinder(h=100, r=3*1.075, center=true);
  }