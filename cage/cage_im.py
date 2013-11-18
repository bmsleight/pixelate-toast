#! /usr/bin/python
# -*- coding: UTF-8 -*-
from __future__ import division
import os, sys, re, argparse, random

from solid import *
from solid.utils import *
from solid import screw_thread 

SEGMENTS = 120

min_wire_free = 1
frame_length = 7.5

#min_wire_free = 1.5
#frame_length = 9

bread_base = 12

'''
Min Wall Supported: 0.8mm (Unpolished) · 1.0mm (Polished)
Min Wall Free: 0.9mm (Unpolished) · 1.0mm (Polished)
Min Wire Supported: 1.3mm (Unpolished) · 1.5mm (Polished)
Min Wire Free: 1.5mm (Unpolished) · 2.0mm (Polished)
Min Embossed Detail: 0.7mm (Unpolished) · 0.8mm (Polished)
Min Engraved Detail: 0.7mm (Unpolished) · 0.8mm (Polished)
Min Bounding Box: x+y+z >= 7.5mm
Max Bounding Box: 230x180x310mm (Unpolished) · 150x150x150mm (Polished)
Min Escape Hole: 4mm (1 hole) · 2mm (2 holes) · Big models require multiple holes
Interlocking or Enclosed Part?: Yes
Multiple Part per STL: Yes
Clearance: 0.5mm
Accuracy: ± 0.15mm, then ± 0.15% of longest axis
'''

def frame(maxx=3, maxy=3):
    maxy = int(maxy)
    maxx = int(maxx)
    frame_wire = min_wire_free*2
    strut = cube([frame_wire, frame_wire, maxy*frame_length+bread_base+frame_length/1.5], center=False)
    strut = back((frame_wire)/2)(left(frame_wire*0.75)(down(frame_wire/2)(strut)))
    f = strut + right(maxx*frame_length+(frame_wire*0.5))(strut)


#    f = cube([maxx*frame_length, min_wire_free*3, maxy*frame_length], center=False)
    return f



def door(position = 2, tab_holder_upright = True, top_tab_extra = False, end_x = False, show = True, vert_connector = False):
# cylinder(r=battery_diameter_bottom/2, h=battery_h_bottom)
    if show == False:
        return union()

    end_block = cube([min_wire_free, min_wire_free, min_wire_free], center=False)
    end_block = back(min_wire_free/2)(left(min_wire_free/2)(down(min_wire_free/2)(end_block)))
    if top_tab_extra or (tab_holder_upright==False):
        f = end_block
    else:
        f = union()

    if top_tab_extra:
        # Dont need upright at the very top
        pass
    else:
        if vert_connector:
            f += cylinder(r=min_wire_free/2, h=frame_length)
        pass
    if end_x:
        return f 
    else:
        f += rotate([0, 90, 0])(cylinder(r=min_wire_free/2, h=frame_length))
    door_length = frame_length - (min_wire_free*2)
    d = cube([door_length, min_wire_free, frame_length - (min_wire_free*2)], center=False)
    gap_length = min_wire_free*2
    gap_height = min_wire_free*1.5
    d -= up(door_length-gap_height)(right(door_length/2-gap_length/2)(cube([gap_length, min_wire_free, gap_height], center=False)))
    d = up(min_wire_free)(d)
    d = right(min_wire_free)(d)
    d = back(min_wire_free/2)(d)
    if position == 0:
        d = rotate([17.5, 0, 0])(d)
    if position == 1:
        d = rotate([-90, 0, 0])(d)
    if position == 2:
        d = rotate([-45, 0, 0])(d)
    c = cylinder(r=4*min_wire_free/2, h=min_wire_free)
    c -= cylinder(r=2*min_wire_free/2, h=frame_length)
    c = right(frame_length/2 - min_wire_free/2)(rotate([0, 90, 0])(c))

    # forks
    if top_tab_extra: 
        k = union()
    else:
        k = back(min_wire_free/2)(cube([min_wire_free, min_wire_free, min_wire_free*1.5], center=False))
        k += cube([min_wire_free, min_wire_free*3, min_wire_free], center=False)
        k = down(min_wire_free)(k)
    if tab_holder_upright:
        k += back(min_wire_free*3)(cube([min_wire_free, min_wire_free*3, min_wire_free], center=False) + down(min_wire_free*1.5)(cube([min_wire_free, min_wire_free, min_wire_free*2], center=False)))


    k = down(min_wire_free/2)(k)
    k = right(frame_length/2-min_wire_free*2)(k) + right(frame_length/2+min_wire_free)(k)
    if top_tab_extra:
        # Long based on bottom
        # Hanging down from Bread....
        if vert_connector:
            k += up(0)(right(0)(cylinder(r=min_wire_free/2, h=frame_length*2)))
        k += up(frame_length*2)(right(min_wire_free)(back(frame_length/2)(cube([min_wire_free, bread_base+frame_length, min_wire_free], center=False))))
        k += up(frame_length*2)(right(0)(back(min_wire_free/2)(cube([frame_length, min_wire_free, min_wire_free], center=False) )))
    if top_tab_extra:
        return (f + k)
    else:
        return (f + d + c + k)


