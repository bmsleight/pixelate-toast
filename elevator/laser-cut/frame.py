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
h_strut_width = slate_width + (p_thickness*2)
h_strut_length = 25

def add_layers(drawing):
    drawing.add_layer('OUTLINE', color=256)
    drawing.add_layer('ENGRAVE', color=256)
    drawing.add_layer('CUTSINNEREARLY', color=256)
    drawing.add_layer('CUTSINNER', color=256)
    drawing.add_layer('CUTSOUTER', color=256)


def captive_hut(drawing, startx, starty):
    drawing.add(dxf.rectangle((startx, starty) , 15, 3,  layer='CUTSINNEREARLY', color=3))
    drawing.add(dxf.rectangle((startx+(15-3)/2, starty-3), 3, 9,  layer='CUTSINNEREARLY', color=3))


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
      drawing.add(dxf.line( (startx+p_thickness, starty + (h_strut_length*n) ), 
                            (startx+p_thickness, starty + (h_strut_length*n) + (h_strut_length/3) ),
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
      drawing.add(dxf.line( (startx, starty + (h_strut_length*n) + (h_strut_length/3) ), 
                            (startx, starty + (h_strut_length*n) + (h_strut_length*2/3) ),
                            layer='CUTSINNER', color=4) 
                 )     
      drawing.add(dxf.line( (startx+p_thickness, starty + (h_strut_length*n) + (h_strut_length*2/3)), 
                            (startx+p_thickness, starty + (h_strut_length*n) + (h_strut_length) ),
                            layer='CUTSINNER', color=4) 
                 )
      # Middle right
      drawing.add(dxf.line( (startx-p_thickness+h_strut_width, starty + (h_strut_length*n) ), 
                            (startx-p_thickness+h_strut_width, starty + (h_strut_length*n) + (h_strut_length/3) ),
                            layer='CUTSINNER', color=4) 
                 )
      drawing.add(dxf.line( (startx-p_thickness+h_strut_width, starty + (h_strut_length*n) + (h_strut_length/3) ), 
                            (startx+h_strut_width, starty + (h_strut_length*n) + (h_strut_length/3) ),
                            layer='CUTSINNER', color=1) 
                 )

      #middle middle left
      drawing.add(dxf.line( (startx-p_thickness+h_strut_width, starty + (h_strut_length*n) + (h_strut_length*2/3) ), 
                            (startx+h_strut_width, starty + (h_strut_length*n) + (h_strut_length*2/3)),
                            layer='CUTSINNER', color=1) 
                 )
      drawing.add(dxf.line( (startx+h_strut_width, starty + (h_strut_length*n) + (h_strut_length/3) ), 
                            (startx+h_strut_width, starty + (h_strut_length*n) + (h_strut_length*2/3) ),
                            layer='CUTSINNER', color=1) 
                 )     
      drawing.add(dxf.line( (startx-p_thickness+h_strut_width, starty + (h_strut_length*n) + (h_strut_length*2/3)), 
                            (startx-p_thickness+h_strut_width, starty + (h_strut_length*n) + (h_strut_length) ),
                            layer='CUTSINNER', color=1) 
                 )
      # middle left screw head
      captive_hut(drawing, startx, starty + (h_strut_length*n) + h_strut_length/2) 
      #drawing.add(dxf.rectangle((startx, starty + (h_strut_length*n) + h_strut_length/2) , 3, 3,  layer='CUTSINNEREARLY', color=3))


  drawing.add(dxf.line( (startx, starty + (h_strut_length*number_of_struts) ), 
                        (startx+h_strut_width, starty + (h_strut_length*number_of_struts) ),
                        layer='CUTSINNEREARLY', color=3) 
             )
  return (x_increment, y_increment)



if __name__ == '__main__':
    # git rev-parse --short HEAD 
    name="/tmp/frame.dxf"
    drawing = dxf.drawing(name)
    drawing.add(dxf.rectangle((0, 0) , 210, 297,  layer='OUTLINE', color=1))
    x_increment = 0
    y_increment = 0
    (x_increment, y_increment) = slates(drawing, 0, 0, 2)  
    (x_increment, y_increment) = horizontal_strut(drawing,x_increment, y_increment, 3)  
    drawing.save()
    print("drawing '%s' created.\n" % name)

  
