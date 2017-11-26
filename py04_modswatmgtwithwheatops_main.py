# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 09:50:42 2017

This code was developed to modify the 
mgt files that have problems with winterwheat simulation.
The rotation they worked on is not correct.

The program will have the following steps:
    1. read in mgt files
    2. determine whether it is wheat mgt
    3. If it is, read in the old, and change the order
    of them.

@author: qyfen
"""
from py04_modswatmgtwithwheatops_parms import *
from py04_modswatmgtwithwheatops_funcs import *

PARMS = PARAMETERS()
SWATUtil = SWATUtil()


def changewheatmgt(hruno):

    
    SWATUtil.removemodmgtf(hruno)
    
    # The first step is to copy the original
    # mgt to modified mgt.
    SWATUtil.copyorigmgttomodfd(hruno)
    
    # Then determine the variables
    # to be modified.
    PARMS.mgtparms, PARMS.opslines = SWATUtil.mgt_reader(hruno)    
    
# Then run the programs
for hruidx in range(100): #len(PARMS.hrunolist)):
    
    changewheatmgt(PARMS.hrunolist[hruidx])
    
    currlu = PARMS.mgtparms["mgtln0"].split(" ")[7].split(":")[1]

    if currlu in PARMS.wheatlandlu:
#    if currlu == "CWHT":
        print("yes", currlu, PARMS.hrunolist[hruidx])
        
    
    
    
    
    
    
    
    
    
    
    
    
    