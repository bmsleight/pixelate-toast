include <variables.scad>;
use <pully.scad>;
use <motor.scad>;

T10_pulley_dia = tooth_spacing (10,0.93);

rotate([0,90,0]) translate([0,0,0]) pulley ( "T10" , T10_pulley_dia , 2.5 , 6.13 );
rotate([90,-37.5,270]) translate([-8.1,0,12])   StepMotor28BYJ();
