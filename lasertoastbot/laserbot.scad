include <lasercut.scad>; 
include <motor.scad>; 
include <bearing.scad>; 

thickness=3.1;
bearing_center_x = 0;
bearing_center_y = 0;
bearing_center_z = 48-5;
bearing_offset_x = 20;
bearing_offset_y = 20;

bottom_standoff_h = 20;
bottom_standoff_w = 80;
bottom_standoff_x = bearing_center_x - bottom_standoff_w/2;
bottom_standoff_y = bearing_center_y - bearing_offset_x - thickness;
bottom_standoff_z = 0;
bottom_standoff_offset_y = 50;

bottom_side_h = 115;
bottom_side_w = 35;
bottom_side_x = 0;
bottom_side_y = 0;
bottom_side_z = 0;

bearing_plate_w = bottom_standoff_w;
bearing_plate_h = bottom_side_h;
bearing_cutout_w = 19;
bearing_cutout_h = 7;

lower_motor_x = 0-42/2;
lower_motor_y = 34;

toast_plate_w = 200;
toast_plate_h = 85;
toast_plate_x = -toast_plate_w/2;
toast_plate_y = -toast_plate_h/2;
x_rods_length = toast_plate_w - 15;
x_rods_diameter = 6;


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
    cutouts_centre_x = bearing_offset_x+bearing_cutout_w/2 +1; // where 1 is a bodge
    cutouts_centre_y = bearing_offset_y +bearing_cutout_h/2 + 2.5; // where 1 is a bodge
    tie_w = 5;
    tie_h = 2;
    tie_ou = 9;
    tie_od = 4;
    translate([-bottom_standoff_w/2, bottom_standoff_y - thickness*2 , bottom_side_w]) rotate([0, 0,0]) 
        lasercutoutSquare(thickness=thickness, x=bearing_plate_w, y=bearing_plate_h,        
        captive_nut_holes=[
            [LEFT, 0, bearing_plate_h/4],
            [LEFT, 0, bearing_plate_h*3/4],
            [RIGHT, bearing_plate_w, bearing_plate_h/4],
            [RIGHT, bearing_plate_w, bearing_plate_h*3/4],   
            ],
        cutouts = [
            [  cutouts_centre_x+bearing_offset_x,  cutouts_centre_y+bearing_offset_y, bearing_cutout_w, bearing_cutout_h],
            [  cutouts_centre_x-bearing_offset_x,  cutouts_centre_y+bearing_offset_y, bearing_cutout_w, bearing_cutout_h],
                [  cutouts_centre_x+bearing_offset_x,  cutouts_centre_y-bearing_offset_y, bearing_cutout_w, bearing_cutout_h],
                [  cutouts_centre_x-bearing_offset_x,  cutouts_centre_y-bearing_offset_y, bearing_cutout_w, bearing_cutout_h],
    // Tie clips
                [  cutouts_centre_x-bearing_offset_x+(bearing_cutout_w-tie_w)/2,  cutouts_centre_y-bearing_offset_y + tie_ou, tie_w, tie_h],
                [  cutouts_centre_x-bearing_offset_x++(bearing_cutout_w-tie_w)/2,  cutouts_centre_y-bearing_offset_y - tie_od, tie_w, tie_h],
                [  cutouts_centre_x+bearing_offset_x+(bearing_cutout_w-tie_w)/2,  cutouts_centre_y-bearing_offset_y + tie_ou, tie_w, tie_h],
                [  cutouts_centre_x+bearing_offset_x++(bearing_cutout_w-tie_w)/2,  cutouts_centre_y-bearing_offset_y - tie_od, tie_w, tie_h],
                [  cutouts_centre_x-bearing_offset_x+(bearing_cutout_w-tie_w)/2,  cutouts_centre_y+bearing_offset_y + tie_ou, tie_w, tie_h],
                [  cutouts_centre_x-bearing_offset_x++(bearing_cutout_w-tie_w)/2,  cutouts_centre_y+bearing_offset_y - tie_od, tie_w, tie_h],
                [  cutouts_centre_x+bearing_offset_x+(bearing_cutout_w-tie_w)/2,  cutouts_centre_y+bearing_offset_y + tie_ou, tie_w, tie_h],
                [  cutouts_centre_x+bearing_offset_x++(bearing_cutout_w-tie_w)/2,  cutouts_centre_y+bearing_offset_y - tie_od, tie_w, tie_h],
        ],
        circles_remove = [
                [14,bearing_plate_w/2, 85],
                [2.5,bearing_plate_w/2-34.2/2, 85-34.2/2],
                [2.5,bearing_plate_w/2+34.2/2, 85-34.2/2],
                [2.5,bearing_plate_w/2-34.2/2, 85+34.2/2],
                [2.5,bearing_plate_w/2+34.2/2, 85+34.2/2],
                ]
    );
}

