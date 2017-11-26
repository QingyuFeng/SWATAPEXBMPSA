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

import os


class PARAMETERS(object):

    """ Parameters related to the program """
    def __init__(self):
        
        self.infd_swatmain = "01_swatmodelling"
        self.infd_swattxtinout = os.path.join(
                            self.infd_swatmain,
                            "01_default")
        
        self.originalmgt = os.path.join(
                            self.infd_swatmain,
                            "04_originalmgt")
        
        self.modifiedmgtnew = os.path.join(
                    self.infd_swatmain,
                    "08_modifiedmgt_wheat")
        
        # all land use types in the SWAT model
        self.wheatlandlu = ["CWHT", "SYWH", "WHCN"]
        
        self.infn_hrunolst = "hrugisnum.list"
        self.hrunolist = self.gethrulist()

        # parameters related to management
        self.mgtparms = {}
        # The ops lines here is actually operation
        # lines in the mgt file
        self.opslines = {}        

    def gethrulist(self):
        
        infn = os.path.join(self.infd_swatmain,
                            self.infn_hrunolst)
        
        try: 
            infid = open(infn, "r")
        except:
            print("File %s does not exist!" %(infn))
            return        
        
        lif = infid.readlines()
        infid.close()
        
        for lidx in range(len(lif)):
            lif[lidx] = lif[lidx][:-1]
            
        return lif        
        
        
        
        
        
        
        
        
        