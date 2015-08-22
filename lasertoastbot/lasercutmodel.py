#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division

import os, sys, copy

from solid import *
from solid.utils import *


class tab:
    def __init__(self, tab_type, x=0, y=0, tab_orientation="up", number=1):
        # 1 is a female captive nut
        # 2 is the male captive nut  
        self.tab_type = tab_type
        self.x = x
        self.y = y
        self.tab_orientation = tab_orientation
        self.number = number


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
    def __init__(self, thickness, kerf = 0.2):
        self.thickness = thickness
        self.laser_cut_outs = []
        self.kerf = kerf
        self.extra_scad = ""
    def find_cut_out(self, name_of_cut_out):
        foundIndex = -1
        for i in range(0, len(self.laser_cut_outs)):
            if name_of_cut_out == self.laser_cut_outs[i].name:
                foundIndex = i
        return foundIndex

    def rough_layout_2d(self, max_width = 0):
        # max(y for x, y in l)
        max_sizes = []
        for laser_cut_out in self.laser_cut_outs:
            # Find wide/heighest point then add 4*thickness as boarder
            max_x = max(x for x, y in laser_cut_out.points) + 3*self.thickness
            max_y = max(y for x, y in laser_cut_out.points) + 3*self.thickness
            max_sizes.append((max_x, max_y))
        x_flat_place, y_flat_place = (0,0)
        y_inc_max = 0
        if max_width == 0:
            max_width = max(x for x, y in max_sizes)
        for i in range(0, len(self.laser_cut_outs)):
            self.laser_cut_outs[i].x_y_flat_place = (x_flat_place, y_flat_place)
            x_inc, y_inc = max_sizes[i]
            if y_inc > y_inc_max:
                y_inc_max = y_inc
            x_flat_place += x_inc
            if i < len(self.laser_cut_outs) - 1:
                # not at last peice
                next_x, next_y = max_sizes[i+1]
                if (x_flat_place + next_x) > max_width:
                    x_flat_place = 0 
                    y_flat_place += y_inc_max
                    y_inc_max = 0
                else:
                    pass

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

    def copy_laser_cut_out(self, old_name, new_name):
        foundIndex = self.find_cut_out(old_name)
        if foundIndex !=-1:
            c = copy.deepcopy(self.laser_cut_outs[foundIndex])
            c.name = new_name
            self.laser_cut_outs.append(c)

    def copy_laser_cut_out(self, old_name, new_name, x_y_z_position):
        foundIndex = self.find_cut_out(old_name)
        if foundIndex !=-1:
            c = copy.deepcopy(self.laser_cut_outs[foundIndex])
            c.name = new_name
            c.x_y_z_position = x_y_z_position
            self.laser_cut_outs.append(c)

    def update_x_y_z(self, name_of_cut_out, x_y_z_position):
        foundIndex = self.find_cut_out(name_of_cut_out)
        if foundIndex !=-1:
            self.laser_cut_outs[foundIndex].x_y_z_position = x_y_z_position


    def add_tab(self, name_of_cut_out, tab_type, x=0, y=0, tab_orientation="up", number=1):
        foundIndex = self.find_cut_out(name_of_cut_out)
        if foundIndex !=-1:
            new_tab = tab(tab_type=tab_type, x=x, y=y, tab_orientation=tab_orientation, number=number)
            self.laser_cut_outs[foundIndex].tabs.append(new_tab)
        else:
            print("No cutout for tab - raise exception")

    def add_box(self, name, width=200, height=50, depth=100, x_y_z_position=(0,0,0), number_sides=6, number_tabs=8):
        # Make adjustments so that box bound inside width, height anf depth and at x,y,z position
        x, y, z = x_y_z_position
        y = y + self.thickness
        depth = depth - 2*self.thickness
        height = height - self.thickness
        if number_sides > 4:
            x = x + self.thickness
            width = width - self.thickness
        if number_sides > 5:
