include <variables.scad>;
use <metal-parts.scad>;
use <motor.scad>;
use <pully.scad>;

module xConnector()
{
  bearingHolder();
  translate([0,0,-bearing_os*1.1])  connectorFeet();
  translate([0,0,bearing_os*1.1+radius_tr*1+(bearing_t*2.21)/2])  bearingHolderTop();

}

module xConnector_motor()
{
  bearingHolder();
  translate([0,0,-bearing_os*1.1])  connectorFeet();
  translate([0,0,bearing_os*1.1+radius_tr*1+(bearing_t*2.21)/2])  bearingHolderTopMotor();
}


module bearingHolder()
{
  difference()
  {
    cube([connector_width_, bearing_t*2, bearing_os*2.2+radius_tr*2], center=true);
   // Bearing hole
   translate([0,bearing_t,0]) rotate([90,0,0])  cylinder(h=bearing_t*2, r=bearing_os*1.05, center=true);
   // Treaded rod hole
    translate([0,0,0]) rotate([90,0,0])  cylinder(h=bearing_t*4, r=radius_tr*1.15, center=true);
   // Treaded rod to hole bearing
    translate([0,0,connector_width_/2]) cylinder(h=radius_bolt*7, r=radius_tr*1.1, center=true);
  }


  translate([0,bearing_t+radius_bolt*2,0])  difference()
  {
  // To hole a bolt to hold the bearing in place
    cube([connector_width_, radius_bolt*4, bearing_os*2.2+radius_tr*2], center=true);
    cube([bearing_os*2.2, radius_bolt*8, bearing_os*4], center=true);
    translate([0,-radius_bolt*0.8,0]) rotate([0,90,0])  cylinder(h=connector_width, r=radius_bolt*1.1, center=true);
  }

}

module connectorFeet()
{
  difference()
  {
    cube([connector_width_+radius_tr*12, bearing_t*2, radius_tr*2], center=true);
    cube([bearing_os*2.2, bearing_t*4, radius_tr*4], center=true);
     translate([connector_width_/2+radius_tr*4,0,0])  cylinder(h=radius_bolt*10, r=radius_bolt*1.15, center=true);
     translate([-connector_width_/2-radius_tr*4,0,0])  cylinder(h=radius_bolt*10, r=radius_bolt*1.15, center=true);
  }

}


module bearingHolderTop(remove_top=false)
{
  difference()
  {
    cube([connector_width_+radius_tr*6, bearing_t*2, bearing_t*2.2+radius_tr*4], center=true);
    if(remove_top==false)
    {
      cube([connector_width_+radius_tr*2, bearing_t*6, bearing_t*2.2], center=true);
    }
    if(remove_top==true)
    {
     translate([0,0,radius_tr*2]) cube([connector_width_+radius_tr*2, bearing_t*6, bearing_t*2.2+radius_tr*4], center=true);
     translate([0,bearing_t*2.5,-radius_tr*2]) cube([connector_width_*2, bearing_t*4, bearing_t*2.2+radius_tr*4], center=true);

    }
    translate([0,0,-radius_tr*4])  cube([bearing_os*2.1, bearing_t*4, bearing_t*4.4], center=true);
   // Treaded rod to hole bearing
   cylinder(h=radius_bolt*20, r=radius_tr*1.1, center=true);
  }
}

module bearingHolderTopMotor()
{
  translate([0,bearing_t*1-radius_tr*0.5,-5])  difference()
  {
    cube([connector_width_+radius_tr*5, bearing_t*2+radius_tr*3, 42], center=true);
    translate([0,0,radius_tr*2]) cube([connector_width_-radius_tr*2, bearing_t*6, 84], center=true);
    translate([0,bearing_t*2,-radius_tr*2.5]) cube([connector_width_*2, bearing_t*4, 40], center=true);
    translate([0,0,-radius_tr*2.75])  cube([connector_width_-0.1, bearing_t*4, 42], center=true);
    // Treaded rod to hole bearing
    cylinder(h=radius_bolt*20, r=radius_tr*1.1, center=true);
    translate([17.5,3.6,-9])	cylinder(h = 84, r = 2.1, center = true, $fn = 32);
    translate([-17.5,3.6,-9])	cylinder(h = 84, r = 2.1, center = true, $fn = 32);

  }
}

module xConnector_motor_wBearing()
{
  rotate([0, 0,0])  translate([0,bearing_t/2,0]) bearing();
  xConnector_motor();
  translate([0,8.1,44.25]) rotate([0,0,270]) StepMotor28BYJ();
  translate([0,0,33]) rotate([0,180,0]) pully_dummy();

}


module xConnector_wBearing(top=False)
{
  rotate([0, 0,0])  translate([0,bearing_t/2,0]) bearing();
  xConnector();
  if (top==true)
  {
    rotate([90, 0,0])  translate([0,bearing_os*1.1+bearing_t*1.1,0]) bearing();
    rotate([90, 0,0])  translate([0,bearing_os*1.1+bearing_t*2.2,0]) bearing();
  }
}


//!xConnector();

//!xConnector_motor_wBearing();
//!xConnector_wBearing(top=true);

// Print
//!rotate([90, 0,0]) xConnector();

// Print
!rotate([90, 0,0]) xConnector_motor();




