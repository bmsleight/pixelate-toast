#!/usr/bin/env python
#coding:utf-8

import sys
import os
import math

import dxfwrite
from dxfwrite import DXFEngine as dxf

p_thickness = 3
toast_x = 120 # At least
toast_x = 120 # Any length - really ~ 12 <-> 15
slate_width = 160 # Toast plus gaps
slate_length = 10 # Toast plus gaps
h_strut_width = slate_width + (p_thickness*2)  + (20) # Need some added space to stop jams
h_strut_length = 30
side_width = 200
side_height = 100
spacers = 21.0 # for ridges
side_position_fraction_x = side_width/7
side_position_fraction_y = side_height/7
height_ridge_from_top = 20
ridge_height = 9

#Gear size = 56.3
gear_height = 69/2
motor_height = 42.3
motor_centre_height_from_top = height_ridge_from_top + gear_height 
# This woudl make the gear - touch the bottom of the bottom of the ridge
# So adding the ridge thickness and the stacks thickness...
motor_centre_height_from_top = height_ridge_from_top + gear_height - p_thickness*2
motor_screw_offset_from_centre = 31/2
motor_height_bottom = motor_centre_height_from_top - motor_height/2.0 +motor_height + p_thickness
motor_length = 48

def add_layers(drawing):
    drawing.add_layer('OUTLINE', color=256)
    drawing.add_layer('ENGRAVE', color=256)
    drawing.add_layer('CUTSINNEREARLY', color=256)
    drawing.add_layer('CUTSINNER', color=256)
    drawing.add_layer('CUTSOUTER', color=256)
    drawing.add_layer('INFOONLY', color=256)


def captive_hut(drawing, startx, starty):
    drawing.add(dxf.rectangle((startx, starty) , 15, 3,  layer='CUTSINNEREARLY', color=3))
    drawing.add(dxf.rectangle((startx+(15-3)/2, starty-3), 3, 9,  layer='CUTSINNEREARLY', color=3))

# Yes yes shoudl re-use code... .. .
def captive_hut_right_angle(drawing, startx, starty):
    drawing.add(dxf.rectangle((startx-3/2.0, starty) , 3, 15,  layer='CUTSINNEREARLY', color=3))
    drawing.add(dxf.rectangle((startx-3/2.0-3, starty+(15-3)/2.0), 9, 3,  layer='CUTSINNEREARLY', color=3))
#    drawing.add(dxf.rectangle((startx-3/2.0-3, starty), 9, 3,  layer='CUTSINNEREARLY', color=3))


def slates(drawing, startx, starty, number_of_slates):
  x_increment = 0
  y_increment = 0
  for n in range(0, number_of_slates):
      # top of slates
      drawing.add(dxf.line( (startx, starty + (slate_length*n) ), 
                            (startx+slate_width, starty + (slate_length*n) ),
                            layer='CUTSINNEREARLY', color=3) 
                 )
      # left hand side cable tie hole
      drawing.add(dxf.rectangle((startx + 5, starty + 2.5 + (slate_length*n)) , 10, 5,  layer='CUTSINNEREARLY', color=3))
      # right hand side cable tie hole
      drawing.add(dxf.rectangle((startx + slate_width- 15, starty + 2.5+ (slate_length*n)) , 10, 5,  layer='CUTSINNEREARLY', color=3))
      # Cog hole
      drawing.add(dxf.rectangle((startx + 100, starty + 2.5+ (slate_length*n)) , 10, 5,  layer='CUTSINNEREARLY', color=3))

      y_increment = y_increment + slate_length
  # bottom of slates
  drawing.add(dxf.line( (startx, starty + (slate_length*number_of_slates) ), 
                            (startx+slate_width, starty + (slate_length*number_of_slates) ),
                            layer='CUTSINNEREARLY', color=3) 
                 )

  # left and right sides of slates
  drawing.add(dxf.line( (startx, starty ), 
                        (startx, starty + (slate_length*number_of_slates) ),
                        layer='CUTSINNER', color=4) 
             )
  drawing.add(dxf.line( (startx+slate_width, starty ), 
                        (startx+slate_width, starty + (slate_length*number_of_slates) ),
                        layer='CUTSINNER', color=4) 
             )
   
  return (x_increment, y_increment)

