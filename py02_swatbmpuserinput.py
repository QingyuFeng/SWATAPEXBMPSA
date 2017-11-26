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
class NUTRIENT4R(object):
    
    # BMP types can be implemented in series
    # Multiple BMP are inplemented in ["BMP1", "BMP2"]
    # The characters need to be selected from the above list.

    # The first variable in the list of each BMP 
    # is the switch indicating whether the BMP will
    # be simulated. 
    def __init__(self):
    #    self.fertappdate = [[9, 15]]
        self.fertappdate = [1, [5, 1]]
    
        # Nutrient amount
        # Same as the date, if multiple application is specified.
        # the amount of each can be specified.
        # feramount = ["amount1", "amount2"]
    #    self.fertamount = ["200"]
        self.fertamount = [1, 100]
        
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
                NURTIENT4R.fertsurfratio[1] = 1.0
                NURTIENT4R.fertid[1] = 2

            elif scenarioline[4] == "Manure":
                NURTIENT4R.fertappdate[1][0] = int(scenarioline[1])
                NURTIENT4R.fertamount[1] = float(scenarioline[1])
                NURTIENT4R.fertsurfratio[1] = 1.0
                NURTIENT4R.fertid[1] = 45  
                
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
                
                NURTIENT4R.fertsurfratio[1] = 1.0
                NURTIENT4R.fertsurfratio[2] = 1.0
                
                # half half also means half element P and manure
                NURTIENT4R.fertid[1] = 2  
                NURTIENT4R.fertid[2] = 45  

        elif scenarioline[3] == "Subsurface":
            # For subsurface, pay attention to ratio
            if scenarioline[4] == "Element P":
                # Need to determine all four variables
                NURTIENT4R.fertappdate[1][0] = int(scenarioline[1])
                NURTIENT4R.fertamount[1] = float(scenarioline[1])
                # SWAT do not like 0, if 0, a 0.2 will be 
                # assumed
                NURTIENT4R.fertsurfratio[1] = 0.01
                NURTIENT4R.fertid[1] = 2

            elif scenarioline[4] == "Manure":
                NURTIENT4R.fertappdate[1][0] = int(scenarioline[1])
                NURTIENT4R.fertamount[1] = float(scenarioline[1])
                NURTIENT4R.fertsurfratio[1] = 0.01
                NURTIENT4R.fertid[1] = 45  
                
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
                
                NURTIENT4R.fertsurfratio[1] = 0.01
                NURTIENT4R.fertsurfratio[2] = 0.01
                
                # half half also means half element P and manure
                NURTIENT4R.fertid[1] = 2  
                NURTIENT4R.fertid[2] = 45  
                            

        elif scenarioline[3] == "Half half":
            # For half and half, things are complex.
            # This half half here means half surface and 
            # half subsurface. 
            if scenarioline[4] == "Element P":
                # Need to determine all four variables
                NURTIENT4R.fertappdate[1][0] = int(scenarioline[1])
                NURTIENT4R.fertamount[1] = float(scenarioline[1])
                # SWAT do not like 0, if 0, a 0.2 will be 
                # assumed
                NURTIENT4R.fertsurfratio[1] = 0.5
                NURTIENT4R.fertid[1] = 2

            elif scenarioline[4] == "Manure":
                NURTIENT4R.fertappdate[1][0] = int(scenarioline[1])
                NURTIENT4R.fertamount[1] = float(scenarioline[1])
                NURTIENT4R.fertsurfratio[1] = 0.5
                NURTIENT4R.fertid[1] = 45  
                
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
                
                NURTIENT4R.fertsurfratio[1] = 0.5
                NURTIENT4R.fertsurfratio[2] = 0.5
                
                # half half also means half element P and manure
                NURTIENT4R.fertid[1] = 2  
                NURTIENT4R.fertid[2] = 45  





class COVERCROPS(object):
    
    # Cover crops are planted after harvest of the main crop and
    # then harvest and kill the next year before planting.
    # Common cover crops include:
    # radish(#121),
    # rye (#30)
    # Oats (#32)
    # ryegrass (#44)
    # Alfalfa (#52)
    # Clover (#54)
    cvcropplant = [0, 121]
    

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
    fltstrip = [0, [0.25, 40.0, 0.0]]
    
    

