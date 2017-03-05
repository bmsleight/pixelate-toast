
cell_size = 15;
hole = 10;
cells = 3;
marble = 8;

top_thickness = 2.0;
$fn=50;

base_layer = 1;
bottom_layer =  + marble + 2;
slot_width_gap = cell_size - 2;
slot_width = slot_width_gap - 1;
slot_height_gap = 3;
slot_height = 2;

sliders_layer = 1 + slot_height_gap + 1 + slot_height_gap + 1;
interface_layer = top_thickness;
top_layer = marble/2 - 1;

total_height = base_layer + bottom_layer + sliders_layer + top_layer;


module block()
{
    cube([(cells) * cell_size, (cells) * cell_size, total_height], center=true);
}

module channels()
{
    for (x =[0:cells-1])
    {
        for (y =[0:cells-1])
        {
            translate([+cell_size/2 - cells*0.5*cell_size,0,0 ]) 
            translate([0, +cell_size/2 - cells*0.5*cell_size,0 ]) 
            translate([cell_size*x,cell_size*y,0]) cylinder(h=total_height*2, d=hole, center=true);
        }
    }
}


module slots()
{
    for (x =[0:cells-1])
    {
        translate([+cell_size/2 - cells*0.5*cell_size,0,0 ]) 
        translate([cell_size*x,0,0 ]) 
        translate([0,0,total_height/2 - slot_height_gap/2 - top_layer - 1]) 
        cube([slot_width_gap, (cells+1) * cell_size, slot_height_gap], center=true);
    }
    for (y =[0:cells-1])
    {
        translate([0, +cell_size/2 - cells*0.5*cell_size,0 ]) 
        translate([0, cell_size*y,0 ]) 
        translate([0,0,total_height/2 - slot_height_gap/2 - top_layer - 1 - slot_height_gap -1 ]) 
        cube([(cells+1) * cell_size, slot_width_gap, slot_height_gap], center=true);
    }

}

module truss()
{
    color("blue") difference() 
    {
        cube([slot_width, (cells+1.5) * cell_size, slot_height], center=true);
        union()
        {
            for (y =[0:cells-1])
            {
                translate([0, +cell_size/2 - cells*0.5*cell_size,0 ]) 
                translate([0, cell_size*y,hole/2.5 ]) 
                {
                    resize([hole,hole*2,hole]) sphere(d=hole,center=true);
                    cylinder(h=hole*2, d=hole, center=true);
                }
            }
        }
    }
}


module base()
{
    translate([0,0,-total_height/2 + base_layer/2])
    cube([(cells) * cell_size, (cells) * cell_size, base_layer], center=true);
}


module mainBlock()
{
    difference() 
    {
        block();
        channels();
        slots();
    }
    base();
}

module pin()
{
    translate([0,0,marble/4]) cylinder(h=marble/2, d=marble, center=true);
    translate([0,0,0]) sphere(d=marble, center=true);
}


!mainBlock();
translate([0,cell_size/2,total_height/2 - slot_height_gap/2 - top_layer - 1]) truss();
*pin();