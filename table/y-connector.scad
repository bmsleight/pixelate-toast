include <variables.scad>;
use <metal-parts.scad>;
use <motor.scad>;
use <pully.scad>;
use <x-connector.scad>;
use <belts.scad>;


include <Pulley_T-MXL-XL-HTD-GT2_N-tooth.scad>;


module yConnector()
{
  difference()
  {
    union()	
    {
      bearingHolder(top_hole=false, hold_bolt=false);
      translate([0,0,(bearing_os*2.2+radius_tr*2)/2+bearing_t*1.5]) cube([bearing_t, bearing_t*2, bearing_t*3], center=true);
      translate([bearing_os,0,(bearing_os*2.2+radius_tr*2)/2+bearing_t*2.5]) cube([bearing_os*2, bearing_t*2, bearing_t], center=true);
    }
    translate([bearing_t+radius_tr*1.1,0,0]) cylinder(h=100, r=radius_tr*1.1, center=true);
  }
}

module yConnector_seperator()
{
  difference()
  {
    cube([bearing_os*2, 42.5,bearing_os*2], center=true);
    translate([0,0,0]) rotate([90,0,0])  cylinder(h=42.5*2, r=radius_tr*1.15, center=true);
  }
}

module xConnector_wBearing_double()
{
  translate([0,0,0])
  {

  xConnector_wBearing(top=true);
//  translate([-42.,0,0])bearingHolder(top_hole=false, hold_bolt=true);
  translate([-y_bars_apart,0,0]) xConnector_plain_wBearing();
  }
}


module yConnector_allparts()
{
  mirror([0,0,0]) translate([0,-27.5,0]) yConnector();
  mirror([0,1,0]) translate([0,-27.5,0]) yConnector();
  yConnector_seperator();
}

module yConnector_wBearing()
{
  yConnector_allparts();
  translate([bearing_os,0,43]) rotate([0,0,90]) xConnector_wBearing_double();
}

module yConnector_wMotor()
{
  yConnector_allparts();
  translate([bearing_os,0,43]) rotate([0,0,90]) xConnector_motor_wBearing();
}


//!xConnector_wBearing_double();
//yConnector_wMotor();
yConnector_wBearing();