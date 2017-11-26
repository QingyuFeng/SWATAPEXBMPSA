# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 09:50:42 2017

This is developed to convert the
hru information for the SWAT model
to the APEX model.

The parameters required for specifilized
was provided in the one note table.

To convert, I need to do prepare the following
things:
    1. APEX Common database: these files only 
    need one copy and will be stored in one 
    external folder for easy access.
    2. Write the .sub, .sit, .mgt, .sol, .ops,
    for each station.
    3. Prepare a set of wp1, .wnd, and .dly files
    for all subareas. I need to explore how to 
    get the nearest dly station and assign
    it to the specific subarea file.


@author: qyfen
"""

from py01_swathru2apexsub_funcs import *
from py01_swathru2apexsub_parms import parameters
import os
import pprint, shutil


parms = parameters()
fun_json = jsonfiles()
fun_swat = swatfile()
fun_apex = apexfile()



class apexinputs:
    
    # hruid will be the hru gis number
    def __init__(self, hruid):
        
        """This sub file need the source files to 
        get the information, need json to be updated,
        need writer to write new files"""
        
        # After get the json, I need to modify the 
        # values in the json object and use the modified information
        # to write the apex input files. The values 
        # for modifying the jsons will be get from 
        # various hru files. These will be stored in a
        # dictionary.
        
        # This dictionary will all variables except that
        # for management and soil. Management practices has a 
        # lot variables and will be stored in a separate
        # dictionary.
        self.inp_onefield = {}
        self.mgt2ops = {}
        self.sol2sol = {}

        # HRU file for SWAT
        self.inp_onefield = fun_swat.readf_hru(hruid, self.inp_onefield)
        
        # mgt file for SWAT
        self.mgt2ops = fun_swat.readf_mgt(hruid, self.mgt2ops)

        # sol file for SWAT: get the ssurgo number
        self.sol2sol = fun_swat.readf_sol(hruid, self.sol2sol)       

        # wgn file for SWAT
        self.inp_onefield = fun_swat.readf_wgn(hruid, self.inp_onefield)
        
        # wgn file for SWAT
        self.inp_onefield = fun_swat.readf_sub(hruid, self.inp_onefield)
              
        
        self.sitejson = fun_json.read_json(parms.fn_sitejson)
        self.subjson = fun_json.read_json(parms.fn_subjson)
        self.opsjson = fun_json.read_json(parms.fn_opsjson)
        self.soljson = fun_json.read_json(parms.fn_soljson)

        # Then I shall start write these files
        # First modifying the json file and then call the function
        # to write the specific files
        
        # update site json
        self.sitejson = fun_apex.updatejson_sit(self.sitejson, 
                                                hruidx, 
                                                hrunolist, 
                                                self.inp_onefield)

        # update sub json
        self.subjson = fun_apex.updatejson_sub(self.subjson, 
                                                hruidx, 
                                                hrunolist, 
                                                self.inp_onefield,
                                                self.mgt2ops)

        # update soil json
        self.soljson = fun_apex.updatejson_sol(self.soljson, 
                                                hruidx, 
                                                hrunolist, 
                                                self.sol2sol)


        # update management json
        self.opsjson = fun_apex.updatejson_ops(self.opsjson, 
                                                hruidx, 
                                                hrunolist, 
                                                self.mgt2ops)
#        pprint.pprint(self.opsjson)

        
hrunolist = parms.gethrulist()

# While looping through all hrus, there are some files acting
# as a list and these shall be written during the process.
# These files include: 
# APEXRUN.DAT
# SOILCOM.DAT
# OPSCCOM.DAT
# WDLSTCOM.DAT
# SITECOM.DAT
# SUBCOM.DAT
# The monthly wind and weather generator files will be prepared
# separately.




for hruidx in xrange(1,5):#5000,len(hrunolist)):
    
    print(hruidx+1, hrunolist[hruidx])
    apexsub = apexinputs(hrunolist[hruidx])

    fidrun = fun_apex.initrunfiles()
    fidsolcom = fun_apex.initsolcom()
    fidopscom = fun_apex.initopscom()
    fiddlycom = fun_apex.initdlycom()
    fidsitcom = fun_apex.initsitecom()
    fidsubcom = fun_apex.initsubcom()

    fun_apex.write_runlines(fidrun, hruidx, hrunolist)
    fun_apex.writesolcomline(fidsolcom, hruidx, hrunolist)
    fun_apex.writeopscomline(fidopscom, hruidx, hrunolist)
    fun_apex.writedlycomline(fiddlycom, hruidx, hrunolist)
    fun_apex.writesitcomline(fidsitcom, hruidx, hrunolist)
    fun_apex.writesubcomline(fidsubcom, hruidx, hrunolist)
    
    fun_apex.writefile_sit(apexsub.sitejson, hruidx, hrunolist)
    fun_apex.writefile_sub(apexsub.subjson, hruidx, hrunolist)
    fun_apex.writefile_sol(apexsub.soljson, hruidx, hrunolist, apexsub.sol2sol)
    fun_apex.writefile_ops(apexsub.opsjson, hruidx, hrunolist, apexsub.mgt2ops)

    fun_apex.closerunfiles(fidrun)
    fun_apex.closecomfiles(fidsolcom)
    fun_apex.closecomfiles(fidopscom)
    fun_apex.closecomfiles(fiddlycom)
    fun_apex.closecomfiles(fidsitcom)
    fun_apex.closecomfiles(fidsubcom)


    # After generating the input files, call submodule to run the 
    # apex inside this and then copy the output out.
    # After running, delete the output.
    
    #Run APEX
    fun_apex.run_apex()

    fn_awp = "R%s.AWP" %(hrunolist[hruidx])
    fn_msa = "R%s.MSA" %(hrunolist[hruidx])
    fn_mws = "R%s.MWS" %(hrunolist[hruidx])
    fn_out = "R%s.OUT" %(hrunolist[hruidx])
    fn_wss = "R%s.WSS" %(hrunolist[hruidx])
    
    fddes = os.path.join("..",
                         parms.outfd_outputmain,
                         parms.outfd_scenario)
    
    shutil.copy(fn_awp, fddes)
    shutil.copy(fn_msa, fddes)
    shutil.copy(fn_mws, fddes)

    # remove output files after copying.
    os.remove(fn_awp)
    os.remove(fn_msa)
    os.remove(fn_mws)
    os.remove(fn_out)
    os.remove(fn_wss)
    
    # remove generated files
    os.remove("APEXRUN.DAT")   
    os.remove("SOILCOM.DAT") 
    os.remove("OPSCCOM.DAT") 
    os.remove("WDLSTCOM.DAT") 
    os.remove("SITECOM.DAT") 
    os.remove("SUBACOM.DAT") 
    os.remove("OP%s.OPC" %(hrunolist[hruidx]))     
    os.remove("SIT%s.SIT" %(hrunolist[hruidx]))     
    os.remove("SUB%s.SUB" %(hrunolist[hruidx]))     
    os.remove("SOL%s.SOL" %(hrunolist[hruidx]))     

    os.chdir("../../")
    
    # afterrunning, copy output out.
#    outfn = "R%s.AWS"
    