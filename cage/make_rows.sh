#!/bin/bash
for i in {0..15}
do
   python cage_im.py -s test.scad  -x 15 -y 15 -j $i ; openscad -o rows/row$i.stl test.scad
   echo "Welcome $i times"
done
