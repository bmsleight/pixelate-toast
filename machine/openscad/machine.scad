
$fn=60;
back_plate_size = 150;
top_holder_length = 70;
wood_thickness = 5;
minimum_thickness = 5;
connector = 10;

top_clip_length = 30;


whole_machine();
//parts();

module back_plate() {
    color("Sienna") {
        difference() {
            cube(size = [back_plate_size, wood_thickness, back_plate_size], center = true);
        mirror([ 0, 0, 0 ]) translate([-back_plate_size/2 + connector*1.5, connector*.75, back_plate_size/2]) rotate([0,90,0])  holes_connector();
        mirror([ 1, 0, 0 ]) translate([-back_plate_size/2 + connector*1.5, connector*.75, back_plate_size/2]) rotate([0,90,0]) holes_connector();
        mirror([ 0, 0, 0 ]) translate([(top_holder_length - connector)/2, 0, back_plate_size/2-connector/2]) rotate([90, 0, 0])  cylinder(h = connector*2, r=connector/4, center = true);
        mirror([ 1, 0, 0 ]) translate([(top_holder_length - connector)/2, 0, back_plate_size/2-connector/2]) rotate([90, 0, 0])  cylinder(h = connector*2, r=connector/4, center = true);
        }
    }
}

module top_holder(c_size = connector) {
    color("Blue") translate([0, connector/2, back_plate_size/2 + connector/2]) {
        rotate([0, 180, 90]) {
            translate([0, 0, -connector]) precursor_simple_connector(connector,0, 5);
            translate([wood_thickness, 0, 0]) cube(size = [wood_thickness, top_holder_length, 10], center = true);
        }
        rotate([0, -90, 0]) {
            mirror([ 0, 0, 0 ]) translate([-connector/2, wood_thickness/2, top_holder_length/2-connector/2])  precursor_simple_connector(connector);
            mirror([ 0, 0, 1 ]) translate([-connector/2, wood_thickness/2, top_holder_length/2-connector/2])  precursor_simple_connector(connector);
        }
        translate([0, -wood_thickness, connector*1.25]) cube(size = [connector, wood_thickness, connector*3.5], center = true);
        translate([0, -wood_thickness+ connector/4, connector*2.5]) rotate([90, 0, 0]) cylinder(h = connector*.5, r=connector/4, center = true);

    }
}

module top_clip(c_size = connector) {
    color("Blue") translate([0, connector*1.5, back_plate_size/2 + connector*1.5]) {
        rotate([0, 0, 90]) {
            translate([0, connector, 0]) precursor_simple_connector(connector,0, 5);
            translate([0, -connector, 0]) precursor_simple_connector(connector,0, 5);
            translate([wood_thickness, 0, 0]) cube(size = [wood_thickness, top_clip_length, 10], center = true);
        }
        translate([0, wood_thickness, connector])  cube(size = [10, wood_thickness, 20], center = true);
        translate([0, connector*.25, 15])  rotate([90, 0, 0]) cylinder(h = connector*.5, r=connector/4, center = true);
        translate([0, wood_thickness, -connector*2]) {
            difference() {
               cube(size = [top_clip_length, wood_thickness, connector*4.5], center = true);
               rotate([90, 0, 0]) translate([0, connector/8, 0]) cylinder(h = connector, r=connector/4, center = true);
            }
        translate([0, -connector/2, -connector*2]) cube(size = [top_clip_length, wood_thickness, connector/2], center = true);
        }
    }
}


module side_connectors() {
    mirror([ 1, 0, 0 ]) translate([-back_plate_size/2 + connector*1.5, connector*.75, back_plate_size/2]) rotate([0,90,0]) simple_connector(connector, 1);
    mirror([ 0, 0, 0 ])  translate([-back_plate_size/2 + connector*1.5, connector*.75, back_plate_size/2]) rotate([0,90,0]) simple_connector(connector, 1);
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

module precursor_simple_connector(c_size, side_pins, l = 10) {
    difference() {
        hull() {
            translate([l/2,0,0]) cube(c_size, center = true);
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

module parts() {
//    simple_connector(connector, 1);
//    translate([0, -connector*1.5, -(back_plate_size/2 + connector*1.5)]) top_clip();
//    translate([0, -connector/2, -(back_plate_size/2 + connector/2)]) top_holder();
}



module whole_machine() {
  	 back_plate();
    top_holder();
    top_clip();
    side_connectors();

    
//    holes_connector();
    
    
}


