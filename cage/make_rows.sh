#!/bin/bash


size=$1
mkdir rows
rm rows/*
#for i in {0..15}
for i in $(eval echo {0..$size})
do
   python cage_im.py -s test.scad  -x $size -y $size -j $i ; openscad -o rows/row$i.stl test.scad
done

python cage_im.py -s test.scad  -x $size -y $size -j $i -n -m ; openscad -o rows/frame.stl test.scad

# Use meshlabserver to cobin into one stl file
meshlabserver -i ./rows/* -o cage_mesh_not_clean.stl -s mesh_flatten.mlx
