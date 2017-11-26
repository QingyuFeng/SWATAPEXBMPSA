# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 09:50:42 2017

This class contains all BMPs specified by
user to simulate.

@author: qyfen
"""

######################################################
# module import
######################################################


######################################################
# User input
######################################################

"""
# BMP 
# The simulation of BMP was conducted in series.
# You can input one or more BMP variables. Different BMP
# may require different inputs and need to be specified 
# correspondingly.

BMP that are included in this script include:
    1. nutrient placement ("NUPLACE")
    2. nutrient amount ("NUAMOUNT")
    3. nutrient time ("NUTIME")
    3. nutrient source ("NUSOURCE")

"""
class NURTIENT4R(object):
    
    # BMP types can be implemented in series
    # Multiple BMP are inplemented in ["BMP1", "BMP2"]
    # The characters need to be selected from the above list.

    # The first variable in the list of each BMP 
    # is the switch indicating whether the BMP will
    # be simulated. 
    def __init__(self):
#    self.fertappdate = [[9, 15]]
        self.fertappdate = [1, [11, 28]]
    
        # Nutrient amount
        # Same as the date, if multiple application is specified.
        # the amount of each can be specified.
        # feramount = ["amount1", "amount2"]
    #    self.fertamount = ["200"]
        self.fertamount = [1, 200]
        
        # Nutrient placement
        # Same as the date, if multiple application is specified.
        # the amount of each can be specified.
        # feramount = ["ratio1", "ratio2"]
    #    self.fertsurfratio = ["0"]
        # The value range from 0 to 1
        self.fertsurfratio = [1, 0.5]
    
        # Fertilizer number
        # If the user want to specify the type of the fertilizer,
        # you can also specify that from the database of fertilizer
        # id.
        self.fertid = [1, 22]
    
        # For APEX, it is also possible to simulate the impor
        # While, it is mainly for the purpose of economic
        # analysis. So, I will not include it here.



class COVERCROPS(object):
    
    # Cover crops are planted after harvest of the main crop and
    # then harvest and kill the next year before planting.
    # Common cover crops include:
    # radish(#134)
    
    # rye (#19)
    # Oats (#16)
    # ryegrass (#41)
    # Alfalfa (#31)
    # Clover (#32)
    cvcropplant = [0, 19]
    
    # This is the cover crop time delta
    # after than the last operation of the 
    # normal crop. I will put 7 as default.
    cvcropplantdatetd = [0, 7]
    
    # This is the cover crop time delta
    # before than the first operation of the 
    # normal crop. I will put 7 as default.
    cvcropkilldatetd = [0, 7]
    

class FILTERSTRIPS(object):
    
    # Simulation of filter strips in the SWAT model
    # included parameters:
    # mgt_op code = 4
    # VFSCON: Fration of the total runoff from the entire 
    #         field entering the most concentrated 10% of
    #         the VFS. Set a value between 0.25 to 0.75, 
    #         recommend 0.5
    # VFSRATIO: Field area to VFS area ratio, recommended
    #           value of 40 -60
    # VFSCH: Fraction of flow through the most concentrated
    #        10% of the VFS that is fully channelized.
    #        Recommended  value of 0 unless VFS has failed.
    # To switch this on, set the first element to be 1.
    # Then, the three parameters are listed in the second 
    # element, which is also a list.[VFSCON, VFSRATIO, VFSCH]
    iflag_inst = 0
    FS_PEC = 0.6
    FS_SLPfactor = 0.25
    FS_SPLG = 10
    FS_UPN = 0.1
    FS_RCHL = 10
    FS_CHN = 0.1
    FS_RCHL = 0.010 #km
    FS_RCHD = 0.01
    FS_RCBW = 0.1
    FS_RCTW = 0.2
    FS_RCHN = 0.2
    FS_RCHC = 0.001
    FS_RCHK = 0.3
    FS_RFPW = 0
    FS_RFPL = 0.01
    FS_FFPQ = 0.95
    FS_LUNS = 22

    FS_Crop = 35 # 35 is for Timothy
    
    FS_AreaFrac = 0.1 # Range from 0 to 1.
    FS_width = 10 # Maximum 30m
    

class NUTRIENT4R_SFunc(object):
    
    def scenarioinput(self, NURTIENT4R, scenarioline):
        # This function modify the values of nutrient management
        # based on scenarios
        # It looks like all four will be 1s. 
        # The main thing is to determine the length of 
        # variables. There will be the following scenarios:
        # The most influencing variable will be:
        # plancement: placement required two dates.
        # types: manure. 
        # Start with placement:
        if scenarioline[3] == "Surface":
            if scenarioline[4] == "Element P":
                # Need to determine all four variables
                NURTIENT4R.fertappdate[1][0] = int(scenarioline[1])
                NURTIENT4R.fertamount[1] = float(scenarioline[1])
                # For APEX, the fertilizer ratio was represented
                # by TLD. Here, the ratio will represent the
                # till ID:
                # 260: for subsurface, TLD = 75
                # 265: for surface, TLD = 0
                NURTIENT4R.fertsurfratio[1] = 265 
                # In APEX, element P is 54,
                # Manure is 1
                NURTIENT4R.fertid[1] = 54

            elif scenarioline[4] == "Manure":
                NURTIENT4R.fertappdate[1][0] = int(scenarioline[1])
                NURTIENT4R.fertamount[1] = float(scenarioline[1])
                # In APEX, manure only have one application: 266,
                # I will add a new line (269) to make the subsurface app
                # application.
                NURTIENT4R.fertsurfratio[1] = 266
                NURTIENT4R.fertid[1] = 1  
                
            elif scenarioline[4] == "Half half":
                # Dealing with the ratio needs to modify
                # others: half half under this condition is the
                # amount of fertilizer.
                # This needs two dates, two amount.
#                tempdate1 = [5,1]
#                tempamount1 = 0
#                tempratio1 = 0
#                tempid1 = 0
                NURTIENT4R.fertappdate.append([5,1])
                NURTIENT4R.fertamount.append(0)
                NURTIENT4R.fertsurfratio.append(0)
                NURTIENT4R.fertid.append(0)
                                
                # Scenario 1: time
                # Scenario 2: amount
                # Scenario 3: placement
                # Scenario 4: type
                # 0 for month, 1 for date. All date started with 1
                NURTIENT4R.fertappdate[1][0]=int(scenarioline[1])
                NURTIENT4R.fertappdate[1][1]=1
                NURTIENT4R.fertappdate[2][0]=int(scenarioline[1])
                NURTIENT4R.fertappdate[2][1]=2
                
                NURTIENT4R.fertamount[1] = float(scenarioline[2])/2
                NURTIENT4R.fertamount[2] = float(scenarioline[2])/2
                
                NURTIENT4R.fertsurfratio[1] = 265
                NURTIENT4R.fertsurfratio[2] = 266
                
                # half half also means half element P and manure
                NURTIENT4R.fertid[1] = 54  
                NURTIENT4R.fertid[2] = 1  

        elif scenarioline[3] == "Subsurface":
            # For subsurface, pay attention to ratio
            if scenarioline[4] == "Element P":
                # Need to determine all four variables
                NURTIENT4R.fertappdate[1][0] = int(scenarioline[1])
                NURTIENT4R.fertamount[1] = float(scenarioline[1])
                # SWAT do not like 0, if 0, a 0.2 will be 
                # assumed
                NURTIENT4R.fertsurfratio[1] = 260
                NURTIENT4R.fertid[1] = 54

            elif scenarioline[4] == "Manure":
                NURTIENT4R.fertappdate[1][0] = int(scenarioline[1])
                NURTIENT4R.fertamount[1] = float(scenarioline[1])
                NURTIENT4R.fertsurfratio[1] = 269
                NURTIENT4R.fertid[1] = 1  
                
            elif scenarioline[4] == "Half half":
                # Dealing with the ratio needs to modify
                # others: half half under this condition is the
                # amount of fertilizer.
                # This needs two dates, two amount.
                NURTIENT4R.fertappdate.append([5,1])
                NURTIENT4R.fertamount.append(0)
                NURTIENT4R.fertsurfratio.append(0)
                NURTIENT4R.fertid.append(0)
                                                 
                # Scenario 1: time
                # Scenario 2: amount
                # Scenario 3: placement
                # Scenario 4: type
                # 0 for month, 1 for date. All date started with 1
                NURTIENT4R.fertappdate[1][0]=int(scenarioline[1])
                NURTIENT4R.fertappdate[1][1]=1
                NURTIENT4R.fertappdate[2][0]=int(scenarioline[1])
                NURTIENT4R.fertappdate[2][1]=2
                
                NURTIENT4R.fertamount[1] = float(scenarioline[2])/2
                NURTIENT4R.fertamount[2] = float(scenarioline[2])/2
                
                NURTIENT4R.fertsurfratio[1] = 260
                NURTIENT4R.fertsurfratio[2] = 269
                
                # half half also means half element P and manure
                NURTIENT4R.fertid[1] = 54  
                NURTIENT4R.fertid[2] = 1  
                            

        elif scenarioline[3] == "Half half":
            # For half and half, things are complex.
            # This half half here means half surface and 
            # half subsurface. 
            if scenarioline[4] == "Element P":
                # Dealing with the ratio needs to modify
                # others: half half under this condition is the
                # amount of fertilizer.
                # This needs two dates, two amount.
                NURTIENT4R.fertappdate.append([5,1])
                NURTIENT4R.fertamount.append(0)
                NURTIENT4R.fertsurfratio.append(0)
                NURTIENT4R.fertid.append(0)
                                                 
                # Scenario 1: time
                # Scenario 2: amount
                # Scenario 3: placement
                # Scenario 4: type
                # 0 for month, 1 for date. All date started with 1
                NURTIENT4R.fertappdate[1][0]=int(scenarioline[1])
                NURTIENT4R.fertappdate[1][1]=1
                NURTIENT4R.fertappdate[2][0]=int(scenarioline[1])
                NURTIENT4R.fertappdate[2][1]=2
                
                NURTIENT4R.fertamount[1] = float(scenarioline[2])/2
                NURTIENT4R.fertamount[2] = float(scenarioline[2])/2
                
                NURTIENT4R.fertsurfratio[1] = 265
                NURTIENT4R.fertsurfratio[2] = 260
                
                # half half also means half element P and manure
                NURTIENT4R.fertid[1] = 54  
                NURTIENT4R.fertid[2] = 54 

            elif scenarioline[4] == "Manure":
                # Dealing with the ratio needs to modify
                # others: half half under this condition is the
                # amount of fertilizer.
                # This needs two dates, two amount.
                NURTIENT4R.fertappdate.append([5,1])
                NURTIENT4R.fertamount.append(0)
                NURTIENT4R.fertsurfratio.append(0)
                NURTIENT4R.fertid.append(0)
                                                 
                # Scenario 1: time
                # Scenario 2: amount
                # Scenario 3: placement
                # Scenario 4: type
                # 0 for month, 1 for date. All date started with 1
                NURTIENT4R.fertappdate[1][0]=int(scenarioline[1])
                NURTIENT4R.fertappdate[1][1]=1
                NURTIENT4R.fertappdate[2][0]=int(scenarioline[1])
                NURTIENT4R.fertappdate[2][1]=2
                
                NURTIENT4R.fertamount[1] = float(scenarioline[2])/2
                NURTIENT4R.fertamount[2] = float(scenarioline[2])/2
                
                NURTIENT4R.fertsurfratio[1] = 266
                NURTIENT4R.fertsurfratio[2] = 269
                
                # half half also means half element P and manure
                NURTIENT4R.fertid[1] = 1  
                NURTIENT4R.fertid[2] = 1                 
                
            elif scenarioline[4] == "Half half":
                # Dealing with the ratio needs to modify
                # others: half half under this condition is the
                # amount of fertilizer.
                # This needs two dates, two amount.
                NURTIENT4R.fertappdate.append([5,1])
                NURTIENT4R.fertamount.append(0)
                NURTIENT4R.fertsurfratio.append(0)
                NURTIENT4R.fertid.append(0)

                NURTIENT4R.fertappdate.append([5,2])
                NURTIENT4R.fertamount.append(0)
                NURTIENT4R.fertsurfratio.append(0)
                NURTIENT4R.fertid.append(0)

                NURTIENT4R.fertappdate.append([5,3])
                NURTIENT4R.fertamount.append(0)
                NURTIENT4R.fertsurfratio.append(0)
                NURTIENT4R.fertid.append(0)

                # Scenario 1: time
                # Scenario 2: amount
                # Scenario 3: placement
                # Scenario 4: type
                # 0 for month, 1 for date. All date started with 1
                NURTIENT4R.fertappdate[1][0]=int(scenarioline[1])
                NURTIENT4R.fertappdate[1][1]=1
                NURTIENT4R.fertappdate[2][0]=int(scenarioline[1])
                NURTIENT4R.fertappdate[2][1]=2
                NURTIENT4R.fertappdate[1][0]=int(scenarioline[1])
                NURTIENT4R.fertappdate[1][1]=3
                NURTIENT4R.fertappdate[2][0]=int(scenarioline[1])
                NURTIENT4R.fertappdate[2][1]=4
                
                NURTIENT4R.fertamount[1] = float(scenarioline[2])/2
                NURTIENT4R.fertamount[2] = float(scenarioline[2])/2
                NURTIENT4R.fertamount[3] = float(scenarioline[2])/2
                NURTIENT4R.fertamount[4] = float(scenarioline[2])/2
                
                NURTIENT4R.fertsurfratio[1] = 266
                NURTIENT4R.fertsurfratio[2] = 269
                NURTIENT4R.fertsurfratio[1] = 265
                NURTIENT4R.fertsurfratio[2] = 260
                                
                
                # half half also means half element P and manure
                NURTIENT4R.fertid[1] = 1  
                NURTIENT4R.fertid[2] = 1 
                NURTIENT4R.fertid[3] = 54  
                NURTIENT4R.fertid[4] = 54     