#            x = x + self.thickness
            width = width - 2*self.thickness

        # End Adjustments
        side_name = name + " 1"
        self.add_square_cut_out(side_name, width=width, height=depth, orientation=1, x_y_z_position=(x,y,z))
        self.add_tab(side_name, tab_type=5, tab_orientation="up", number=number_tabs)
        self.add_tab(side_name, tab_type=5, tab_orientation="down", number=number_tabs)
        if number_sides > 4:
            self.add_tab(side_name, tab_type=5, tab_orientation="left", number=number_tabs)
        if number_sides > 5:
            self.add_tab(side_name, tab_type=5, tab_orientation="right", number=number_tabs)
        if number_sides > 1:
            side_name_old = side_name 
            side_name = name + " 6"
            # Note dice sides, so the first four are 1,6, 2,5, followed by 3,4
            self.copy_laser_cut_out(side_name_old, side_name, (x,y,z+height))
            if number_sides > 4:
                self.add_tab(side_name, tab_type=4, x=0, y=depth+self.thickness/2, tab_orientation="left")
            if number_sides > 5:
                self.add_tab(side_name, tab_type=4, x=width, y=depth+self.thickness/2, tab_orientation="right")
        if number_sides > 2:
            side_name = name + " 2"
            self.add_square_cut_out(side_name, width=width, height=height-self.thickness, orientation=3, x_y_z_position=(x,y,z+self.thickness))
            self.add_tab(side_name, tab_type=6, tab_orientation="up", number=number_tabs)
            self.add_tab(side_name, tab_type=6, tab_orientation="down", number=number_tabs)
            if number_sides > 4:
                self.add_tab(side_name, tab_type=5, tab_orientation="left", number=number_tabs)
            if number_sides > 5:
                self.add_tab(side_name, tab_type=5, tab_orientation="right", number=number_tabs)
            if number_sides > 3:
                side_name_old = side_name 
                side_name = name + " 5"
                self.copy_laser_cut_out(side_name_old, side_name, (x,y+depth+self.thickness,z+self.thickness))
        if number_sides > 4:
            side_name = name + " 3"
            self.add_square_cut_out(side_name, width=height-self.thickness, height=depth, orientation=2, x_y_z_position=(x,y,z+self.thickness))
            self.add_tab(side_name, tab_type=6, tab_orientation="up", number=number_tabs)
            self.add_tab(side_name, tab_type=6, tab_orientation="down", number=number_tabs)
            self.add_tab(side_name, tab_type=6, tab_orientation="left", number=number_tabs)
            self.add_tab(side_name, tab_type=6, tab_orientation="right", number=number_tabs)
            # The missing squares
            self.add_tab(side_name, tab_type=4, x=0, y=depth+self.thickness/2, tab_orientation="left")
            self.add_tab(side_name, tab_type=4, x=0, y=-self.thickness/2, tab_orientation="left")
            self.add_tab(side_name, tab_type=4, x=height-self.thickness/2, y=0, tab_orientation="down")
        if number_sides > 5:
                side_name_old = side_name 
                side_name = name + " 4"
                self.copy_laser_cut_out(side_name_old, side_name, (x+width+self.thickness,y,z+self.thickness))


    def add_inner_cutout(self, name_of_cut_out, inner_points):
        foundIndex = self.find_cut_out(name_of_cut_out)
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
    def write_scad_file(self, filename, three_d=True, text=True, text_scale=1):
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
            output += "\t\t\t\t\tlinear_extrude(height = " + str(self.thickness) + " , center = false) "
            if three_d:
                output += "offset(delta = -" + str(self.kerf/2) + ") \n"
            else:
                output += "\n"
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
                        if tab.tab_orientation == "down" or tab.tab_orientation == "up":
                            tab_points = [(tab.x,tab.y-t/2.0), (tab.x+t,tab.y-t/2.0), (tab.x+t,tab.y+t/2.0),
                                          (tab.x,tab.y+t/2.0), (tab.x,tab.y-t/2.0)]
                        else:
                            tab_points = [(tab.x-t/2.0,tab.y-t/2.0), (tab.x+t/2.0,tab.y-t/2.0), (tab.x+t/2.0,tab.y+t/2.0),
                                          (tab.x-t/2.0,tab.y+t/2.0), (tab.x-t/2.0,tab.y-t/2.0)]
                        points += self.polygon_points_format(tab_points)
                        path += "," + str(range(path_num, path_num+len(tab_points)))
                        path_num += len(tab_points)
                        if tab.tab_orientation == "down" or tab.tab_orientation == "up":
                            tab_points = [(tab.x,tab.y+t*1.5), (tab.x+t,tab.y+t*1.5), (tab.x+t,tab.y+t*4.5),
                                          (tab.x,tab.y+t*4.5), (tab.x,tab.y+t*1.5)]
                        else:
                            tab_points = [(tab.x+t*1.5,tab.y-t/2.0), (tab.x+t*1.5,tab.y-t/2.0+t), (tab.x+t*4.5,tab.y-t/2.0+t),
                                          (tab.x+t*4.5,tab.y-t/2.0), (tab.x+t*1.5,tab.y-t/2.0)]
                        points += self.polygon_points_format(tab_points)
                        path += "," + str(range(path_num, path_num+len(tab_points)))
                        path_num += len(tab_points)
                        if tab.tab_orientation == "down" or tab.tab_orientation == "up":
                            tab_points = [(tab.x,tab.y+t*1.5-t*6), (tab.x+t,tab.y+t*1.5-t*6), (tab.x+t,tab.y+t*4.5-t*6),
                                          (tab.x,tab.y+t*4.5-t*6), (tab.x,tab.y+t*1.5-t*6)]
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
                    if tab.tab_type == 5 or tab.tab_type == 6:
                        # five starts down, six starts in up position
                        max_x = max(x for x, y in laser_cut_out.points)
                        min_x = min(x for x, y in laser_cut_out.points)
                        max_y = max(y for x, y in laser_cut_out.points)
                        min_y = min(y for x, y in laser_cut_out.points)
                        start_x, start_y = (0,0)
                        if tab.tab_orientation == "up":
                            start_x = min_x
                            start_y = max_y
                            end_x = max_x
                            end_y = max_y
                            inc_y = t
                            inc_x = (end_x - start_x)/float(tab.number*2)
                        if tab.tab_orientation == "down":
                            start_x = min_x
                            start_y = min_y-t
                            end_x = max_x
                            end_y = min_y
                            inc_y = t
                            inc_x = (end_x - start_x)/float(tab.number*2)
                        if tab.tab_orientation == "left":
                            start_x = min_x-2*t
                            start_y = min_y
                            end_x = min_x
                            end_y = max_y
                            inc_y = (end_y - start_y)/float(tab.number*2)
                            inc_x = t
                        if tab.tab_orientation == "right":
                            start_x = max_x-t
                            start_y = min_y
                            end_x = max_x
                            end_y = max_y
                            inc_y = (end_y - start_y)/float(tab.number*2)
                            inc_x = t
                        tab_points = []
                        for notches in range(0, tab.number):
                            if (tab.tab_orientation == "up") or (tab.tab_orientation == "down"):
                                if tab.tab_type == 5:
                                    tab_points = [(start_x+inc_x, start_y), (start_x+inc_x*2, start_y), (start_x+inc_x*2, start_y+inc_y),
                                                  (start_x+inc_x, start_y+inc_y), (start_x+inc_x, start_y)]
                                if tab.tab_type == 6:
                                    tab_points = [(start_x, start_y), (start_x+inc_x, start_y), (start_x+inc_x, start_y+inc_y),
                                                  (start_x, start_y+inc_y), (start_x, start_y)]
                            if (tab.tab_orientation == "left") or (tab.tab_orientation == "right"):
                                if tab.tab_type == 5:
                                    tab_points = [(start_x+inc_x, start_y+inc_y), (start_x+inc_x*2, start_y+inc_y), (start_x+inc_x*2, start_y+inc_y+inc_y),
                                                  (start_x+inc_x, start_y+inc_y+inc_y), (start_x+inc_x, start_y+inc_y)]
                                if tab.tab_type == 6:
                                    tab_points = [(start_x+t, start_y), (start_x+inc_x+t, start_y), (start_x+inc_x+t, start_y+inc_y),
                                                  (start_x+t, start_y+inc_y), (start_x+t, start_y)]


                            if tab.tab_orientation == "up" or tab.tab_orientation == "down":
                                start_x += inc_x*2
                            if tab.tab_orientation == "left" or tab.tab_orientation == "right":
                                start_y += inc_y*2
                            points += self.polygon_points_format(tab_points)
                            path += "," + str(range(path_num, path_num+len(tab_points)))
                            path_num += len(tab_points)
#                            tab_points = []


            output += "\t\t\t\t\tpolygon(points=[" + points + "], paths=[" + path + "]); \n"
            output += "\t\t\t\t} // End union \n"
            if text:
                t = str(self.thickness)
                output += '\t\t\t\ttranslate(['+t+','+t+',-'+t+'/2]) linear_extrude(height = ' + t + '*2)  text("' + laser_cut_out.name + '", size='+t+'*'+str(text_scale)+'); \n'
            output += "\t\t\t} // End difference \n"
            output += "\t\t} // End rotate \n"
            output += "\t} // End translate \n"
            output += "} // End union \n\n"
        if not three_d:
            output += "} // end projection \n\n"
        else:
            output += "// Extra scad \n" + self.extra_scad + "\n\n"
        
        # Now write
        f = open(filename, "w")
        f.write(output)
        f.close()
    

