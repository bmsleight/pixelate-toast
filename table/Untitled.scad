include <variables.scad>;
use <metal-parts.scad>;
use <motor.scad>;
use <pully.scad>;
use <belts.scad>;


include <Pulley_T-MXL-XL-HTD-GT2_N-tooth.scad>;

pulley ( "T5" , T5_pulley_dia , 1.19 , 3.264 );

translate([0,0,75]) pulley ( "T10" , T10_pulley_dia , 2.5 , 6.13 );

translate([-25,-6,14]) color("red")
{
  belt_len(profile = 2, belt_width = 10, len = 50);
  translate([25,-4,0]) cube([50,7.5,10], center=true);
}