module toastPlate()
{
    diff = toast_plate_w - x_rods_length;
    tie_w = 5;
    tie_h = 2;

    translate([toast_plate_x, toast_plate_y , bearing_center_z-thickness/2]) rotate([0, 0,0]) 
        lasercutoutSquare(thickness=thickness, x=toast_plate_w, y=toast_plate_h,
            cutouts = [
               [(diff )/2, (toast_plate_h-x_rods_diameter-1)/2-bearing_offset_y,x_rods_length, x_rods_diameter+1],
               [(diff )/2, (toast_plate_h-x_rods_diameter-1)/2+bearing_offset_y,x_rods_length, x_rods_diameter+1],
               [(diff +diff )/2, (toast_plate_h-x_rods_diameter*2.5)/2+bearing_offset_y,x_rods_length-diff , x_rods_diameter*2.5],
               [(diff +diff )/2, (toast_plate_h-x_rods_diameter*2.5)/2-bearing_offset_y,x_rods_length-diff , x_rods_diameter*2.5],

      // Cable ties holes
               [(diff  )/2, (toast_plate_h-x_rods_diameter*2.5)/2-bearing_offset_y,tie_w , tie_h],
               [(diff  )/2, (toast_plate_h+x_rods_diameter*2.5 - tie_h*2)/2-bearing_offset_y,tie_w , tie_h],
               [(diff  )/2+x_rods_length-tie_w, (toast_plate_h-x_rods_diameter*2.5)/2-bearing_offset_y,tie_w , tie_h],
               [(diff  )/2+x_rods_length-tie_w, (toast_plate_h+x_rods_diameter*2.5)/2-bearing_offset_y,tie_w , tie_h],
      // Cable ties holes
               [(diff  )/2, (toast_plate_h-x_rods_diameter*2.5)/2+bearing_offset_y,tie_w , tie_h],
               [(diff  )/2, (toast_plate_h+x_rods_diameter*2.5 - tie_h*2)/2+bearing_offset_y,tie_w , tie_h],
               [(diff  )/2+x_rods_length-tie_w, (toast_plate_h-x_rods_diameter*2.5)/2+bearing_offset_y,tie_w , tie_h],
               [(diff  )/2+x_rods_length-tie_w, (toast_plate_h+x_rods_diameter*2.5)/2+bearing_offset_y,tie_w , tie_h],
        ]
    
    
    );
}

module bearings()
{
    for (y = [bearing_center_y - bearing_offset_y, bearing_center_y + bearing_offset_y])
    {
        for (x = [bearing_center_x - bearing_offset_x, bearing_center_x + bearing_offset_x])
        {
            translate([x,y, bearing_center_z]) bearing();
        }        
        translate([0,y, bearing_center_z]) rotate([0,90,0]) color("silver") cylinder(h = x_rods_length, d=x_rods_diameter,  center = true);
    }               
}

module lowerMotor()
{
    translate([lower_motor_x, lower_motor_y, 0]) 
    {
        nema17();
        cog_d = 25;
        translate([42/2,42/2,bearing_center_z-thickness/2]) cylinder(h=thickness, d=cog_d );
    }
}



bearings();
bottomStandoffs();
bottomSides();
bearingPlate();
//lowerMotor();
toastPlate();
