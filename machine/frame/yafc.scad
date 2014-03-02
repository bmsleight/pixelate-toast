
$fn=60;
radius_tr = 6/2;
sl = 300;
sxl =  500;
wt = 3.2;


module yafc(ang=0) 
{
    r = radius_tr;
    hyp = sqrt(r*3*r*3*2);
    rotate([ang,0,0]) difference() 
    {
        hull() 
        {
            translate([r*9, r*9, 0])  cylinder(h=r*2, r=r*3, center=true);
            translate([hyp/2-r, hyp/2-r, 0])  cube([hyp, hyp, r*2], center=true);
        }
#    translate([r*9, r*9, 0])  cylinder(h=r*8, r=r, center=true);

    }
}

module connector() 
{
    translate([-radius_tr*9, -radius_tr*9, radius_tr*9]) 
    {
        rotate([0,0,0])  yafc() ;
        rotate([0,90,0])  yafc() ;
        rotate([-90,0,0]) yafc() ;
    }
}



module connector_center() 
{
    translate([-radius_tr*9, -radius_tr*9, radius_tr*9]) 
    {
        rotate([0,0,0])  yafc() ;
        rotate([0,90,0])  yafc() ;
        translate([0, 0, -radius_tr]) rotate([-90,0,0]) yafc(ang=-45) ;
    }
}

connector();

//connector_center();

