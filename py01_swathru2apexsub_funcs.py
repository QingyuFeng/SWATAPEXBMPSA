# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 09:50:42 2017

This contains all functions for the main program.


@author: qyfen
"""

from py01_swathru2apexsub_parms import parameters
import os, sys, subprocess, shutil
import time
import fortranformat as ff


parms = parameters()





#######################################################

class swatfile:
        
    #######################################################
    def checkfileexist(self, filename):
        if not os.path.isfile(filename):
            print("File does not exists: {0}".format(filename))
            sys.exit()

    #######################################################
    def readf_hru(self, hrugisid, inp_onefield):
        fn_hru = os.path.join(parms.infd_swat, 
                               parms.dft_swattio, 
                               '%s.hru' %(hrugisid))
        
        self.checkfileexist(fn_hru)
        
        lif_hru = self.readtext(fn_hru)
        
        del(lif_hru[0])
        for lidx in xrange(len(lif_hru)):
            try:
                lif_hru[lidx] = float(lif_hru[lidx].split("|")[0])
            except:
                pass
            
        inp_onefield["subfrac"] = lif_hru[0]
        inp_onefield["slopelength"] = lif_hru[1]
        inp_onefield["slopesteep"] = lif_hru[2]
        inp_onefield["overlandmanningn"] = lif_hru[3]

        return inp_onefield
    
    #######################################################
    def readf_mgt(self, hrugisid, mgt2ops):
        
        fn_mgt = os.path.join(parms.infd_swat, 
                               parms.dft_swattio, 
                               '%s.mgt' %(hrugisid))
        
        self.checkfileexist(fn_mgt)
        
        lif_mgt = self.readtext(fn_mgt)    

        # Processing the management lines
        mgt2ops["landuse"] = lif_mgt[0].split(" ")[7].split(":")[1]
        mgt2ops["swatcn2"] = float(lif_mgt[10].split("|")[0])
        mgt2ops["ddrain"] = float(lif_mgt[24].split("|")[0])
        mgt2ops["tdrain"] = float(lif_mgt[25].split("|")[0])
        mgt2ops["gdrain"] = float(lif_mgt[26].split("|")[0])
        

        # This fortran formatter helps to read
        # the management lines as formatted by the SWAT fortran code.
        # The structure is fixed.
        # If one line has number of 17 or 0, should be 0, but 17
        # was also used. 
        # This means end of one year. 
        # This will be used to count the total rotation years.
        
        yr_rotation = 0
        
        swatopschdul = ff.FortranRecordReader(
        '(1x,i2,1x,i2,1x,f8.3,1x,i2,1x,i4,1x,i3,1x,i2,1x,f12.5,1x,f6.2,1x,f11.5,1x,f4.2,1x,f6.2,1x,f5.2,i12)')

        mgt2ops["opslines"] = {}
        # SWAT has only one line need crop id, but APEX require
        # all lines. I will get it here.
        mgt2ops["swatcropid"] = "0" 

        for lidx in range(30, len(lif_mgt)):
            lif_mgt[lidx] = swatopschdul.read(lif_mgt[lidx])
            tempopsline = {}
            for lidx2 in range(len(lif_mgt[lidx])):
                tempopsline["mgt%i" %(lidx2+1)] = lif_mgt[lidx][lidx2]

            mgt2ops["opslines"]["op%i" %(lidx)] = tempopsline
            
            if tempopsline["mgt4"] == 1:
                mgt2ops["swatcropid"] = str(tempopsline["mgt5"])
    
            if lif_mgt[lidx][3] == 17:
                yr_rotation = yr_rotation+1
        
        mgt2ops["rotyrs"] = yr_rotation
               
        return mgt2ops


    #######################################################
    def readf_sol(self, hrugisid, sol2sol):
        
        fn_sol = os.path.join(parms.infd_swat, 
                               parms.dft_swattio, 
                               '%s.sol' %(hrugisid)) 
        
        self.checkfileexist(fn_sol)
        
        lif_sol = self.readtext(fn_sol)    
        sol2sol["solstgoname"] = lif_sol[0].split(" ")[9]#.split(":")[1]
        sol2sol["solname"] = lif_sol[1].split(":")[1]
        sol2sol["hsg"] = self.hsgletter2num(lif_sol[2].split(" ")[-1][:-1])
        
        for lidx in xrange(7,len(lif_sol)-1):
            lif_sol[lidx] = lif_sol[lidx].split(":")[1].split(" ")
            while "" in lif_sol[lidx]:
                lif_sol[lidx].remove("")       
            lif_sol[lidx][-1] = lif_sol[lidx][-1][:-1]
            lif_sol[lidx] = map(float, lif_sol[lidx])

        sol2sol["layerdepth"] = lif_sol[7]
        sol2sol["bulkdensity"] = lif_sol[8]
        sol2sol["ksat"] = lif_sol[10]
        sol2sol["orgc"] = lif_sol[11]
        sol2sol["clay"] = lif_sol[12]
        sol2sol["silt"] = lif_sol[13]
        sol2sol["sand"] = lif_sol[14]
        sol2sol["rockfr"] = lif_sol[15]
        
        
        
        sol2sol["solalbedo"] = sum(lif_sol[16])/len(lif_sol[16])
        sol2sol["salinity"] = lif_sol[18]
        sol2sol["ph"] = lif_sol[19]
        sol2sol["caco3"] = lif_sol[20]

        return sol2sol

    #######################################################
    def readf_wgn(self, hrugisid, inp_onefield):
        
        # subid will be the first 5 digit of hru plus four 0s.
        subid = "{0}0000".format(hrugisid[:5])
        
        fn_wgn = os.path.join(parms.infd_swat, 
                           parms.dft_swattio, 
                           '%s.wgn' %(subid)) 
        
        self.checkfileexist(fn_wgn)
        
        lif_wgn = self.readtext(fn_wgn)    

        for lidx in xrange(1,3):
            lif_wgn[lidx] = lif_wgn[lidx].split(" ")
            while "" in lif_wgn[lidx]:
                lif_wgn[lidx].remove("")    
        
        inp_onefield["lat"] = float(lif_wgn[1][2])
        inp_onefield["long"] = float(lif_wgn[1][5][:-1])
        inp_onefield["elev"] = float(lif_wgn[2][3])

        return inp_onefield



    #######################################################
    def readf_sub(self, hrugisid, inp_onefield):
        
        # subid will be the first 5 digit of hru plus four 0s.
        subid = "{0}0000".format(hrugisid[:5])
        
        fn_sub = os.path.join(parms.infd_swat, 
                           parms.dft_swattio, 
                           '%s.sub' %(subid)) 
        
        self.checkfileexist(fn_sub)
        
        lif_sub = self.readtext(fn_sub)    
                
        # area in SWAT is in km2, and in APEX is in ha. 
        inp_onefield["areasub"] = float(lif_sub[1].split("|")[0])*100
        inp_onefield["prcpstnno"] = float(lif_sub[6].split("|")[0])
        inp_onefield["tempstnno"] = float(lif_sub[7].split("|")[0])
        inp_onefield["chmanningn"] = float(lif_sub[28].split("|")[0])
        
        inp_onefield["hruno"] = float(lif_sub[52].split("|")[0])
        # I will get the channel length from the sub
        # and divide the number by the total number of hrus.
        # This was not done since in .SIT, there is a parameter
        # named SWAT basin length.
        
        inp_onefield["chlength"] = float(lif_sub[24].split("|")[0])
        inp_onefield["chslope"] = float(lif_sub[25].split("|")[0])

        return inp_onefield



    #######################################################
    def readtext(self, filename):
        
        fid = open(filename, "r")
        lif = fid.readlines()
        fid.close()
        
        return lif
        



    def hsgletter2num(self, hsgletter):
        
        # convert hsg from ABCD to 1234
        hsgl2n = {"A": 1, "B": 2, "C": 3, "D": 4}
        
        hsgnum = hsgl2n[hsgletter]
        
        return hsgnum












#######################################################

class apexfile:
    
    
    def __init__(self):
        
        self.outfd_apexdft = os.path.join(parms.infd_apex, 
                           parms.dft_apextio) 
        
        self.swatplant = parms.get_swatplantdict()
        self.apexcrop = parms.get_apexcropdict()
        self.apexfert = parms.get_apexfertdict()
        self.swatfert = parms.get_swatfertdict()
        self.apexpest = parms.get_apexpestdict()
        self.swatpest = parms.get_swatpestdict()
        self.apextill = parms.get_apextilldict()
        self.swattill = parms.get_swattilldict()
        self.apexluncn = parms.getapexluncn()        

        
#        for value in self..itervalues():
#            if not value in self.apexcrop.keys():
#                    print(value)
            #print(swatfert)

    
    #######################################################
    def initrunfiles(self):
    
        outfid_run = 0
        outfid_run = open(r"%s/APEXRUN.DAT" %(self.outfd_apexdft), "w")

        return outfid_run


    #######################################################
    def initsitecom(self):

        outfn_sitcom = "SITECOM.DAT"
        outfid_sitcom = open(r"%s/%s" %(self.outfd_apexdft,
                                        outfn_sitcom), "w")
        return outfid_sitcom



    #######################################################
    def initsolcom(self):

        outfn_solcom = "SOILCOM.DAT"
        outfid_solcom = open(r"%s/%s" %(self.outfd_apexdft,
                                        outfn_solcom), "w")
        return outfid_solcom



    #######################################################
    def initopscom(self):

        outfn_opscom = "OPSCCOM.DAT"
        outfid_opscom = open(r"%s/%s" %(self.outfd_apexdft,
                                        outfn_opscom), "w")
        return outfid_opscom


    #######################################################
    def initdlycom(self):

        outfn_dlycom = "WDLSTCOM.DAT"
        outfid_dlycom = open(r"%s/%s" %(self.outfd_apexdft,
                                        outfn_dlycom), "w")
        return outfid_dlycom



    #######################################################
    def initsubcom(self):

        outfn_subcom = "SUBACOM.DAT"
        outfid_subcom = open(r"%s/%s" %(self.outfd_apexdft,
                                        outfn_subcom), "w")
        return outfid_subcom




    #######################################################
    def write_runlines(self, runfid, hruidx, hrunolist):
    
        # APEXRUN is read with free format in APEX.exe
        runfid.writelines(u"%-10s%7i%7i%7i%7i%7i%7i\n" %(\
                            "R%s" %(hrunolist[hruidx]) ,\
                            hruidx+1,\
                            0,\
                            0,\
                            hruidx+1,\
                            0, 0\
                            ))
    


    #######################################################
    def writesitcomline(self, fidsitcom, hruidx, hrunolist):

        fidsitcom.writelines("%5i\tSIT%s.SIT\n" %(hruidx+1,
                                              hrunolist[hruidx]))



    def updatejson_sit(self, json_sit, hruidx, hrunolist, inp_onefield):
        
    
        json_sit["model_setup"]["siteid"]= "1"
        json_sit["model_setup"]["description_line1"]= "R%s" %(hrunolist[hruidx])
        json_sit["model_setup"]["generation_date"]= time.strftime("%d/%m/%Y") 
        json_sit["model_setup"]["nvcn"]= "4"
        json_sit["model_setup"]["outflow_release_method_isao"]= "0"

        json_sit["geographic"]["latitude_ylat"]= inp_onefield["lat"]
        json_sit["geographic"]["longitude_xlog"]= inp_onefield["long"]
        json_sit["geographic"]["elevation_elev"]= inp_onefield["elev"]

        json_sit["runoff"]["peakrunoffrate_apm"]= "1.00"
        json_sit["co2"]["co2conc_atmos_co2x"]= "330.00"
        json_sit["nitrogen"]["no3n_irrigation_cqnx"]= "0.00"
        json_sit["nitrogen"]["nitrogen_conc_rainfall_rfnx"]= "0.00"
        json_sit["manure"]["manure_p_app_upr"]= "0.00"
        json_sit["manure"]["manure_n_app_unr"]= "0.00"
        json_sit["irrigation"]["auto_irrig_adj_fir0"]= "0.00"
        json_sit["channel"]["basin_channel_length_bchl"]= inp_onefield["chlength"]
        json_sit["channel"]["basin_chalnel_slp_bchs"]= inp_onefield["chslope"]

        return json_sit

    
    def writefile_sit(self, inf_usrjson, hruidx, hrunolist):
        
        outfn_sit = "SIT%s.SIT" %(hrunolist[hruidx])
        # Write the Site file
        outfid_sit = open(r"%s/%s" %(self.outfd_apexdft,
                                     outfn_sit), "w")
        # APEXRUN is read with free format in APEX.exe
        # Write line 1:
        outfid_sit.writelines("%s\n".rjust(74, " ") %(outfn_sit[:-4]))
        # Write line 2:
        outfid_sit.writelines("%s\n".rjust(70, " ") %(outfn_sit))
        # Write line 3:
        outfid_sit.writelines("Outlet 1\n".rjust(74, " "))
        # Write line 4
        outfid_sit.writelines(u"%8.3f%8.3f%8.2f%8s%8s%8s%8s%8s%8s%8s\n" %(\
                            float(inf_usrjson["geographic"]["latitude_ylat"]),\
                            float(inf_usrjson["geographic"]["longitude_xlog"]),\
                            float(inf_usrjson["geographic"]["elevation_elev"]),\
                            inf_usrjson["runoff"]["peakrunoffrate_apm"],\
                            inf_usrjson["co2"]["co2conc_atmos_co2x"],\
                            inf_usrjson["nitrogen"]["no3n_irrigation_cqnx"],\
                            inf_usrjson["nitrogen"]["nitrogen_conc_rainfall_rfnx"],\
                            inf_usrjson["manure"]["manure_p_app_upr"],\
                            inf_usrjson["manure"]["manure_n_app_unr"],\
                            inf_usrjson["irrigation"]["auto_irrig_adj_fir0"]\
                            ))
        # Write Line 5
        outfid_sit.writelines(u"%8s%8s%8s%8s%8s%8s%8s%8s%8s%8s\n" %(\
                            0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00,\
                            inf_usrjson["channel"]["basin_channel_length_bchl"],\
                            inf_usrjson["channel"]["basin_chalnel_slp_bchs"]\
                            ))
        # Write Line 6
        outfid_sit.writelines("\n")
        # Write Line 7
        outfid_sit.writelines("%8i%8i%8i%8i%8i%8i%8i%8i%8i%8i\n" %(\
                            0, 0, 0, 0, 0, 0, 0, 0, 0, 0\
                            ))
        # Write Line 8
        outfid_sit.writelines("%8.2f%8.2f%8.2f%8.2f%8.2f%8.2f%8.2f%8.2f%8.2f%8.2f\n" %(\
                            0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00,0.00, 0.00\
                            ))
        # Write Line 9
        outfid_sit.writelines("\n")     
        # Write Line 10
        outfid_sit.writelines("\n")  
        # Write Line 11
        outfid_sit.writelines("\n")       
         
        outfid_sit.close()
    
        
        



    #######################################################
    def writesolcomline(self, fidsolcom, hruidx, hrunolist):

        fidsolcom.writelines("%5i\tSOL%s.SOL\n" %(hruidx+1,
                                              hrunolist[hruidx]))



    def updatejson_sol(self,
                       json_sol,
                       hruidx,
                       hrunolist,
                       sol2sol):
        
        json_sol["line1"]["soilname"]= sol2sol["solname"]

        json_sol["line2"]["abledo_salb"]= sol2sol["solalbedo"]
        json_sol["line2"]["hydrologicgroup_hsg"]= sol2sol["hsg"]
        json_sol["line2"]["initialwatercontent_ffc"]= "0.00"
        json_sol["line2"]["minwatertabledep_wtmn"]= "0.00"
        json_sol["line2"]["maxwatertabledep_wtmx"]= "0.00"
        json_sol["line2"]["initialwatertable_wtbl"]= "0.00"
        json_sol["line2"]["groundwaterstorage_gwst"]= "0.00"
        json_sol["line2"]["max_groundwater_gwmx"]= "0.00"
        json_sol["line2"]["gw_residenttime_rftt"]= "0.00"
        json_sol["line2"]["return_overtotalflow_rfpk"] = "0.00"

        json_sol["line3"]["min_layerdepth_tsla"]= "10.00"
        json_sol["line3"]["weatheringcode_xids"]= "0.00"
        json_sol["line3"]["cultivationyears_rtn1"]= "50.00"
        json_sol["line3"]["grouping_xidk"]= "2.00"
        json_sol["line3"]["min_maxlayerthick_zqt"]= "0.01"
        json_sol["line3"]["minprofilethick_zf"]= "0.05"
        json_sol["line3"]["minlayerthick_ztk"]= "0.05"
        json_sol["line3"]["org_c_biomass_fbm"]= "0.03"
        json_sol["line3"]["org_c_passive_fhp"]= "0.30"

        # Starting from this line, the written will be based on the total 
        # this soil have:

        for layidx in xrange(len(sol2sol["layerdepth"])):
                        
            json_sol["line4_layerdepth"]["z%i" %(layidx+1)] = sol2sol["layerdepth"][layidx]
            json_sol["line5_moistbulkdensity"]["z%i" %(layidx+1)] = sol2sol["bulkdensity"][layidx]
            json_sol["line8_sand"]["z%i" %(layidx+1)] = sol2sol["sand"][layidx]
            json_sol["line9_silt"]["z%i" %(layidx+1)] = sol2sol["silt"][layidx]
            json_sol["line11_ph"]["z%i" %(layidx+1)] = sol2sol["ph"][layidx]
            json_sol["line13_orgc_conc_woc"]["z%i" %(layidx+1)] = sol2sol["orgc"][layidx]
            json_sol["line14_caco3_cac"]["z%i" %(layidx+1)] = sol2sol["caco3"][layidx]
            json_sol["line16_rock_rok"]["z%i" %(layidx+1)] = sol2sol["rockfr"][layidx]
            json_sol["line22_ksat"]["z%i" %(layidx+1)] = sol2sol["ksat"][layidx]
            json_sol["line26_electricalcond_ec"]["z%i" %(layidx+1)] = sol2sol["salinity"][layidx]
            json_sol["layerid"]["z%i" %(layidx+1)]= layidx+1
        
        
        
        return json_sol




    def writefile_sol(self, inf_usrjson, hruidx, hrunolist, sol2sol):
        
        outfn_sol = "SOL%s.SOL" %(hrunolist[hruidx])
        # Write the Site file
        wfid_sol = open(r"%s/%s" %(self.outfd_apexdft, 
                                     outfn_sol), "w")

        # Write line 1: desctiption
        sol_l1 = 0
        sol_l1 = "%20s" %(inf_usrjson["line1"]["soilname"])
        wfid_sol.writelines(sol_l1)
    
        # Writing line 2
        sol_l2 = 0
        #    ! SOIL PROPERTIES
    

        sol_l2 = "%8.2f%8.2f%8.2f%8.2f%8.2f%8.2f%8.2f%8.2f%8.2f%8.2f\n"\
                        %(float(inf_usrjson["line2"]["abledo_salb"]),\
                          float(inf_usrjson["line2"]["hydrologicgroup_hsg"]), 0.00,\
                          float(inf_usrjson["line2"]["minwatertabledep_wtmn"]),\
                          0.00, 0.00, 0.00, 0.00, 0.00, 0.00)
        wfid_sol.writelines(sol_l2)
    
        # Line 3:  Same format as line 2, different parameters. 
        # Some values were set to prevent any potential model run failure.
        # the 5th variable ZQT, should be from 0.01 to 0.25.
        # the 6th and 7th variable ZF should be from 0.05 to 0.25
        # the 8 and 9 should be larger than 0.03 and 0.3
        # The 10th should be left blank
        sol_l3 = 0
        sol_l3 = "%8.2f%8.2f%8.2f%8.2f%8.2f%8.2f%8.2f%8.2f%8.2f        \n"\
                    %(float(inf_usrjson["line3"]["min_layerdepth_tsla"]), 
                        float(inf_usrjson["line3"]["weatheringcode_xids"]),
                        float(inf_usrjson["line3"]["cultivationyears_rtn1"]),
                        float(inf_usrjson["line3"]["grouping_xidk"]),
                        float(inf_usrjson["line3"]["min_maxlayerthick_zqt"]),
                        float(inf_usrjson["line3"]["minprofilethick_zf"]),
                        float(inf_usrjson["line3"]["minlayerthick_ztk"]),
                        float(inf_usrjson["line3"]["org_c_biomass_fbm"]),
                        float(inf_usrjson["line3"]["org_c_passive_fhp"])
                        )
        wfid_sol.writelines(sol_l3)
    
        # Starting from line 4, the variables will be writen for 
        # properties for eacy layer, and each column represent one layer.
        # It is better to use a loop to do the writing.
    
        sol_layer_pro = [""]*52
        layeridxlst = []
        for lyidx in xrange(len(sol2sol["layerdepth"])):
#            print(inf_usrjson["layerid"]["z%i" %(lyidx+1)])
            layeridxlst.append(int(inf_usrjson["layerid"]["z%i" %(lyidx+1)]))
#        

        
        for layeridx in range(0, max(layeridxlst)):
            if layeridx < max(layeridxlst)-1:
        #  !  4  Z    = DEPTH TO BOTTOM OF LAYERS(m)            
                sol_layer_pro[3] = sol_layer_pro[3] + "%8.2f" \
                    %(float(inf_usrjson["line4_layerdepth"]["z%i" %(layeridx+1)])/100)
    #  !  5  BD   = BULK DENSITY(t/m3)                
                sol_layer_pro[4] = sol_layer_pro[4] + "%8.2f" \
                    %(float(inf_usrjson["line5_moistbulkdensity"]["z%i" %(layeridx+1)]))
    #  !  6  UW   = SOIL WATER CONTENT AT WILTING POINT(1500 KPA)(m/m)                                             
    #  !            (BLANK IF UNKNOWN)                
                sol_layer_pro[5] = sol_layer_pro[5] + "%8.2f" \
                    %(float(inf_usrjson["line6_wiltingpoint"]["z%i" %(layeridx+1)])/100)
    #  !  7  FC   = WATER CONTENT AT FIELD CAPACITY(33KPA)(m/m)                                                    
    #  !            (BLANK IF UNKNOWN)                
                sol_layer_pro[6] = sol_layer_pro[6] + "%8.2f" \
                    %(float(inf_usrjson["line7_fieldcapacity"]["z%i" %(layeridx+1)])/100)
    #  !  8  SAN  = % SAND                 
                sol_layer_pro[7] = sol_layer_pro[7] + "%8.2f" \
                    %(float(inf_usrjson["line8_sand"]["z%i" %(layeridx+1)]))
    #  !  9  SIL  = % SILT                
                sol_layer_pro[8] = sol_layer_pro[8] + "%8.2f" \
                    %(float(inf_usrjson["line9_silt"]["z%i" %(layeridx+1)]))
    #  ! 10  WN   = INITIAL ORGANIC N CONC(g/t)       (BLANK IF UNKNOWN)                
                sol_layer_pro[9] = sol_layer_pro[9] + "%8.2f" \
                    %(0.00)
    #  ! 11  PH   = SOIL PH                
                sol_layer_pro[10] = sol_layer_pro[10] + "%8.2f" \
                    %(float(inf_usrjson["line11_ph"]["z%i" %(layeridx+1)]))
    #  ! 12  SMB  = SUM OF BASES(cmol/kg)              (BLANK IF UNKNOWN)
                sol_layer_pro[11] = sol_layer_pro[11] + "%8.2f" \
                    %(float(inf_usrjson["line12_sumofbase_smb"]["z%i" %(layeridx+1)]))
    #  ! 13  WOC  = ORGANIC CARBON CONC(%)                
                sol_layer_pro[12] = sol_layer_pro[12] + "%8.2f" \
                    %(float(inf_usrjson["line13_orgc_conc_woc"]["z%i" %(layeridx+1)]))
    #  ! 14  CAC  = CALCIUM CARBONATE(%)                 
                sol_layer_pro[13] = sol_layer_pro[13] + "%8.2f" \
                    %(float(inf_usrjson["line14_caco3_cac"]["z%i" %(layeridx+1)]))
    #  ! 15  CEC  = CATION EXCHANGE CAPACITY(cmol/kg)(BLANK IF UNKNOWN                
                sol_layer_pro[14] = sol_layer_pro[14] + "%8.2f" \
                    %(float(inf_usrjson["line15_cec"]["z%i" %(layeridx+1)]))
    #  ! 16  ROK  = COARSE FRAGMENTS(% VOL)              (BLANK IF UNKNOWN)           
                sol_layer_pro[15] = sol_layer_pro[15] + "%8.2f" \
                    %(100-float(inf_usrjson["line16_rock_rok"]["z%i" %(layeridx+1)]))
    #  ! 17  CNDS = INITIAL SOL N CONC(g/t)            (BLANK IF UNKNOWN) 
                sol_layer_pro[16] = sol_layer_pro[16] + "%8.2f" \
                    %(float(inf_usrjson["line17_inisolnconc_cnds"]["z%i" %(layeridx+1)]))
    #  ! 18  SSF  = INITIAL SOL P CONC(g/t)       (BLANK IF UNKNOWN)
                sol_layer_pro[17] = sol_layer_pro[17] + "%8.2f" \
                    %(float(inf_usrjson["line18_soilp_ssf"]["z%i" %(layeridx+1)]))
    #  ! 19  RSD  = CROP RESIDUE(t/ha)                (BLANK IF UNKNOWN)   
                sol_layer_pro[18] = sol_layer_pro[18] + "%8.2f" \
                    %(0.00)
    #  ! 20  BDD  = BULK DENSITY(OVEN DRY)(t/m3)   (BLANK IF UNKNOWN)                
                sol_layer_pro[19] = sol_layer_pro[19] + "%8.2f" \
                    %(float(inf_usrjson["line20_drybd_bdd"]["z%i" %(layeridx+1)]))
    #  ! 21  PSP  = P SORPTION RATIO                   (BLANK IF UNKNOWN)                  
                sol_layer_pro[20] = sol_layer_pro[20] + "%8.2f" \
                    %(0.00) 
    #  ! 22  SATC = SATURATED CONDUCTIVITY(mm/h)     (BLANK IF UNKNOWN)
                sol_layer_pro[21] = sol_layer_pro[21] + "%8.2f" \
                    %(float(inf_usrjson["line22_ksat"]["z%i" %(layeridx+1)]))
    #  ! 23  HCL  = LATERAL HYDRAULIC CONDUCTIVITY(mm/h)                
                sol_layer_pro[22] = sol_layer_pro[22] + "%8.2f" \
                    %(0.00)
    #  ! 24  WPO  = INITIAL ORGANIC P CONC(g/t)      (BLANK IF UNKNOWN)                
                sol_layer_pro[23] = sol_layer_pro[23] + "%8.2f" \
                    %(float(inf_usrjson["line24_orgp_wpo"]["z%i" %(layeridx+1)]))
    #  ! 25  DHN  = EXCHANGEABLE K CONC (g/t)                
                sol_layer_pro[24] = sol_layer_pro[24] + "%8.2f" \
                    %(0.00)
    #  ! 26  ECND = ELECTRICAL COND (mmho/cm)                
                sol_layer_pro[25] = sol_layer_pro[25] + "%8.2f" \
                    %(float(inf_usrjson["line26_electricalcond_ec"]["z%i" %(layeridx+1)]))
    #  ! 27  STFR = FRACTION OF STORAGE INTERACTING WITH NO3 LEACHING                                              
    #  !                                               (BLANK IF UNKNOWN)                
                sol_layer_pro[26] = sol_layer_pro[26] + "%8.2f" \
                    %(0.00)
    #  ! 28  SWST = INITIAL SOIL WATER STORAGE (m/m)                
                sol_layer_pro[27] = sol_layer_pro[27] + "%8.2f" \
                    %(0.00)
    #  ! 29  CPRV = FRACTION INFLOW PARTITIONED TO VERTICLE CRACK OR PIPE FLOW                
                sol_layer_pro[28] = sol_layer_pro[28] + "%8.2f" \
                    %(0.00)
    #  ! 30  CPRH = FRACTION INFLOW PARTITIONED TO HORIZONTAL CRACK OR PIPE                                        
    #  !            FLOW                 
                sol_layer_pro[29] = sol_layer_pro[29] + "%8.2f" \
                    %(0.00)
    #  ! 31  WLS  = STRUCTURAL LITTER(kg/ha)           (BLANK IF UNKNOWN)                
                sol_layer_pro[30] = sol_layer_pro[30] + "%8.2f" \
                    %(0.00)
    #  ! 32  WLM  = METABOLIC LITTER(kg/ha)            (BLANK IF UNKNOWN)            
                sol_layer_pro[31] = sol_layer_pro[31] + "%8.2f" \
                    %(0.00)
    #  ! 33  WLSL = LIGNIN CONTENT OF STRUCTURAL LITTER(kg/ha)(B I U)                
                sol_layer_pro[32] = sol_layer_pro[32] + "%8.2f" \
                    %(0.00)
    #  ! 34  WLSC = CARBON CONTENT OF STRUCTURAL LITTER(kg/ha)(B I U) 
                sol_layer_pro[33] = sol_layer_pro[33] + "%8.2f" \
                    %(0.00)
    #  ! 35  WLMC = C CONTENT OF METABOLIC LITTER(kg/ha)(B I U)
                sol_layer_pro[34] = sol_layer_pro[34] + "%8.2f" \
                    %(0.00)
    #  ! 36  WLSLC= C CONTENT OF LIGNIN OF STRUCTURAL LITTER(kg/ha)(B I U)
                sol_layer_pro[35] = sol_layer_pro[35] + "%8.2f" \
                    %(0.00)
    #  ! 37  WLSLNC=N CONTENT OF LIGNIN OF STRUCTURAL LITTER(kg/ha)(BIU)
                sol_layer_pro[36] = sol_layer_pro[36] + "%8.2f" \
                    %(0.00)
    #  ! 38  WBMC = C CONTENT OF BIOMASS(kg/ha)(BIU)
                sol_layer_pro[37] = sol_layer_pro[37] + "%8.2f" \
                    %(0.00)
    #  ! 39  WHSC = C CONTENT OF SLOW HUMUS(kg/ha)(BIU)
                sol_layer_pro[38] = sol_layer_pro[38] + "%8.2f" \
                    %(0.00)
    #  ! 40  WHPC = C CONTENT OF PASSIVE HUMUS(kg/ha)(BIU)
                sol_layer_pro[39] = sol_layer_pro[39] + "%8.2f" \
                    %(0.00)
    #  ! 41  WLSN = N CONTENT OF STRUCTURAL LITTER(kg/ha)(BIU)
                sol_layer_pro[40] = sol_layer_pro[40] + "%8.2f" \
                    %(0.00)
    #  ! 42  WLMN = N CONTENT OF METABOLIC LITTER(kg/ha)(BIU)
                sol_layer_pro[41] = sol_layer_pro[41] + "%8.2f" \
                    %(0.00)
    #  ! 43  WBMN = N CONTENT OF BIOMASS(kg/ha)(BIU)
                sol_layer_pro[42] = sol_layer_pro[42] + "%8.2f" \
                    %(0.00)
    #  ! 44  WHSN = N CONTENT OF SLOW HUMUS(kg/ha)(BIU)
                sol_layer_pro[43] = sol_layer_pro[43] + "%8.2f" \
                    %(0.00)
    #  ! 45  WHPN = N CONTENT OF PASSIVE HUMUS(kg/ha)(BIU)
                sol_layer_pro[44] = sol_layer_pro[44] + "%8.2f" \
                    %(0.00)
    #  ! 46  FE26 = IRON CONTENT(%)
                sol_layer_pro[45] = sol_layer_pro[45] + "%8.2f" \
                    %(0.00)
    #  ! 47  SULF = SULFUR CONTENT(%)                 
                sol_layer_pro[46] = sol_layer_pro[46] + "%8.2f" \
                    %(0.00)
    #  ! 48  ASHZ = SOIL HORIZON(A,B,C)                                                                            
                sol_layer_pro[47] = sol_layer_pro[47] + "%8s" \
                    %(" ")
    #   ! 49  CGO2 = O2 CONC IN GAS PHASE (g/m3 OF SOIL AIR)
                sol_layer_pro[48] = sol_layer_pro[48] + "%8.2f" \
                    %(0.00)
    #   ! 50  CGCO2= CO2 CONC IN GAS PHASE (g/m3 OF SOIL AIR)                                                       
                sol_layer_pro[49] = sol_layer_pro[49] + "%8.2f" \
                    %(0.00)
    #   ! 51  CGN2O= N2O CONC IN GAS PHASE (g/m3 OF SOIL AIR)                 
                sol_layer_pro[50] = sol_layer_pro[50] + "%8.2f" \
                    %(0.00)
            else:
        #  !  4  Z    = DEPTH TO BOTTOM OF LAYERS(m)            
                sol_layer_pro[3] = sol_layer_pro[3] + "%8.2f\n" \
                    %(float(inf_usrjson["line4_layerdepth"]["z%i" %(layeridx+1)])/100)
    #  !  5  BD   = BULK DENSITY(t/m3)                
                sol_layer_pro[4] = sol_layer_pro[4] + "%8.2f\n" \
                    %(float(inf_usrjson["line5_moistbulkdensity"]["z%i" %(layeridx+1)]))
    #  !  6  UW   = SOIL WATER CONTENT AT WILTING POINT(1500 KPA)(m/m)                                             
    #  !            (BLANK IF UNKNOWN)                
                sol_layer_pro[5] = sol_layer_pro[5] + "%8.2f\n" \
                    %(float(inf_usrjson["line6_wiltingpoint"]["z%i" %(layeridx+1)])/100)
    #  !  7  FC   = WATER CONTENT AT FIELD CAPACITY(33KPA)(m/m)                                                    
    #  !            (BLANK IF UNKNOWN)                
                sol_layer_pro[6] = sol_layer_pro[6] + "%8.2f\n" \
                    %(float(inf_usrjson["line7_fieldcapacity"]["z%i" %(layeridx+1)])/100)
    #  !  8  SAN  = % SAND                 
                sol_layer_pro[7] = sol_layer_pro[7] + "%8.2f\n" \
                    %(float(inf_usrjson["line8_sand"]["z%i" %(layeridx+1)]))
    #  !  9  SIL  = % SILT                
                sol_layer_pro[8] = sol_layer_pro[8] + "%8.2f\n" \
                    %(float(inf_usrjson["line9_silt"]["z%i" %(layeridx+1)]))
    #  ! 10  WN   = INITIAL ORGANIC N CONC(g/t)       (BLANK IF UNKNOWN)                
                sol_layer_pro[9] = sol_layer_pro[9] + "%8.2f\n" \
                    %(0.00)
    #  ! 11  PH   = SOIL PH                
                sol_layer_pro[10] = sol_layer_pro[10] + "%8.2f\n" \
                    %(float(inf_usrjson["line11_ph"]["z%i" %(layeridx+1)]))
    #  ! 12  SMB  = SUM OF BASES(cmol/kg)              (BLANK IF UNKNOWN)
                sol_layer_pro[11] = sol_layer_pro[11] + "%8.2f\n" \
                    %(float(inf_usrjson["line12_sumofbase_smb"]["z%i" %(layeridx+1)]))
    #  ! 13  WOC  = ORGANIC CARBON CONC(%)                
                sol_layer_pro[12] = sol_layer_pro[12] + "%8.2f\n" \
                    %(float(inf_usrjson["line13_orgc_conc_woc"]["z%i" %(layeridx+1)]))
    #  ! 14  CAC  = CALCIUM CARBONATE(%)                 
                sol_layer_pro[13] = sol_layer_pro[13] + "%8.2f\n" \
                    %(float(inf_usrjson["line14_caco3_cac"]["z%i" %(layeridx+1)]))
    #  ! 15  CEC  = CATION EXCHANGE CAPACITY(cmol/kg)(BLANK IF UNKNOWN                
                sol_layer_pro[14] = sol_layer_pro[14] + "%8.2f\n" \
                    %(float(inf_usrjson["line15_cec"]["z%i" %(layeridx+1)]))
    #  ! 16  ROK  = COARSE FRAGMENTS(% VOL)              (BLANK IF UNKNOWN)           
                sol_layer_pro[15] = sol_layer_pro[15] + "%8.2f\n" \
                    %(100-float(inf_usrjson["line16_rock_rok"]["z%i" %(layeridx+1)]))
    #  ! 17  CNDS = INITIAL SOL N CONC(g/t)            (BLANK IF UNKNOWN) 
                sol_layer_pro[16] = sol_layer_pro[16] + "%8.2f\n" \
                    %(float(inf_usrjson["line17_inisolnconc_cnds"]["z%i" %(layeridx+1)]))
    #  ! 18  SSF  = INITIAL SOL P CONC(g/t)       (BLANK IF UNKNOWN)
                sol_layer_pro[17] = sol_layer_pro[17] + "%8.2f\n" \
                    %(float(inf_usrjson["line18_soilp_ssf"]["z%i" %(layeridx+1)]))
    #  ! 19  RSD  = CROP RESIDUE(t/ha)                (BLANK IF UNKNOWN)   
                sol_layer_pro[18] = sol_layer_pro[18] + "%8.2f\n" \
                    %(0.00)
    #  ! 20  BDD  = BULK DENSITY(OVEN DRY)(t/m3)   (BLANK IF UNKNOWN)                
                sol_layer_pro[19] = sol_layer_pro[19] + "%8.2f\n" \
                    %(float(inf_usrjson["line20_drybd_bdd"]["z%i" %(layeridx+1)]))
    #  ! 21  PSP  = P SORPTION RATIO                   (BLANK IF UNKNOWN)                  
                sol_layer_pro[20] = sol_layer_pro[20] + "%8.2f\n" \
                    %(0.00) 
    #  ! 22  SATC = SATURATED CONDUCTIVITY(mm/h)     (BLANK IF UNKNOWN)
                sol_layer_pro[21] = sol_layer_pro[21] + "%8.2f\n" \
                    %(float(inf_usrjson["line22_ksat"]["z%i" %(layeridx+1)]))
    #  ! 23  HCL  = LATERAL HYDRAULIC CONDUCTIVITY(mm/h)                
                sol_layer_pro[22] = sol_layer_pro[22] + "%8.2f\n" \
                    %(0.00)
    #  ! 24  WPO  = INITIAL ORGANIC P CONC(g/t)      (BLANK IF UNKNOWN)                
                sol_layer_pro[23] = sol_layer_pro[23] + "%8.2f\n" \
                    %(float(inf_usrjson["line24_orgp_wpo"]["z%i" %(layeridx+1)]))
    #  ! 25  DHN  = EXCHANGEABLE K CONC (g/t)                
                sol_layer_pro[24] = sol_layer_pro[24] + "%8.2f\n" \
                    %(0.00)
    #  ! 26  ECND = ELECTRICAL COND (mmho/cm)                
                sol_layer_pro[25] = sol_layer_pro[25] + "%8.2f\n" \
                    %(float(inf_usrjson["line26_electricalcond_ec"]["z%i" %(layeridx+1)]))
    #  ! 27  STFR = FRACTION OF STORAGE INTERACTING WITH NO3 LEACHING                                              
    #  !                                               (BLANK IF UNKNOWN)                
                sol_layer_pro[26] = sol_layer_pro[26] + "%8.2f\n" \
                    %(0.00)
    #  ! 28  SWST = INITIAL SOIL WATER STORAGE (m/m)                
                sol_layer_pro[27] = sol_layer_pro[27] + "%8.2f\n" \
                    %(0.00)
    #  ! 29  CPRV = FRACTION INFLOW PARTITIONED TO VERTICLE CRACK OR PIPE FLOW                
                sol_layer_pro[28] = sol_layer_pro[28] + "%8.2f\n" \
                    %(0.00)
    #  ! 30  CPRH = FRACTION INFLOW PARTITIONED TO HORIZONTAL CRACK OR PIPE                                        
    #  !            FLOW                 
                sol_layer_pro[29] = sol_layer_pro[29] + "%8.2f\n" \
                    %(0.00)
    #  ! 31  WLS  = STRUCTURAL LITTER(kg/ha)           (BLANK IF UNKNOWN)                
                sol_layer_pro[30] = sol_layer_pro[30] + "%8.2f\n" \
                    %(0.00)
    #  ! 32  WLM  = METABOLIC LITTER(kg/ha)            (BLANK IF UNKNOWN)            
                sol_layer_pro[31] = sol_layer_pro[31] + "%8.2f\n" \
                    %(0.00)
    #  ! 33  WLSL = LIGNIN CONTENT OF STRUCTURAL LITTER(kg/ha)(B I U)                
                sol_layer_pro[32] = sol_layer_pro[32] + "%8.2f\n" \
                    %(0.00)
    #  ! 34  WLSC = CARBON CONTENT OF STRUCTURAL LITTER(kg/ha)(B I U) 
                sol_layer_pro[33] = sol_layer_pro[33] + "%8.2f\n" \
                    %(0.00)
    #  ! 35  WLMC = C CONTENT OF METABOLIC LITTER(kg/ha)(B I U)
                sol_layer_pro[34] = sol_layer_pro[34] + "%8.2f\n" \
                    %(0.00)
    #  ! 36  WLSLC= C CONTENT OF LIGNIN OF STRUCTURAL LITTER(kg/ha)(B I U)
                sol_layer_pro[35] = sol_layer_pro[35] + "%8.2f\n" \
                    %(0.00)
    #  ! 37  WLSLNC=N CONTENT OF LIGNIN OF STRUCTURAL LITTER(kg/ha)(BIU)
                sol_layer_pro[36] = sol_layer_pro[36] + "%8.2f\n" \
                    %(0.00)
    #  ! 38  WBMC = C CONTENT OF BIOMASS(kg/ha)(BIU)
                sol_layer_pro[37] = sol_layer_pro[37] + "%8.2f\n" \
                    %(0.00)
    #  ! 39  WHSC = C CONTENT OF SLOW HUMUS(kg/ha)(BIU)
                sol_layer_pro[38] = sol_layer_pro[38] + "%8.2f\n" \
                    %(0.00)
    #  ! 40  WHPC = C CONTENT OF PASSIVE HUMUS(kg/ha)(BIU)
                sol_layer_pro[39] = sol_layer_pro[39] + "%8.2f\n" \
                    %(0.00)
    #  ! 41  WLSN = N CONTENT OF STRUCTURAL LITTER(kg/ha)(BIU)
                sol_layer_pro[40] = sol_layer_pro[40] + "%8.2f\n" \
                    %(0.00)
    #  ! 42  WLMN = N CONTENT OF METABOLIC LITTER(kg/ha)(BIU)
                sol_layer_pro[41] = sol_layer_pro[41] + "%8.2f\n" \
                    %(0.00)
    #  ! 43  WBMN = N CONTENT OF BIOMASS(kg/ha)(BIU)
                sol_layer_pro[42] = sol_layer_pro[42] + "%8.2f\n" \
                    %(0.00)
    #  ! 44  WHSN = N CONTENT OF SLOW HUMUS(kg/ha)(BIU)
                sol_layer_pro[43] = sol_layer_pro[43] + "%8.2f\n" \
                    %(0.00)
    #  ! 45  WHPN = N CONTENT OF PASSIVE HUMUS(kg/ha)(BIU)
                sol_layer_pro[44] = sol_layer_pro[44] + "%8.2f\n" \
                    %(0.00)
    #  ! 46  FE26 = IRON CONTENT(%)
                sol_layer_pro[45] = sol_layer_pro[45] + "%8.2f\n" \
                    %(0.00)
    #  ! 47  SULF = SULFUR CONTENT(%)                 
                sol_layer_pro[46] = sol_layer_pro[46] + "%8.2f\n" \
                    %(0.00)
    #  ! 48  ASHZ = SOIL HORIZON(A,B,C)                                                                            
                sol_layer_pro[47] = sol_layer_pro[47] + "%8s\n" \
                    %(" ")
    #   ! 49  CGO2 = O2 CONC IN GAS PHASE (g/m3 OF SOIL AIR)
                sol_layer_pro[48] = sol_layer_pro[48] + "%8.2f\n" \
                    %(0.00)
    #   ! 50  CGCO2= CO2 CONC IN GAS PHASE (g/m3 OF SOIL AIR)                                                       
                sol_layer_pro[49] = sol_layer_pro[49] + "%8.2f\n" \
                    %(0.00)
    #   ! 51  CGN2O= N2O CONC IN GAS PHASE (g/m3 OF SOIL AIR)                 
                sol_layer_pro[50] = sol_layer_pro[50] + "%8.2f\n" \
                    %(0.00)
    
        for layproidx in range(3, 51):
            wfid_sol.writelines(sol_layer_pro[layproidx])
    
        
        wfid_sol.close()





    #######################################################
    def writeopscomline(self, fidopscom, hruidx, hrunolist):

        fidopscom.writelines("%5i\tOP%s.OPC\n" %(hruidx+1,
                                              hrunolist[hruidx]))



    def updatejson_ops(self,
                       json_ops,
                       hruidx,
                       hrunolist,
                       mgt2ops):

        lenopslines = len(mgt2ops["opslines"]) 
        
        # Yearidx was used to write the year of operation
        # It will be updated by adding one year after 17 was
        # encountered.
        yearidx = 1
        
        # rotactr: rotation counter:
        # Due to the skipping, the looping index will be skipped
        # also. Index was used to write the index of opsjson. In order
        # to make it continuous, the idx for the opsjson will be 
        # reduced by the number of skipping.
        # Kill counter: in SWAT, there is harvest and kill together.
        # But in APEX, there is not one like this. I will need to add
        # one line, also for the index in the opsjson index.
        rotactr = 0
        killctr = 0

        
        for lidx in range(lenopslines):
            
#            print(mgt2ops["opslines"]["op%i" %(lidx+30)])
            # Crop id will be used to identify the land use number
            cropid = "0"
            
            # When there is a rotation marker, the line of operation need to be 
            # skipped, thus the operation number in the ops json need to 
            # be minus one. 
            # If there is an harvest and kill operation, one kill line need to be 
            # added, the counter need to be added one.

            # First check whether this is the line marking the end of
            # one rotation year. This means mgt4 = 17
            if (mgt2ops["opslines"]["op%i" %(lidx+30)]["mgt4"] == 17) or (
                 mgt2ops["opslines"]["op%i" %(lidx+30)]["mgt4"] == 0):
                rotactr = rotactr-1
                yearidx = yearidx+1
                continue
            else:
                # I will first assign this as all 3. OPV2 was said to be 
                # the curve number. I will see whether enter CN works.
                # If not, I will go back and modify this based on CN in SWAT.
                cropid = mgt2ops["swatcropid"]*1
#                    # This should be the crop id in the APEX db
                json_ops["jx6_cropid"]["jx6_cropid%i"
                        %(lidx+rotactr+killctr)]=self.apexcrop[self.swatplant[cropid]]
                
                json_ops["lun_landuseno"]["lun_landuseno%i"
                        %(lidx+rotactr+killctr)]=self.apexluncn[self.swatplant[cropid]][4] 
                json_ops["iaui_autoirr"]["iaui_autoirr%i" %(lidx+rotactr+killctr)]=500
                json_ops["iauf_autofert"]["iauf_autofert%i" %(lidx+rotactr+killctr)]=261
                json_ops["iamf_automanualdepos"]["iamf_automanualdepos%i" %(lidx+rotactr+killctr)]=268
                json_ops["ispf_autosolman"]["ispf_autosolman%i" %(lidx+rotactr+killctr)]=266
                json_ops["ilqf_atliqman"]["ilqf_atliqman%i" %(lidx+rotactr+killctr)]=265
                json_ops["iaul_atlime"]["iaul_atlime%i" %(lidx+rotactr+killctr)]=267

                # Next decide whether the scheduling is based on heat unit
                # or by date.
                # If by heat unit, use it, else, assume jan 1 for all  
                # operaiton and enter heat unit.
                

                if mgt2ops["opslines"]["op%i" %(lidx+30)]["mgt3"] != 0:
                    json_ops["jx1_year"]["jx1_year%i" %(lidx+rotactr+killctr)]=yearidx
                    json_ops["jx2_month"]["jx2_month%i" %(lidx+rotactr+killctr)]=1
                    json_ops["jx3_day"]["jx3_day%i" %(lidx+rotactr+killctr)]=1
                    json_ops["opv7"]["opv7_%i"
                        %(lidx+rotactr+killctr)] = mgt2ops["opslines"]["op%i" %(lidx+30)]["mgt3"]
                else:
                    # If in the SWAT model, schedule is based on date, 
                    # get the date
                    json_ops["jx1_year"]["jx1_year%i" %(lidx+rotactr+killctr)]=yearidx
                    json_ops["jx2_month"]["jx2_month%i"
                        %(lidx+rotactr+killctr)]=mgt2ops["opslines"]["op%i" %(lidx+30)]["mgt1"]
                    json_ops["jx3_day"]["jx3_day%i"
                        %(lidx+rotactr+killctr)]=mgt2ops["opslines"]["op%i" %(lidx+30)]["mgt2"]
                    # OPV7: time of peration as fraction
                    json_ops["opv7"]["opv7_%i" %(lidx+rotactr+killctr)]=0.00
                
                # Management options:
                # 1 for planting and begining of growing season
                # This will determined that the planting operation
                # need to be assigned. The planting, will 
                # all be determined based on crop types.

                if mgt2ops["opslines"]["op%i" %(lidx+30)]["mgt4"] == 1:
                    json_ops["jx4_tillid"]["jx4_tillid%i" 
                        %(lidx+rotactr+killctr)] = self.apexluncn[self.swatplant[cropid]][2]                       
                    json_ops["jx5_tractid"]["jx5_tractid%i" 
                        %(lidx+rotactr+killctr)] = self.apexluncn[self.swatplant[cropid]][3]                                  
                    # jx 7 has four functions:
                    # XMTU, LYR, Pesticide ID and fertilizer id
                    # XMTU and LYR is for trees, I will give a specific number
                    # here: 10 years to go to mature
                    if self.apexluncn[self.swatplant[cropid]][11] == "WOOD":
                        json_ops["jx7"]["jx7_%i" %(lidx+rotactr+killctr)]=10
                    else:
                        json_ops["jx7"]["jx7_%i" %(lidx+rotactr+killctr)]=0
                
                    # OPV1: potential heat units
                    #       stocking rate,
                    #       irrigation application volumn
                    #       fertilization rate
                    #       pesticide rate
                    #       lime rate
                    json_ops["opv1"]["opv1_%i" 
                        %(lidx+rotactr+killctr)] = mgt2ops["opslines"]["op%i" %(lidx+30)]["mgt8"] 
                    
                    # OPV2 to 6 does not change with operation type.
                    # I will leave them as it is and set them as fixed
                    # values.
                    # OPV2: 2condition CSC runoff curve number
                    # or land use number, I will enter the CN here
                    # from the SWAT, since it was calibrated
                    # pest control factor
                    # OPV3: Auto irrigation trigger
                    # OPV4: runoff volume/vol irrigation water
                    # applied. 
                    # OPV5: plant population:
                    # factor to adjust automatic irrigation volume
                    # OPV6: Maximum annual N fertilizer applied to a crop
                    json_ops["opv2"]["opv2_%i" %(lidx+rotactr+killctr
                            )] = self.apexluncn[self.swatplant[cropid]][4]                
                    json_ops["opv3"]["opv3_%i" %(lidx+rotactr+killctr)] = 0                
                    json_ops["opv4"]["opv4_%i" %(lidx+rotactr+killctr)] = 0                
                    json_ops["opv5"]["opv5_%i" %(lidx+rotactr+killctr)] = 0                
                    json_ops["opv6"]["opv6_%i" %(lidx+rotactr+killctr)] = 0                
                    json_ops["opv8"]["opv8_%i" %(lidx+rotactr+killctr)] = 0                
                                        
    
                # 2 for irrigation operation
                # In tillage, there are 8 till for irrigation:
                # GATEPIPE 382, CNTR PVT 500, IRR100HP 501, FLOODIRR 502,
                # ALDRPIRR 530, WY WWELL 531, WYCDITCH 533, WYGTPIPE 534
                # I will assume all of them to be 500
                elif mgt2ops["opslines"]["op%i" %(lidx+30)]["mgt4"] == 2:
                    json_ops["jx4_tillid"]["jx4_tillid%i" 
                        %(lidx+rotactr+killctr)] = 500                      
                    json_ops["jx5_tractid"]["jx5_tractid%i" 
                        %(lidx+rotactr+killctr)] = 0                                  
                    # jx 7 has four functions:
                    # XMTU, LYR, Pesticide ID and fertilizer id
                    # XMTU and LYR is for trees, I will give a specific number
                    # here: 10 years to go to mature
                    if self.apexluncn[self.swatplant[cropid]][11] == "WOOD":
                        json_ops["jx7"]["jx7_%i" %(lidx+rotactr+killctr)]=10
                    else:
                        json_ops["jx7"]["jx7_%i" %(lidx+rotactr+killctr)]=0
                
                    # OPV1: potential heat units
                    #       stocking rate,
                    #       irrigation application volumn
                    #       fertilization rate
                    #       pesticide rate
                    #       lime rate
                    # I am not sure whether they have irrigation in this 
                    # model, but if there is a number, it will be 
                    # entered here
                    json_ops["opv1"]["opv1_%i" 
                        %(lidx+rotactr+killctr)] = mgt2ops["opslines"]["op%i" %(lidx+30)]["mgt8"]
                                   
                    # OPV2 to 6 does not change with operation type.
                    # I will leave them as it is and set them as fixed
                    # values.
                    # OPV2: 2condition CSC runoff curve number
                    # or land use number, I will enter the CN here
                    # from the SWAT, since it was calibrated
                    # pest control factor
                    # OPV3: Auto irrigation trigger
                    # OPV4: runoff volume/vol irrigation water
                    # applied. 
                    # OPV5: plant population:
                    # factor to adjust automatic irrigation volume
                    # OPV6: Maximum annual N fertilizer applied to a crop
                    json_ops["opv2"]["opv2_%i" %(lidx+rotactr+killctr
                            )] = self.apexluncn[self.swatplant[cropid]][4]                
                    json_ops["opv3"]["opv3_%i" %(lidx+rotactr+killctr)] = 0                
                    json_ops["opv4"]["opv4_%i" %(lidx+rotactr+killctr)] = 0                
                    json_ops["opv5"]["opv5_%i" %(lidx+rotactr+killctr)] = 0                
                    json_ops["opv6"]["opv6_%i" %(lidx+rotactr+killctr)] = 0                
                    json_ops["opv8"]["opv8_%i" %(lidx+rotactr+killctr)] = 0                
                                        
                # 3 for fertilizer operation
                # In tillage, there are 7 till for irrigation:
                # AREIALFT 258, ANHYTRAC 259
                # ANHYTRLR, 260, DRYFERLR 261, LQDFTRLR 265,
                # SPFTSPDR 267, FERTRENT 271
                # I will assume them to be all 259
                elif mgt2ops["opslines"]["op%i" %(lidx+30)]["mgt4"] == 3:
                    json_ops["jx4_tillid"]["jx4_tillid%i" 
                        %(lidx+rotactr+killctr)] = 259                      
                    json_ops["jx5_tractid"]["jx5_tractid%i" 
                        %(lidx+rotactr+killctr)] = 615                                  
                    # jx 7 has four functions:
                    # XMTU, LYR, Pesticide ID and fertilizer id
                    # XMTU and LYR is for trees, I will give a specific number
                    # here: 10 years to go to mature
                    if self.apexluncn[self.swatplant[cropid]][11] == "WOOD":
                        json_ops["jx7"]["jx7_%i" %(lidx+rotactr+killctr)]=10
                    else:
                        # For other crops, I will need the fert id here:
                        fertid = "0"    
                        fertid = str(mgt2ops["opslines"]["op%i" %(lidx+30)]["mgt5"])
                        
#                            print(self.swatfert)
#                            print(mgt2ops["opslines"]["op%i" %(lidx+30)])
                        
                        json_ops["jx7"]["jx7_%i" 
                                %(lidx+rotactr+killctr)]=self.apexfert[self.swatfert[fertid]]
                    # OPV1: potential heat units
                    #       stocking rate,
                    #       irrigation application volumn
                    #       fertilization rate
                    #       pesticide rate
                    #       lime rate
                    # I am not sure whether they have irrigation in this 
                    # model, I will assume no irrigation.
                    json_ops["opv1"]["opv1_%i" 
                        %(lidx+rotactr+killctr)] = mgt2ops["opslines"]["op%i" %(lidx+30)]["mgt8"]                        
                    
                    # OPV2 to 6 does not change with operation type.
                    # I will leave them as it is and set them as fixed
                    # values.
                    # OPV2: 2condition CSC runoff curve number
                    # or land use number, I will enter the CN here
                    # from the SWAT, since it was calibrated
                    # pest control factor
                    # OPV3: Auto irrigation trigger
                    # OPV4: runoff volume/vol irrigation water
                    # applied. 
                    # OPV5: plant population:
                    # factor to adjust automatic irrigation volume
                    # OPV6: Maximum annual N fertilizer applied to a crop
                    json_ops["opv2"]["opv2_%i" %(lidx+rotactr+killctr
                            )] = self.apexluncn[self.swatplant[cropid]][4]                
                    json_ops["opv3"]["opv3_%i" %(lidx+rotactr+killctr)] = 0                
                    json_ops["opv4"]["opv4_%i" %(lidx+rotactr+killctr)] = 0                
                    json_ops["opv5"]["opv5_%i" %(lidx+rotactr+killctr)] = 0                
                    json_ops["opv6"]["opv6_%i" %(lidx+rotactr+killctr)] = 0                
                    json_ops["opv8"]["opv8_%i" %(lidx+rotactr+killctr)] = 0                
                                        
                # 4 for pesticide operation
                # In tillage, there are 7 till for irrigation:
                # AERIALCH 272, CHEMIMPL 273, CHEMLGSP 274, CGE30TLR 277,
                # CHEMRENT 283
                   
                # I will assume them to be all 273
                elif mgt2ops["opslines"]["op%i" %(lidx+30)]["mgt4"] == 4:
                    json_ops["jx4_tillid"]["jx4_tillid%i" 
                        %(lidx+rotactr+killctr)] = 273                      
                    json_ops["jx5_tractid"]["jx5_tractid%i" 
                        %(lidx+rotactr+killctr)] = 615                                  
                    # jx 7 has four functions:
                    # XMTU, LYR, Pesticide ID and fertilizer id
                    # XMTU and LYR is for trees, I will give a specific number
                    # here: 10 years to go to mature
                    if self.apexluncn[self.swatplant[cropid]][11] == "WOOD":
                        json_ops["jx7"]["jx7_%i" %(lidx+rotactr+killctr)]=10
                    else:
                        # For other crops, I will need the fert id here:
                        pestid = "0"    
                        pestid = str(mgt2ops["opslines"]["op%i" %(lidx+30)]["mgt5"])
                            
                        json_ops["jx7"]["jx7_%i" 
                                %(lidx+rotactr+killctr)]=self.apexpest[self.swatpest[pestid]]
                    # OPV1: potential heat units
                    #       stocking rate,
                    #       irrigation application volumn
                    #       fertilization rate
                    #       pesticide rate
                    #       lime rate
                    # I am not sure whether they have irrigation in this 
                    # model, I will assume no irrigation.
                    json_ops["opv1"]["opv1_%i" 
                        %(lidx+rotactr+killctr)] = mgt2ops["opslines"]["op%i" %(lidx+30)]["mgt8"]                        
                                            
                    # OPV2 to 6 does not change with operation type.
                    # I will leave them as it is and set them as fixed
                    # values.
                    # OPV2: 2condition CSC runoff curve number
                    # or land use number, I will enter the CN here
                    # from the SWAT, since it was calibrated
                    # pest control factor
                    # OPV3: Auto irrigation trigger
                    # OPV4: runoff volume/vol irrigation water
                    # applied. 
                    # OPV5: plant population:
                    # factor to adjust automatic irrigation volume
                    # OPV6: Maximum annual N fertilizer applied to a crop
                    json_ops["opv2"]["opv2_%i" %(lidx+rotactr+killctr
                            )] = self.apexluncn[self.swatplant[cropid]][4]                
                    json_ops["opv3"]["opv3_%i" %(lidx+rotactr+killctr)] = 0                
                    json_ops["opv4"]["opv4_%i" %(lidx+rotactr+killctr)] = 0                
                    json_ops["opv5"]["opv5_%i" %(lidx+rotactr+killctr)] = 0                
                    json_ops["opv6"]["opv6_%i" %(lidx+rotactr+killctr)] = 0                
                    json_ops["opv8"]["opv8_%i" %(lidx+rotactr+killctr)] = 0                
                                        
                    
                # 5 for harvest and kill operation
                # I should pay attention, if there is no kill, 
                # I have to add one line after the harvest date.
                elif mgt2ops["opslines"]["op%i" %(lidx+30)]["mgt4"] == 5:
                    
                    # Tillage was operated based on crop types
                    # The crop types was classified into different crops
                    # based on the LUN numbers: ROWC, FALW, SGRN, PAST,
                    # WOOD, IMPV
                    if self.apexluncn[self.swatplant[cropid]][11] == "ROWC": 
                        json_ops["jx4_tillid"]["jx4_tillid%i" 
                            %(lidx+rotactr+killctr)] = 292                      
                        json_ops["jx5_tractid"]["jx5_tractid%i" 
                            %(lidx+rotactr+killctr)] = 30      
                                
                    elif self.apexluncn[self.swatplant[cropid]][11] == "SGRN": 
                        json_ops["jx4_tillid"]["jx4_tillid%i" 
                            %(lidx+rotactr+killctr)] = 292                      
                        json_ops["jx5_tractid"]["jx5_tractid%i" 
                            %(lidx+rotactr+killctr)] = 30                                    
                                
                    elif self.apexluncn[self.swatplant[cropid]][11] == "PAST": 
                        json_ops["jx4_tillid"]["jx4_tillid%i" 
                            %(lidx+rotactr+killctr)] = 310                      
                        json_ops["jx5_tractid"]["jx5_tractid%i" 
                            %(lidx+rotactr+killctr)] = 12                
                                
                    elif self.apexluncn[self.swatplant[cropid]][11] == "WOOD": 
                        json_ops["jx4_tillid"]["jx4_tillid%i" 
                            %(lidx+rotactr+killctr)] = 310                      
                        json_ops["jx5_tractid"]["jx5_tractid%i" 
                            %(lidx+rotactr+killctr)] = 0                                       
                                
                    else: 
                        json_ops["jx4_tillid"]["jx4_tillid%i" 
                            %(lidx+rotactr+killctr)] = 310                      
                        json_ops["jx5_tractid"]["jx5_tractid%i" 
                            %(lidx+rotactr+killctr)] = 12                                       
                                                                    
                                
                    # jx 7 has four functions:
                    # XMTU, LYR, Pesticide ID and fertilizer id
                    # XMTU and LYR is for trees, I will give a specific number
                    # here: 10 years to go to mature
                    if self.apexluncn[self.swatplant[cropid]][11] == "WOOD":
                        json_ops["jx7"]["jx7_%i" %(lidx+rotactr+killctr)]=10
                    else:
                        json_ops["jx7"]["jx7_%i" 
                                %(lidx+rotactr+killctr)]=0
                    # OPV1: potential heat units
                    #       stocking rate,
                    #       irrigation application volumn
                    #       fertilization rate
                    #       pesticide rate
                    #       lime rate
                    # I am not sure whether they have irrigation in this 
                    # model, I will assume no irrigation.
                    json_ops["opv1"]["opv1_%i" 
                        %(lidx+rotactr+killctr)] = 0                        

                    # OPV2 to 6 does not change with operation type.
                    # I will leave them as it is and set them as fixed
                    # values.
                    # OPV2: 2condition CSC runoff curve number
                    # or land use number, I will enter the CN here
                    # from the SWAT, since it was calibrated
                    # pest control factor
                    # OPV3: Auto irrigation trigger
                    # OPV4: runoff volume/vol irrigation water
                    # applied. 
                    # OPV5: plant population:
                    # factor to adjust automatic irrigation volume
                    # OPV6: Maximum annual N fertilizer applied to a crop
                    json_ops["opv2"]["opv2_%i" %(lidx+rotactr+killctr
                            )] = self.apexluncn[self.swatplant[cropid]][4]                
                    json_ops["opv3"]["opv3_%i" %(lidx+rotactr+killctr)] = 0                
                    json_ops["opv4"]["opv4_%i" %(lidx+rotactr+killctr)] = 0                
                    json_ops["opv5"]["opv5_%i" %(lidx+rotactr+killctr)] = 0                
                    json_ops["opv6"]["opv6_%i" %(lidx+rotactr+killctr)] = 0                
                    json_ops["opv8"]["opv8_%i" %(lidx+rotactr+killctr)] = 0                
                                        
                    # After processing this line, there should be one line 
                    # added for kill
                    # I will need to add one line and also update
                    # the counter and total lines for looping.
                    # Before the kill counter is updated, the line
                    # for kill will be added
                    json_ops["jx1_year"]["jx1_year%i" %(lidx+rotactr+killctr+1)]=yearidx
                    
                    if mgt2ops["opslines"]["op%i" %(lidx+30)]["mgt3"] != 0:
                        json_ops["jx2_month"]["jx2_month%i" %(lidx+rotactr+killctr+1)]=1
                        json_ops["jx3_day"]["jx3_day%i" %(lidx+rotactr+killctr+1)]=1
                        json_ops["opv7"]["opv7_%i"
                            %(lidx+rotactr+killctr+1)] = mgt2ops["opslines"]["op%i" %(lidx+30)]["mgt3"]
                    else:
                        # If in the SWAT model, schedule is based on date, 
                        # get the date
                        json_ops["jx2_month"]["jx2_month%i"
                            %(lidx+rotactr+killctr+1)]=mgt2ops["opslines"]["op%i" %(lidx+30)]["mgt1"]
                        json_ops["jx3_day"]["jx3_day%i"
                            %(lidx+rotactr+killctr+1)]=mgt2ops["opslines"]["op%i" %(lidx+30)]["mgt2"]
                        # OPV7: time of peration as fraction
                        json_ops["opv7"]["opv7_%i"
                            %(lidx+rotactr+killctr+1)]=0.00

    
                    json_ops["jx4_tillid"]["jx4_tillid%i" 
                        %(lidx+rotactr+killctr+1)] = 451                      
                    json_ops["jx5_tractid"]["jx5_tractid%i" 
                        %(lidx+rotactr+killctr+1)] = 0  
                    json_ops["jx6_cropid"]["jx6_cropid%i"
                        %(lidx+rotactr+killctr+1)]=self.apexcrop[self.swatplant[cropid]]
                    json_ops["jx7"]["jx7_%i" 
                        %(lidx+rotactr+killctr+1)]=0                        
                    json_ops["opv1"]["opv1_%i" %(lidx+rotactr+killctr+1)] = 0  
                    json_ops["opv2"]["opv2_%i" %(lidx+rotactr+killctr+1)] = self.apexluncn[self.swatplant[cropid]][4]                
                    json_ops["opv3"]["opv3_%i" %(lidx+rotactr+killctr+1)] = 0                
                    json_ops["opv4"]["opv4_%i" %(lidx+rotactr+killctr+1)] = 0                
                    json_ops["opv5"]["opv5_%i" %(lidx+rotactr+killctr+1)] = 0                
                    json_ops["opv6"]["opv6_%i" %(lidx+rotactr+killctr+1)] = 0                          
                    json_ops["opv8"]["opv8_%i" %(lidx+rotactr+killctr+1)] = 0                          
                    # operaiton and enter heat unit.
                    if mgt2ops["opslines"]["op%i" %(lidx+30)]["mgt3"] != 0:
                        json_ops["opv7"]["opv7_%i"
                            %(lidx+rotactr+killctr+1)] = mgt2ops["opslines"]["op%i" %(lidx+30)]["mgt3"]
                    else:
                        # OPV7: time of peration as fraction
                        json_ops["opv7"]["opv7_%i" %(lidx+rotactr+killctr+1)]=0.00

                    killctr = killctr + 1
                    
                    
                # 6 for tillage operation
                elif mgt2ops["opslines"]["op%i" %(lidx+30)]["mgt4"] == 6:
                    
                    tillid = "0"    
                    tillid = mgt2ops["opslines"]["op%i" %(lidx+30)]["mgt5"]

                    json_ops["jx4_tillid"]["jx4_tillid%i" 
                        %(lidx+rotactr+killctr)] = self.apextill[self.swattill[tillid]]  
                    
                    json_ops["jx5_tractid"]["jx5_tractid%i" 
                        %(lidx+rotactr+killctr)] = 18                                  
                    # jx 7 has four functions:
                    # XMTU, LYR, Pesticide ID and fertilizer id
                    # XMTU and LYR is for trees, I will give a specific number
                    # here: 10 years to go to mature
                    if self.apexluncn[self.swatplant[cropid]][11] == "WOOD":
                        json_ops["jx7"]["jx7_%i" %(lidx+rotactr+killctr)]=10
                    else:
                        json_ops["jx7"]["jx7_%i" %(lidx+rotactr+killctr)]=0
                    # OPV1: potential heat units
                    #       stocking rate,
                    #       irrigation application volumn
                    #       fertilization rate
                    #       pesticide rate
                    #       lime rate
                    # I am not sure whether they have irrigation in this 
                    # model, I will assume no irrigation.
                    json_ops["opv1"]["opv1_%i" 
                        %(lidx+rotactr+killctr)] = 0   
                            
                    # OPV2 to 6 does not change with operation type.
                    # I will leave them as it is and set them as fixed
                    # values.
                    # OPV2: 2condition CSC runoff curve number
                    # or land use number, I will enter the CN here
                    # from the SWAT, since it was calibrated
                    # pest control factor
                    # OPV3: Auto irrigation trigger
                    # OPV4: runoff volume/vol irrigation water
                    # applied. 
                    # OPV5: plant population:
                    # factor to adjust automatic irrigation volume
                    # OPV6: Maximum annual N fertilizer applied to a crop
                    json_ops["opv2"]["opv2_%i" %(lidx+rotactr+killctr
                            )] = self.apexluncn[self.swatplant[cropid]][4]                
                    json_ops["opv3"]["opv3_%i" %(lidx+rotactr+killctr)] = 0                
                    json_ops["opv4"]["opv4_%i" %(lidx+rotactr+killctr)] = 0                
                    json_ops["opv5"]["opv5_%i" %(lidx+rotactr+killctr)] = 0                
                    json_ops["opv6"]["opv6_%i" %(lidx+rotactr+killctr)] = 0                
                    json_ops["opv8"]["opv8_%i" %(lidx+rotactr+killctr)] = 0                
                                        
                    
                            
                # 7 for harvest only
                # I should pay attention, if there is no kill, 
                # I have to add one line after the harvest date.
                elif mgt2ops["opslines"]["op%i" %(lidx+30)]["mgt4"] == 7:
                    
                    # Tillage was operated based on crop types
                    # The crop types was classified into different crops
                    # based on the LUN numbers: ROWC, FALW, SGRN, PAST,
                    # WOOD, IMPV
                    if self.apexluncn[self.swatplant[cropid]][11] == "ROWC": 
                        json_ops["jx4_tillid"]["jx4_tillid%i" 
                            %(lidx+rotactr+killctr)] = 292                      
                        json_ops["jx5_tractid"]["jx5_tractid%i" 
                            %(lidx+rotactr+killctr)] = 30      
                                
                    elif self.apexluncn[self.swatplant[cropid]][11] == "SGRN": 
                        json_ops["jx4_tillid"]["jx4_tillid%i" 
                            %(lidx+rotactr+killctr)] = 292                      
                        json_ops["jx5_tractid"]["jx5_tractid%i" 
                            %(lidx+rotactr+killctr)] = 30                                    
                                
                    elif self.apexluncn[self.swatplant[cropid]][11] == "PAST": 
                        json_ops["jx4_tillid"]["jx4_tillid%i" 
                            %(lidx+rotactr+killctr)] = 261                      
                        json_ops["jx5_tractid"]["jx5_tractid%i" 
                            %(lidx+rotactr+killctr)] = 12                
                                
                    elif self.apexluncn[self.swatplant[cropid]][11] == "WOOD": 
                        json_ops["jx4_tillid"]["jx4_tillid%i" 
                            %(lidx+rotactr+killctr)] = 310                      
                        json_ops["jx5_tractid"]["jx5_tractid%i" 
                            %(lidx+rotactr+killctr)] = 12                                       
                                
                    else: 
                        json_ops["jx4_tillid"]["jx4_tillid%i" 
                            %(lidx+rotactr+killctr)] = 310                      
                        json_ops["jx5_tractid"]["jx5_tractid%i" 
                            %(lidx+rotactr+killctr)] = 12                                       
                                                                    
                                
                    # jx 7 has four functions:
                    # XMTU, LYR, Pesticide ID and fertilizer id
                    # XMTU and LYR is for trees, I will give a specific number
                    # here: 10 years to go to mature
                    if self.apexluncn[self.swatplant[cropid]][11] == "WOOD":
                        json_ops["jx7"]["jx7_%i" %(lidx+rotactr+killctr)]=10
                    else:
                        json_ops["jx7"]["jx7_%i" 
                                %(lidx+rotactr+killctr)]=0
                    # OPV1: potential heat units
                    #       stocking rate,
                    #       irrigation application volumn
                    #       fertilization rate
                    #       pesticide rate
                    #       lime rate
                    # I am not sure whether they have irrigation in this 
                    # model, I will assume no irrigation.
                    json_ops["opv1"]["opv1_%i" 
                        %(lidx+rotactr+killctr)] = 0    
                
                    # OPV2 to 6 does not change with operation type.
                    # I will leave them as it is and set them as fixed
                    # values.
                    # OPV2: 2condition CSC runoff curve number
                    # or land use number, I will enter the CN here
                    # from the SWAT, since it was calibrated
                    # pest control factor
                    # OPV3: Auto irrigation trigger
                    # OPV4: runoff volume/vol irrigation water
                    # applied. 
                    # OPV5: plant population:
                    # factor to adjust automatic irrigation volume
                    # OPV6: Maximum annual N fertilizer applied to a crop
                    json_ops["opv2"]["opv2_%i" %(lidx+rotactr+killctr
                            )] = self.apexluncn[self.swatplant[cropid]][4]                
                    json_ops["opv3"]["opv3_%i" %(lidx+rotactr+killctr)] = 0                
                    json_ops["opv4"]["opv4_%i" %(lidx+rotactr+killctr)] = 0                
                    json_ops["opv5"]["opv5_%i" %(lidx+rotactr+killctr)] = 0                
                    json_ops["opv6"]["opv6_%i" %(lidx+rotactr+killctr)] = 0                
                    json_ops["opv8"]["opv8_%i" %(lidx+rotactr+killctr)] = 0                
                                        
                                        
                
                # 8 for kill and end of growing season
                # I should pay attention, if there is no kill, 
                # I have to add one line after the harvest date.
                elif mgt2ops["opslines"]["op%i" %(lidx+30)]["mgt4"] == 8:
                    json_ops["jx4_tillid"]["jx4_tillid%i" 
                        %(lidx+rotactr+killctr)] = 451                      
                    json_ops["jx5_tractid"]["jx5_tractid%i" 
                        %(lidx+rotactr+killctr)] = 0                                       

                    # jx 7 has four functions:
                    # XMTU, LYR, Pesticide ID and fertilizer id
                    # XMTU and LYR is for trees, I will give a specific number
                    # here: 10 years to go to mature
                    if self.apexluncn[self.swatplant[cropid]][11] == "WOOD":
                        json_ops["jx7"]["jx7_%i" %(lidx+rotactr+killctr)]=10
                    else:
                        json_ops["jx7"]["jx7_%i" 
                                %(lidx+rotactr+killctr)]=0
                    # OPV1: potential heat units
                    #       stocking rate,
                    #       irrigation application volumn
                    #       fertilization rate
                    #       pesticide rate
                    #       lime rate
                    # I am not sure whether they have irrigation in this 
                    # model, I will assume no irrigation.
                    json_ops["opv1"]["opv1_%i" 
                        %(lidx+rotactr+killctr)] = 0  
                            
                    # OPV2 to 6 does not change with operation type.
                    # I will leave them as it is and set them as fixed
                    # values.
                    # OPV2: 2condition CSC runoff curve number
                    # or land use number, I will enter the CN here
                    # from the SWAT, since it was calibrated
                    # pest control factor
                    # OPV3: Auto irrigation trigger
                    # OPV4: runoff volume/vol irrigation water
                    # applied. 
                    # OPV5: plant population:
                    # factor to adjust automatic irrigation volume
                    # OPV6: Maximum annual N fertilizer applied to a crop
                    json_ops["opv2"]["opv2_%i" %(lidx+rotactr+killctr
                            )] = self.apexluncn[self.swatplant[cropid]][4]                
                    json_ops["opv3"]["opv3_%i" %(lidx+rotactr+killctr)] = 0                
                    json_ops["opv4"]["opv4_%i" %(lidx+rotactr+killctr)] = 0                
                    json_ops["opv5"]["opv5_%i" %(lidx+rotactr+killctr)] = 0                
                    json_ops["opv6"]["opv6_%i" %(lidx+rotactr+killctr)] = 0                
                    json_ops["opv8"]["opv8_%i" %(lidx+rotactr+killctr)] = 0                
                                        
                    # 9 grazing
                elif mgt2ops["opslines"]["op%i" %(lidx+30)]["mgt4"] == 9:
                    json_ops["jx4_tillid"]["jx4_tillid%i" 
                        %(lidx+rotactr+killctr)] = 426                      
                    json_ops["jx5_tractid"]["jx5_tractid%i" 
                        %(lidx+rotactr+killctr)] = 0                                       

                    # jx 7 has four functions:
                    # XMTU, LYR, Pesticide ID and fertilizer id
                    # XMTU and LYR is for trees, I will give a specific number
                    # here: 10 years to go to mature
                    if self.apexluncn[self.swatplant[cropid]][11] == "WOOD":
                        json_ops["jx7"]["jx7_%i" %(lidx+rotactr+killctr)]=10
                    else:
                        json_ops["jx7"]["jx7_%i" 
                                %(lidx+rotactr+killctr)]=0
                    # OPV1: potential heat units
                    #       stocking rate,
                    #       irrigation application volumn
                    #       fertilization rate
                    #       pesticide rate
                    #       lime rate
                    # I am not sure whether they have irrigation in this 
                    # model, I will assume no irrigation.
                    json_ops["opv1"]["opv1_%i" 
                        %(lidx+rotactr+killctr)] = 0  

                    # OPV2 to 6 does not change with operation type.
                    # I will leave them as it is and set them as fixed
                    # values.
                    # OPV2: 2condition CSC runoff curve number
                    # or land use number, I will enter the CN here
                    # from the SWAT, since it was calibrated
                    # pest control factor
                    # OPV3: Auto irrigation trigger
                    # OPV4: runoff volume/vol irrigation water
                    # applied. 
                    # OPV5: plant population:
                    # factor to adjust automatic irrigation volume
                    # OPV6: Maximum annual N fertilizer applied to a crop
                    json_ops["opv2"]["opv2_%i" %(lidx+rotactr+killctr
                            )] = self.apexluncn[self.swatplant[cropid]][4]                
                    json_ops["opv3"]["opv3_%i" %(lidx+rotactr+killctr)] = 0                
                    json_ops["opv4"]["opv4_%i" %(lidx+rotactr+killctr)] = 0                
                    json_ops["opv5"]["opv5_%i" %(lidx+rotactr+killctr)] = 0                
                    json_ops["opv6"]["opv6_%i" %(lidx+rotactr+killctr)] = 0                
                    json_ops["opv8"]["opv8_%i" %(lidx+rotactr+killctr)] = 0                
     
                # 10 auto irrigation
                elif mgt2ops["opslines"]["op%i" %(lidx+30)]["mgt4"] == 10:
                    json_ops["jx4_tillid"]["jx4_tillid%i" 
                        %(lidx+rotactr+killctr)] = 500                      
                    json_ops["jx5_tractid"]["jx5_tractid%i" 
                        %(lidx+rotactr+killctr)] = 0                                       

                    # jx 7 has four functions:
                    # XMTU, LYR, Pesticide ID and fertilizer id
                    # XMTU and LYR is for trees, I will give a specific number
                    # here: 10 years to go to mature
                    if self.apexluncn[self.swatplant[cropid]][11] == "WOOD":
                        json_ops["jx7"]["jx7_%i" %(lidx+rotactr+killctr)]=10
                    else:
                        json_ops["jx7"]["jx7_%i" 
                                %(lidx+rotactr+killctr)]=0
                    # OPV1: potential heat units
                    #       stocking rate,
                    #       irrigation application volumn
                    #       fertilization rate
                    #       pesticide rate
                    #       lime rate
                    # I am not sure whether they have irrigation in this 
                    # model, I will assume no irrigation.
                    json_ops["opv1"]["opv1_%i" 
                        %(lidx+rotactr+killctr)] = 100  

                    # OPV2 to 6 does not change with operation type.
                    # I will leave them as it is and set them as fixed
                    # values.
                    # OPV2: 2condition CSC runoff curve number
                    # or land use number, I will enter the CN here
                    # from the SWAT, since it was calibrated
                    # pest control factor
                    # OPV3: Auto irrigation trigger
                    # OPV4: runoff volume/vol irrigation water
                    # applied. 
                    # OPV5: plant population:
                    # factor to adjust automatic irrigation volume
                    # OPV6: Maximum annual N fertilizer applied to a crop
                    json_ops["opv2"]["opv2_%i" %(lidx+rotactr+killctr
                            )] = self.apexluncn[self.swatplant[cropid]][4]                
                    json_ops["opv3"]["opv3_%i" %(lidx+rotactr+killctr)] = 0.3                
                    json_ops["opv4"]["opv4_%i" %(lidx+rotactr+killctr)] = 0                
                    json_ops["opv5"]["opv5_%i" %(lidx+rotactr+killctr)] = 0                
                    json_ops["opv6"]["opv6_%i" %(lidx+rotactr+killctr)] = 0                
                    json_ops["opv8"]["opv8_%i" %(lidx+rotactr+killctr)] = 0                     
                
                
                # 11 auto fertilization
                elif mgt2ops["opslines"]["op%i" %(lidx+30)]["mgt4"] == 11:
                    json_ops["jx4_tillid"]["jx4_tillid%i" 
                        %(lidx+rotactr+killctr)] = 259                      
                    json_ops["jx5_tractid"]["jx5_tractid%i" 
                        %(lidx+rotactr+killctr)] = 615                                       

                    # jx 7 has four functions:
                    # XMTU, LYR, Pesticide ID and fertilizer id
                    # XMTU and LYR is for trees, I will give a specific number
                    # here: 10 years to go to mature
                    if self.apexluncn[self.swatplant[cropid]][11] == "WOOD":
                        json_ops["jx7"]["jx7_%i" %(lidx+rotactr+killctr)]=10
                    else:
                        # For other crops, I will need the fert id here:
                        fertid = "0"    
                        fertid = str(mgt2ops["opslines"]["op%i" %(lidx+30)]["mgt5"])
                        
#                            print(self.swatfert)
#                            print(mgt2ops["opslines"]["op%i" %(lidx+30)])
                        
                        json_ops["jx7"]["jx7_%i" 
                                %(lidx+rotactr+killctr)]=self.apexfert[self.swatfert[fertid]]
                    # OPV1: potential heat units
                    #       stocking rate,
                    #       irrigation application volumn
                    #       fertilization rate
                    #       pesticide rate
                    #       lime rate
                    # I am not sure whether they have irrigation in this 
                    # model, I will assume no irrigation.
                    json_ops["opv1"]["opv1_%i" 
                        %(lidx+rotactr+killctr)] = 50  

                    # OPV2 to 6 does not change with operation type.
                    # I will leave them as it is and set them as fixed
                    # values.
                    # OPV2: 2condition CSC runoff curve number
                    # or land use number, I will enter the CN here
                    # from the SWAT, since it was calibrated
                    # pest control factor
                    # OPV3: Auto irrigation trigger
                    # OPV4: runoff volume/vol irrigation water
                    # applied. 
                    # OPV5: plant population:
                    # factor to adjust automatic irrigation volume
                    # OPV6: Maximum annual N fertilizer applied to a crop
                    json_ops["opv2"]["opv2_%i" %(lidx+rotactr+killctr
                            )] = self.apexluncn[self.swatplant[cropid]][4]                
                    json_ops["opv3"]["opv3_%i" %(lidx+rotactr+killctr)] = 0                
                    json_ops["opv4"]["opv4_%i" %(lidx+rotactr+killctr)] = 0                
                    json_ops["opv5"]["opv5_%i" %(lidx+rotactr+killctr)] = 0                
                    json_ops["opv6"]["opv6_%i" %(lidx+rotactr+killctr)] = 800                
                    json_ops["opv8"]["opv8_%i" %(lidx+rotactr+killctr)] = 0                     
                                
                
                # 12 street sweeping operation
                # 13 release impound
                # 14 continuous fertilization
                # 15 continuous pesticides
                # 0 or 17 end of year rotation flag.
                
                # There should not be operation for others.
                else:
                    json_ops["jx4_tillid"]["jx4_tillid%i" 
                        %(lidx+rotactr+killctr)] = 0                      
                    json_ops["jx5_tractid"]["jx5_tractid%i" 
                        %(lidx+rotactr+killctr)] = 0                                       

                    # jx 7 has four functions:
                    # XMTU, LYR, Pesticide ID and fertilizer id
                    # XMTU and LYR is for trees, I will give a specific number
                    # here: 10 years to go to mature
                    if self.apexluncn[self.swatplant[cropid]][11] == "WOOD":
                        json_ops["jx7"]["jx7_%i" %(lidx+rotactr+killctr)]=10
                    else:
                        json_ops["jx7"]["jx7_%i" 
                                %(lidx+rotactr+killctr)]=0
                    # OPV1: potential heat units
                    #       stocking rate,
                    #       irrigation application volumn
                    #       fertilization rate
                    #       pesticide rate
                    #       lime rate
                    # I am not sure whether they have irrigation in this 
                    # model, I will assume no irrigation.
                    json_ops["opv1"]["opv1_%i" 
                        %(lidx+rotactr+killctr)] = 0  
                
                                            # OPV2 to 6 does not change with operation type.
                    # I will leave them as it is and set them as fixed
                    # values.
                    # OPV2: 2condition CSC runoff curve number
                    # or land use number, I will enter the CN here
                    # from the SWAT, since it was calibrated
                    # pest control factor
                    # OPV3: Auto irrigation trigger
                    # OPV4: runoff volume/vol irrigation water
                    # applied. 
                    # OPV5: plant population:
                    # factor to adjust automatic irrigation volume
                    # OPV6: Maximum annual N fertilizer applied to a crop
                    json_ops["opv2"]["opv2_%i" %(lidx+rotactr+killctr
                            )] = self.apexluncn[self.swatplant[cropid]][4]                
                    json_ops["opv3"]["opv3_%i" %(lidx+rotactr+killctr)] = 0                
                    json_ops["opv4"]["opv4_%i" %(lidx+rotactr+killctr)] = 0                
                    json_ops["opv5"]["opv5_%i" %(lidx+rotactr+killctr)] = 0                
                    json_ops["opv6"]["opv6_%i" %(lidx+rotactr+killctr)] = 0                
                    json_ops["opv8"]["opv8_%i" %(lidx+rotactr+killctr)] = 0                

        
        return json_ops



    def writefile_ops(self, inf_usrjson, hruidx, hrunolist, mgt2ops):
        
        opsf_name = "OP%s.OPC" %(hrunolist[hruidx])
        
        # Start writing ops files    
        wfid_ops = 0
        wfid_ops = open(r"%s/%s" %(self.outfd_apexdft, 
                                     opsf_name), "w")

        # Writing line 1: description, this will be the name of the mgt
        wfid_ops.writelines("%s\n" %(opsf_name))
        
        # Writing line 2: general parameters
        # This depends on the land cover and hydrologic soil group.
        # HSG can be get from soil data.
        # In ArcAPEX land use number is set in the database for each operation.
        # In my database, I shall include it in the json file and update
        # this number while user select new land use types.
        # This will be input in the database with the list of mgt table.
        # The model will get hsg from the soil file. I only need to input the 
        # land use number
        ops_l2 = "%4i%4i%4i%4i%4i%4i%4i\n"\
                        %(float(inf_usrjson["lun_landuseno"]["lun_landuseno1"]),\
                          float(inf_usrjson["iaui_autoirr"]["iaui_autoirr1"]),\
    			float(inf_usrjson["iauf_autofert"]["iauf_autofert1"]),\
    			float(inf_usrjson["iamf_automanualdepos"]["iamf_automanualdepos1"]),\
    			float(inf_usrjson["ispf_autosolman"]["ispf_autosolman1"]),\
    			float(inf_usrjson["ilqf_atliqman"]["ilqf_atliqman1"]),\
    			float(inf_usrjson["iaul_atlime"]["iaul_atlime1"]))
        wfid_ops.writelines(ops_l2)
        
        # Writing line 3 to line N
        # N is the total number of operations, this will be determined as
        # length of one parameter in the json file. Here, I used year
        no_ops = len(inf_usrjson["jx1_year"])
        
        ops_templine = 0
    
        for opsidx in range(no_ops):
            
            ops_templine = "%3s%3s%3s%5s%5s%5s%5s%8.2f%8.2f%8.2f%8.2f%8.2f%8.2f%8.2f%8.2f\n"\
    				%(
    				inf_usrjson["jx1_year"]["jx1_year%i" %(opsidx)],\
    				inf_usrjson["jx2_month"]["jx2_month%i" %(opsidx)],\
    				inf_usrjson["jx3_day"]["jx3_day%i" %(opsidx)],\
    				inf_usrjson["jx4_tillid"]["jx4_tillid%i" %(opsidx)],\
    				inf_usrjson["jx5_tractid"]["jx5_tractid%i" %(opsidx)],\
    				inf_usrjson["jx6_cropid"]["jx6_cropid%i" %(opsidx)],\
    				inf_usrjson["jx7"]["jx7_%i" %(opsidx)],\
    				float(inf_usrjson["opv1"]["opv1_%i" %(opsidx)]),\
    				float(inf_usrjson["opv2"]["opv2_%i" %(opsidx)]),\
    				float(inf_usrjson["opv3"]["opv3_%i" %(opsidx)]),\
    				float(inf_usrjson["opv4"]["opv4_%i" %(opsidx)]),\
    				float(inf_usrjson["opv5"]["opv5_%i" %(opsidx)]),\
    				float(inf_usrjson["opv6"]["opv6_%i" %(opsidx)]),\
    				float(inf_usrjson["opv7"]["opv7_%i" %(opsidx)]),\
    				float(inf_usrjson["opv8"]["opv8_%i" %(opsidx)])
    				
                                    )
    	
            wfid_ops.writelines(ops_templine)
    
        # write end line
        ops_endline = "%3i%3i%3i%5i%5i%5i%5i%8.2f%8.2f%8.2f%8.2f%8.2f%8.2f%8.2f\n"\
                        %(0, 0, 0, 0, 0, 0, 0,\
                        0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00)
        
        wfid_ops.writelines(ops_endline)
    
        wfid_ops.close()





    #######################################################
    def writedlycomline(self, fiddlycom, hruidx, hrunolist):

        fiddlycom.writelines("%5i\tWD%s.DLY\n" %(hruidx+1,
                                              hrunolist[hruidx]))



    #######################################################
    def writesubcomline(self, fidsubcom, hruidx, hrunolist):

        fidsubcom.writelines("%5i\tSUB%s.SUB\n" %(hruidx+1,
                                              hrunolist[hruidx]))



    def updatejson_sub(self, 
                       json_sub,
                       hruidx, 
                       hrunolist, 
                       inp_onefield,
                       mgt2ops):

        json_sub["model_setup"]["subid_snum"]= "1"
        json_sub["model_setup"]["description_title"]="SUB%s" %(hrunolist[hruidx])
        json_sub["model_setup"]["owner_id"]= "1"
        json_sub["model_setup"]["nvcn"]= "4"
        json_sub["model_setup"]["outflow_release_method_isao"]= "0.00"

        json_sub["geographic"]["wsa_ha"]= inp_onefield["areasub"]*inp_onefield["subfrac"]
        json_sub["geographic"]["latitude_xct"]= inp_onefield["lat"]
        json_sub["geographic"]["longitude_yct"]= inp_onefield["long"]
        json_sub["geographic"]["avg_upland_slplen_splg"]= inp_onefield["slopelength"]
        json_sub["geographic"]["avg_upland_slp"]= inp_onefield["slopesteep"]
        json_sub["geographic"]["uplandmanningn_upn"] = inp_onefield["overlandmanningn"]
        # Channel length is the distance along the channel from the outlet to 
        # the most distant point on the watershed. For areas less than 20ha, use zero
        # Otherwise, it can be estimated from length-width ratio of watershed.
        # Here, I assume it as slope length.
        json_sub["geographic"]["channellength_chl"]= inp_onefield["chlength"]/inp_onefield["hruno"]
        json_sub["geographic"]["channelslope_chs"]= inp_onefield["slopesteep"]
        # For agricultural land, I will use excavated or dredged, and
        # not maintained. 
        json_sub["geographic"]["channelmanningn_chn"]=inp_onefield["chmanningn"]
        json_sub["geographic"]["channel_depth_chd"]= "0.2"
        # Reach is between where channel starts or enters the subarea
        # and leaves the subarea. For extreme or field simulation here,
        # we use same value as chl.
        json_sub["geographic"]["reach_length_rchl"]= inp_onefield["chlength"]/inp_onefield["hruno"]
        json_sub["geographic"]["reach_depth_rchd"]= "0.2"
        json_sub["geographic"]["reach_bottom_width_rcbw"]= "0.10"
        json_sub["geographic"]["reach_top_width_rctw"] = "0.50"
        json_sub["geographic"]["reach_slope_rchs"]= inp_onefield["slopesteep"]
        json_sub["geographic"]["reach_manningsn_rchn"]= inp_onefield["chmanningn"]
        json_sub["geographic"]["reach_uslec_rchc"]= "0.005"
        json_sub["geographic"]["reach_uslek_rchk"] = "0.30"
        json_sub["geographic"]["reach_floodplain_rfpw"]= "0.00"
        json_sub["geographic"]["reach_floodplain_length_rfpl"]= "0.00"
        json_sub["geographic"]["rch_ksat_adj_factor_sat1"]= "1.00"

        # This will override that value specified in the ops file.
        # In other words, if I have different values for different tillage, the 
        # values will be modified to this value. If it is set to zero,
        # LUN will not be modified.
        json_sub["land_use_type"]["land_useid_luns"]= "0"
        json_sub["land_use_type"]["standing_crop_residue_stdo"]= "0.00"

        json_sub["soil"]["soilid"]= hruidx+1

        json_sub["management"]["opeartionid_iops"]= hruidx+1
        json_sub["management"]["min_days_automow_imw"]= "0.00"
        json_sub["management"]["min_days_autonitro_ifa"]= "0.00"
        json_sub["management"]["liming_code_lm"]= "1"
        json_sub["management"]["furrow_dike_code_ifd"]= "0.00"
        json_sub["management"]["fd_water_store_fdsf"]= "0.010"
        json_sub["management"]["autofert_lagoon_idf1"]= "0.00"
        json_sub["management"]["auto_manure_feedarea_idf2"]= "0.00"
        json_sub["management"]["auto_commercial_p_idf3"]= "0.00"
        json_sub["management"]["auto_commercial_n_idf4"]= "0.00"
        json_sub["management"]["auto_solid_manure_idf5"]= "0.00"
        json_sub["management"]["auto_commercial_k_idf6"]= "0.00"
        json_sub["management"]["nstress_trigger_auton_bft"]= "0.00"
        json_sub["management"]["auton_rate_fnp4"]= "0.00"
        json_sub["management"]["auton_manure_fnp5"]= "0.00"
        json_sub["management"]["max_annual_auton_fmx"]= "0.00"

        json_sub["drainage"]["drainage_depth_idr"]=mgt2ops["ddrain"] 
        json_sub["drainage"]["drain_days_end_w_stress_drt"]= mgt2ops["tdrain"]/24

        json_sub["grazing"]["feeding_area_ii"]= "1"
        json_sub["grazing"]["manure_app_area_iapl"]= "0.00"
        json_sub["grazing"]["feedarea_pile_autosolidmanure_rate_fnp2"]= "0.00"
        json_sub["grazing"]["herds_eligible_forgrazing_ny1"]= "1"
        json_sub["grazing"]["herds_eligible_forgrazing_ny2"]= "0.00"
        json_sub["grazing"]["herds_eligible_forgrazing_ny3"]= "0.010"
        json_sub["grazing"]["herds_eligible_forgrazing_ny4"]= "0.00"
        json_sub["grazing"]["herds_eligible_forgrazing_ny5"]= "0.00"
        json_sub["grazing"]["herds_eligible_forgrazing_ny6"]= "0.00"
        json_sub["grazing"]["herds_eligible_forgrazing_ny7"]= "0.00"
        json_sub["grazing"]["herds_eligible_forgrazing_ny8"]= "0.00"
        json_sub["grazing"]["herds_eligible_forgrazing_ny9"]= "0.00"
        json_sub["grazing"]["herds_eligible_forgrazing_ny10"]= "0.00"
        json_sub["grazing"]["grazing_limit_herd_xtp1"]= "1"
        json_sub["grazing"]["grazing_limit_herd_xtp2"]= "0.00"
        json_sub["grazing"]["grazing_limit_herd_xtp3"]= "0.010"
        json_sub["grazing"]["grazing_limit_herd_xtp4"]= "0.00"
        json_sub["grazing"]["grazing_limit_herd_xtp5"]= "0.00"
        json_sub["grazing"]["grazing_limit_herd_xtp6"]= "0.00"
        json_sub["grazing"]["grazing_limit_herd_xtp7"]= "0.00"
        json_sub["grazing"]["grazing_limit_herd_xtp8"]= "0.00"
        json_sub["grazing"]["grazing_limit_herd_xtp9"]= "0.00"
        json_sub["grazing"]["grazing_limit_herd_xtp10"]= "0.00"

        json_sub["weather"]["daily_wea_stnid_iwth"]= hruidx+1
        json_sub["weather"]["begin_water_in_snow_sno"]= "0.00"

        json_sub["wind_erosion"]["azimuth_land_slope_amz"]= "0"
        json_sub["wind_erosion"]["field_widthkm"]= "0.00"
        json_sub["wind_erosion"]["field_lenthkm_fl"]= "0"
        json_sub["wind_erosion"]["angel_of_fieldlength_angl"]= "0.00"

        json_sub["water_erosion"]["usle_p_pec"]= "1.00"
        json_sub["flood_plain"]["flood_plain_frac_ffpq"]= "0.02"
        json_sub["flood_plain"]["fp_ksat_adj_factor_fps1"]= "1.00"

        json_sub["urban"]["urban_frac_urbf"]= "0.00"

        json_sub["reservoir"]["elev_emers_rsee"]= "0"
        json_sub["reservoir"]["res_area_emers_rsae"]= "0.00"
        json_sub["reservoir"]["runoff_emers_rsve"]= "0"
        json_sub["reservoir"]["elev_prins_rsep"]= "0.00"
        json_sub["reservoir"]["res_area_prins_rsap"]= "0"
        json_sub["reservoir"]["runoff_prins_rsvp"]= "0.00"
        json_sub["reservoir"]["ini_res_volume_rsv"]= "0"
        json_sub["reservoir"]["avg_prins_release_rate_rsrr"]="0.00"
        json_sub["reservoir"]["ini_sed_res_rsys"]= "0.00"
        json_sub["reservoir"]["ini_nitro_res_rsyn"]= "0"
        json_sub["reservoir"]["hydro_condt_res_bottom_rshc"]= "0.00"
        json_sub["reservoir"]["time_sedconc_tonormal_rsdp"]= "0"
        json_sub["reservoir"]["bd_sed_res_rsbd"]= "0.00"

        json_sub["pond"]["frac_pond_pcof"]= "0"
        json_sub["pond"]["frac_lagoon_dalg"]= "0.00"
        json_sub["pond"]["lagoon_vol_ratio_vlgn"]= "0.00"
        json_sub["pond"]["wash_water_to_lagoon_coww"]= "0"
        json_sub["pond"]["time_reduce_lgstorage_nom_ddlg"]= "0.00"
        json_sub["pond"]["ratio_liquid_manure_to_lg_solq"]= "0"
        json_sub["pond"]["frac_safety_lg_design_sflg"]= "0.00"

        json_sub["buffer"]["frac_buffer_bcof"]= "0.00"
        json_sub["buffer"]["buffer_flow_len_bffl"]= "0.00"

        json_sub["irrigation"]["regidity_irrig_nirr"]= "0.00"
        json_sub["irrigation"]["irrigation_irr"]= "0"
        json_sub["irrigation"]["min_days_btw_autoirr_iri"]= "0.00"
        json_sub["irrigation"]["waterstress_triger_irr_bir"]= "0"
        json_sub["irrigation"]["irr_lost_runoff_efi"]= "0.00"
        json_sub["irrigation"]["max_annual_irri_vol_vimx"]= "0.00"
        json_sub["irrigation"]["min_single_irrvol_armn"]= "0"
        json_sub["irrigation"]["max_single_irrvol_armx"]= "0.00"
        json_sub["irrigation"]["factor_adj_autoirr_firg"]= "0"
        json_sub["irrigation"]["subareaid_irrwater_irrs"]= "0.00"

        json_sub["point_source"]["point_source_ipts"]= "0.00"

        return json_sub;



    def writefile_sub(self, inf_usrjson, hruidx, hrunolist):
        
        outfn_sub = "SUB%s.SUB" %(hrunolist[hruidx])
        # Write the Site file
        outfid_sub = open(r"%s/%s" %(self.outfd_apexdft, 
                                     outfn_sub), "w")
        # APEXRUN is read with free format in APEX.exe
        # Write line 1:
        outfid_sub.writelines("%8i%8i\n" %(1, 1))
        # Write line 2:
        outfid_sub.writelines(u"%8s%8s%8s%8s%8s%8s%8s%8s%8s%8s%8s%8s\n" %(\
                            inf_usrjson["soil"]["soilid"],\
                            inf_usrjson["management"]["opeartionid_iops"],\
                            inf_usrjson["model_setup"]["owner_id"],\
                            inf_usrjson["grazing"]["feeding_area_ii"],\
                            inf_usrjson["grazing"]["manure_app_area_iapl"],\
                            0.00,\
                            inf_usrjson["model_setup"]["nvcn"],\
                            inf_usrjson["weather"]["daily_wea_stnid_iwth"],\
                            inf_usrjson["point_source"]["point_source_ipts"],\
                            inf_usrjson["model_setup"]["outflow_release_method_isao"],\
                            inf_usrjson["land_use_type"]["land_useid_luns"],\
                            inf_usrjson["management"]["min_days_automow_imw"]\
                            ))
        # Write line 3:
        outfid_sub.writelines(u"%8s%8s%8.2f%8.2f%8s%8s%8s%8s\n" %(\
                            inf_usrjson["weather"]["begin_water_in_snow_sno"],\
                            inf_usrjson["land_use_type"]["standing_crop_residue_stdo"],\
                            float(inf_usrjson["geographic"]["latitude_xct"]),\
                            float(inf_usrjson["geographic"]["longitude_yct"]),\
                            inf_usrjson["wind_erosion"]["azimuth_land_slope_amz"],\
                            inf_usrjson["wind_erosion"]["field_lenthkm_fl"],\
                            inf_usrjson["wind_erosion"]["field_widthkm"],\
                            inf_usrjson["wind_erosion"]["angel_of_fieldlength_angl"]\
                            ))
        # Write line 4
        outfid_sub.writelines(u"%8.2f%8.2f%8.2f%8.2f%8.2f%8.2f%8.2f%8.2f%8.2f%8.2f\n" %(\
                            float(inf_usrjson["geographic"]["wsa_ha"]),\
                            float(inf_usrjson["geographic"]["channellength_chl"]),\
                            float(inf_usrjson["geographic"]["channel_depth_chd"]),\
                            float(inf_usrjson["geographic"]["channelslope_chs"]),\
                            float(inf_usrjson["geographic"]["channelmanningn_chn"]),\
                            float(inf_usrjson["geographic"]["avg_upland_slp"]),\
                            float(inf_usrjson["geographic"]["avg_upland_slplen_splg"]),\
                            float(inf_usrjson["geographic"]["uplandmanningn_upn"]),\
                            float(inf_usrjson["flood_plain"]["flood_plain_frac_ffpq"]),\
                            float(inf_usrjson["urban"]["urban_frac_urbf"])\
                            ))
        # Write Line 5
        outfid_sub.writelines(u"%8.2f%8.2f%8.2f%8.2f%8.2f%8.2f%8.2f%8.2f%8.2f%8.2f%8.2f%8.2f\n" %(\
                            float(inf_usrjson["geographic"]["reach_length_rchl"]),\
                            float(inf_usrjson["geographic"]["reach_depth_rchd"]),\
                            float(inf_usrjson["geographic"]["reach_bottom_width_rcbw"]),\
                            float(inf_usrjson["geographic"]["reach_top_width_rctw"]),\
                            float(inf_usrjson["geographic"]["reach_slope_rchs"]),\
                            float(inf_usrjson["geographic"]["reach_manningsn_rchn"]),\
                            float(inf_usrjson["geographic"]["reach_uslec_rchc"]),\
                            float(inf_usrjson["geographic"]["reach_uslek_rchk"]),\
                            float(inf_usrjson["geographic"]["reach_floodplain_rfpw"]),\
                            float(inf_usrjson["geographic"]["reach_floodplain_length_rfpl"]),\
                            float(inf_usrjson["geographic"]["rch_ksat_adj_factor_sat1"]),\
                            float(inf_usrjson["flood_plain"]["fp_ksat_adj_factor_fps1"])\
                            ))
        # Write Line 6
        outfid_sub.writelines(u"%8.2f%8.2f%8.2f%8.2f%8.2f%8.2f%8.2f%8.2f%8.2f%8.2f\n"%(\
                            float(inf_usrjson["reservoir"]["elev_emers_rsee"]),\
                            float(inf_usrjson["reservoir"]["res_area_emers_rsae"]),\
                            float(inf_usrjson["reservoir"]["runoff_emers_rsve"]),\
                            float(inf_usrjson["reservoir"]["elev_prins_rsep"]),\
                            float(inf_usrjson["reservoir"]["res_area_prins_rsap"]),\
                            float(inf_usrjson["reservoir"]["runoff_prins_rsvp"]),\
                            float(inf_usrjson["reservoir"]["ini_res_volume_rsv"]),\
                            float(inf_usrjson["reservoir"]["avg_prins_release_rate_rsrr"]),\
                            float(inf_usrjson["reservoir"]["ini_sed_res_rsys"]),\
                            float(inf_usrjson["reservoir"]["ini_nitro_res_rsyn"])\
                            ))
        # Write Line 7
        outfid_sub.writelines(u"%8s%8s%8s%8s%8s%8s\n" %(\
                            inf_usrjson["reservoir"]["hydro_condt_res_bottom_rshc"],\
                            inf_usrjson["reservoir"]["time_sedconc_tonormal_rsdp"],\
                            inf_usrjson["reservoir"]["bd_sed_res_rsbd"],\
                            inf_usrjson["pond"]["frac_pond_pcof"],\
                            inf_usrjson["buffer"]["frac_buffer_bcof"],\
                            inf_usrjson["buffer"]["buffer_flow_len_bffl"]\
                            ))
        # Write Line 8
        outfid_sub.writelines(u"%8s%8s%8s%8s%8s%8.1f%8s%8s%8s%8s%8s%8s%8s\n" %(\
                            inf_usrjson["irrigation"]["irrigation_irr"],\
                            inf_usrjson["irrigation"]["min_days_btw_autoirr_iri"],\
                            inf_usrjson["management"]["min_days_autonitro_ifa"],\
                            inf_usrjson["management"]["liming_code_lm"],\
                            inf_usrjson["management"]["furrow_dike_code_ifd"],\
                            float(inf_usrjson["drainage"]["drainage_depth_idr"]),\
                            inf_usrjson["management"]["autofert_lagoon_idf1"],\
                            inf_usrjson["management"]["auto_manure_feedarea_idf2"],\
                            inf_usrjson["management"]["auto_commercial_p_idf3"],\
                            inf_usrjson["management"]["auto_commercial_n_idf4"],\
                            inf_usrjson["management"]["auto_solid_manure_idf5"],\
                            inf_usrjson["management"]["auto_commercial_k_idf6"],\
                            inf_usrjson["irrigation"]["subareaid_irrwater_irrs"]\
                            ))
        # Write Line 9
        outfid_sub.writelines(u"%8s%8s%8s%8s%8s%8s%8s%8s%8s%8s\n" %(\
                            inf_usrjson["irrigation"]["waterstress_triger_irr_bir"],\
                            inf_usrjson["irrigation"]["irr_lost_runoff_efi"],\
                            inf_usrjson["irrigation"]["max_annual_irri_vol_vimx"],\
                            inf_usrjson["irrigation"]["min_single_irrvol_armn"],\
                            inf_usrjson["irrigation"]["max_single_irrvol_armx"],\
                            inf_usrjson["management"]["nstress_trigger_auton_bft"],\
                            inf_usrjson["management"]["auton_rate_fnp4"],\
                            inf_usrjson["management"]["max_annual_auton_fmx"],\
                            inf_usrjson["drainage"]["drain_days_end_w_stress_drt"],\
                            inf_usrjson["management"]["fd_water_store_fdsf"]\
                            )) 
        # Write Line 10
        outfid_sub.writelines(u"%8s%8s%8s%8s%8s%8s%8s%8s%8s%8s\n" %(\
                            inf_usrjson["water_erosion"]["usle_p_pec"],\
                            inf_usrjson["pond"]["frac_lagoon_dalg"],\
                            inf_usrjson["pond"]["lagoon_vol_ratio_vlgn"],\
                            inf_usrjson["pond"]["wash_water_to_lagoon_coww"],\
                            inf_usrjson["pond"]["time_reduce_lgstorage_nom_ddlg"],\
                            inf_usrjson["pond"]["ratio_liquid_manure_to_lg_solq"],\
                            inf_usrjson["pond"]["frac_safety_lg_design_sflg"],\
                            inf_usrjson["grazing"]["feedarea_pile_autosolidmanure_rate_fnp2"],\
                            inf_usrjson["management"]["auton_manure_fnp5"],\
                            inf_usrjson["irrigation"]["factor_adj_autoirr_firg"]\
                            ))                        
        # Write Line 11
        outfid_sub.writelines(u"%8s%8s%8s%8s%8s%8s%8s%8s%8s%8s\n" %(\
                            inf_usrjson["grazing"]["herds_eligible_forgrazing_ny1"],\
                            inf_usrjson["grazing"]["herds_eligible_forgrazing_ny2"],\
                            inf_usrjson["grazing"]["herds_eligible_forgrazing_ny3"],\
                            inf_usrjson["grazing"]["herds_eligible_forgrazing_ny4"],\
                            inf_usrjson["grazing"]["herds_eligible_forgrazing_ny5"],\
                            inf_usrjson["grazing"]["herds_eligible_forgrazing_ny6"],\
                            inf_usrjson["grazing"]["herds_eligible_forgrazing_ny7"],\
                            inf_usrjson["grazing"]["herds_eligible_forgrazing_ny8"],\
                            inf_usrjson["grazing"]["herds_eligible_forgrazing_ny9"],\
                            inf_usrjson["grazing"]["herds_eligible_forgrazing_ny10"]\
                            ))                          
        # Write Line 12
        outfid_sub.writelines(u"%8s%8s%8s%8s%8s%8s%8s%8s%8s%8s\n" %(\
                            inf_usrjson["grazing"]["grazing_limit_herd_xtp1"],\
                            inf_usrjson["grazing"]["grazing_limit_herd_xtp2"],\
                            inf_usrjson["grazing"]["grazing_limit_herd_xtp3"],\
                            inf_usrjson["grazing"]["grazing_limit_herd_xtp4"],\
                            inf_usrjson["grazing"]["grazing_limit_herd_xtp5"],\
                            inf_usrjson["grazing"]["grazing_limit_herd_xtp6"],\
                            inf_usrjson["grazing"]["grazing_limit_herd_xtp7"],\
                            inf_usrjson["grazing"]["grazing_limit_herd_xtp8"],\
                            inf_usrjson["grazing"]["grazing_limit_herd_xtp9"],\
                            inf_usrjson["grazing"]["grazing_limit_herd_xtp10"]\
                            ))                         
                            
                            
                            
        outfid_sub.close()






    #######################################################
    def closerunfiles(self, fid):
        
        fid.writelines("%10s%7i%7i%7i%7i%7i%7i\n" %(\
                    "XXXXXXXXXX", 0, 0, 0, 0, 0, 0\
                    ))
        
        fid.close()





    #######################################################
    def closecomfiles(self, fid):
        
        fid.close()



    def run_apex(self):
        
        os.chdir(os.path.join(parms.infd_apex, parms.dft_apextio))
        
        retcode = subprocess.Popen('APEX1501_64R.exe')
        retcode.wait()


        

        




#######################################################

    
class jsonfiles:
        
    def read_json(self, fn_json):
        
        import json
        import pprint
        
        jsonname = os.path.join(
                        parms.infd_apex, 
                        parms.infd_json, 
                          fn_json)
        
        inf_usrjson = 0
        
        with open(jsonname) as json_file:    
            inf_usrjson = json.loads(json_file.read())
#        pprint.pprint(inf_usrjson)
        json_file.close()
        
        return inf_usrjson

    
    
    
    
