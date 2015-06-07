#!/usr/bin/env python
#coding:utf-8

import sys
import os
import math

import dxfwrite
from dxfwrite import DXFEngine as dxf

slate_width = 173 # Toast plus gaps
slate_length = 15 # Toast plus gaps

def add_layers(drawing):
    drawing.add_layer('OUTLINE', color=256)
    drawing.add_layer('ENGRAVE', color=256)
    drawing.add_layer('CUTSINNEREARLY', color=256)
    drawing.add_layer('CUTSINNER', color=256)
    drawing.add_layer('CUTSOUTER', color=256)
    drawing.add_layer('INFOONLY', color=256)



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
      drawing.add(dxf.rectangle((startx + 5, starty + 5 + (slate_length*n)) , 5, 5,  layer='CUTSINNEREARLY', color=3))
      # right hand side cable tie hole
      drawing.add(dxf.rectangle((startx + slate_width- 10, starty + 5 + (slate_length*n)) , 5, 5,  layer='CUTSINNEREARLY', color=3))
      # Cog hole
      drawing.add(dxf.rectangle((startx + 130, starty + 5 + (slate_length*n)) , 5, 5,  layer='CUTSINNEREARLY', color=3))

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


if __name__ == '__main__':
    # git rev-parse --short HEAD 
    name="/tmp/tracks_for_frame.dxf"
    drawing = dxf.drawing(name)
#    drawing.add(dxf.rectangle((0, 0) , 210, 297,  layer='OUTLINE', color=1))
    startx = 0
    starty = 0
    x_increment = 0
    y_increment = 0
    (x_increment, y_increment) = slates(drawing, startx, starty, 12) 
    startx = startx + x_increment
    starty = starty + y_increment
    drawing.save()
    print("drawing '%s' created.\n" % name)

  
