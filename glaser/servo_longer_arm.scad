include <variables.scad>;
use <pully.scad>;
use <motor.scad>;
use <bearings.scad>;

$fn=100;

module servo_arm()
{
  union() hull()
  {
    translate([0,0,0]) cylinder (h = servo_arm_start_large_c_d, r=servo_arm_start_large_c_r, center = true);
    translate([servo_arm_length-servo_arm_start_small_c_r,0,0]) cylinder (h = servo_arm_start_large_c_d, r=servo_arm_start_small_c_r, center = true);
  }

}


module new_servo_arm()
{
  union() hull()
  {
    translate([0,0,0]) cylinder (h = servo_arm_start_large_c_d, r=servo_arm_start_large_c_r*1.5, center = true);
    translate([(servo_arm_length-servo_arm_start_small_c_r)*2,0,0]) cylinder (h = servo_arm_start_large_c_d, r=servo_arm_start_small_c_r, center = true);
  }

}

module new_servo_arm_cube()
{
  translate([38/2,0,0]) cube([38,4,servo_arm_start_large_c_d], center=true);
  translate([38,5,-0.25]) rotate([0,0,-30]) cube([4,10,4], center=true);
  translate([38,5,-0.25]) rotate([270,0,-30]) translate([0,0,5.25]) cylinder (h =0.5, r1=2, r2=0, center=true);


}


difference()
{
  translate([6,0,-3]) union()
   {
     difference()
     {
       cube([27.5,15,6], center=true);
       translate([0,7.5,0]) cube([4,2,6*2], center=true);
       translate([9,7.5,0]) cube([4,2,6*2], center=true);
       translate([0,-7.5,0]) cube([4,2,6*2], center=true);
       translate([9,-7.5,0]) cube([4,2,6*2], center=true);

     }
     translate([0,0,-0.75]) new_servo_arm_cube();
     translate([0,0,-0.75]) new_servo_arm();
   }
   translate([0,0,0.5]) scale([1.05,1.05,1]) servo_arm();
}

//servo_arm();

//new_servo_arm();