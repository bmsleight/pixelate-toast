include <variables.scad>;
use <pully.scad>;
use <motor.scad>;
use <bearings.scad>;

!y_pulley();

module y_pulley()
{

  pulley ( "T10" , 0 , 2.5 , 6.13 );
  translate([0,0,8.]) difference() 
  {
    union()
    {
      cylinder(h=6, r=6.13);
      translate([0,0,6.]) cylinder(h=3, r1=6.13, r2=8.13);
   mirror([0,0,1])  translate([0,0,-3.]) cylinder(h=3, r1=6.13, r2=8.13);
    }
  #  translate([0,0,4.5]) cube([2,20,3], center=true);
    cylinder(h=100, r=2.5, center=true);

  }

}