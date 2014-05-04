include <variables.scad>;

module bearing_LM6UU()
{
  color("grey") rotate([0,90,0]) difference()
  {
    cylinder(h=linear_bearing_len,r=linear_bearing_or, center=true);
    cylinder(h=linear_bearing_len*2,r=linear_bearing_ir, center=true);
  }
}


module bearing_thin()
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
