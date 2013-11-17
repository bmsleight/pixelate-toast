#!/bin/bash
mkdir rows
rm rows/*
for i in {0..15}
do
   python cage_im.py -s test.scad  -x 15 -y 15 -j $i ; openscad -o rows/row$i.stl test.scad
   echo "Welcome $i times"
done

python cage_im.py -s test.scad  -x 15 -y 15 -j $i -n -m ; openscad -o rows/frame.stl test.scad

# Use meshlabserver to cobin into one stl file
meshlabserver -i ./rows/* -o cage_mesh_not_clean.stl -s mesh_flatten.mlx
