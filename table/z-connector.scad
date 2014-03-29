include <variables.scad>;
use <metal-parts.scad>;
use <motor.scad>;
use <pully.scad>;
use <x-connector.scad>;
use <belts.scad>;


include <Pulley_T-MXL-XL-HTD-GT2_N-tooth.scad>;


 
translate([-14,15,35]) union()
{
  rotate([0,90,0]) translate([0,0,0]) pulley ( "T10" , T10_pulley_dia , 2.5 , 6.13 );
  rotate([90,-37.5,270]) translate([-8.1,0,12])   StepMotor28BYJ();
}

module belt_centered(len=100)
{
rotate([0,90,0]) translate([-len/2,2.5,0])
  {
    translate([5,0,0])  belt_len(profile = 3, belt_width = 10, len = 80);
    translate([0,-7.6,-5])  cube([80,7.5,10]);
  }
}

module zConnector()
{
  rotate([0,0,270]) 
  {
    mirror([1,0,0]) translate([21,0,0]) bearingHolder(top_hole=false, hold_bolt=false);
    mirror([0,0,0]) translate([21,0,0]) bearingHolder(top_hole=false, hold_bolt=false);
    translate([0,-2.625,0]) cube([20,6.75,24.75], center=true);

    translate([-32.3,0,30]) difference()
    {
      cube([8,12,40], center=true);
      translate([0,0,20-5.5]) rotate([90,0,0])  cylinder(h=connector_width, r=radius_bolt*1.1, center=true);
    }
    translate([-10.75,0,15]) difference()
    {
      cube([8,12,10], center=true);
      translate([0,0,0.75]) rotate([90,0,0])  cylinder(h=connector_width, r=radius_bolt*1.1, center=true);
    }
    translate([32.4,0,15]) difference()
    {
      cube([8,12,10], center=true);
      translate([0,0,0.75]) rotate([90,0,0])  cylinder(h=connector_width, r=radius_bolt*1.1, center=true);
    }
  }


}

module zConnector_motor()
{
}


belt_centered(len=100);
mirror([0,0,0]) translate([-6,0,0]) zConnector();
mirror([1,0,0]) translate([-6,0,0]) zConnector();

//translate([-12.4,27.5,35])  zConnector_motor();

//#cube([100,100,100], center=true);


//Print
//!zConnector();

//Print
//!rotate([0,90,0]) zConnector_motor();