include <variables.scad>;
use <metal-parts.scad>;




module xConnector()
{
  difference()
  {
    cube([connector_width, bearing_t*2, connector_height], center=true);
   // Bearing hole
   translate([0,bearing_t,0]) rotate([90,0,0])  cylinder(h=bearing_t*2, r=bearing_os*1.05, center=true);
   // Treaded rod hole
    translate([0,0,0]) rotate([90,0,0])  cylinder(h=bearing_t*4, r=radius_tr*1.05, center=true);
   // Side cuts
    translate([connector_width/2,0,radius_bolt*6])  cube([radius_bolt*12, bearing_t*4, connector_height+radius_bolt*4], center=true);
    translate([-connector_width/2,0,radius_bolt*6])  cube([radius_bolt*12, bearing_t*4, connector_height+radius_bolt*4], center=true);
   // Bolt holding bearing space
    translate([0,0,connector_height/2-radius_bolt*4])  cube([radius_tr*4, bearing_t*4, radius_tr*2], center=true);
   // Treaded rod to hole bearing
    translate([0,0,connector_height/2]) rotate([0,0,0])  cylinder(h=radius_bolt*6, r=radius_tr*1.1, center=true);
   // Holding down bolts
   translate([connector_width/2-radius_bolt*3,0,-connector_height/2]) rotate([0,0,0])  cylinder(h=radius_bolt*10, r=radius_bolt*1.15, center=true);
   translate([-connector_width/2+radius_bolt*3,0,-connector_height/2]) rotate([0,0,0])  cylinder(h=radius_bolt*10, r=radius_bolt*1.15, center=true);
  }

  translate([0,bearing_t+radius_bolt*2,0])  difference()
  {
  // To hole a bolt to hold the bearing in place
    cube([connector_width-radius_bolt*12, radius_bolt*4, bearing_os*2.2], center=true);
    cube([bearing_os*2.2, radius_bolt*8, bearing_os*4], center=true);
    translate([0,-radius_bolt*0.8,0]) rotate([0,90,0])  cylinder(h=connector_width, r=radius_bolt*1.1, center=true);
  }


}

module xConnector_wBearing(top=False)
{
  rotate([0, 0,0])  translate([0,bearing_t/2,0]) bearing();
  xConnector();
  if (top==true)
  {
    rotate([90, 0,0])  translate([0,connector_height/2+bearing_t/2,0]) bearing();
  }
}


! xConnector_wBearing();

// Print
//rotate([90, 0,0]) xConnector();