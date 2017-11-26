# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 09:50:42 2017

This contains all functions for the main program.

Parameters are those generated or modified by other 
classes. 
global variables are general fixed variables.



@author: qyfen
"""

import os, shutil
import fortranformat as ff
import time


class PARAMETERS:
    
    """ Parameters related to the program """
    def __init__(self):
        
        self.infd_swatmain = "01_swatmodelling"
        self.infd_swattxtinout = os.path.join(
                            self.infd_swatmain,
                            "01_default")
        
        self.modifiedmgt = os.path.join(
                            self.infd_swatmain,
                            "03_modifiedmgt")
        
        self.modifiedops = os.path.join(
                            self.infd_swatmain,
                            "06_modifiedops")
                
        self.originalmgt = os.path.join(
                            self.infd_swatmain,
                            "04_originalmgt")
        
        self.originalops = os.path.join(
                            self.infd_swatmain,
                            "05_originalops")
                       
        
        self.outfd_outputmain = os.path.join(
                            self.infd_swatmain,
                            "07_output")
        
        # Need to be modified for each run
        self.outfd_scenario = "01_baseline"
        
        self.infn_hrunolst = "hrugisnum.list"
        
        self.hrunolist = self.gethrulist()
        
        self.ierror = 0
        
        # parameters related to management
        self.mgtparms = {}
        # The ops lines here is actually operation
        # lines in the mgt file
        self.opslines = {}
        self.bmpopsfileheader = ""
        self.bmplinesops = {}
        
        # all land use types in the SWAT model
        self.croplandlu = ["CCRN", "CSOY", "CWHT",
                          "SYCN", "SYWH", "WHCN"]
        self.otherlandlu = ["FRSD", "PAST", "URHD", "URMD",
                          "WATR"] 
        
        # Block of codes to define P application, get fert db
        self.infd_apex = "02_apexmodelling"
        self.fn_swatfert = "fert.dat"
        self.fd_swat2apexdb = "06_dbswat2apex"
        self.swatfert = self.get_swatfertdict()

        self.infn_scenarios = "scenarios.csv"
        self.scenariolns = self.get_scenarioparam()
        
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




    def get_swatfertdict(self):
        
        # This functio will create a dictionary
        # of swat crop database. The dictionary
        # key will be the plant id in the model.
        # The purpose is to get the crop name
        # to be selected by APEX
        
        fn = os.path.join(self.infd_apex,
                          self.fd_swat2apexdb,
                          self.fn_swatfert)
        
        fid = open(fn, "r")
        lif = fid.readlines()
        fid.close()
        
        swatfert = {}        
                
        for lidx in range(len(lif)):
            lif[lidx] = lif[lidx].split(" ")
            while "" in lif[lidx]:
                lif[lidx].remove("")

            swatfert[lif[lidx][0]] = lif[lidx]
        
        return swatfert  
    
    
    def get_scenarioparam(self):
        
        import csv
        
        scenariolines = []
        
        with open(self.infn_scenarios, "rb") as csvfile:
            scenariordr = csv.reader(csvfile, delimiter=",")
            for row in scenariordr:
                scenariolines.append(row)
                
        return scenariolines
        
        
        
    def removecreatefolder(self, foldername):
        
        if not os.path.isdir(foldername):
            os.mkdir(foldername)  
        else:
            shutil.rmtree(foldername)
            os.mkdir(foldername)  

    
    def removemgtinswattio(self, hruno):
        
        mgttoberemoved = os.path.join(self.infd_swattxtinout,
                            "%s.mgt" %(hruno))
        if os.path.isfile(mgttoberemoved):
            os.remove(mgttoberemoved)
        
        
    
    
    def copymgttoswattios(self, hruno):
        
        sourcemgt = os.path.join(self.modifiedmgt,
                            "%s.mgt" %(hruno))
        shutil.copy2(sourcemgt, self.infd_swattxtinout)
                
        
        
    def copyorigmgttoswattios(self, hruno):
        
        sourcemgt = os.path.join(self.originalmgt,
                            "%s.mgt" %(hruno))
        shutil.copy2(sourcemgt, self.infd_swattxtinout)
                       
        
        
        
        
        
    def removeopsinswattio(self, hruno):
        
        opstoberemoved = os.path.join(self.infd_swattxtinout,
                            "%s.ops" %(hruno))
        if os.path.isfile(opstoberemoved):
            os.remove(opstoberemoved)
                
        
        
    
    def copyopstoswattios(self, hruno):
        
        sourceops = os.path.join(self.modifiedops,
                            "%s.ops" %(hruno))
        shutil.copy2(sourceops, self.infd_swattxtinout)
            
        
        
    def copyorigopstoswattios(self, hruno):
        
        sourceops = os.path.join(self.originalops,
                            "%s.ops" %(hruno))
        shutil.copy2(sourceops, self.infd_swattxtinout)
                
                                

        