#!/bin/bash
# This get the unique land use 4 letter
# code of each hru.
sort 01_swatmodelling/swatlu.txt | uniq > mgtunique.lst

