$fn=60;
radius_tr = 6/2;
sl = 300;
sxl =  500;
wt = 3.2;

module screwthread(h=sl, r=radius_tr, center=true) 
{
    color("DarkGray") cylinder(h=h, r=r, center=center);
}

module screwbase(t = [0,0,0], a = [0,0,0], h=sl, r=radius_tr, center=true)
{
    translate(t) rotate(a) screwthread(h=h, r=r, center=center);
}

module frame_base() 
{ 
    for ( y = [-sl/2 : sl : sl/2] )
    {
        for ( z = [-sl/2 : sl : sl/2] )
        {
            screwbase([0, y, z], [0,90,0], h=sxl);
        }
    }

    for ( x = [-sxl/2 : sxl : sxl/2] )
    {
        screwbase([x, -sl/2, 0], [0,0,90], h=sl);
    }


    for ( x = [-sxl/2 : sxl : sxl/2] )
    {
        screwbase([x, sl/2, 100], [0,0,90], h=sxl);
    }

    for ( x = [-sxl/2 : sxl : sxl/2] )
    {
        for ( z = [-sl/2 : sl : sl/2] )
        {
            screwbase([x, 0, z], [90,0,0]);
        }
    }
}

module frame_ramp()
{
    screwbase(t = [sxl/2,0,0], a=[45,0,0], h=sxl);
    screwbase(t = [-sxl/2,0,0], a=[45,0,0], h=sxl);
    screwbase(t = [-sxl/2,-sl/2,0], a=[0,0,90], h=sl);
    screwbase(t = [sxl/2,-sl/2,0], a=[0,0,90], h=sl);
    screwbase(t = [0,-sl/2,sl/2], a=[0,90,0], h=sxl);

    // Top of backing board
    screwbase([0, -cos(45)*(sl/4), cos(45)*(sl/4)], [0,90,0], h=sxl);

    //Diaganal stuts to support z-motor
    screwbase(t = [sxl/2,(sl/2-sl/3),-sl/(3*2)], a=[-45,0,0], h=sl);
    screwbase(t = [-sxl/2,(sl/2-sl/3),-sl/(3*2)], a=[-45,0,0], h=sl);

    screwbase(t = [0,sl/2,-sl/2], a=[0,90,0], h=sxl);
    screwbase(t = [0,sl/2-sl/(3*2),0], a=[0,90,0], h=sxl);
    screwbase(t = [0,sl/2,sl/2-sl/3], a=[0,90,0], h=sxl);

}


module base_plate()
{
    translate([0,sl/2-sl/3,sl/3])  rotate([-45,0,0]) cube([sl,sl,wt], center=true);
}


module frame ()
{
    translate([0,0,-sl/2]) frame_base();
    translate([0,0,sl/2]) frame_ramp();
    base_plate();
}

frame();