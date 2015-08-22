#! /usr/bin/env python
# -*- coding: utf-8 -*-

import lasercutmodel

thickness=3.1
laserbot = lasercutmodel.model(thickness=thickness, kerf = 0.2)

laserbot.add_square_cut_out("front stand", width=86, height=20, orientation=3, x_y_z_position=(0,2*thickness,0))
#Slots
laserbot.add_inner_cutout_square("front stand",  width=thickness, height=10, offset_x=thickness, offset_y=0)
laserbot.add_inner_cutout_square("front stand",  width=thickness, height=10, offset_x=86-2*thickness, offset_y=0)
# copy to back
laserbot.copy_laser_cut_out("front stand", "front stand 2", (0, 125-thickness,0)) 

hp_1 = 33

laserbot.add_square_cut_out("front stand side", width=hp_1, height=125, orientation=2, x_y_z_position=(86-thickness,0,0))
# Slots
laserbot.add_inner_cutout_square("front stand side",  width=10, height=thickness, offset_y=thickness, offset_x=0)
laserbot.add_inner_cutout_square("front stand side",  width=10, height=thickness, offset_y=125-2*thickness, offset_x=0)
# copy to back

laserbot.add_square_cut_out("bearing base", width=86, height=115, orientation=1, x_y_z_position=(0,0,hp_1))
laserbot.add_tab("bearing base", tab_type=2, x=thickness*1, y=40, tab_orientation="up")
laserbot.add_tab("front stand side", tab_type=1, x=hp_1, y=40, tab_orientation="right")
laserbot.add_tab("bearing base", tab_type=2, x=thickness*1, y=115-25, tab_orientation="up")
laserbot.add_tab("front stand side", tab_type=1, x=hp_1, y=115-25, tab_orientation="right")
laserbot.add_tab("bearing base", tab_type=2, x=86-thickness*2, y=hp_1, tab_orientation="up")
laserbot.add_tab("bearing base", tab_type=2, x=86-thickness*2, y=115-25, tab_orientation="up")
laserbot.copy_laser_cut_out("front stand side", "front stand side 2", (2*thickness,0,0))

#Motor Mounting
laserbot.add_circle_cut_out("bearing base", x=42, y=94, r=14)
laserbot.add_circle_cut_out("bearing base", x=42-33/2, y=94-33/2, r=3/2)
laserbot.add_circle_cut_out("bearing base", x=42+33/2, y=94-33/2, r=3/2)
laserbot.add_circle_cut_out("bearing base", x=42-33/2, y=94+33/2, r=3/2)
laserbot.add_circle_cut_out("bearing base", x=42+33/2, y=94+33/2, r=3/2)

#Bearing holes
bearing_offset_x = 47
bearing_offset_y = 40
laserbot.add_inner_cutout_square("bearing base", width=19, height=6, offset_x=8, offset_y=17)
laserbot.add_inner_cutout_square("bearing base", width=19, height=6, offset_x=8+bearing_offset_x, offset_y=17)
laserbot.add_inner_cutout_square("bearing base", width=19, height=6, offset_x=8, offset_y=17+bearing_offset_y)
laserbot.add_inner_cutout_square("bearing base", width=19, height=6, offset_x=8+bearing_offset_x, offset_y=17+bearing_offset_y)
#Bearing cable tie holes
laserbot.add_inner_cutout_square("bearing base", width=4, height=2, offset_x=8+bearing_offset_x+19/2, offset_y=17+bearing_offset_y-5)
laserbot.add_inner_cutout_square("bearing base", width=4, height=2, offset_x=8+bearing_offset_x+19/2, offset_y=17+bearing_offset_y+10)
laserbot.add_inner_cutout_square("bearing base", width=4, height=2, offset_x=8+bearing_offset_x+19/2, offset_y=17-5)
laserbot.add_inner_cutout_square("bearing base", width=4, height=2, offset_x=8+bearing_offset_x+19/2, offset_y=17+10)
laserbot.add_inner_cutout_square("bearing base", width=4, height=2, offset_x=8+19/2, offset_y=17+bearing_offset_y-5)
laserbot.add_inner_cutout_square("bearing base", width=4, height=2, offset_x=8+19/2, offset_y=17+bearing_offset_y+10)
laserbot.add_inner_cutout_square("bearing base", width=4, height=2, offset_x=8+19/2, offset_y=17-5)
laserbot.add_inner_cutout_square("bearing base", width=4, height=2, offset_x=8+19/2, offset_y=17+10)



#laserbot.add_square_cut_out("base plate", width=200, height=130, orientation=1, x_y_z_position=(-20,0,56))

'''
base_plate_width = 130
base_plate_height = 200
base_plate_z = 56

laserbot.add_square_cut_out("base plate", width=base_plate_width, height=base_plate_height, orientation=1, x_y_z_position=(0,0,56))
'''

laserbot.extra_scad = '''

module bearing()
{
    difference()
    {
        rotate([0,90,0]) color("orange") cylinder(h = 19, d=12,  center = false);
        translate([-1,0,0]) rotate([0,90,0]) color("orange") cylinder(h = 22, d=6,  center = false);
    }
}


//http://www.thingiverse.com/thing:84339
module stepperMotor(caseSize, caseHeight, holeSpacing, holeDiameter, shaftDiameter, shaftHeight, shaftCollarDiameter, shaftCollarThickness)
{
	
	//Mounting Hole Depth is predefined @ >= 4.5mm
	mountingHoleDepth = 4.5;

	union()
	{

		//Shaft
		//Note: We add 1mm and translate to -1 in Z to show shaft 
		//on bottom of motor
		translate([caseSize/2,caseSize/2,-1]) 
		cylinder(r=shaftDiameter/2, h=caseHeight+shaftHeight+1);	

		//Shaft collar
		translate([caseSize/2,caseSize/2,caseHeight]) 
		cylinder(r=shaftCollarDiameter/2, h=shaftCollarThickness);

		difference()
		{
			cube([caseSize, caseSize, caseHeight]);
		
			translate([(caseSize-holeSpacing)/2,(caseSize-holeSpacing)/2,caseHeight-mountingHoleDepth]) 
			cylinder(r=holeDiameter/2, h=mountingHoleDepth);

			translate([caseSize-((caseSize-holeSpacing)/2),(caseSize-holeSpacing)/2,caseHeight-mountingHoleDepth]) 
			cylinder(r=holeDiameter/2, h=mountingHoleDepth);

			translate([(caseSize-holeSpacing)/2,caseSize-((caseSize-holeSpacing)/2),caseHeight-mountingHoleDepth]) 
			cylinder(r=holeDiameter/2, h=mountingHoleDepth);

			translate([caseSize-((caseSize-holeSpacing)/2),caseSize-((caseSize-holeSpacing)/2),caseHeight-mountingHoleDepth]) 
			cylinder(r=holeDiameter/2, h=mountingHoleDepth);
		}
	}
	
}

//Predefined NEMA17 stepper motor
module nema17()
{
	color("silver") stepperMotor(42.1, 33.2, 31, 3, 5, 24, 22, 2);
}



#translate([ 8,20,41])  bearing();
translate([55,20,41])  bearing();
translate([ 8,60,41])  bearing();
#translate([55,60,41])  bearing();

*translate([21,73,0])  nema17();
'''

laserbot.rough_layout_2d()

laserbot.write_scad_file("laserbot.scad", text=False)
laserbot.write_scad_file("laserbot_2d.scad", three_d=False, text=False)
