# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 09:50:42 2017

This script was created to modify the SWAT 
input files for simulation of BMP parameters.

Target input of BMPs include:
    1. nutrient management: placement, method, amount, time.
    2. cover crops
    3. grassed filter strips
    
The program will be modulized and allow expansion to other BMPs.

These three targeted BMPs mainly require modification of
mgt and ops files. 

@author: qyfen
"""

######################################################
# module import
######################################################

from py02_swatbmpfuncs import SWATUtil
from py02_swatbmpparms import PARAMETERS
from py02_swatbmpuserinput import *

PARMS = PARAMETERS()
SWATUtil = SWATUtil()
NUTRIENT4R = NUTRIENT4R()
COVERCROPS = COVERCROPS()
FILTERSTRIPS = FILTERSTRIPS()
NUTRIENT4R_SFunc = NUTRIENT4R_SFunc()

import os, subprocess
import glob, shutil
from datetime import datetime 

######################################################
# User input
######################################################


def main_hrumodifier(hruno):

    # This main program deals with each hru bmp.
    # Loop through each hru and modify the 
    # desired BMP. 
    # First, make sure all mgts are the same as default.
    PARMS.removemgtinswattio(PARMS.hrunolist[hruidx])
    # copy the orignal to the default folder
    # Then copy the files         
    PARMS.copyorigmgttoswattios(PARMS.hrunolist[hruidx])
    
    # The first step is to determine the variables
    # to be modified.
    PARMS.mgtparms, PARMS.opslines = SWATUtil.mgt_reader(hruno,
                                                         PARMS.infd_swattxtinout)    
    
    # First, empty the ops files.
    SWATUtil.empty_opsfile(hruno, PARMS)
    # Then, I need to modify the desired parameters
    # This depends on the BMPs desired.
    # The first series of BMP is to simulate the nutrient
    # management.
    # These BMPs are mainly applied on crop land.
    # It was defined in the parameters. So, if
    # it does not cropland, continue
    currlu = PARMS.mgtparms["mgtln0"].split(" ")[7].split(":")[1]

    if currlu in PARMS.croplandlu:
        
        # Start applying BMPs.
        # Applying nutrient management.
        # If any of the fert option is larger than 0, run it
        if (NUTRIENT4R.fertamount[0] == 1 or 
            NUTRIENT4R.fertappdate[0] == 1 or
            NUTRIENT4R.fertid[0] == 1 or
            NUTRIENT4R.fertsurfratio[0] == 1):
            PARMS.opslines = SWATUtil.nutrientmanagement(NUTRIENT4R, 
                                                     PARMS.opslines, 
                                                     PARMS.swatfert)
        
            # Applying cover crops
            if COVERCROPS.cvcropplant[0] == 1:
                SWATUtil.addcovercrops(COVERCROPS, PARMS)

            # Then write the opslines to a the original parameter files.

            SWATUtil.updatemgt(hruno, PARMS)
        
            # After finishing run the modification, copy the output from 
            # modified mgt to the default files
            # But first, delete the mgt in the default folder to make
            # sure that the copy is good.
            PARMS.removemgtinswattio(PARMS.hrunolist[hruidx])
            # Then copy the files         
            PARMS.copymgttoswattios(PARMS.hrunolist[hruidx])
        
        
        
        # Adding filter strips
        # For OPS files, if there is not ops,
        # The current one will be emptyed. 
        # If we need to add one line, based on the template.
        if FILTERSTRIPS.fltstrip[0] == 1:
            SWATUtil.update_opslines(hruno, PARMS, FILTERSTRIPS)
            SWATUtil.updateopsfile(hruno, PARMS)
            PARMS.removeopsinswattio(PARMS.hrunolist[hruidx])
            # Then copy the files         
            PARMS.copyopstoswattios(PARMS.hrunolist[hruidx])
        
                    
            
# To include a main program is for the potential 
# of multiple processing.

#import os
#luselst = "swatlu.txt"
#fn = os.path.join(PARMS.infd_swatmain,
#                  luselst)
#fid = open(fn, "w")

# I need to put the series into a loop.
# The steps include:
# 1. get the parameter values
# 2. remove the modified ops and mgt files
# 3. modify the parameters
# 4. Run the programs
# 5. Copy the output to the output folder.
# 6. Delete the output folder from the running folder.
            
# I will write the returning code into a file, if
# it is not zero, it will be recorded, but the program
# will continue with the next file
fid_error = open("scenariorunrecord.txt", "w")
starttime = 0
timeelapse = 0
# Step 1: loop through each scenario
            
for scenidx in range(3, len(PARMS.scenariolns)):
    
    starttime=datetime.now() 
    print("Processing scenario %s: \n" %(
            PARMS.scenariolns[scenidx]))
    print(starttime.strftime("%Y-%m-%d %H:%M:%S"))
    
    NUTRIENT4R_SFunc.scenarioinput(NUTRIENT4R,
                   PARMS.scenariolns[scenidx])
    
    # After appending the input variable, I need to 
    # Prepare the output folder:
    PARMS.outfd_scenario = os.path.join(
                        PARMS.outfd_outputmain,
                        "S%s_outputs" %(
                        PARMS.scenariolns[scenidx][0]))
    # Then process the temporary management files
    PARMS.removecreatefolder(PARMS.outfd_scenario)
    PARMS.removecreatefolder(PARMS.modifiedmgt)
    PARMS.removecreatefolder(PARMS.modifiedops)
    
    print("Adding BMPs\n")
    # Then run the programs
    for hruidx in range(len(PARMS.hrunolist)):
        main_hrumodifier(PARMS.hrunolist[hruidx])
    
    timeelapse = datetime.now()-starttime
    starttime = datetime.now()
    print("Time used: \n", timeelapse)
    print("Current time: \n", starttime.strftime("%Y-%m-%d %H:%M:%S"))

    print("Running SWAT")
    # After finishing the modification, the next step is to run the 
    # SWAT model.
    os.chdir(PARMS.infd_swattxtinout)
    swatrunstatus = 9999
    swatrunstatus = subprocess.call(
            "./swat2012spcon61464.exe",
            shell=True)
    fid_error.writelines("Scenario_%s\t%i" %(PARMS.scenariolns[scenidx],
                                             swatrunstatus))
    
    timeelapse = datetime.now()-starttime
    starttime = datetime.now()
    print("Time used: \n", timeelapse)
    print("Current time: \n", starttime.strftime("%Y-%m-%d %H:%M:%S"))

    # After running, change the folder back to main
    # Then remove the modified mgt, and copy the original
    # mgt back to the text in out since the mgt modification
    # all started with the default mgt.
    os.chdir("../..")
    
    # I forget to copy the output to the output folder
    print("Copy output to output folder")

    outputlist = []
    for file in glob.glob(os.path.join(PARMS.infd_swattxtinout,
                                       "output.*")):
        outputlist.append(file)
        
    for outfidx in outputlist:
        shutil.copy2(outfidx, PARMS.outfd_scenario)
    
    
    
    print("Post Processing files")
    
    timeelapse = datetime.now()-starttime
    starttime = datetime.now()
    print("Time used: \n", timeelapse)
    print("Current time: \n", starttime.strftime("%Y-%m-%d %H:%M:%S"))

    for hruidx in range(len(PARMS.hrunolist)):
            
        # After finishing run the modification, copy the output from 
        # modified mgt to the default files
        # But first, delete the mgt in the default folder to make
        # sure that the copy is good.
        PARMS.removemgtinswattio(PARMS.hrunolist[hruidx])
        # Then copy the files         
        PARMS.copyorigmgttoswattios(PARMS.hrunolist[hruidx])
    
        PARMS.removeopsinswattio(PARMS.hrunolist[hruidx])
        # Then copy the files         
        PARMS.copyorigopstoswattios(PARMS.hrunolist[hruidx])
            
    print("Finished one BMP simulation")
    
fid_error.close()  
#
#fid.close()    