# door(position = 2, tab_holder_upright = True, top_tab_extra = False)

def doors(random_pos =False , maxx=3, maxy=3, just = -1):
    ds = union()
    maxy = int(maxy) - 1
    maxx = int(maxx) - 1
    for x in range(0, maxx+2):
        for y in range(0, maxy+2):
            if (just == -1) or (just == y):
                show = True
            else:
                show = False
            if x==maxx+1:
                end_x = True
            else:
                end_x = False
            if y==0:
                tab_holder_upright = False
            else:
                tab_holder_upright = True
            if y==maxy+1:
                top_tab_extra = True
            else:
                top_tab_extra = False
            if (x%5)==0:
                vert_connector = True
            else:
                vert_connector = False
            if random_pos:
                r = random.choice([0,1]) 
                d = door(r, tab_holder_upright, top_tab_extra, end_x, show, vert_connector)
            else:
                d = door(tab_holder_upright = tab_holder_upright, top_tab_extra = top_tab_extra, end_x = end_x, show = show, vert_connector = vert_connector)
            ds += right(x*frame_length)(up(y*frame_length)(d))
#    ds += back(min_wire_free/2)(left(min_wire_free/2)(down(min_wire_free/2)(cube([min_wire_free, min_wire_free, min_wire_free], center=False))))
    return ds

if __name__ == '__main__':    
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', action='store', dest='fn',
                    default="60", help='openscad $fn=')
    parser.add_argument('-s', action='store', dest='openscad',
                    help='Openscad file name')
    parser.add_argument('-r', action='store_true', default=False,
                    dest='random_pos',
                    help='Set pixels in random positions')
    parser.add_argument('-x', action='store', dest='x',
                    default="3", help='x')
    parser.add_argument('-y', action='store', dest='y',
                    default="3", help='y')
    parser.add_argument('-j', action='store', dest='just',
                    default="-1", help='Just print out row j')
    parser.add_argument('-m', action='store_true', default=False,
                    dest='frame',
                    help='Draw the bulky outside frame')
    parser.add_argument('-n', action='store_true', default=False,
                    dest='nodoors',
                    help='Dont draw the doors (everythign but the frame')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    options = parser.parse_args()

    a = union()
    if options.frame:
        a = a + frame(maxx=options.x, maxy=options.y)
    if not options.nodoors:
        a = a + doors(random_pos = options.random_pos, maxx=options.x, maxy=options.y, just = int(options.just) ) 
    fn = '$fn=' + options.fn + ';'
    scad_render_to_file( a, options.openscad, include_orig_code=True, file_header=fn)