def horizontal_strut(drawing, startx, starty, number_of_struts):
  x_increment = 0
  y_increment = 0
  for n in range(0, number_of_struts):
      # top of slates
      drawing.add(dxf.line( (startx, starty + (h_strut_length*n) ), 
                            (startx+h_strut_width, starty + (h_strut_length*n) ),
                            layer='CUTSINNEREARLY', color=3) 
                 )
      # straight, extrusion for screw, straight

      # Middle left
      drawing.add(dxf.line( (startx, starty + (h_strut_length*n) ), 
                            (startx, starty + (h_strut_length*n) + (h_strut_length/3) ),
                            layer='CUTSINNER', color=4) 
                 )
      drawing.add(dxf.line( (startx+p_thickness, starty + (h_strut_length*n) + (h_strut_length/3) ), 
                            (startx, starty + (h_strut_length*n) + (h_strut_length/3) ),
                            layer='CUTSINNER', color=4) 
                 )

      #middle middle left
      drawing.add(dxf.line( (startx+p_thickness, starty + (h_strut_length*n) + (h_strut_length*2/3) ), 
                            (startx, starty + (h_strut_length*n) + (h_strut_length*2/3)),
                            layer='CUTSINNER', color=4) 
                 )
      drawing.add(dxf.line( (startx+p_thickness, starty + (h_strut_length*n) + (h_strut_length/3) ), 
                            (startx+p_thickness, starty + (h_strut_length*n) + (h_strut_length*2/3) ),
                            layer='CUTSINNER', color=4) 
                 )     
      drawing.add(dxf.line( (startx, starty + (h_strut_length*n) + (h_strut_length*2/3)), 
                            (startx, starty + (h_strut_length*n) + (h_strut_length) ),
                            layer='CUTSINNER', color=4) 
                 )
      # Middle right
      drawing.add(dxf.line( (startx+h_strut_width, starty + (h_strut_length*n) ), 
                            (startx+h_strut_width, starty + (h_strut_length*n) + (h_strut_length/3) ),
                            layer='CUTSINNER', color=4) 
                 )
      drawing.add(dxf.line( (startx-p_thickness+h_strut_width, starty + (h_strut_length*n) + (h_strut_length/3) ), 
                            (startx+h_strut_width, starty + (h_strut_length*n) + (h_strut_length/3) ),
                            layer='CUTSINNER', color=4) 
                 )

      #middle middle left
      drawing.add(dxf.line( (startx-p_thickness+h_strut_width, starty + (h_strut_length*n) + (h_strut_length*2/3) ), 
                            (startx+h_strut_width, starty + (h_strut_length*n) + (h_strut_length*2/3)),
                            layer='CUTSINNER', color=4) 
                 )
      drawing.add(dxf.line( (startx-p_thickness+h_strut_width, starty + (h_strut_length*n) + (h_strut_length/3) ), 
                            (startx-p_thickness+h_strut_width, starty + (h_strut_length*n) + (h_strut_length*2/3) ),
                            layer='CUTSINNER', color=4) 
                 )     
      drawing.add(dxf.line( (startx+h_strut_width, starty + (h_strut_length*n) + (h_strut_length*2/3)), 
                            (startx+h_strut_width, starty + (h_strut_length*n) + (h_strut_length) ),
                            layer='CUTSINNER', color=4) 
                 )
      # Caphut screw head
      captive_hut(drawing, startx, starty + (h_strut_length*n) + (h_strut_length)/2-1.5) 
      captive_hut(drawing, startx+h_strut_width-15, starty + (h_strut_length*n) + h_strut_length/2-1.5) 
      #drawing.add(dxf.rectangle((startx, starty + (h_strut_length*n) + h_strut_length/2) , 3, 3,  layer='CUTSINNEREARLY', color=3))
      if n == 0:
          # Base - 
          drawing.add(dxf.rectangle((startx+h_strut_width-motor_length-p_thickness*2, starty + (h_strut_length*n) + (h_strut_length)/2.0 -1.5 ), 3, 3,  layer='CUTSINNEREARLY', color=3))
          drawing.add(dxf.rectangle((startx+h_strut_width-motor_length-p_thickness*2, starty + (h_strut_length*n) + (h_strut_length)/2.0 -1.5 - 12), 3, 9,  layer='CUTSINNEREARLY', color=3))
          drawing.add(dxf.rectangle((startx+h_strut_width-motor_length-p_thickness*2, starty + (h_strut_length*n) + (h_strut_length)/2.0 +1.5 + 3), 3, 9,  layer='CUTSINNEREARLY', color=3))

  drawing.add(dxf.line( (startx, starty + (h_strut_length*number_of_struts) ), 
                        (startx+h_strut_width, starty + (h_strut_length*number_of_struts) ),
                        layer='CUTSINNEREARLY', color=3) 
             )
  y_increment = h_strut_length*number_of_struts
  return (x_increment, y_increment )


