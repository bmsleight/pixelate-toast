$fn=60;
radius_tr = 6/2;
sl = 300;
sxl =  500;
wt = 3.2;

connector_offset = 20;

co = connector_offset;

//Used for loops
sl_f = -sl/2-radius_tr*2;
sl_i = sl+radius_tr*4;
sl_t = sl/2+radius_tr*2;
sxl_f = -sxl/2-radius_tr*2;
sxl_i = sxl+radius_tr*4;
sxl_t = sxl/2+radius_tr*2;


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




 
    for ( y = [sl_f : sl_i: sl_t] )
    {
        for ( z = [sl_f : sl_i: sl_t] )
        {
           screwbase([0, y, z], [0,90,0], h=sxl);
        }
    }

    for ( x = [sxl_f : sxl_i: sxl_t] )
    {
        screwbase([x, -sl/2-radius_tr*2, 0], [0,0,90], h=sl);
    }


    for ( x = [sxl_f : sxl_i: sxl_t] )
    {
        screwbase([x, sl/2+radius_tr*2, (sxl-sl)/2], [0,0,90], h=sxl);
    }

    for ( x = [sxl_f : sxl_i: sxl_t]  )
    {
        for ( z = [sl_f : sl_i: sl_t] )
        {
            screwbase([x, 0, z], [90,0,0]);
        }
    }
}

module frame_ramp()
{
    screwbase(t = [sxl_f,sl_f,radius_tr*4], a=[0,0,90], h=sl);
    screwbase(t = [sxl_t,sl_f,radius_tr*4], a=[0,0,90], h=sl);

    screwbase(t = [sxl/2,0,0], a=[45,0,0], h=sxl);
    screwbase(t = [-sxl/2,0,0], a=[45,0,0], h=sxl);

    screwbase(t = [0,-sl/2,sl/2], a=[0,90,0], h=sxl);

    // Top of backing board
    screwbase([0, -cos(45)*(sl/4), cos(45)*(sl/4)], [0,90,0], h=sxl);

    //Diaganal stuts to support z-motor
    screwbase(t = [sxl/2,(sl/2-sl/3),-sl/(3*2)], a=[-45,0,0], h=sl);
    screwbase(t = [-sxl/2,(sl/2-sl/3),-sl/(3*2)], a=[-45,0,0], h=sl);

   // screwbase(t = [0,sl/2,-sl/2], a=[0,90,0], h=sxl);
    screwbase(t = [0,sl/2-sl/(3*2),0], a=[0,90,0], h=sxl);
    screwbase(t = [0,sl/2,sl/2-sl/3], a=[0,90,0], h=sxl);

}


// m6 Width Across Corners 11.05
module yafc(ang=0) 
{
    r = radius_tr;
    hyp = sqrt(r*3*r*3*2);
    rotate([0,ang,0]) difference() 
    {
        hull() 
        {
            translate([r*9, r*9, 0])  cylinder(h=r*2, r=r*3, center=true);
            translate([hyp/2-r, hyp/2-r, 0])  cube([hyp, hyp, r*2], center=true);
        }
    translate([r*9, r*9, 0])  cylinder(h=r*24, r=r*1.25, center=true);

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


module connector() 
{
    rotate([90,0,0]) translate([-radius_tr*9, -radius_tr*9, radius_tr*9]) 
    {
        rotate([0,0,0])  yafc() ;
        rotate([0,90,0])  yafc() ;
        rotate([-90,0,0]) yafc() ;
    }
}


module double_flat_connector()
{
    shift= ((radius_tr*2)*2)*2.25;
        connector();
    mirror([ 1, 0, 0 ]) connector();
}


module double_angled_connector()
{
    shift= ((radius_tr*2)*2)*2.25;
        connector_angled_a();
     rotate([180,0,180]) mirror([0,1,0]) connector();
}



module connector_angled_a() 
{
    translate([-radius_tr*9, -radius_tr*9, radius_tr*9]) 
    {
        rotate([0,0,0])  yafc() ;
        rotate([0,90,0])  yafc() ;
        translate([radius_tr, radius_tr/2, 0]) rotate([-90,0,0]) yafc(ang=-45	) ;
    }
}


module floor_connectors() 
{
//    translate([-sxl/2,-sl/2-6,-sl]) rotate([180,90,0]) connector();
//[sxl_f,sl_f,-sl-radius_tr*2]

    translate([sxl_f,sl_f,-sl-radius_tr*2]) rotate([180,90,0]) connector();
    translate([sxl_t,sl_f,-sl-radius_tr*2]) rotate([180,90,90]) connector();
    translate([sxl_t,sl_t,-sl-radius_tr*2]) rotate([180,90,180]) connector();
    translate([sxl_f,sl_t,-sl-radius_tr*2]) rotate([180,90,270]) connector();
}

module mid_connectors() 
{
//    translate([0,0, -sl]) rotate([0,180,0]) floor_connectors();

    translate([sxl_f,sl_f,radius_tr*2]) rotate([180,90,0]) double_flat_connector();
    translate([sxl_t,sl_f,radius_tr*2]) rotate([180,90,90]) double_flat_connector();

    translate([sxl_t,sl_t,radius_tr*2]) rotate([180,90,0]) double_angled_connector();

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
    floor_connectors();
    mid_connectors();
}

//  The top left
//rotate([0,90,180]) connector_angled_a();



//connector();

frame();