include <variables.scad>;
use <pully.scad>;
use <x-connector.scad>;
use <y-connector.scad>;
use <z-connector.scad>;
use <metal-parts.scad>;
use <belts.scad>;

x_gap = 252.;

rotate([0, 0,   0]) translate([x_gap,250,0]) xConnector_wBearing(top=true);
rotate([0, 0, 180]) translate([-x_gap,250,0]) xConnector_motor_wBearing();
translate([x_gap,0,0]) treaded_rod(length=500);

rotate([0, 0,   0]) translate([-x_gap,250,0]) xConnector_plain_wBearing();
rotate([0, 0, 180]) translate([x_gap,250,0]) xConnector_plain_wBearing();
translate([-x_gap,0,0]) treaded_rod(length=500);

rotate([0, 0, 90])  translate([0,0,42.5]) treaded_rod(length=500);
rotate([0, 0, 90])  translate([y_bars_apart,0,42.5]) treaded_rod(length=500);

translate([0,46,42.5]) zConnector_motor();
translate([-x_gap,0,0]) yConnector_wMotor();
rotate([0, 0, 180]) translate([-x_gap,0,0])  yConnector_wBearing();

//color("white")belt_len(profile = 2, belt_width = 5, len = 100);

//pully_dummy();

 