def side_holes_for_struts(drawing, startx, starty):
    drawing.add(dxf.rectangle((startx, starty) , h_strut_length/3, p_thickness,  layer='CUTSINNEREARLY', color=3))
    drawing.add(dxf.rectangle((startx+(h_strut_length*2/3), starty) , h_strut_length/3, p_thickness,  layer='CUTSINNEREARLY', color=3))
    drawing.add(dxf.rectangle((startx+(h_strut_length)/2-1.5, starty) , p_thickness, p_thickness,  layer='CUTSINNEREARLY', color=3))

def side_holes_for_ridge(drawing, startx, starty, start=1):
    spacer = side_width/spacers
    for n in range(start, int(spacers), 2): # every other one, but not the first 
        drawing.add(dxf.rectangle((startx+(spacer*n), starty) , spacer, p_thickness,  layer='CUTSINNEREARLY', color=3))

def motor_mount_holes(drawing, startx, starty):
    drawing.add(dxf.circle(3/2.0, (startx+motor_screw_offset_from_centre, starty+motor_screw_offset_from_centre), layer='CUTSINNEREARLY', color=3))
    drawing.add(dxf.circle(3/2.0, (startx-motor_screw_offset_from_centre, starty+motor_screw_offset_from_centre), layer='CUTSINNEREARLY', color=3))
    drawing.add(dxf.circle(3/2.0, (startx+motor_screw_offset_from_centre, starty-motor_screw_offset_from_centre), layer='CUTSINNEREARLY', color=3))
    drawing.add(dxf.circle(3/2.0, (startx-motor_screw_offset_from_centre, starty-motor_screw_offset_from_centre), layer='CUTSINNEREARLY', color=3))
    drawing.add(dxf.circle(gear_height, (startx, starty), layer='INFOONLY', color=7))
    drawing.add(dxf.circle(gear_height-3, (startx, starty), layer='INFOONLY', color=7))
    drawing.add(dxf.rectangle((startx-motor_height/2.0, starty-motor_height/2.0) , motor_height, motor_height,  layer='INFOONLY', color=7))

def side_r(drawing, startx, starty, motor_hole = False):
    drawing.add(dxf.rectangle((startx, starty) , side_width, side_height,  layer='CUTSOUTER', color=5))
    side_holes_for_struts(drawing, startx+side_position_fraction_x, starty+side_position_fraction_y)
    side_holes_for_struts(drawing, startx+side_position_fraction_x*5, starty+side_position_fraction_y)
    if motor_hole:
        # Motor position
        side_holes_for_struts(drawing, startx+side_position_fraction_x*5, starty+side_height-motor_height_bottom)
        side_holes_for_struts(drawing, startx+side_position_fraction_x*5, starty+side_height-motor_height_bottom+motor_height+p_thickness)
        motor_mount_holes(drawing, startx+side_position_fraction_x*5+h_strut_length/2.0, starty+side_height-motor_centre_height_from_top)
    side_holes_for_struts(drawing, startx+side_position_fraction_x*3, starty+side_position_fraction_y*4)
    side_holes_for_ridge(drawing, startx, starty+side_height-height_ridge_from_top)
    y_increment = side_height
    return (x_increment, y_increment)

