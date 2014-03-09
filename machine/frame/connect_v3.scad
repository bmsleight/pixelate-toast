

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

  for ( t = [45 : 90 : 360] )
  {
    for ( s = [0 : 90 : 360] )
    {
      rotate([s, t, 0])  side(m);
    }
  }


}


module connector_pre(simple=true, cuts=2)
{
  m = 8;
  if(simple==true)
  {
    difference() 
    {
      sphere(radius_tr*(m));
      rotate([90, 0, 0]) translate([0, 0, radius_tr*-m*1.41]) cube([radius_tr*m*2, radius_tr*m*2, radius_tr*m*2], center=true);
    }  
  }
  else
  {
    difference() 
    {
      sphere(radius_tr*(m));
      loop(m);
      sphere(radius_tr*(m-2));
      if(cuts>0)
      {
        rotate([90, 0, 0]) translate([0, 0, radius_tr*-m*1.41]) cube([radius_tr*m*2, radius_tr*m*2, radius_tr*m*2], center=true);
      }
      if(cuts>1)
      {
        rotate([0, 0, 90]) translate([0, 0, radius_tr*-m*1.41]) cube([radius_tr*m*2, radius_tr*m*2, radius_tr*m*2], center=true);      }
      if(cuts>2)
      {
        rotate([0, 90, 0]) translate([0, 0, radius_tr*-m*1.41]) cube([radius_tr*m*2, radius_tr*m*2, radius_tr*m*2], center=true);
      }
    }
  }
}


module connector(simple=true, cuts=2)
{
  if(cuts==1)
  {
    rotate([0,0,0]) connector_pre(simple=simple, cuts=cuts);
  }
  if(cuts==2)
  {
    rotate([135,0,0]) connector_pre(simple=simple, cuts=cuts);
  }
  if(cuts==3)
  {
    rotate([-90,135,0]) connector_pre(simple=simple, cuts=cuts);
  }

}

connector(simple=false, cuts=3);