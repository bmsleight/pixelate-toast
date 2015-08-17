#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys

from solid import *
from solid.utils import *

class tab:
    def __init__(self, tab_type, x, y, tab_orientation="up"):
        # 1 is a female captive nut
        # 2 is the male captive nut  
        self.tab_type = tab_type
        self.x = x
        self.y = y
        self.tab_orientation = tab_orientation


class laserCutOut:
    def __init__(self, name, orientation=1, points=[], x_y_z_position=(0,0,0), x_y_flat_place=(0,0) ):
        self.name = name
        # 1 is flat (thickness is z)
        # 2 is thickness is width(x), width is z
        # 3 is thickness if height(y), height is z
        self.orientation = orientation
        # List of points to form a polygon, e.g. [(0,0), (0,100), (100,100), (100,0), (0,0)]
        self.points = points
        # simular to self.points, but a list of a list of points, to allow more than one cutout
        #  e.g. [[(0, 0), (0, 2), (2, 2), (2, 0), (0, 0)], [(0, 1), (0, 2)]]
        self.list_cutout_points = []
        # list of class tab
        self.tabs = []
        self.x_y_z_position = x_y_z_position
        self.x_y_flat_place = x_y_flat_place


class model:
    def __init__(self, thickness):
        self.thickness = thickness
        self.laser_cut_outs = []

    def add_laser_cut_out(self, name, orientation=1, points=[], list_cutout_points=[], x_y_z_position=(0,0,0), x_y_flat_place=(0,0)):
        # NB tabs=[],= not used at this stage
        laser_cut_out = laserCutOut(name=name, orientation=orientation, points=points, 
                                    x_y_z_position=x_y_z_position, x_y_flat_place=x_y_flat_place)
        self.laser_cut_outs.append(laser_cut_out)


    def add_square_cut_out(self, name, width, height, orientation=1,  x_y_z_position=(0,0,0), x_y_flat_place=(0,0)):
        # NB tabs=[],= not used at this stage
        points = [(0,0), (width, 0), (width, height), (0, height), (0,0)]
        self.add_laser_cut_out(name=name, orientation=orientation, points=points, 
                                    x_y_z_position=x_y_z_position, x_y_flat_place=x_y_flat_place)

    def add_tab(self, name_of_cut_out, tab_type, x, y, tab_orientation="up"):
        foundIndex = -1
        for i in range(0, len(self.laser_cut_outs)):
            if name_of_cut_out == self.laser_cut_outs[i].name:
                foundIndex = i
        if foundIndex !=-1:
            new_tab = tab(tab_type=tab_type, x=x, y=y, tab_orientation=tab_orientation)
            self.laser_cut_outs[foundIndex].tabs.append(new_tab)
        else:
            print("No cutout for tab - raise exception")

    def add_inner_cutout(self, name_of_cut_out, inner_points):
        foundIndex = -1
        for i in range(0, len(self.laser_cut_outs)):
            if name_of_cut_out == self.laser_cut_outs[i].name:
                foundIndex = i
        if foundIndex !=-1:
            current_cutout_points = self.laser_cut_outs[foundIndex].list_cutout_points
            self.laser_cut_outs[foundIndex].list_cutout_points.append(inner_points)
        else:
            print("No cutout for name - raise exception")

    def add_inner_cutout_square(self, name_of_cut_out, width, height, offset_x=0, offset_y=0):
        inner_points = [(offset_x, offset_y), (offset_x+width, offset_y), (offset_x+width, offset_y+height), (offset_x, offset_y+height), (offset_x, offset_y)]
        self.add_inner_cutout(name_of_cut_out, inner_points)

    def polygon_points_format(self, points):
        rpoints = ""
        for point in points:
            x, y = point
            rpoints += "[" + str(x) + "," + str(y) + "],"
        return rpoints
    def write_scad_file(self, filename, three_d=True):
        output = "// Made with lasercutmodel.py \n\n\n"
        if not three_d:
            output += "projection(cut = false)\n union() {\n"
        

        for laser_cut_out in self.laser_cut_outs:
            rotates = {1 : "rotate([0,0,0]) ", 2 : "rotate([0,-90,0]) ",  3 : "rotate([90,0,0]) "}
            if three_d:
                x,y,z = laser_cut_out.x_y_z_position
                rotates_text = rotates[laser_cut_out.orientation]
            else:
                z = 0
                x,y = laser_cut_out.x_y_flat_place
                rotates_text = rotates[1]
            output += "// " + laser_cut_out.name + " \n"
            output += "union() { \n"
            output += "\ttranslate([" + str(x) + "," + str(y) + "," + str(z) + "]) { \n"
            output += "\t\t" + rotates_text + "{ \n"        
            output += "\t\t\tdifference() { \n"        
            output += "\t\t\t\tunion() { \n"        
            output += "\t\t\t\t\tlinear_extrude(height = " + str(self.thickness) + " , center = false) \n"
            path = str(range(0, len(laser_cut_out.points)))
            points = self.polygon_points_format(laser_cut_out.points)
            path_num = len(laser_cut_out.points)
            if laser_cut_out.list_cutout_points:
                for cutout_points in laser_cut_out.list_cutout_points:
                    points += self.polygon_points_format(cutout_points)
                    path += "," + str(range(path_num, path_num+len(cutout_points)))
                    path_num += len(cutout_points)
            if laser_cut_out.tabs:
                for tab in laser_cut_out.tabs:
                    t = self.thickness
                    if tab.tab_type == 1:
                        if tab.tab_orientation == "up":
                            start_x = tab.x - self.thickness/2.0
                            start_y = tab.y
                        if tab.tab_orientation == "down":
                            start_x = tab.x - self.thickness/2.0
                            start_y = tab.y + self.thickness * 3
                        if tab.tab_orientation == "left":
                            start_x = tab.x + self.thickness
                            start_y = tab.y + self.thickness * 1.5
                        if tab.tab_orientation == "right":
                            start_x = tab.x - self.thickness-t
                            start_y = tab.y + self.thickness * 1.5
                        #cross hole
                        tab_points = [(start_x,start_y), (start_x+t, start_y), (start_x+t, start_y-t), (start_x+t+t, start_y-t),
                                      (start_x+t+t, start_y-t-t), (start_x+t, start_y-t-t), (start_x+t, start_y-t-t-t),  
                                      (start_x, start_y-t-t-t), (start_x, start_y-t-t), (start_x-t, start_y-t-t),
                                      (start_x-t, start_y-t), (start_x, start_y-t), (start_x, start_y)
                                     ]
                        points += self.polygon_points_format(tab_points)
                        path += "," + str(range(path_num, path_num+len(tab_points)))
                        path_num += len(tab_points)
                        if tab.tab_orientation == "down":
                            start_y = tab.y - self.thickness 
                        if tab.tab_orientation == "right":
                            start_x = start_x + (4*t) 
                        if tab.tab_orientation == "down" or tab.tab_orientation == "up":
                            start_x = start_x - t - (3*t)
                            # Stick out part 1
                            tab_points = [(start_x,start_y), (start_x+(3*t),start_y), (start_x+(3*t),start_y+t), 
                                          (start_x,start_y+t), (start_x,start_y)]
                        else:
                            start_x = start_x - 2*t
                            tab_points = [(start_x,start_y), (start_x,start_y+(3*t)), (start_x+t,start_y+(3*t)),
                                          (start_x+t,start_y), (start_x,start_y)]
                        points += self.polygon_points_format(tab_points)
                        path += "," + str(range(path_num, path_num+len(tab_points)))
                        path_num += len(tab_points)
                        if tab.tab_orientation == "down" or tab.tab_orientation == "up":
                            start_x = start_x + (6*t)
                            # Stick out part 2
                            tab_points = [(start_x,start_y), (start_x+(3*t),start_y), (start_x+(3*t),start_y+t), 
                                          (start_x,start_y+t), (start_x,start_y)]
                        else:
                            start_y = start_y - 6*t
                            tab_points = [(start_x,start_y), (start_x,start_y+(3*t)), (start_x+t,start_y+(3*t)),
                                          (start_x+t,start_y), (start_x,start_y)]
                        points += self.polygon_points_format(tab_points)
                        path += "," + str(range(path_num, path_num+len(tab_points)))
                        path_num += len(tab_points)
                    if tab.tab_type == 2:
                        tab_points = [(tab.x-t/2.0,tab.y-t/2.0), (tab.x+t/2.0,tab.y-t/2.0), (tab.x+t/2.0,tab.y+t/2.0),
                                      (tab.x-t/2.0,tab.y+t/2.0), (tab.x-t/2.0,tab.y-t/2.0)]
                        points += self.polygon_points_format(tab_points)
                        path += "," + str(range(path_num, path_num+len(tab_points)))
                        path_num += len(tab_points)
                        if tab.tab_orientation == "down" or tab.tab_orientation == "up":
                            tab_points = [(tab.x-t/2.0,tab.y+t*1.5), (tab.x-t/2.0+t,tab.y+t*1.5), (tab.x-t/2.0+t,tab.y+t*4.5),
                                          (tab.x-t/2.0,tab.y+t*4.5), (tab.x-t/2.0,tab.y+t*1.5)]
                        else:
                            tab_points = [(tab.x+t*1.5,tab.y-t/2.0), (tab.x+t*1.5,tab.y-t/2.0+t), (tab.x+t*4.5,tab.y-t/2.0+t),
                                          (tab.x+t*4.5,tab.y-t/2.0), (tab.x+t*1.5,tab.y-t/2.0)]
                        points += self.polygon_points_format(tab_points)
                        path += "," + str(range(path_num, path_num+len(tab_points)))
                        path_num += len(tab_points)
                        if tab.tab_orientation == "down" or tab.tab_orientation == "up":
                            tab_points = [(tab.x-t/2.0,tab.y+t*1.5-t*6), (tab.x-t/2.0+t,tab.y+t*1.5-t*6), (tab.x-t/2.0+t,tab.y+t*4.5-t*6),
                                          (tab.x-t/2.0,tab.y+t*4.5-t*6), (tab.x-t/2.0,tab.y+t*1.5-t*6)]
                        else:
                            tab_points = [(tab.x+t*1.5-t*6,tab.y-t/2.0), (tab.x+t*1.5-t*6,tab.y-t/2.0+t), (tab.x+t*4.5-t*6,tab.y-t/2.0+t),
                                          (tab.x+t*4.5-t*6,tab.y-t/2.0), (tab.x+t*1.5-t*6,tab.y-t/2.0)]
                        points += self.polygon_points_format(tab_points)
                        path += "," + str(range(path_num, path_num+len(tab_points)))
                        path_num += len(tab_points)
                    if tab.tab_type == 3 or tab.tab_type == 4:
                        start_x = tab.x
                        start_y = tab.y
                        if tab.tab_orientation == "down":
                            start_y = start_y - t
                        if tab.tab_orientation == "left":
                            start_x = start_x - t/2.0
                            start_y = start_y - t/2.0
                        if tab.tab_orientation == "right":
                            start_x = start_x + t/2.0
                            start_y = start_y - t/2.0
                        if tab.tab_orientation == "mid":
                            start_y = start_y - t/2.0

                        tab_points = [(start_x-t/2.0, start_y), (start_x-t/2.0, start_y+t), (start_x-t/2.0+t, start_y+t),
                                      (start_x-t/2.0+t, start_y), (start_x-t/2.0, start_y)]
                        points += self.polygon_points_format(tab_points)
                        path += "," + str(range(path_num, path_num+len(tab_points)))
                        path_num += len(tab_points)
                        



            output += "\t\t\t\t\tpolygon(points=[" + points + "], paths=[" + path + "]); \n"
            output += "\t\t\t\t} // End union \n"
            t = str(self.thickness)
            output += '\t\t\t\ttranslate(['+t+','+t+',-'+t+'/2]) linear_extrude(height = ' + t + '*2)  text("' + laser_cut_out.name + '", size='+t+'); \n'
            output += "\t\t\t} // End difference \n"
            output += "\t\t} // End rotate \n"
            output += "\t} // End translate \n"
            output += "} // End union \n\n"
        if not three_d:
            output += "} // end projection \n\n"
        
        # Now write
        f = open(filename, "w")
        f.write(output)
        f.close()
    

