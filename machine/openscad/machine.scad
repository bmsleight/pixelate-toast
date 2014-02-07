
$fn=60;
back_plate_size = 150;
top_holder_length = 50;
wood_thickness = 5;

minimum_thickness = 5;
connector = 10;

whole_machine();

module back_plate() {
    color("Sienna") {
        difference() {
            cube(size = [back_plate_size, wood_thickness, back_plate_size], center = true);
        mirror([ 0, 0, 0 ]) translate([back_plate_size/2  - connector, 0, back_plate_size/2 - connector*2]) holes_connector();
        mirror([ 1, 0, 0 ]) translate([back_plate_size/2  - connector, 0, back_plate_size/2 - connector*2]) holes_connector();
        translate([0, 0, back_plate_size/2 - connector]) rotate([0, 90, 0]) holes_connector();
        }
    }
}

module top_holder(c_size = connector) {
    color("Blue") translate([0, connector/2, back_plate_size/2 + connector/2]) {
        rotate([0, 180, 90]) {
            difference() {
                precursor_simple_connector(connector,0);
                translate([17.5, 0, 0]) cube(20, center = true);
            }
            translate([wood_thickness, 0, 0]) cube(size = [wood_thickness, top_holder_length, 10], center = true);
        }
        rotate([0, -90, 0]) {
            mirror([ 0, 0, 0 ]) translate([-connector/2, wood_thickness/2, top_holder_length/2-connector/2])  precursor_simple_connector(connector);
            mirror([ 0, 0, 1 ]) translate([-connector/2, wood_thickness/2, top_holder_length/2-connector/2])  precursor_simple_connector(connector);
        }
    }
}


module side_connectors() {
    mirror([ 1, 0, 0 ]) translate([-back_plate_size/2, 7.5, back_plate_size/2 - connector*2]) simple_connector(connector, 1);
    mirror([ 0, 0, 0 ]) translate([-back_plate_size/2, 7.5, back_plate_size/2 - connector*2]) simple_connector(connector, 1);

}



module holes_connector(c_size = connector) {
    rotate([90, 0, 0]) {
        translate([c_size/2, 0, 0])       cylinder(h = c_size*2, r=c_size/4, center = true);
        translate([c_size/2, c_size, 0])  cylinder(h = c_size*2, r=c_size/4, center = true);
        translate([c_size/2, -c_size, 0]) cylinder(h = c_size*2, r=c_size/4, center = true);
    }
}



module simple_connector(c_size = connector, side_pins = 1) {
    color("Blue") {
        difference() {
            union() {
                precursor_simple_connector(c_size);
                if (side_pins == 1)  {
                    precursor_simple_connector_side_pins(c_size);
                }
            }
            translate([c_size/2, 0, 0]) rotate([90, 0, 0]) cylinder(h = c_size*2, r=c_size/4, center = true);
        }
    }
}

module precursor_simple_connector(c_size, side_pins) {
    difference() {
        hull() {
            translate([c_size/2,0,0]) cube(c_size, center = true);
            translate([-c_size/2,0,0]) rotate([90, 0, 0]) cylinder(h = c_size, r=c_size/2, center = true);
        }
        translate([-c_size/2,0,0]) rotate([90, 0, 0]) cylinder(h = c_size*2, r=c_size/4, center = true);
    }
}

module precursor_simple_connector_side_pins(c_size) {
    hull() {
        translate([c_size/2, 0, c_size]) rotate([90, 0, 0]) cylinder(h = c_size, r=c_size/4, center = true);
        translate([c_size/2, 0, -c_size]) rotate([90, 0, 0]) cylinder(h = c_size, r=c_size/4, center = true);
    }
    translate([c_size/2, -c_size/2, c_size]) rotate([90, 0, 0]) cylinder(h = c_size*2, r=c_size/4, center = true);
    translate([c_size/2, -c_size/2, -c_size]) rotate([90, 0, 0]) cylinder(h = c_size*2, r=c_size/4, center = true);
}




module whole_machine() {
	 back_plate();
    top_holder();
    side_connectors();

    
//    holes_connector();
    
    
}