def motor_front_face(drawing, startx, starty):
    top_struct_at_y    = side_height-motor_height_bottom+motor_height+p_thickness*2
    bottom_struct_at_y = side_position_fraction_y
    mff_height = top_struct_at_y - bottom_struct_at_y
    #drawing.add(dxf.rectangle((startx, starty) , motor_height, mff_height,  layer='CUTSOUTER', color=5)) #square motor width=height
    drawing.add(dxf.line( (startx, starty+p_thickness ), 
                          (startx+(motor_height/2.0)-(9*1.5), starty+p_thickness),
                          layer='CUTSINNEREARLY', color=3) 
                 )
    drawing.add(dxf.line( (startx+(motor_height/2.0)-(9*1.5), starty+p_thickness ), 
                          (startx+(motor_height/2.0)-(9*1.5), starty),
                          layer='CUTSINNEREARLY', color=3) 
                 )
    drawing.add(dxf.line( (startx+(motor_height), starty+p_thickness ), 
                          (startx+(motor_height)-(motor_height/2.0)+(9*1.5), starty+p_thickness),
                          layer='CUTSINNEREARLY', color=3) 
                 )
    drawing.add(dxf.line( (startx+(motor_height)-(motor_height/2.0)+(9*1.5), starty+p_thickness ), 
                          (startx+(motor_height)-(motor_height/2.0)+(9*1.5), starty),
                          layer='CUTSINNEREARLY', color=3) 
                 )
    drawing.add(dxf.line( (startx+(motor_height/2.0)-(9*0.5), starty+p_thickness ), 
                          (startx+(motor_height/2.0)+(9*0.5), starty+p_thickness),
                          layer='CUTSINNEREARLY', color=3) 
                 )
    drawing.add(dxf.line( (startx+(motor_height/2.0)+(9*0.5), starty+p_thickness ), 
                          (startx+(motor_height/2.0)+(9*0.5), starty),
                          layer='CUTSINNEREARLY', color=3) 
                 )
    drawing.add(dxf.line( (startx+(motor_height/2.0)-(9*0.5), starty+p_thickness ), 
                          (startx+(motor_height/2.0)-(9*0.5), starty),
                          layer='CUTSINNEREARLY', color=3) 
                 )
    drawing.add(dxf.line( (startx, starty-p_thickness+mff_height ), 
                          (startx+(motor_height/2.0)-(9*1.5), starty-p_thickness+mff_height),
                          layer='CUTSINNEREARLY', color=3) 
                 )
    drawing.add(dxf.line( (startx+(motor_height/2.0)-(9*1.5), starty-p_thickness+mff_height ), 
                          (startx+(motor_height/2.0)-(9*1.5), starty+mff_height),
                          layer='CUTSINNEREARLY', color=3) 
                 )
    drawing.add(dxf.line( (startx+(motor_height), starty-p_thickness+mff_height ), 
                          (startx+(motor_height)-(motor_height/2.0)+(9*1.5), starty-p_thickness+mff_height),
                          layer='CUTSINNEREARLY', color=3) 
                 )
    drawing.add(dxf.line( (startx+(motor_height)-(motor_height/2.0)+(9*1.5), starty-p_thickness+mff_height ), 
                          (startx+(motor_height)-(motor_height/2.0)+(9*1.5), starty+mff_height),
                          layer='CUTSINNEREARLY', color=3) 
                 )
    drawing.add(dxf.line( (startx+(motor_height/2.0)-(9*0.5), starty-p_thickness+mff_height), 
                          (startx+(motor_height/2.0)+(9*0.5), starty-p_thickness+mff_height),
                          layer='CUTSINNEREARLY', color=3) 
                 )
    drawing.add(dxf.line( (startx+(motor_height/2.0)+(9*0.5), starty-p_thickness+mff_height), 
                          (startx+(motor_height/2.0)+(9*0.5), starty+mff_height),
                          layer='CUTSINNEREARLY', color=3) 
                 )
    drawing.add(dxf.line( (startx+(motor_height/2.0)-(9*0.5), starty-p_thickness+mff_height), 
                          (startx+(motor_height/2.0)-(9*0.5), starty+mff_height),
                          layer='CUTSINNEREARLY', color=3) 
                 )
    # top line
    drawing.add(dxf.line( (startx, starty+mff_height), 
                          (startx+motor_height, starty+mff_height),
                          layer='CUTSOUTER', color=5) 
                 )
    # sides
    drawing.add(dxf.line( (startx, starty), 
                          (startx, starty+mff_height),
                          layer='CUTSOUTER', color=5) 
                 )
    drawing.add(dxf.line( (startx+motor_height, starty), 
                          (startx+motor_height, starty+mff_height),
                          layer='CUTSOUTER', color=5) 
                 )
    motor_mount_holes(drawing, startx+motor_height/2.0, starty+mff_height-motor_height/2.0-p_thickness)
    captive_hut_right_angle(drawing, startx+motor_height/2.0, starty)
    captive_hut_right_angle(drawing, startx+motor_height/2.0, starty+mff_height-15)
    y_increment = mff_height
    x_increment = motor_height
    return (x_increment, y_increment)

