

$fn=60;
radius_tr = 6/2;
sl = 300;
sxl =  500;
wt = 3.2;

connector_offset = 20;

co = connector_offset;


module side(m=8)
{
  translate([0, 0, radius_tr*-m]) 
  {
    cube([radius_tr*m, radius_tr*m, radius_tr], center=true);
    cylinder(h=radius_tr*2*m, r=radius_tr*1.25, center=true);
    translate([0, 0, radius_tr*2.5]) cube([radius_tr*4, radius_tr*4, radius_tr], center=true);
  }
}

module loop(m=8)
{
  for ( t = [0 : 90 : 360] )
  {
    for ( s = [0 : 45 : 360] )
    {
      rotate([s, t, 0])  side(m);
    }
  }
}

module connector()
{
  m = 8;
  difference() 
  {
    sphere(radius_tr*(m));
    loop(m);
    sphere(radius_tr*(m-2));
    rotate([90, 0, 0]) translate([0, 0, radius_tr*-m*1.41]) cube([radius_tr*m*2, radius_tr*m*2, radius_tr*m*2], center=true);
  }
}


rotate([-90,0,0]) connector();