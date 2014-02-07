include <common/conf.scad>
include <common/local.scad>
include <common/common.scad>
include <common/version.scad>
include <base/nut.scad>
include <base/hex.scad>
include <base/aluminiumProfiles.scad>
include <base/pipe.scad>
include <base/washer.scad>
include <base/hex_socket.scad>
include <base/batteries.scad>
include <base/bearings.scad>
module ASME_B18_2_2(key="3/8 in", part_mode="default"){
	check_parameter_type("ASME B18.2.2","key",key,"Table Index");

	measures_0 = hexagonnut3_table_0(key);
	if(measures_0 == "Error"){
		BOLTS_error("Table look-up failed in ASME B18.2.2, table 0");
	}
	if(BOLTS_MODE == "bom"){
		if(!(part_mode == "diff")){
			echo(str(" ","Hexagon"," ","nut"," ","ASME B18.2.2"," ","-"," ",key," "));
		}
		cube();
	} else {
		nut1(convert_to_default_unit(measures_0[0],"in"), convert_to_default_unit(measures_0[1],"in"), convert_to_default_unit(measures_0[2],"in"));
	}
}

function ASME_B18_2_2_dims(key="3/8 in", part_mode="default") = [
	["s", convert_to_default_unit(hexagonnut3_table_0(key)[1],"in")],
	["d1", convert_to_default_unit(hexagonnut3_table_0(key)[0],"in")],
	["key", key],
	["m_max", convert_to_default_unit(hexagonnut3_table_0(key)[2],"in")]];

