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


def hole_connector(depth=15):
    sc = left((15-depth)/2)(cube([depth, 10, 10], center=True))
    sc = sc + left(7.5)(rotate([90, 0, 0])(cylinder(r=5, h=10, center=True)))
    sc = sc - left(7.5)(rotate([90, 0, 0])(cylinder(r=2.5, h=20, center=True)))
    return sc


def back_cross():
    back_cross_z = bread_base_z + 40
    bc =  cube([10, 5, back_cross_z], center=True)
    bc =  bc + forward(0)(down(7.5)(cube([bread_base_x, 5, bread_base_z+25], center=True)))

    bc =  bc - up(back_cross_z/2-10/2)(back(5)(rotate([90, 0, 0])(cylinder(r=2.5, h=10, center=True))))
    bc =  bc + up(back_cross_z/2-30)(back(5)(rotate([90, 0, 0])(cylinder(r=2.5, h=10, center=True))))

    bc =  bc + up(bread_base_z/2)(back_beam())
    
    return bc

def back_beam():
    bb = cube([bread_base_x, 5, 10], center=True)
    bb = bb + back(2.5)(rotate([0,0,90])(hole_connector(depth=10)))
    bb = bb + back(7.5)(left(bread_base_x/2-2.5)(hole_connector()))
    bb = bb + back(7.5)(right(bread_base_x/2-2.5)(rotate([0, 0, 180])(hole_connector())))
    return bb




def clip():
    clip_x = bread_base_x/2
    clip_z = 40
    clip_y = 5
    clip = cube([clip_x, clip_y, clip_z], center=True)
    clip = clip + down(10)(forward(5)(rotate([90, 0, 0])(cylinder(r=2.5, h=5, center=True))))
    clip = clip - up(15)(forward(2.5)(rotate([90, 0, 0])(cylinder(r=2.5, h=5, center=True))))
    clip = clip + right(10)(rotate([0,0,270])(hole_connector(depth=10)))
    clip = clip + left(10)(rotate([0,0,270])(hole_connector(depth=10)))
    clip = clip + down(clip_z/2-(clip_y/4))(forward(clip_y/2)(cube([clip_x, clip_y/2, clip_y/2], center=True)))

    return clip


def whole_model():
    wm = union()
    wm = back_cross() 
    wm = wm + up(bread_base_z/2)(back(17.5)(clip()))
    return wm


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
    a = whole_model()
 
    scad_render_to_file(a, options.openscad, include_orig_code=True, file_header='$fn=' + options.fn + ';')
