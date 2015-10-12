include <lasercut.scad>; 

// http://www.thingiverse.com/thing:697243
include <sg90.scad>;

thickness=3.1;

// top gap, window, offset for arm, half of server 
// remeber top gap need to allow for big bread
overall_x = 120;
overall_y = 30+100+50+12.6/2;
window_x = 100;
window_y = 100;

toast_thick = 20; //14 + 6mm space





module topPlate()
{
    lasercutoutSquare(thickness=thickness, x=overall_x, y=overall_y,
        cutouts = [[10,50+12.6/2,100,100]],
            captive_nuts=[
                [DOWN, overall_x/2, 0],
                [UP, overall_x/5, overall_y],
                [UP, overall_x-overall_x/5, overall_y],
                ]
    ); 
}

module bottomPlate()
{
    translate([0,0,15])
        lasercutoutSquare(thickness=thickness, x=overall_x, y=overall_y,
            captive_nuts=[
                [DOWN, overall_x/2, 0],
                [UP, overall_x/5, overall_y],
                [UP, overall_x-overall_x/5, overall_y],
                ]
        ); 
}

module squeezePlate()
{
    // Remeber bread has to fit on this plate
    // includign the pillar used to lift
    // Size of bread - http://pt.barwap.com/size-of-bread.html
    // 140mm by 110mm by 14mm.
    translate([0,50+12.6/2-20,-toast_thick])
        lasercutoutSquare(thickness=thickness, x=120, y=150-5
        ); 
}

module leg()
{
    lasercutoutSquare(thickness=thickness, x=thickness*12, y=toast_thick+15+thickness*2+10
        );
}

module legs()
{
    translate([overall_x/2-thickness*12/2,0,-toast_thick-10]) rotate([90,0,0]) leg();
    translate([overall_x/5-thickness*12/2,overall_y+thickness,-toast_thick-10]) rotate([90,0,0]) leg();
    translate([overall_x-overall_x/5-thickness*12/2,overall_y+thickness,-toast_thick-10]) rotate([90,0,0]) leg();
}

module servoXY()
{
    translate([20,12.6,22.8+15-1]) rotate([180,0,0]) servoSG90();
    translate([overall_x-20,0,22.8+15-1]) rotate([180,0,180]) servoSG90();
    translate([overall_x/2+17,overall_y-thickness*2,41]) rotate([0,90,180]) servoSG90();
}

color("Khaki",0.5)
{
    topPlate();
    bottomPlate();
    squeezePlate();
    legs();
}

servoXY();
