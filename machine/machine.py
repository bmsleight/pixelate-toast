#! /usr/bin/python
# -*- coding: UTF-8 -*-
from __future__ import division
import os, sys, re, argparse, random

from solid import *
from solid.utils import *





if __name__ == '__main__':    
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    parser.add_argument('-s', action='store', dest='openscad',
                    default="machine.scad", help='Openscad file name')
    parser.add_argument('-f', action='store', dest='fn',
                    default="60", help='openscad $fn=')
    options = parser.parse_args()

    a = union()
    scad_render_to_file(a, options.openscad, include_orig_code=True, file_header='$fn=' + options.fn + ';')
