include <variables.scad>;
use <pully.scad>;
use <motor.scad>;
use <bearings.scad>;


x_connector(motor_m=false);
x_bars();
translate([gap_between_x_bars/2,0,9.5]) rotate([90,0,0]) bearing_thin();
translate([gap_between_x_bars/2,0,16]) rotate([90,0,0]) bearing_thin();

//color("blue") translate([12.5,-2,8]) cube([4.5,4,20]);

//!rotate([90,180,0]) x_connector();
//!rotate([90,180,0]) x_connector(motor_m=false);
!x_microswitch_holder();

module x_bars(expand=false) 
{
  color("Grey") rotate([90,0,0])
  {
    if(expand==false)
    {
      translate([gap_between_x_bars/2,0,0]) cylinder(h=250,r=radius_tr, center=true);
      translate([-gap_between_x_bars/2,0,0]) cylinder(h=250,r=radius_tr, center=true);
    }
    if(expand==true)
    {
      translate([gap_between_x_bars/2,0,0]) cylinder(h=250,r=radius_tr*1.2, center=true);
      translate([-gap_between_x_bars/2,0,0]) cylinder(h=250,r=radius_tr*1.2, center=true);
    }
  }
}

module x_connector(motor_m=true) 
{
  difference()
  {
    union()
    {
      cube([32, 4, 12], center=true);
      if(motor_m==true)
      {
        translate([-gap_between_x_bars/2,-4,16])  
        {
          x_motor_mount();
        }
      }
      if(motor_m==false)
      {
        mirror([1,0,0]) translate([-gap_between_x_bars/2,-4,16])  
        {
          x_motor_mount(connected=true);
        }
      }

/*      if(motor_m==false)
      {
        translate([gap_between_x_bars/2,0,14])  
        {
          x_barring_mount();
        }
      }
*/
     }
    x_bars(expand=true);
  }
  // Hold bolts for x-bars
  translate([gap_between_x_bars/2+6,-4,0])  rotate([0,0,90]) x_bolt_holder(short=true);
  translate([-gap_between_x_bars/2-6,-4,0])  rotate([0,0,90]) x_bolt_holder(short=true);
  
  // bolt down to floot
  translate([-25,-4,-12])   rotate([90,0,0])  x_bolt_holder();
  mirror([1,0,0]) translate([-25,-4,-12]) rotate([90,0,0])  x_bolt_holder();
  translate([-14,-1,-10]) cube([6,6,8], center=true);
  translate([14,-1,-10]) cube([6,6,8], center=true);
  

}

module x_bolt_holder(short=false)
{
  if(short==false)
  {
    difference()
    {
      cube([12+4, 4, 12], center=true);
      translate([-2,0,0])  rotate([90,0,0]) cylinder(h=250,r=radius_bolt*1.05, center=true);
    }
  }
  if(short==true)
  {
    difference()
    {
      cube([12, 4, 12], center=true);
      translate([0,0,0])  rotate([90,0,0]) cylinder(h=250,r=radius_bolt*1.05, center=true);
    }
  }

}


module x_motor_mount(connected=false)
{
  difference()
  {
    cube([motor_mounting_gap+17, 12, motor_reverse_height+4], center=true);
    translate([0,-10, -4])   cube([motor_mounting_gap*2, 24, motor_reverse_height+4], center=true);
    translate([0,4, 0]) cube([motor_mounting_gap+8, 12, motor_reverse_height-4], center=true);
    translate([-motor_mounting_gap/2,0,motor_reverse_height/2])  rotate([0,0,0]) cylinder(h=12,r=radius_bolt*1.05, center=true);
    translate([motor_mounting_gap/2,0,motor_reverse_height/2])  rotate([0,0,0]) cylinder(h=12,r=radius_bolt*1.05, center=true);
    translate([0,0,motor_reverse_height/2])  rotate([0,0,0]) cylinder(h=12,r=radius_tr*1.05, center=true);
    if (connected==false)
    {
      translate([0,4, 8]) cube([motor_mounting_gap-12, 12*2, motor_reverse_height+4], center=true);
    }
    if (connected==true)
    {
      translate([motor_mounting_gap/2,-4, 8]) cube([(motor_mounting_gap+8)/2, 12, motor_reverse_height], center=true);
      translate([-motor_mounting_gap/2,-4, 8]) cube([(motor_mounting_gap+8)/2, 12, motor_reverse_height], center=true);
    }
  }
  if (connected==true)
  {
    translate([0,0,-8]) difference() 
    {
      translate([-0.5,0,-2.])  cube([15,12,4] , center=true);
      cylinder(h=12,r=radius_tr*1.05, center=true);

    }
  }
}



module x_barring_mount()
{
 cube([4.5,4,16], center=true);

}


module x_microswitch_holder()
{
  rotate([270,0,0]) difference()
  {
    translate([0.5,0,0]) cube([12+3, 5, 40], center=true);
    translate([-2,0,-14])  rotate([90,0,0]) cylinder(h=250,r=radius_bolt*1.1, center=true);
#    translate([2.05,-4,14])   cube([12, 5*1.1, 6.25*1.1], center=true);
//    translate([9,0,14])   cube([4, 5.25, 3], center=true);
    translate([-8,0,14])   cube([4, 5.25, 4], center=true);

  }
}



