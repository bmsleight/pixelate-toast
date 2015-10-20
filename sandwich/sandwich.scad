include <lasercut.scad>; 

// http://www.thingiverse.com/thing:697243
include <sg90.scad>;

include <arms_and_poker.scad>;

$fn=60;
thickness=3.1;

// top gap, window, offset for arm, half of server 
// remeber top gap need to allow for big bread
overall_x = 120;
overall_y = 30+100+50+12.6/2;
window_x = 100;
window_y = 100;

toast_thick = 20; //14 + 6mm space

squeeze_x = 120;
squeeze_y = 150-5;
location_y = 50+12.6/2-20;

circles_remove_cables = [
                [thickness, overall_x/2, (overall_y + location_y)/2],
                [thickness/2, overall_x/2 - squeeze_x/2 + 10, (overall_y + location_y)/2- squeeze_y/2 + 10],
                [thickness/2, overall_x/2 - squeeze_x/2 + 10, (overall_y + location_y)/2 +squeeze_y/2 - 10],
                [thickness/2, overall_x/2 + squeeze_x/2 - 10, (overall_y + location_y)/2- squeeze_y/2 + 10],
                [thickness/2, overall_x/2 + squeeze_x/2 - 10, (overall_y + location_y)/2 +squeeze_y/2 - 10],
                // Half way of the above
                [thickness/2, overall_x/2 - squeeze_x/4 + 10/2, (overall_y + location_y)/2- squeeze_y/4 + 10/2],
                [thickness/2, overall_x/2 - squeeze_x/4 + 10/2, (overall_y + location_y)/2 +squeeze_y/4 - 10/2],
                [thickness/2, overall_x/2 + squeeze_x/4 - 10/2, (overall_y + location_y)/2- squeeze_y/4 + 10/2],
                [thickness/2, overall_x/2 + squeeze_x/4 - 10/2, (overall_y + location_y)/2 +squeeze_y/4 - 10/2],
                
                ];
                
circles_remove_cables_squeeze = [
                [thickness/2, 10, 10],
                [thickness/2, 10, squeeze_y - 10],
                [thickness/2, squeeze_x - 10, 10],
                [thickness/2, squeeze_x - 10, squeeze_y - 10],
                ];
                
sg90_pair_mount_holes_remove = [
                [1,17.25,6.3],
                [1,45.50,6.3],                
                // 2nd Servo
                [1,74.5,6.3],                
                [1,74.5+28.25,6.3],                
                ];


module topPlate()
{
    lasercutoutSquare(thickness=thickness, x=overall_x, y=overall_y,
        cutouts = [[10,50+12.6/2,100,100]],
        captive_nuts=[
            [DOWN, overall_x/2, 0],
            [UP, overall_x/5, overall_y],
            [UP, overall_x-overall_x/5, overall_y],
            ],
        circles_remove = circles_remove_cables
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
                ],
            captive_nut_holes=[
                [LEFT,overall_x/2,overall_y-42]
                ],
            simple_tab_holes=[
                [MID,overall_x/2-thickness,overall_y-42-thickness*5]
                ],
            circles_remove = concat(circles_remove_cables, sg90_pair_mount_holes_remove)
    ); 
}

module squeezePlate()
{
    // Remeber bread has to fit on this plate
    // includign the pillar used to lift
    // Size of bread - http://pt.barwap.com/size-of-bread.html
    // 140mm by 110mm by 14mm.
    translate([0,location_y+2.5,-toast_thick]) //dont ask me why +2.5
        lasercutoutSquare(thickness=thickness, x=squeeze_x, y=squeeze_y,
                circles_remove = circles_remove_cables_squeeze
        ); 
}

module liftSupport()
{
    translate([overall_x/2+thickness,overall_y-42-thickness*6,15+thickness]) 
        {
            rotate([90,0,90]) 
                lasercutoutSquare(thickness=thickness, x=61, y=20,
                    cutouts = [
                            [32,0,24.5,12.7]
                        ],
                    slits=[
                            [DOWN,thickness*3/2,0,10]
                        ],
                    captive_nuts=[
                            [DOWN, thickness*6, 0]
                        ],
                    circles_remove = [
                        [1, 30, 6],
                        [1, 30+28.5, 6]

                        ]
                );
            translate([-thickness*4, thickness*2, 0]) rotate([90,0,0]) 
                liftSupportBeam();
        }
}

module liftSupportBeam()
{
    lasercutoutSquare(thickness=thickness, x=thickness*6, y=30,
        simple_tabs=[
                [DOWN, thickness*5/2,0]
            ],
        slits=[
                [UP,thickness*9/2,30,20],
                [UP,thickness*4/2,30,thickness]
            ]
        );
}



module leg()
{
    lasercutoutSquare(thickness=thickness, x=thickness*12, y=toast_thick+15+thickness*2+10,
            captive_nut_holes=[
                [UP,thickness*12/2,(toast_thick+15+thickness*2+10)],
                [UP,thickness*12/2,(toast_thick+thickness*2+10)]
                ]
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
    translate([overall_x/2+25,overall_y-thickness-1.7,18]) rotate([90,0,270]) servoSG90();
}

color("Khaki",0.5)
{
    topPlate();
    bottomPlate();
    squeezePlate();
    liftSupport();
    legs();
    translate([-150,0,0]) rotate([0,0,90]) arm();
}

servoXY();

//TO DO SERVER MOUNTING SCREWS