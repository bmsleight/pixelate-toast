include <variables.scad>;
use <pully.scad>;
use <x-connector.scad>;
use <metal-parts.scad>;


rotate([0, 0,   0]) translate([140,140,0]) xConnector_wBearing(top=true);
rotate([0, 0, 180]) translate([-140,140,0]) xConnector_wBearing();
translate([140,0,0]) treaded_rod();

rotate([0, 0,   0]) translate([-140,140,0]) xConnector_wBearing(top=true);
rotate([0, 0, 180]) translate([140,140,0]) xConnector_wBearing();
translate([-140,0,0]) treaded_rod();


pully_dummy();; 