include <variables.scad>;
use <pully.scad>;
use <motor.scad>;
use <bearings.scad>;


// Big to tight at the moment
!clip();

rotate([0,180,180]) translate([0,0,-20]) clip();


module clip()
{
  difference()
  {
    union()
    {
      // Upright
      cube([50,12,5], center=true);
      // Down of cross
      translate([25-(12/2),0,0]) cube([12,50,5], center=true);
      // Extra lip to grip
      translate([25-(3/2),0,3]) cube([3,50,3], center=true);
      // Mount for hinges
      translate([0,6,0]) cube([12,6*2,5], center=true);
      translate([0,6*1.5,5]) 
      {
        hinge_part();
      }
      translate([0,6*-0.5,5]) 
      {
        hinge_part();
      }
      // Spring knob
      translate([-20,0,5]) cylinder(h=5,r=radius_bolt*1.05, center=true);
    }
    // Hole for hindge bolt
    translate([0,0,10]) rotate([90,0,0]) cylinder(h=200,r=radius_bolt*1.10, center=true);

  }
}

module hinge_part()
{
        hull()
        {
          cube([12,6,10], center=true);
          translate([0,0,5]) rotate([90,0,0]) cylinder(h=6,r=6, center=true);
        }

}