def motor_front_top_face(drawing, startx, starty):
#    drawing.add(dxf.rectangle((startx, starty) , motor_height, motor_length-p_thickness*2,  layer='CUTSOUTER', color=5))
    drawing.add(dxf.line( (startx, starty + motor_length+p_thickness*2), 
                          (startx+motor_height, starty + motor_length+p_thickness*2),
                          layer='CUTSOUTER', color=5) 
                 )
    drawing.add(dxf.line( (startx+motor_height, starty ), 
                          (startx+motor_height, starty + motor_length+p_thickness*2),
                          layer='CUTSOUTER', color=5) 
                 )
    drawing.add(dxf.rectangle((startx+motor_height/2.0-1.5, starty) , 3, 3,  layer='CUTSINNEREARLY', color=3))
    drawing.add(dxf.rectangle((startx+motor_height/2.0-1.5-12, starty) , 9, 3,  layer='CUTSINNEREARLY', color=3))
    drawing.add(dxf.rectangle((startx+motor_height/2.0+1.5+3, starty) , 9, 3,  layer='CUTSINNEREARLY', color=3))
    captive_hut_right_angle(drawing, startx+motor_height/2.0, starty + motor_length+p_thickness*2-15)
    drawing.add(dxf.line( (startx+motor_height/2.0-h_strut_length/(3*2), starty + motor_length+p_thickness ), 
                          (startx+motor_height/2.0+h_strut_length/(3*2), starty + motor_length+p_thickness ),
                          layer='CUTSINNEREARLY', color=3) 
                 )
    drawing.add(dxf.line( (startx+motor_height/2.0-h_strut_length/(3*2), starty + motor_length+p_thickness ), 
                          (startx+motor_height/2.0-h_strut_length/(3*2), starty + motor_length+p_thickness*2 ),
                          layer='CUTSINNEREARLY', color=3) 
                 )
    drawing.add(dxf.line( (startx+motor_height/2.0+h_strut_length/(3*2), starty + motor_length+p_thickness ), 
                          (startx+motor_height/2.0+h_strut_length/(3*2), starty + motor_length+p_thickness*2 ),
                          layer='CUTSINNEREARLY', color=3) 
                 )
    drawing.add(dxf.line( (startx+motor_height, starty + motor_length+p_thickness), 
                          (startx+motor_height/2.0+h_strut_length/(3*2)+h_strut_length/3, starty + motor_length+p_thickness),
                          layer='CUTSINNEREARLY', color=3) 
                 )
    drawing.add(dxf.line( (startx+motor_height/2.0+h_strut_length/(3*2)+h_strut_length/3, starty + motor_length+p_thickness), 
                          (startx+motor_height/2.0+h_strut_length/(3*2)+h_strut_length/3, starty + motor_length+p_thickness*2),
                          layer='CUTSINNEREARLY', color=3) 
                 )
    drawing.add(dxf.line( (startx, starty + motor_length+p_thickness), 
                          (startx+motor_height/2.0-h_strut_length/(3*2)-h_strut_length/3, starty + motor_length+p_thickness),
                          layer='CUTSINNEREARLY', color=3) 
                 )
    drawing.add(dxf.line( (startx+motor_height/2.0-h_strut_length/(3*2)-h_strut_length/3, starty + motor_length+p_thickness), 
                          (startx+motor_height/2.0-h_strut_length/(3*2)-h_strut_length/3, starty + motor_length+p_thickness*2),
                          layer='CUTSINNEREARLY', color=3) 
                 )
    return (x_increment, y_increment)

def ridge(drawing, startx, starty):
    side_holes_for_ridge(drawing, startx, starty+ridge_height-p_thickness, start=0)
    drawing.add(dxf.rectangle((startx, starty) , side_width, ridge_height,  layer='CUTSOUTER', color=5))
    y_increment = ridge_height
    return (x_increment, y_increment)


if __name__ == '__main__':
    # git rev-parse --short HEAD 
    name="/tmp/frame.dxf"
    drawing = dxf.drawing(name)
#    drawing.add(dxf.rectangle((0, 0) , 210, 297,  layer='OUTLINE', color=1))
    startx = 0
    starty = 0
    x_increment = 0
    y_increment = 0
    (x_increment, y_increment) = slates(drawing, startx, starty, 1) 
    startx = startx + x_increment
    starty = starty + y_increment
    (x_increment, y_increment) = horizontal_strut(drawing,startx, starty, 3)
    startx = startx + x_increment
    starty = starty + y_increment
    (x_increment, y_increment) = side_r(drawing, startx, starty, motor_hole=True)  
    startx = startx + x_increment
    starty = starty + y_increment
    (x_increment, y_increment) = side_r(drawing, startx, starty)  
    startx = startx + x_increment
    starty = starty + y_increment
    (x_increment, y_increment) = ridge(drawing, startx, starty)  
    startx = startx + x_increment
    starty = starty + y_increment
    (x_increment, y_increment) = ridge(drawing, startx, starty)  
    startx = startx + x_increment
    starty = starty + y_increment
    (x_increment, y_increment) = motor_front_face(drawing, startx, starty)
    (x_increment, y_increment) = motor_front_top_face(drawing, startx+x_increment, starty)

    drawing.save()
    print("drawing '%s' created.\n" % name)

  
