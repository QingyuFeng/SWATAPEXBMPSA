#!/bin/bash
# This script was written to generate
# a text files containing all HRU numbers# in one project. 
# It was written to be run under the
# Default folder. 

for i in  01_swatmodelling/01_default/*.hru; do
    name1=${i##*\/}
    name2=${name1%%\.hru}
    echo $name2
done > 01_swatmodelling/hrugisnum.list
