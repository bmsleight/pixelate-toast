include <variables.scad>;
use <metal-parts.scad>;

module flat_sub_connector()
{

  difference()
  {
    cube([c_height+radius_tr*9, radius_tr*4, radius_tr*2], center=true);
    translate([(c_height+radius_tr*8)/2-radius_tr*2, 0, 0]) rotate([0,0,0]) cylinder(h=radius_tr*80, r=radius_bolt*1.05, center=true);
    translate([-(c_height+radius_tr*8)/2+radius_tr*2, 0, 0]) rotate([0,0,0]) cylinder(h=radius_tr*80, r=radius_bolt*1.05, center=true);
//     cube([c_height-radius_tr*1, radius_tr*8, radius_tr*4], center=true);
  }
}

module xConnector()
{

  translate([0, radius_tr, 0]) difference() 
  {
    cube([c_height, radius_tr*2, c_height + bread_h], center=true);
   translate([0, 0, 0]) rotate([90,0,0]) cylinder(h=radius_tr*8, r=bearing_os*1.05, center=true);
//    translate([0, 0, ( c_height + bread_h)/-2]) cube([c_height/2, radius_tr*4, (c_height + bread_h)/1.5], center=true);
    translate([0, 0, (c_height + bread_h)/-2+radius_tr*3]) cube([radius_tr*4, radius_tr*4, radius_bolt*2], center=true);

  }
  translate([0, -radius_tr, 0]) difference() 
  {
    cube([c_height, radius_tr*2, c_height + bread_h], center=true);
    translate([0, 0, 0]) rotate([90,0,0]) cylinder(h=radius_tr*8, r=radius_tr*1.25, center=true);
    translate([0, 0, (c_height + bread_h)/-2+radius_tr*3]) cube([radius_tr*4, radius_tr*4, radius_tr*2], center=true);
  }

  translate([0, radius_tr*2.25, 0]) difference() 
  {
    cube([c_height, radius_tr*4.5, (c_height+radius_tr*2)/2], center=true);
    cube([bearing_os*2.2, c_height+radius_tr*4, radius_tr*12], center=true);
   translate([0, radius_tr*0.5, 0]) rotate([90,0,90]) cylinder(h=radius_tr*12, r=radius_bolt*1.05, center=true);
  }
  translate([0, radius_tr*0, (c_height + bread_h)/-2+radius_tr*1]) 
  {
    flat_sub_connector();
  }

  translate([0, radius_tr*0, (c_height + bread_h)/+2])  
  {
    flat_sub_connector();
  }

}

module double_flat_sub_connector()
{
  flat_sub_connector();
  translate([0, 0, radius_tr*2]) flat_sub_connector();
}


module bearing_connect()
{
  difference()
  {
    double_flat_sub_connector();
    cube([bearing_os*2+radius_tr*4, radius_tr*6, radius_tr*4], center=true);
  }
  translate([0, 0, radius_tr*2.]) difference()
  {
    cube([bearing_os*2+radius_tr*5, radius_tr*4, radius_tr*2], center=true);
  }
  translate([0, 0, radius_tr*1])  cylinder(h=radius_tr*4, r=radius_tr*0.975, center=true);
}


module xConnector_wBearing()
{
  translate([0, radius_tr, ( bread_h)/2]) bearing();
  xConnector();
}

//xConnector_wBearing();

//rotate([0,180,0]) bearing_connect();
//rotate([90,0,0]) bearing();

//Printing
rotate([90,0,0])   xConnector();