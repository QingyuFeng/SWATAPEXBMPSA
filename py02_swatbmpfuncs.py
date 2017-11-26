# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 09:50:42 2017

This contains all functions for the main program.


@author: qyfen
"""

######################################################
# module import
######################################################

import os
import fortranformat as ff


######################################################
# class defining
######################################################

class SWATUtil(object):
    
    # Reading mgt files
    def mgt_reader(self, hruno, swatinpfd):
        
        fn_mgt = "%s.mgt" %(hruno)
        
        fn = os.path.join(swatinpfd, 
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
        

    ######################################################
    def nutrientmanagement(self, 
                           NUTRIENT4R,
                           opslinesdict,
                           swatfertdict):
        
        from datetime import date, timedelta
        # The process will start with looping throught he management
        # lines.
        for key1, value1 in opslinesdict.iteritems():
            key2s = sorted([k for k, v in opslinesdict[key1].items()])
            # Since there are more than one fertilizer
            # application dates, I will include a number
            # to record the total number and then modify 
            # the dates by adding one day, in order to 
            # facilitate the sorting later.
            # Also, all original P fertilizer application will be
            # deleted.
            # After deleting, the opsline1 might be deleted.
            tmp_pfertln = opslinesdict[key1][key2s[0]].copy()
            # There are two things to do for the modification:
            # 1. delete the current opslines
            # 2. update the keys in the key2s list 
            for kidx in range(len(key2s)):
                if opslinesdict[key1][key2s[kidx]]["mgtop"] == 3:
                    opslinesdict[key1].pop(key2s[kidx], None)
            # After deleting the old P application, add new lines
            # based on the bmp data
            # For nutrient management, the operations are
            # mon, day, HU, mgtop, mgt1, mgt2, 
            # mgt3, mgt4, mgt6, mgt7, mgt8, mgt9
            # mgt1: fert_id
            # mgt4: fert amount
            # mgt5: fert surface

            # There might be several new lines to be added 
            for addidx in range(1, len(NUTRIENT4R.fertamount)):
                # Modify the tmp_pfertln value and add it to the
                # dictionary
                tmp_pfertln["mon"] = NUTRIENT4R.fertappdate[addidx][0]
                tmp_pfertln["day"] = NUTRIENT4R.fertappdate[addidx][1]
                tmp_pfertln["HU"] = 0.0
                tmp_pfertln["mgtop"] = 3
                tmp_pfertln["mgt1"] = NUTRIENT4R.fertid[addidx]
                tmp_pfertln["mgt2"] = 0
                tmp_pfertln["mgt3"] = 0
                tmp_pfertln["mgt4"] = NUTRIENT4R.fertamount[addidx]
                tmp_pfertln["mgt5"] = NUTRIENT4R.fertsurfratio[addidx]
#                tmp_pfertln["mgt6"] = 3
#                tmp_pfertln["mgt7"] = 3
#                tmp_pfertln["mgt8"] = 3
#                tmp_pfertln["mgt9"] = 3
                opslinesdict[key1]["addopsln%i" %(addidx)] = tmp_pfertln



            # The last step is to update the orders of ops by 
            # To do so, I need two lists:
            # One list is used to store the new order with date
            # The other is to store the old order. 
            # This is basically establishing a relationship
            # dict deal with the old and new order. 
            # The new order is sorted by date.
            # Remember, only deal with date and keys.
                
            # using the datetime as the key. Sort
            # datetime, and based on the index of datetime list,
            # assign a new opsline.
            # Get a new key list for looping.
            key22s = [k for k, v in opslinesdict[key1].items()]
            orderdict = {}
            datelist = []
            tmdlt1 = timedelta(days = 1)

            for kidx2 in range(len(key22s)):
                # First get a datetime object.
                # Since we do not have a year, a dummy 2000 
                # was used. 
                # The last line was 17 without dates, the day
                # will be 0. Thus, 
                # it was assigned as Dec 31 as the last day
                structime = 0
                if not opslinesdict[key1][key22s[kidx2]]["day"] == 0:
                    structime = date(2000,
                        opslinesdict[key1][key22s[kidx2]]["mon"],
                        opslinesdict[key1][key22s[kidx2]]["day"])
                    # Update the dates if it already exists in the 
                    # date list
                    while structime in datelist:
                        structime = structime + tmdlt1
                        
                    # Then update the dates in the dictionary
                    opslinesdict[key1][key22s[kidx2]]["mon"]=structime.month
                    opslinesdict[key1][key22s[kidx2]]["day"]=structime.day                  
                    
                else:
                    structime = date(2000, 12, 30)
                
                datelist.append(structime)
                orderdict[structime] = []
                orderdict[structime].append(key22s[kidx2])

            # After getting the order bmp, I will need to 
            # sort the list for date and then assign a new
            # key to the order.
            # For each date in the order dict, the value
            # is a list with idx 0 as old key, and 1 as
            # new key.
            datelist = sorted(datelist)
            
            for dtidx in range(len(datelist)):
                orderdict[datelist[dtidx]].append("nodopsln%i" %(dtidx))
                       
            # Then update the keys of the old dict.
            # This will be done in two steps:
            # dictionary[new_key] = dictionary[old_key]
            # del dictionary[old_key]

            for odkey, odvalue in orderdict.iteritems():
                
                # The 2 step method does not work since
                # the values are the same. The new key
                # need to be updated.
                opslinesdict[key1][odvalue[1]] = opslinesdict[key1][odvalue[0]]
                del opslinesdict[key1][odvalue[0]]
               
        return opslinesdict






    ######################################################
    def addcovercrops(self, COVERCROPS, PARMS):
        
        from datetime import date, timedelta
        # This function add the operation of cover crops on 
        # the current mgt files.
        # The assumption here is that the cover crops were 
        # planted in the winter and harvested and killed in 
        # next spring.
        # Only one cover crops can be planted.
        
        # The same as the one for nutrient management, 
        # the first step is to generate operation lines.
        # There will be three lines for one cover crop:
        # 1. planting
        # 3. kill
        
        # The planting should be later than the last kill
        # The kill should be earlier than the first planting.
        
        cvcplantline = {}

        # For nutrient management, the operations are
        # mon, day, HU, mgtop, mgt1, mgt2, 
        # mgt3, mgt4, mgt6, mgt7, mgt8, mgt9
        # mgt1: plantid
        # mgt3: curyr_mat
        # mgt4: heatunits
        # mgt5: fert LAI Init
        # mgt6: bio_init
        # mgt7: hi_targ
        cvcplantline["mon"] = 10
        cvcplantline["day"] = 27
        cvcplantline["hu"] = 0
        cvcplantline["mgtop"] = 1
        cvcplantline["mgt1"] = COVERCROPS.cvcropplant[1]
        cvcplantline["mgt2"] = 0
        cvcplantline["mgt3"] = 0
        cvcplantline["mgt4"] = 1300
        cvcplantline["mgt5"] = 0
        cvcplantline["mgt6"] = 0
        cvcplantline["mgt7"] = 0
        cvcplantline["mgt8"] = 0
        cvcplantline["mgt9"] = 0
        cvcplantline["mgt10"] = 0

        cvckillline = {}
        # mgtoption 8 will kill and conver all
        # plant into residue
        cvckillline["mon"] = 4
        cvckillline["day"] = 27
        cvckillline["hu"] = 0
        cvckillline["mgtop"] = 8
        cvckillline["mgt1"] = 0
        cvckillline["mgt2"] = 0
        cvckillline["mgt3"] = 0
        cvckillline["mgt4"] = 0
        cvckillline["mgt5"] = 0
        cvckillline["mgt6"] = 0
        cvckillline["mgt7"] = 0
        cvckillline["mgt8"] = 0
        cvckillline["mgt9"] = 0
        cvckillline["mgt10"] = 0

        timedt = timedelta(days = 7)

        # The next step is to insert the two lines and then reorder
        for key1, value1 in PARMS.opslines.iteritems(): 
            
            key2s = sorted([k for k, v in PARMS.opslines[key1].items()])
            structime = 0
            structime = date(2000,
                PARMS.opslines[key1][key2s[0]]["mon"],
                PARMS.opslines[key1][key2s[0]]["day"])

            cvckillline["mon"] = (structime - timedt).month
            cvckillline["day"] = (structime - timedt).day

            structime2 = 0
            structime2 = date(2000,
                PARMS.opslines[key1][key2s[-2]]["mon"],
                PARMS.opslines[key1][key2s[-2]]["day"])
            
            cvcplantline["mon"] = (structime2 + timedt).month
            cvcplantline["day"] = (structime2 + timedt).day

            PARMS.opslines[key1]["cvcplant"] = cvcplantline
            PARMS.opslines[key1]["cvckill"] = cvckillline


            # The last step is to update the orders of ops by 
            # To do so, I need two lists:
            # One list is used to store the new order with date
            # The other is to store the old order. 
            # This is basically establishing a relationship
            # dict deal with the old and new order. 
            # The new order is sorted by date.
            # Remember, only deal with date and keys.
                
            # using the datetime as the key. Sort
            # datetime, and based on the index of datetime list,
            # assign a new opsline.
            # Get a new key list for looping.
            key22s = [k for k, v in PARMS.opslines[key1].items()]
            orderdict = {}
            datelist = []
            tmdlt1 = timedelta(days = 1)
            
            for kidx2 in range(len(key22s)):
                # First get a datetime object.
                # Since we do not have a year, a dummy 2000 
                # was used. 
                # The last line was 17 without dates, the day
                # will be 0. Thus, 
                # it was assigned as Dec 31 as the last day
                structime = 0
                if not PARMS.opslines[key1][key22s[kidx2]]["day"] == 0:
                    structime = date(2000,
                        PARMS.opslines[key1][key22s[kidx2]]["mon"],
                        PARMS.opslines[key1][key22s[kidx2]]["day"])
                    # Update the dates if it already exists in the 
                    # date list
                    while structime in datelist:
                        structime = structime + tmdlt1
                        
                    # Then update the dates in the dictionary
                    PARMS.opslines[key1][key22s[kidx2]]["mon"]=structime.month
                    PARMS.opslines[key1][key22s[kidx2]]["day"]=structime.day                  
                    
                else:
                    structime = date(2000, 12, 30)
                
                datelist.append(structime)
                orderdict[structime] = []
                orderdict[structime].append(key22s[kidx2])

            # After getting the order bmp, I will need to 
            # sort the list for date and then assign a new
            # key to the order.
            # For each date in the order dict, the value
            # is a list with idx 0 as old key, and 1 as
            # new key.
            datelist = sorted(datelist)
            
            for dtidx in range(len(datelist)):
                orderdict[datelist[dtidx]].append("no2dopsln%i" %(dtidx))

            # Then update the keys of the old dict.
            # This will be done in two steps:
            # dictionary[new_key] = dictionary[old_key]
            # del dictionary[old_key]

            for odkey, odvalue in orderdict.iteritems():

                # The 2 step method does not work since
                # the values are the same. The new key
                # need to be updated.
                PARMS.opslines[key1][odvalue[1]] = PARMS.opslines[key1][odvalue[0]]
                del PARMS.opslines[key1][odvalue[0]]            
            
            key22s = [k for k, v in PARMS.opslines[key1].items()]
            
            
            
    ######################################################
    def updatemgt(self, hruno, PARAmeters):
        
        # This function write the dictionary into SWAT files
        fn_mgt = "%s.mgt" %(hruno)
        
        fnfl_mgt = os.path.join(PARAmeters.modifiedmgt, 
                          fn_mgt)     
                
        fid_mgt = open(fnfl_mgt, "w")
        
        for pidx in range(len(PARAmeters.mgtparms)):
            fid_mgt.writelines(PARAmeters.mgtparms["mgtln%i" %(pidx)])
            
        swatopsln = ff.FortranRecordWriter(
        '(1x,A2,1x,A2,1x,A8,1x,A2,1x,A4,1x,A3,1x,A2,1x,A12,1x,A6,1x,A11,1x,A4,1x,A6,1x,A5,A12)')

        for oidx1, ovalue1 in PARAmeters.opslines.iteritems():
            opslkey = sorted([k for k, v in PARAmeters.opslines[oidx1].items()])
            
            for opidx in opslkey:                
                # First, conver the None in the lines into ""
                opskey = [k for k, v in ovalue1[opidx].items()]
                
                if ovalue1[opidx]["mgtop"] == 0 or ovalue1[opidx]["mgtop"] == 17:
                    # all should be ""
                    for opsidx in opskey:
                        if not opsidx == "mgtop":
                            ovalue1[opidx][opsidx] = " "
                else:
                    for opsidx in opskey:
                        if ovalue1[opidx][opsidx] is None:
                            ovalue1[opidx][opsidx] = " "
                
                fid_mgt.writelines(swatopsln.write(
                    [str(ovalue1[opidx]["mon"]),
                    str(ovalue1[opidx]["day"]),
                    str(ovalue1[opidx]["hu"]),
                    str(ovalue1[opidx]["mgtop"]),
                    str(ovalue1[opidx]["mgt1"]),
                    str(ovalue1[opidx]["mgt2"]),
                    str(ovalue1[opidx]["mgt3"]),
                    str(ovalue1[opidx]["mgt4"]),
                    str(ovalue1[opidx]["mgt5"]),
                    str(ovalue1[opidx]["mgt6"]),
                    str(ovalue1[opidx]["mgt7"]),
                    str(ovalue1[opidx]["mgt8"]),
                    str(ovalue1[opidx]["mgt9"]),
                    str(ovalue1[opidx]["mgt10"])])+"\n")

        fid_mgt.close()  



    ######################################################
    # empty ops files to remove all ops
    def empty_opsfile(self, hruno, PARMS):
        
        fn_ops = "%s.ops" %(hruno)  
        
        fn = os.path.join(PARMS.infd_swattxtinout, 
                          fn_ops)
        
        if os.path.isfile(fn):
            os.remove(fn)
            
        fid = open(fn, "w")
        fid.close()
        

#    ######################################################
#    # Reading ops files
#    def opsfile_reader(self, hruno, PARMS):
#        
#        fn_ops = "%s.ops" %(hruno)  
#        
#        fn = os.path.join(PARMS.infd_swattxtinout, 
#                          fn_ops)
#                
#        try:
#            fid = open(fn, "r")
#        except:
#            print("File %s does not exist!" %(fn_ops))
#            return
#        
#        lif = fid.readlines()
#        fid.close()
#        
#        # Reading will have some issue.
#        # I will create a template and then update the values
#        
#        # The mgt lines will be stored in 
#        # json data. It might be updated later.
#        # Dict is easier.
#        ffreader_swatopsln = ff.FortranRecordReader(
#        '(1x,i2,1x,i2,5x,i4,1x,i2,1x,i4,1x,i3,1x,f6.2,1x,f12.5,1x,f6.2,1x,f11.5,1x,f8.2,1x,f6.2,1x,2f5.2)')
#
#        PARMS.bmplinesops = {}
#        
##        PARMS.bmpopsfileheader = lif[0]
#        
#        for bmpidx in range(1):
#
#            bmpkey = "bmp%i" %(bmpidx)
#            PARMS.bmplinesops[bmpkey] = {}
#            tmpl1 = ffreader_swatopsln.read(lif[bmpidx])
#
#            # mon, day, iyear, mgt_op, mgt1i, mgt2i, mgt3,
#            # mgt4, mgt5, mgt6, mgt7, mgt8, mgt9
#            # For filter strip:
#            # filter_i = mgt1i,
#            # filter_ratio = mgt3
#            # filter_con = mgt4
#            # filter_ch = mgt5
#
#            PARMS.bmplinesops[bmpkey]["mon"] = 1
#            PARMS.bmplinesops[bmpkey]["day"] = 1
#            PARMS.bmplinesops[bmpkey]["iyear"] = 1987
#            PARMS.bmplinesops[bmpkey]["mgtop"] = 4
#            PARMS.bmplinesops[bmpkey]["mgt1"] = 1
#            PARMS.bmplinesops[bmpkey]["mgt2"] = 0
#            PARMS.bmplinesops[bmpkey]["mgt3"] = 0
#            PARMS.bmplinesops[bmpkey]["mgt4"] = 0
#            PARMS.bmplinesops[bmpkey]["mgt5"] = 0
#            PARMS.bmplinesops[bmpkey]["mgt6"] = 0
#            PARMS.bmplinesops[bmpkey]["mgt7"] = 0
#            PARMS.bmplinesops[bmpkey]["mgt8"] = 0
#            PARMS.bmplinesops[bmpkey]["mgt9"] = 0
#            

    ######################################################
    # Reading ops files
    def update_opslines(self, hruno, PARMS, FILTERSTRIPS):

        bmpkey = "newbmp1"
        PARMS.bmplinesops[bmpkey] = {}

        # For filter strip:
        # filter_i = mgt1i,
        # filter_ratio = mgt3
        # filter_con = mgt4
        # filter_ch = mgt5
        PARMS.bmplinesops[bmpkey]["mon"] = 1
        PARMS.bmplinesops[bmpkey]["day"] = 1
        PARMS.bmplinesops[bmpkey]["iyear"] = 1987
        PARMS.bmplinesops[bmpkey]["mgtop"] = 4
        PARMS.bmplinesops[bmpkey]["mgt1"] = 1
        PARMS.bmplinesops[bmpkey]["mgt2"] = 0
        PARMS.bmplinesops[bmpkey]["mgt3"] = FILTERSTRIPS.fltstrip[1][0]
        PARMS.bmplinesops[bmpkey]["mgt4"] = FILTERSTRIPS.fltstrip[1][1]
        PARMS.bmplinesops[bmpkey]["mgt5"] = FILTERSTRIPS.fltstrip[1][2]
        PARMS.bmplinesops[bmpkey]["mgt6"] = 0
        PARMS.bmplinesops[bmpkey]["mgt7"] = 0
        PARMS.bmplinesops[bmpkey]["mgt8"] = 0
        PARMS.bmplinesops[bmpkey]["mgt9"] = 0


    ######################################################
    # Reading ops files
    def updateopsfile(self, hruno, PARMS):
        
        # This function write the dictionary into SWAT files
        fn_ops = "%s.ops" %(hruno)
        
        fnfl_ops = os.path.join(PARMS.modifiedops, 
                          fn_ops)     
                
        fid_ops = open(fnfl_ops, "w")
        
        fid_ops.writelines(PARMS.bmpopsfileheader)
            
        ffwriter_swatopsln = ff.FortranRecordWriter(
        '(1x,A2,1x,A2,5x,A4,1x,A2,1x,A4,1x,A3,1x,A6,1x,A12,1x,A6,1x,A11,1x,A8,1x,A6,1x,2A5)')
        
        opidx = "newbmp1"
        fid_ops.writelines(ffwriter_swatopsln.write(
            [str(PARMS.bmplinesops[opidx]["mon"]),
            str(PARMS.bmplinesops[opidx]["day"]),
            str(PARMS.bmplinesops[opidx]["iyear"]),
            str(PARMS.bmplinesops[opidx]["mgtop"]),
            str(PARMS.bmplinesops[opidx]["mgt1"]),
            str(PARMS.bmplinesops[opidx]["mgt2"]),
            str(PARMS.bmplinesops[opidx]["mgt3"]),
            str(PARMS.bmplinesops[opidx]["mgt4"]),
            str(PARMS.bmplinesops[opidx]["mgt5"]),
            str(PARMS.bmplinesops[opidx]["mgt6"]),
            str(PARMS.bmplinesops[opidx]["mgt7"]),
            str(PARMS.bmplinesops[opidx]["mgt8"]),
            str(PARMS.bmplinesops[opidx]["mgt9"])])+"\n")

        fid_ops.close()  








#
#
#    ######################################################
#    def nutrientmanagement(self, NUTRIENT4R, opslinesdict):
#        
#        from datetime import date
#        # The process will start with a temp lines
#        # Then, this temp lines will be insert later
#        # in to the original ops lines.
#        # This nutrient management will related
#        # to mgtop = 11, which is for fertilization.
#        # There might be more than one nutrient, 
#        # for example, each time can only corresponding
#        # to one date, amount, ratio, type, and id.
#        
#        # Another thing is about the rotation and 
#        # existing fertilizer applications. They will
#        # be deleted.
#        nutlinetoadd = {}
#        apptimes = 0
#        
#        for lidx in range(len(NUTRIENT4R.fertappdate)-1):
#            newkey = "opsnewln%i" %(lidx+1)
#            nutlinetoadd[newkey] = {}
#            
#            # For nutrient management, the operations are
#            # mon, day, HU, mgtop, mgt1, mgt2, 
#            # mgt3, mgt4, mgt6, mgt7, mgt8, mgt9
#            # mgt1: fert_id
#            # mgt4: fert amount
#            # mgt5: fert surface
#            nutlinetoadd[newkey]["mon"] = 9
#            nutlinetoadd[newkey]["day"] = 15
#            nutlinetoadd[newkey]["hu"] = 0
#            nutlinetoadd[newkey]["mgtop"] = 3
#            nutlinetoadd[newkey]["mgt1"] = 1
#            nutlinetoadd[newkey]["mgt2"] = 9
#            nutlinetoadd[newkey]["mgt3"] = 0
#            nutlinetoadd[newkey]["mgt4"] = 0
#            nutlinetoadd[newkey]["mgt5"] = 0
#            nutlinetoadd[newkey]["mgt6"] = 0
#            nutlinetoadd[newkey]["mgt7"] = 0
#            nutlinetoadd[newkey]["mgt8"] = 0
#            nutlinetoadd[newkey]["mgt9"] = 0
#            nutlinetoadd[newkey]["mgt10"] = 0
#        # There might be multiple variables to be updated
#        # do it one by one.
#        # Specify date
#        if NUTRIENT4R.fertappdate[0] == 1:
##            # The BMP of application time need to 
##            # be updated, check which option it is
#            for tidx in range(len(NUTRIENT4R.fertappdate[1])):
#                # Then, modify the variable of date
#                nutlinetoadd["opsnewln%i" %(tidx+1)]["mon"
#                             ] = NUTRIENT4R.fertappdate[1][tidx][0]
#                nutlinetoadd["opsnewln%i" %(tidx+1)]["day"
#                             ] = NUTRIENT4R.fertappdate[1][tidx][1]
#        
#        # Specify amount
#        if NUTRIENT4R.fertamount[0] == 1:
##            # The BMP of application time need to 
##            # be updated, check which option it is
#            for tidx in range(len(NUTRIENT4R.fertamount[1])):
#                # Then, modify the variable of date
#                nutlinetoadd["opsnewln%i" %(tidx+1)]["mgt4"
#                             ] = NUTRIENT4R.fertamount[1][tidx]
#
#        # Specify ratio
#        if NUTRIENT4R.fertsurfratio[0] == 1:
##            # The BMP of application time need to 
##            # be updated, check which option it is
#            for tidx in range(len(NUTRIENT4R.fertsurfratio[1])):
#                # Then, modify the variable of date
#                nutlinetoadd["opsnewln%i" %(tidx+1)]["mgt5"
#                             ] = NUTRIENT4R.fertsurfratio[1][tidx]
#        
#        # Specify id
#        if NUTRIENT4R.fertid[0] == 1:
#            # The BMP of application time need to 
#            # be updated, check which option it is
#            for tidx in range(len(NUTRIENT4R.fertid[1])):
#                # Then, modify the variable of date
#                nutlinetoadd["opsnewln%i" %(tidx+1)]["mgt1"
#                             ] = NUTRIENT4R.fertid[1][tidx]
#                
#        # After get the new lines, they will be added to the 
#        # original ops lines.
#        # The original ops lines will be deleted.
#        
#        
#        # Delete the original fertilizer in all years.
#        for key1, value1 in opslinesdict.iteritems():
#            key2s = [k for k, v in opslinesdict[key1].items()]
#            for kidx in key2s:
#                if opslinesdict[key1][kidx]["mgtop"] == 3:
#                    del opslinesdict[key1][kidx]
#
#            # Also add the new lines to each year
#            for nkey, nvalue in nutlinetoadd.iteritems():
#                opslinesdict[key1][nkey] = nvalue
#                
#            # The last step is to update the orders of ops by 
#            # To do so, I need to lists:
#            # One list is used to store the new order with date
#            # The other is to store the old order. 
#            # This is basically establishing a relationship
#            # dict deal with the old and new order. 
#            # The new order is sorted by date.
#            # Remember, only deal with date and keys.
#                
#            # using the datetime as the key. Sort
#            # datetime, and based on the index of datetime list,
#            # assign a new opsline.
#            # Get a new key list for looping.
#            key22s = [k for k, v in opslinesdict[key1].items()]
#            orderdict = {}
#            datelist = []
#                        
#            for kidx2 in range(len(key22s)):
#                
#                # First get a datetime object.
#                # Since we do not have a year, a dummy 2000 
#                # was used. 
#                # The last line was 17 without dates, the day
#                # will be 0. Thus, 
#                # it was assigned as Dec 31 as the last day
#                structime = 0
#                if not opslinesdict[key1][key22s[kidx2]]["day"] == 0:
#                    structime = date(2000,
#                        opslinesdict[key1][key22s[kidx2]]["mon"],
#                        opslinesdict[key1][key22s[kidx2]]["day"])
#                else:
#                    structime = date(2000, 12, 30)
#                
#                datelist.append(structime)
#                orderdict[structime] = []
#                orderdict[structime].append(key22s[kidx2])
#
#            # After getting the order bmp, I will need to 
#            # sort the list for date and then assign a new
#            # key to the order.
#            # For each date in the order dict, the value
#            # is a list with idx 0 as old key, and 1 as
#            # new key.
#            datelist = sorted(datelist)
#            for dtidx in range(len(datelist)):
#                orderdict[datelist[dtidx]].append("nodopsln%i" %(dtidx))
#                    
#            # Then update the keys of the old dict.
#            # This will be done in two steps:
#            # dictionary[new_key] = dictionary[old_key]
#            # del dictionary[old_key]
#
#            for odkey, odvalue in orderdict.iteritems():
#                # The 2 step method does not work since
#                # the values are the same. The new key
#                # need to be updated.
#                opslinesdict[key1][odvalue[1]] = opslinesdict[key1][odvalue[0]]
#                del opslinesdict[key1][odvalue[0]]
#               
#        return opslinesdict
#
#
#
#
#
#
#
#
#
#
#    ######################################################
#    def nutrientmanagement(self, NUTRIENT4R, opslinesdict, swatfertdict):
#        
#        from datetime import date
#        # The process will start with looping throught he management
#        # lines.
#        for key1, value1 in opslinesdict.iteritems():
#            key2s = sorted([k for k, v in opslinesdict[key1].items()])
#            
#            # Since there are more than one fertilizer
#            # application dates, I will include a number
#            # to record the total number and then modify 
#            # the dates by adding one day, in order to 
#            # facilitate the sorting later.
#            no_fertapp = 0
#            for kidx in range(len(key2s)):
#                if opslinesdict[key1][key2s[kidx]]["mgtop"] == 3:
#                    # Start working on the line values                                
#                    # Specify date  
#                    # If date was not specified, check the original,
#                    # if there are two fertilizer application dates
#                    # on exact the same day, modify the following
#                    # to have one more day.
#                    
#                    # If the date was specified, modify the date.
#                    # If there are more than one application date,
#                    # the second was one day more
#                    # First, check whether the fertilizer is P fertilizer:
#                    fertid = str(opslinesdict[key1][key2s[kidx]]["mgt1"])
#                    # swatfert[fertid] = [no, name, n, p, k ...]
#                    # This is testing whether the P content is larger
#                    # than 0. 
#                    if swatfertdict[fertid][3]>0:
#                        # If date is to be updated
#                        if NUTRIENT4R.fertappdate[0] == 1:
#                            # Then, modify the variable of date
#                            opslinesdict[key1][key2s[kidx]]["mon"
#                                        ] = NUTRIENT4R.fertappdate[1][0]
#                            # This means there is only one P application
#                            if no_fertapp == 0:
#                                opslinesdict[key1][key2s[kidx]]["day"
#                                            ] = NUTRIENT4R.fertappdate[1][1]
#                            else:
#                                # There are two application dates
#                                if (opslinesdict[key1][key2s[kidx]]["day"] == 
#                                    opslinesdict[key1][key2s[kidx-1]]["day"]):
#                                    opslinesdict[key1][key2s[kidx]]["day"
#                                         ] = NUTRIENT4R.fertappdate[1][1] + no_fertapp
#                        else:
#                            if no_fertapp > 0:                                
#                                if (opslinesdict[key1][key2s[kidx]]["day"] == 
#                                    opslinesdict[key1][key2s[kidx-1]]["day"]):
#                                    opslinesdict[key1][key2s[kidx]]["day"
#                                     ] = opslinesdict[key1][key2s[kidx]]["day"] + no_fertapp
#                        # For nutrient management, the operations are
#                        # mon, day, HU, mgtop, mgt1, mgt2, 
#                        # mgt3, mgt4, mgt6, mgt7, mgt8, mgt9
#                        # mgt1: fert_id
#                        # mgt4: fert amount
#                        # mgt5: fert surface
#                        # Then, modify the source
#                        if NUTRIENT4R.fertid[0] == 1:
#                            opslinesdict[key1][key2s[kidx]]["mgt1"
#                                    ] = NUTRIENT4R.fertid[1]
#
#                        # Then, modify the amount
#                        if NUTRIENT4R.fertamount[0] == 1:
#                            # If more than one, all P will be applied in the same day.
#                            # The other will be set as 0.
#                            if no_fertapp == 0:
#                                opslinesdict[key1][key2s[kidx]]["mgt4"] = NUTRIENT4R.fertamount[1]
#                            else:
#                                if (opslinesdict[key1][key2s[kidx]]["mgt1"] ==
#                                    opslinesdict[key1][key2s[kidx-1]]["mgt1"]):
#                                    opslinesdict[key1][key2s[kidx]]["mgt4"
#                                            ] = 0
#
#                        # Then, modify the ratio
#                        if NUTRIENT4R.fertsurfratio[0] == 1:
#                            opslinesdict[key1][key2s[kidx]]["mgt5"] = NUTRIENT4R.fertsurfratio[1]
#
#                    no_fertapp = no_fertapp + 1
#
#            # The last step is to update the orders of ops by 
#            # To do so, I need to lists:
#            # One list is used to store the new order with date
#            # The other is to store the old order. 
#            # This is basically establishing a relationship
#            # dict deal with the old and new order. 
#            # The new order is sorted by date.
#            # Remember, only deal with date and keys.
#                
#            # using the datetime as the key. Sort
#            # datetime, and based on the index of datetime list,
#            # assign a new opsline.
#            # Get a new key list for looping.
#            key22s = [k for k, v in opslinesdict[key1].items()]
#            orderdict = {}
#            datelist = []
#                        
#            for kidx2 in range(len(key22s)):
#                
#                # First get a datetime object.
#                # Since we do not have a year, a dummy 2000 
#                # was used. 
#                # The last line was 17 without dates, the day
#                # will be 0. Thus, 
#                # it was assigned as Dec 31 as the last day
#                structime = 0
#                if not opslinesdict[key1][key22s[kidx2]]["day"] == 0:
#                    structime = date(2000,
#                        opslinesdict[key1][key22s[kidx2]]["mon"],
#                        opslinesdict[key1][key22s[kidx2]]["day"])
#                else:
#                    structime = date(2000, 12, 30)
#                
#                datelist.append(structime)
#                orderdict[structime] = []
#                orderdict[structime].append(key22s[kidx2])
#
#            # After getting the order bmp, I will need to 
#            # sort the list for date and then assign a new
#            # key to the order.
#            # For each date in the order dict, the value
#            # is a list with idx 0 as old key, and 1 as
#            # new key.
#            datelist = sorted(datelist)
#            for dtidx in range(len(datelist)):
#                orderdict[datelist[dtidx]].append("nodopsln%i" %(dtidx))
#                    
#            # Then update the keys of the old dict.
#            # This will be done in two steps:
#            # dictionary[new_key] = dictionary[old_key]
#            # del dictionary[old_key]
#
#            for odkey, odvalue in orderdict.iteritems():
#                # The 2 step method does not work since
#                # the values are the same. The new key
#                # need to be updated.
#                opslinesdict[key1][odvalue[1]] = opslinesdict[key1][odvalue[0]]
#                del opslinesdict[key1][odvalue[0]]
#               
#        return opslinesdict
#
#
#
