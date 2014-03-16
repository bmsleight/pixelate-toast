$fn=60;
include <variables.scad>;

module treaded_rod(radius_tr = 6/2, length=300)
{
  color("DarkGray") 
  {
      rotate([90,0,0])  cylinder(h=length, r=radius_tr, center=true);
  }
}

module bearing()
{
  color("DarkGray") 
  {
    difference() 
    {
      rotate([90,0,0])  cylinder(h=bearing_t*1.05, r=bearing_os, center=true);  // 1.05 to make it render nice
      rotate([90,0,0])  cylinder(h=bearing_t*2, r=radius_tr, center=true);
    }
  }
}


treaded_rod();

!translate([0, radius_tr, ( bread_h)/2]) bearing();