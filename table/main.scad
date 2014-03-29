include <variables.scad>;
use <pully.scad>;
use <x-connector.scad>;
use <metal-parts.scad>;
use <belts.scad>;

rotate([0, 0,   0]) translate([140,140,0]) xConnector_wBearing(top=true);
rotate([0, 0, 180]) translate([-140,140,0]) xConnector_motor_wBearing();
translate([140,0,0]) treaded_rod();

rotate([0, 0,   0]) translate([-140,140,0]) xConnector_plain_wBearing();
rotate([0, 0, 180]) translate([140,140,0]) xConnector_plain_wBearing();
translate([-140,0,0]) treaded_rod();

//color("white")belt_len(profile = 2, belt_width = 5, len = 100);

//pully_dummy();

 