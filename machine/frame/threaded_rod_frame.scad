$fn=60;
radius_tr = 6/2;
sl = 300;
sxl =  500;
wt = 3.2;

connector_offset = 20;

co = connector_offset;

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
    for ( y = [-sl/2+co : sl-co*2 : sl/2-co] )
    {
        for ( z = [-sl/2 : sl : sl/2] )
        {
           screwbase([0, y, z], [0,90,0], h=sxl);
        }
    }

    for ( x = [-sxl/2+co*2 : sxl-co*4 : sxl/2-co*2] )
    {
        screwbase([x, -sl/2+co*2, 0], [0,0,90], h=sl);
    }


    for ( x = [-sxl/2+co*2 : sxl-co*4 : sxl/2-co*2] )
    {
        screwbase([x, sl/2-co*2, (sxl-sl)/2], [0,0,90], h=sxl);
    }

    for ( x = [-sxl/2+co : sxl-co*2 : sxl/2-co] )
    {
        for ( z = [-sl/2+co : sl-co*2 : sl/2-co] )
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


module connector() {

    color("Blue",0.5)  difference() {
    cube([co*2,co*2,co*3], center=true);
    translate([co,co,-co*1.5])  cube([co*2,co*2,co*4], center=true);

    translate([-co*1.5,-co*1.5,-co])
    {
        screwbase([sxl/2, co, 0], [0,90,0], h=sxl, r=radius_tr*1.25);
        screwbase([+co, sxl/2, co], [90,0,0], h=sxl, r=radius_tr*1.25);
        screwbase([co*2, co*2,sxl/2+co], [0,0,90], h=sxl,r=radius_tr*1.25);
    }

    }

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
    translate([-sxl/2+co*1.5,-sl/2+co*1.5,-sl+co]) connector();
}

frame();