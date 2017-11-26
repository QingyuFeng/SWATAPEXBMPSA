# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 09:50:42 2017

This contains all functions for the main program.


@author: qyfen
"""

import os, shutil
import fortranformat as ff



class parameters:

    """ Parameters related to the program """
    def __init__(self):
        
        self.infd_swat = "01_swatmodelling"
        self.dft_swattio = "01_default"
        
        self.infd_apex = "02_apexmodelling"
        self.dft_apextio = "01_simulation"
        self.outfd_outputmain = "07_output"
        
        # Need to be modified for each run
        self.outfd_scenario = "01_baseline"
        
        self.outfd_outscenario = "01_default"
        self.infd_json = "05_json"
        
        self.infn_hrunolst = "hrugisnum.list"
        self.fn_sitejson = "tmp4_sitefile.json"
        self.fn_subjson = "tmp3_subfile.json"
        self.fn_opsjson = "tmp2_opsfile.json"
        self.fn_soljson = "tmp1_solfile.json"
        self.fd_apexdb = "04_apexdb"
        self.fd_swat2apexdb = "06_dbswat2apex"
        
        self.fn_swatplant = "plant.dat"
        self.fn_apexcrop = "CROPSWT.DAT"
        self.fn_swatfert = "fert.dat"
        self.fn_swatpest = "pest.dat"
        self.fn_swattill = "till.dat"
        self.fn_apexfert = "FERTSWT.DAT"
        self.fn_apexpest = "PESTSWT.DAT"
        self.fn_apextill = "TILLSWT.DAT"
        self.fn_apexluncn = "apexlunidcnfromswatdb.dat"
        self.apexfertfull = self.get_apexfertfull()
        
        self.croplandlu = ["CCRN", "CSOY", "CWHT",
                          "SYCN", "SYWH", "WHCN"]
        
        self.infn_scenarios = "scenarios.csv"
        self.scenariolns = self.get_scenarioparam()

        
        
        
        
        
    def gethrulist(self):
        
        infn = os.path.join(self.infd_swat,
                            self.infn_hrunolst)
        
        infid = open(infn, "r")
        lif = infid.readlines()
        infid.close()
        
        for lidx in range(len(lif)):
            lif[lidx] = lif[lidx][:-1]
            
            
        return lif
            
        
    def get_swatplantdict(self):
        
        # This functio will create a dictionary
        # of swat crop database. The dictionary
        # key will be the plant id in the model.
        # The purpose is to get the crop name
        # to be selected by APEX
        
        fn = os.path.join(self.infd_apex,
                          self.fd_swat2apexdb,
                          self.fn_swatplant)
        
        fid = open(fn, "r")
        lif = fid.readlines()
        fid.close()
        
        swatplant = {}
        
        # I will write this out for comparison
        
        fn_out = os.path.join(self.infd_apex,
                          self.fd_swat2apexdb,
                          "swatplant.dat")
        
        fid_out = open(fn_out, "w")
        
        for lidx in range(0, len(lif), 5):
            
            fid_out.writelines(lif[lidx])
            lif[lidx] = lif[lidx].split(" ")

            while "" in lif[lidx]:
                lif[lidx].remove("")
            swatplant[lif[lidx][0]] = lif[lidx][1]
        
        fid_out.close()
        
        
        return swatplant
        
        
    def get_apexcropdict(self):
        
        # This functio will create a dictionary
        # of swat crop database. The dictionary
        # key will be the plant id in the model.
        # The purpose is to get the crop name
        # to be selected by APEX
        
        fn = os.path.join(self.infd_apex,
                          self.fd_swat2apexdb,
                          self.fn_apexcrop)
        
        fid = open(fn, "r")
        lif = fid.readlines()
        fid.close()
        
        apexcrop = {}        
        
        del(lif[0:2])
        
        for lidx in range(len(lif)):
            lif[lidx] = lif[lidx].split(" ")
            while "" in lif[lidx]:
                lif[lidx].remove("")
            lif[lidx] = lif[lidx][:2]

            apexcrop[lif[lidx][1]] = lif[lidx][0]
        
        return apexcrop
        
        
        
    def get_apexfertdict(self):
        
        # This functio will create a dictionary
        # of swat crop database. The dictionary
        # key will be the plant id in the model.
        # The purpose is to get the crop name
        # to be selected by APEX
        
        fn = os.path.join(self.infd_apex,
                          self.fd_swat2apexdb,
                          self.fn_apexfert)
        
        fid = open(fn, "r")
        lif = fid.readlines()
        fid.close()
        
        apexfert = {}        
        
        del(lif[0:2])
        
        for lidx in range(len(lif)):
            lif[lidx] = lif[lidx].split(" ")
            while "" in lif[lidx]:
                lif[lidx].remove("")
            lif[lidx] = lif[lidx][:2]

            apexfert[lif[lidx][1]] = lif[lidx][0]
        
        return apexfert
                
        

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
            lif[lidx] = lif[lidx][:2]

            swatfert[lif[lidx][0]] = lif[lidx][1]
        
        return swatfert        
    

    def get_apexpestdict(self):
        
        fn = os.path.join(self.infd_apex,
                          self.fd_swat2apexdb,
                          self.fn_apexpest)
        
        fid = open(fn, "r")
        lif = fid.readlines()
        fid.close()
        
        apexpest = {}        
        
        apexpestffrder = ff.FortranRecordReader("I5,1X,A16,6E16.6")
        
        del(lif[0:2])
        
        for lidx in range(len(lif)):
            lif[lidx] = apexpestffrder.read(lif[lidx])
            lif[lidx] = lif[lidx][:2]
            apexpest[lif[lidx][1].strip()] = lif[lidx][0]
        
        return apexpest
                
        

    def get_swatpestdict(self):
        
        # This functio will create a dictionary
        # of swat crop database. The dictionary
        # key will be the plant id in the model.
        # The purpose is to get the crop name
        # to be selected by APEX
        
        fn = os.path.join(self.infd_apex,
                          self.fd_swat2apexdb,
                          self.fn_swatpest)
        
        fid = open(fn, "r")
        lif = fid.readlines()
        fid.close()
        
        swatpest = {}        
             
        swatpestffrder = ff.FortranRecordReader(
                "i3,a17,f10.1,f5.2,2f8.1,f5.2,f11.3")
        
        for lidx in range(len(lif)):
            lif[lidx] = swatpestffrder.read(lif[lidx])
            lif[lidx] = lif[lidx][:2]

            swatpest[lif[lidx][0]] = lif[lidx][1].lstrip()
        
        return swatpest            
    
    
    
    

    def get_apextilldict(self):
        
        fn = os.path.join(self.infd_apex,
                          self.fd_swat2apexdb,
                          self.fn_apextill)
        
        fid = open(fn, "r")
        lif = fid.readlines()
        fid.close()
        
        apextill = {}        
        
        apextillffrder = ff.FortranRecordReader(
                '(1X,I4,1X,A8,1X,A4,29F8.0,A8)')
        
        del(lif[0:2])
        
        for lidx in range(len(lif)):
            lif[lidx] = apextillffrder.read(lif[lidx])
            lif[lidx] = lif[lidx][:2]
            apextill[lif[lidx][1].lstrip().strip().lower()] = lif[lidx][0]
        
        return apextill
                
        

    def get_swattilldict(self):
        
        # This functio will create a dictionary
        # of swat crop database. The dictionary
        # key will be the plant id in the model.
        # The purpose is to get the crop name
        # to be selected by APEX
        
        fn = os.path.join(self.infd_apex,
                          self.fd_swat2apexdb,
                          self.fn_swattill)
        
        fid = open(fn, "r")
        lif = fid.readlines()
        fid.close()
        
        swattill = {}        
             
        swattillffrder = ff.FortranRecordReader("(I4,1X,A12,1X,A15,1X,A15)")
        
        # Deal with the upper and lower cases in the names
        tempname = 0
        
        for lidx in range(len(lif)):
            lif[lidx] = swattillffrder.read(lif[lidx])
            lif[lidx] = lif[lidx][:2]
            
            lif[lidx][1] = lif[lidx][1].lstrip().strip().lower()

            tempname = lif[lidx][1][0].lower() + lif[lidx][1][1:]

            swattill[lif[lidx][0]] = tempname
        
        return swattill            
    
    
    def getapexluncn(self):
        
        fn = os.path.join(self.infd_apex,
                          self.fd_swat2apexdb,
                          self.fn_apexluncn)
        
        fid = open(fn, "r")
        lif = fid.readlines()
        fid.close()
        
        apexluncn = {}

        del(lif[0])
        
        for lidx in range(len(lif)):
            lif[lidx] = lif[lidx].split(",")
            lif[lidx][-1] = lif[lidx][-1][:-1]
            
            apexluncn[lif[lidx][1]] = lif[lidx]
        
        return apexluncn
    
    
    
    def get_apexfertfull(self):
        
        # This functio will create a dictionary
        # of swat crop database. The dictionary
        # key will be the plant id in the model.
        # The purpose is to get the crop name
        # to be selected by APEX
        
        fn = os.path.join(self.infd_apex,
                          self.fd_swat2apexdb,
                          self.fn_apexfert)
        
        fid = open(fn, "r")
        lif = fid.readlines()
        fid.close()
        
        apexfertfl = {}        
        
        del(lif[0:2])
        
        for lidx in range(len(lif)):
            lif[lidx] = lif[lidx].split(" ")
            while "" in lif[lidx]:
                lif[lidx].remove("")
            lif[lidx] = lif[lidx]

            apexfertfl[lif[lidx][0]] = lif[lidx]
        
        return apexfertfl
                


        
        
    
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

        
    
    
    
    
    
    