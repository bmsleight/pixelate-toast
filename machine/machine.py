#! /usr/bin/python
# -*- coding: UTF-8 -*-
#
#  python machine.py -s machine.scad  ; openscad machine.scad
#

from __future__ import division
import os, sys, re, argparse, random

from solid import *
from solid.utils import *


#Hate globals ?
bread_base_x = 120
bread_base_z = 100



def back_cross():
    back_cross_z = bread_base_z + 40
    bc =  cube([10, 10, back_cross_z], center=True)
    bc =  bc - up(back_cross_z/2-10/2)(back(5)(rotate([90, 0, 0])(cylinder(r=2.5, h=10, center=True))))
    bc =  bc + up(back_cross_z/2-30)(back(5)(rotate([90, 0, 0])(cylinder(r=2.5, h=10, center=True))))

    bc =  bc + up(bread_base_z/2)(back_beam())
    
    return bc

def back_beam():
    bb = cube([bread_base_x, 10, 10], center=True)
    bb = bb + back(2.5)(rotate([0,0,90])(hole_connector()))
    bb = bb + back(10)(left(bread_base_x/2-2.5)(hole_connector()))
    bb = bb + back(10)(right(bread_base_x/2-2.5)(rotate([0, 0, 180])(hole_connector())))
    return bb



def hole_connector():
    sc = cube([15, 10, 10], center=True)
    sc = sc + left(7.5)(rotate([90, 0, 0])(cylinder(r=5, h=10, center=True)))
    sc = sc - left(7.5)(rotate([90, 0, 0])(cylinder(r=2.5, h=20, center=True)))
    return sc




if __name__ == '__main__':    
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    parser.add_argument('-s', action='store', dest='openscad',
                    default="machine.scad", help='Openscad file name')
    parser.add_argument('-f', action='store', dest='fn',
                    default="60", help='openscad $fn=')
    parser.add_argument('-c', action='store_true', default=False,
                    dest='clip', help='draw clip')
    options = parser.parse_args()

    a = union()
#    a = back_plate()
    a = back_cross()

 
    scad_render_to_file(a, options.openscad, include_orig_code=True, file_header='$fn=' + options.fn + ';')
