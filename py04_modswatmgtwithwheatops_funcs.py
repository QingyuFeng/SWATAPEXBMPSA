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
PARMS = PARAMETERS()

import os, shutil
import fortranformat as ff


class SWATUtil(object):
    
    def copyorigmgttomodfd(self, hruno):
        
        sourcemgt = os.path.join(PARMS.originalmgt,
                            "%s.mgt" %(hruno))
        shutil.copy2(sourcemgt, PARMS.modifiedmgtnew)
                       

    def removemodmgtf(self, hruno):
        
        mgttoberemoved = os.path.join(PARMS.modifiedmgtnew,
                            "%s.mgt" %(hruno))
        if os.path.isfile(mgttoberemoved):
            os.remove(mgttoberemoved)
                
        
        
    

    
    # Reading mgt files
    def mgt_reader(self, hruno):
        
        fn_mgt = "%s.mgt" %(hruno)
        
        fn = os.path.join(PARMS.modifiedmgtnew, 
                          fn_mgt)
        
        try:
            fid = open(fn, "r")
        except:
            print("File %s does not exist!" %(fn_mgt))
            return
        
        lif = fid.readlines()
        fid.close()
        
        # The mgt lines will be stored in 
        # json data. It might be updated later.
        # Dict is easier.
        mgtparms = {}
        
        for lidx1 in range(30):
            
            key1 = "mgtln%i" %(lidx1)
            mgtparms[key1] = lif[lidx1]

        swatopsln = ff.FortranRecordReader(
        '(1x,i2,1x,i2,1x,f8.3,1x,i2,1x,i4,1x,i3,1x,i2,1x,f12.5,1x,f6.2,1x,f11.5,1x,f4.2,1x,f6.2,1x,f5.2,i12)')

        opslines = {}

        rotyr = int(mgtparms["mgtln28"].split("|")[0])
        
        
        for idx in range(rotyr):
            yrkey = "yr%i" %(idx+1) 
            opslines[yrkey] = {}

        yearidx = 1
        yropsid = 1

        # First, create a structure of all dict.
        for lidx2 in range(30, len(lif)):
            yrkey2 = "yr%i" %(yearidx)
            key2 = "opsline%i" %(yropsid)
            yropsid = yropsid + 1
            opslines[yrkey2][key2] = {}
            tmpl1 = swatopsln.read(lif[lidx2])

            opslines[yrkey2][key2]["mon"] = tmpl1[0]
            opslines[yrkey2][key2]["day"] = tmpl1[1]
            opslines[yrkey2][key2]["hu"] = tmpl1[2]
            opslines[yrkey2][key2]["mgtop"] = tmpl1[3]
            opslines[yrkey2][key2]["mgt1"] = tmpl1[4]
            opslines[yrkey2][key2]["mgt2"] = tmpl1[5]
            opslines[yrkey2][key2]["mgt3"] = tmpl1[6]
            opslines[yrkey2][key2]["mgt4"] = tmpl1[7]
            opslines[yrkey2][key2]["mgt5"] = tmpl1[8]
            opslines[yrkey2][key2]["mgt6"] = tmpl1[9]
            opslines[yrkey2][key2]["mgt7"] = tmpl1[10]
            opslines[yrkey2][key2]["mgt8"] = tmpl1[11]
            opslines[yrkey2][key2]["mgt9"] = tmpl1[12]
            opslines[yrkey2][key2]["mgt10"] = tmpl1[13]
            
            if tmpl1[3] == 17 or tmpl1[3] == 0:
                yearidx = yearidx + 1
                yropsid = 1           
        
        return mgtparms, opslines            
        
