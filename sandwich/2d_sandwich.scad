use <lasercut.scad>; 
projection(cut = false) 
	
lasercutout(thickness=3.1, 
             points= [[0, 0], [120, 0], [120, 176.3], [0, 176.3], [0, 0]], 
            simple_tabs = [], 
            simple_tab_holes = [], 
            captive_nuts = [], 
            captive_nut_holes = [], 
            finger_joints = [], 
            circles_add = [], 
            circles_remove = [], 
            slits = [], 
            cutouts = [[10, 56.3, 100, 100]]) 

lasercutout(thickness=3.1, 
             points= [[0, 0], [120, 0], [120, 176.3], [0, 176.3], [0, 0]], 
            simple_tabs = [], 
            simple_tab_holes = [], 
            captive_nuts = [], 
            captive_nut_holes = [], 
            finger_joints = [], 
            circles_add = [], 
            circles_remove = [], 
            slits = [], 
            cutouts = []) 

lasercutout(thickness=3.1, 
             points= [[0, 0], [100, 0], [100, 156.3], [0, 156.3], [0, 0]], 
            simple_tabs = [], 
            simple_tab_holes = [], 
            captive_nuts = [], 
            captive_nut_holes = [], 
            finger_joints = [], 
            circles_add = [], 
            circles_remove = [], 
            slits = [], 
            cutouts = []) 

;
