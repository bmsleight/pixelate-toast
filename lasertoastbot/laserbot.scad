include <lasercut.scad>; 
include <motor.scad>; 
include <bearing.scad>; 

thickness=3.1;
bearing_center_x = 0;
bearing_center_y = 0;
bearing_center_z = 48;
bearing_offset_x = 20;
bearing_offset_y = 20;

bottom_standoff_h = 20;
bottom_standoff_w = 80;
//bottom_standoff_x = bearing_center_x - bottom_standoff_w/2;
bottom_standoff_x = bearing_center_x - bottom_standoff_w/2;
bottom_standoff_y = bearing_center_y - bearing_offset_x - thickness;
bottom_standoff_z = 0;
bottom_standoff_offset_y = 50;

bottom_side_h = 125;
bottom_side_w = 40;
bottom_side_x = 0;
bottom_side_y = 0;
bottom_side_z = 0;

bearing_plate_w = bottom_standoff_w;
bearing_plate_h = bottom_side_h;


module bottomStandoffs()
{
    translate([bottom_standoff_x, bottom_standoff_y, bottom_standoff_z] ) 
   { 
       bottomStandoff();
       translate([0, bottom_side_h-thickness*3, 0])  bottomStandoff();
   }
}

module bottomSides()
{
    translate([-bottom_standoff_x-thickness, bottom_standoff_y-thickness*2, bottom_standoff_z] ) 
        {
            bottomSide();
            translate([-bottom_standoff_w+thickness*3, 0, 0]) bottomSide();
        }
}

module bottomStandoff()
{
    rotate([90,0,0]) 
        lasercutoutSquare(thickness=thickness, x=bottom_standoff_w, y=bottom_standoff_h,
//        captive_nuts=[[UP, 100/2, bottom_standoff_h] ], 
        slits = [
            [UP, thickness*1.5, bottom_standoff_h, bottom_standoff_h/2],
            [UP, bottom_standoff_w-thickness*1.5, bottom_standoff_h, bottom_standoff_h/2],
            ]
    );   
}

module bottomSide()
{
    rotate([0, -90,0]) 
        lasercutoutSquare(thickness=thickness, x=bottom_side_w, y=bottom_side_h,
        slits = [
            [LEFT, 0, thickness*1.5, bottom_standoff_h/2],
            [LEFT, 0, bottom_side_h-thickness*1.5, bottom_standoff_h/2],
            ],
        captive_nuts=[
                [RIGHT, bottom_side_w, bearing_plate_h/4],
                [RIGHT, bottom_side_w, bearing_plate_h*3/4],
            ]
    );   
}

module bearingPlate()
{
    translate([-bottom_standoff_w/2, bottom_standoff_y - thickness*2 , bottom_side_w]) rotate([0, 0,0]) 
        lasercutoutSquare(thickness=thickness, x=bearing_plate_w, y=bearing_plate_h,        
        captive_nut_holes=[
            [LEFT, 0, bearing_plate_h/4],
            [LEFT, 0, bearing_plate_h*3/4],
            [RIGHT, bearing_plate_w, bearing_plate_h/4],
            [RIGHT, bearing_plate_w, bearing_plate_h*3/4]    
            ]
    );   
}


module bearings()
{
    for (x = [bearing_center_x - bearing_offset_x, bearing_center_x + bearing_offset_x])
    {
        for (y = [bearing_center_y - bearing_offset_y, bearing_center_y + bearing_offset_y])
        {
            translate([x,y, bearing_center_z]) bearing();
        }        
    }               
}


bearings();
bottomStandoffs();
bottomSides();
bearingPlate();
