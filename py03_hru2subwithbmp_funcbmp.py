# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 09:50:42 2017

This contains all functions for the bmp program.


@author: qyfen
"""

import pprint

#######################################################

class BMPFUNCS(object):
    
    def nutrientmanagement(self, 
                           NUTRIENT4R, 
                           opsjson,
                           mgt2ops,
                           fertvalues):
        # The steps of simulating BMPs include:
        # 1. Determine whether the land use is cropland
        # 2. Get the BMP variables
        # 3. Modify corresponding files.
        from datetime import date, timedelta
        # Loop through all operations 
        # Some variables will need to be defined as flags.
        # Crop id for each rotation year
        cropidrotyr = []
                
        # Get the length of ops lengths before inserting
        opslen_old = len(opsjson["jx1_year"])    
        
        # original value of line 2 variables.
        operationid0 = opsjson["operationid"]["operationid0"]
        lun_landuseno0 = opsjson["lun_landuseno"]["lun_landuseno0"]
        iaui_autoirr0 = opsjson["iaui_autoirr"]["iaui_autoirr0"]
        iauf_autofert0 = opsjson["iauf_autofert"]["iauf_autofert0"]
        iamf_automanualdepos0 = opsjson["iamf_automanualdepos"]["iamf_automanualdepos0"]
        ispf_autosolman0 = opsjson["ispf_autosolman"]["ispf_autosolman0"]
        ilqf_atliqman0 = opsjson["ilqf_atliqman"]["ilqf_atliqman0"]
        iaul_atlime0 = opsjson["iaul_atlime"]["iaul_atlime0"]
                
        
        
        
        
        # The first step is to delete all P related operation
        # Loop through the length of each variables
        for opidx in range(opslen_old):
            cropid = opsjson["jx6_cropid"]["jx6_cropid%i" %(opidx)]
            operyr = opsjson["jx1_year"]["jx1_year%i" %(opidx)]
            if not [operyr, cropid] in cropidrotyr:
                cropidrotyr.append([operyr, cropid])
            
            # If the operation is P fertilizer application
            # delete the operation lines.
            if opsjson["jx4_tillid"]["jx4_tillid%i" %(opidx)] == 259:
                # After determining that this is fertilizer, check
                # whether it is P fertilizer
                fertid = opsjson["jx7"]["jx7_%i" %(opidx)]
                # If it is phosphorus fertilizer.
                if float(fertvalues[fertid][3]) > 0:
                    # If it is a phosphorus fertilizer
                    # delete the operation
                    del(opsjson["jx1_year"]["jx1_year%i" %(opidx)])
                    del(opsjson["jx2_month"]["jx2_month%i" %(opidx)])
                    del(opsjson["jx3_day"]["jx3_day%i" %(opidx)])
                    del(opsjson["jx4_tillid"]["jx4_tillid%i" %(opidx)])
                    del(opsjson["jx5_tractid"]["jx5_tractid%i" %(opidx)])
                    del(opsjson["jx6_cropid"]["jx6_cropid%i" %(opidx)])
                    del(opsjson["jx7"]["jx7_%i" %(opidx)])
                    del(opsjson["opv1"]["opv1_%i" %(opidx)])
                    del(opsjson["opv2"]["opv2_%i" %(opidx)])
                    del(opsjson["opv3"]["opv3_%i" %(opidx)])
                    del(opsjson["opv4"]["opv4_%i" %(opidx)])
                    del(opsjson["opv5"]["opv5_%i" %(opidx)])
                    del(opsjson["opv6"]["opv6_%i" %(opidx)])
                    del(opsjson["opv7"]["opv7_%i" %(opidx)])
                    del(opsjson["opv8"]["opv8_%i" %(opidx)])
                    
                    del(opsjson["operationid"]["operationid%i" %(opidx)])
                    del(opsjson["lun_landuseno"]["lun_landuseno%i" %(opidx)])
                    del(opsjson["iaui_autoirr"]["iaui_autoirr%i" %(opidx)])
                    del(opsjson["iauf_autofert"]["iauf_autofert%i" %(opidx)])
                    del(opsjson["iamf_automanualdepos"]["iamf_automanualdepos%i" %(opidx)])
                    del(opsjson["ispf_autosolman"]["ispf_autosolman%i" %(opidx)])
                    del(opsjson["ilqf_atliqman"]["ilqf_atliqman%i" %(opidx)])
                    del(opsjson["iaul_atlime"]["iaul_atlime%i" %(opidx)])
        
        
        
        # After deleting, the p fertilization should be inserted based
        # on the nutrient management inputs. Insert one by one.
        # The insertion should be done year by year.
        for nmidx in range(1, len(NUTRIENT4R.fertamount)):
            for yridx in range(mgt2ops["rotyrs"]):
                opsjson["jx1_year"]["jx1_year%i" %(opslen_old)] = yridx+1
                opsjson["jx2_month"]["jx2_month%i" 
                       %(opslen_old)] = NUTRIENT4R.fertappdate[nmidx][0]
                opsjson["jx3_day"]["jx3_day%i"
                       %(opslen_old)] = NUTRIENT4R.fertappdate[nmidx][1]                
                opsjson["jx4_tillid"]["jx4_tillid%i" %(opslen_old)
                    ] = NUTRIENT4R.fertsurfratio[nmidx]
                opsjson["jx5_tractid"]["jx5_tractid%i" %(opslen_old)] = 615
                
                for cidx in cropidrotyr:
                    if cidx[0] == yridx+1:
                        opsjson["jx6_cropid"]["jx6_cropid%i" %(opslen_old)
                            ] = cidx[1]
                opsjson["jx7"]["jx7_%i" %(opslen_old)
                    ] = NUTRIENT4R.fertid[nmidx]
                opsjson["opv1"]["opv1_%i" %(opslen_old)] = NUTRIENT4R.fertamount[nmidx]
                opsjson["opv2"]["opv2_%i" %(opslen_old)] = 0
                opsjson["opv3"]["opv3_%i" %(opslen_old)] = 0
                opsjson["opv4"]["opv4_%i" %(opslen_old)] = 0
                opsjson["opv5"]["opv5_%i" %(opslen_old)] = 0
                opsjson["opv6"]["opv6_%i" %(opslen_old)] = 0
                opsjson["opv7"]["opv7_%i" %(opslen_old)] = 0
                opsjson["opv8"]["opv8_%i" %(opslen_old)] = 0

                opsjson["operationid"]["operationid%i" %(opslen_old)] = operationid0
                opsjson["lun_landuseno"]["lun_landuseno%i" %(opslen_old)] = lun_landuseno0
                opsjson["iaui_autoirr"]["iaui_autoirr%i" %(opslen_old)] = iaui_autoirr0
                opsjson["iauf_autofert"]["iauf_autofert%i" %(opslen_old)] = iauf_autofert0
                opsjson["iamf_automanualdepos"]["iamf_automanualdepos%i"
                       %(opslen_old)] = iamf_automanualdepos0
                opsjson["ispf_autosolman"]["ispf_autosolman%i" %(opslen_old)] = ispf_autosolman0
                opsjson["ilqf_atliqman"]["ilqf_atliqman%i" %(opslen_old)] = ilqf_atliqman0
                opsjson["iaul_atlime"]["iaul_atlime%i" %(opslen_old)] = iaul_atlime0

                opslen_old = opslen_old + 1


        """
        After modifying, it should be reordered for ordering later.
        If there is no fertilizer application, I need to add lines
        Add a variable to record the length of current ops lines
        """
        # Reorder the operation orders by dates
        jx1_year_dict = {}
        jx2_month_dict = {}
        jx3_day_dict = {}
        jx4_tillid_dict = {}
        jx5_tractid_dict = {}
        jx6_cropid_dict = {}
        jx7_dict = {}
        opv1_dict = {}
        opv2_dict = {}
        opv3_dict = {}
        opv4_dict = {}
        opv5_dict = {}
        opv6_dict = {}
        opv7_dict = {}
        opv8_dict = {}
        
        operationid_dict = {}
        lun_landuseno_dict = {}
        iaui_autoirr_dict = {}
        iauf_autofert_dict = {}
        iamf_automanualdepos_dict = {}
        ispf_autosolman_dict = {}
        ilqf_atliqman_dict = {}
        iaul_atlime_dict = {}        
  
        datelist = []
        
        structime = 0
        tmdlt1 = timedelta(days = 1)
        
        # Loop through the length of each variables
        # The keys for each first level are not in sequence now, 
        # but they have the same number, I will use this for the append.
        opskeys = [yrk for yrk, yrv in opsjson["jx1_year"].iteritems()]
        for opdidx in opskeys:           
            # First get a datetime object.
            # Since we do not have a year, a dummy 2000 
            # was used. 
            # The last line was 17 without dates, the day
            # will be 0. Thus, 
            # it was assigned as Dec 31 as the last day
            structime = date(2000+int(opsjson["jx1_year"][opdidx]),
                                    opsjson["jx2_month"]["jx2_month%s" %(opdidx[8:])],
                                    opsjson["jx3_day"]["jx3_day%s" %(opdidx[8:])])
            
            while structime in datelist:
                structime = structime + tmdlt1
                
            opsjson["jx2_month"]["jx2_month%s" %(opdidx[8:])] = structime.month
            opsjson["jx3_day"]["jx3_day%s" %(opdidx[8:])] = structime.day

            datelist.append(structime)
            
            jx1_year_dict[structime] = []
            jx1_year_dict[structime].append(opdidx)
            
            jx2_month_dict[structime] = []
            jx2_month_dict[structime].append("jx2_month%s" %(opdidx[8:]))
            
            jx3_day_dict[structime] = []
            jx3_day_dict[structime].append("jx3_day%s" %(opdidx[8:]))
            
            jx4_tillid_dict[structime] = []
            jx4_tillid_dict[structime].append("jx4_tillid%s" %(opdidx[8:]))
            
            jx5_tractid_dict[structime] = []
            jx5_tractid_dict[structime].append("jx5_tractid%s" %(opdidx[8:]))
            
            jx6_cropid_dict[structime] = []
            jx6_cropid_dict[structime].append("jx6_cropid%s" %(opdidx[8:]))
            
            jx7_dict[structime] = []
            jx7_dict[structime].append("jx7_%s" %(opdidx[8:]))
            
            opv1_dict[structime] = []
            opv1_dict[structime].append("opv1_%s" %(opdidx[8:]))
            
            opv2_dict[structime] = []
            opv2_dict[structime].append("opv2_%s" %(opdidx[8:]))
            
            opv3_dict[structime] = []
            opv3_dict[structime].append("opv3_%s" %(opdidx[8:]))
            
            opv4_dict[structime] = []
            opv4_dict[structime].append("opv4_%s" %(opdidx[8:]))
            
            opv5_dict[structime] = []
            opv5_dict[structime].append("opv5_%s" %(opdidx[8:]))
            
            opv6_dict[structime] = []
            opv6_dict[structime].append("opv6_%s" %(opdidx[8:]))
            
            opv7_dict[structime] = []
            opv7_dict[structime].append("opv7_%s" %(opdidx[8:]))
            
            opv8_dict[structime] = []
            opv8_dict[structime].append("opv8_%s" %(opdidx[8:]))
            
            
            operationid_dict[structime] = []
            operationid_dict[structime].append("operationid%s" %(opdidx[8:]))
            
            lun_landuseno_dict[structime] = []
            lun_landuseno_dict[structime].append("lun_landuseno%s" %(opdidx[8:]))
            
            iaui_autoirr_dict[structime] = []
            iaui_autoirr_dict[structime].append("iaui_autoirr%s" %(opdidx[8:]))
            
            iauf_autofert_dict[structime] = []
            iauf_autofert_dict[structime].append("iauf_autofert%s" %(opdidx[8:]))
            
            iamf_automanualdepos_dict[structime] = []
            iamf_automanualdepos_dict[structime].append("iamf_automanualdepos%s" %(opdidx[8:]))
            
            ispf_autosolman_dict[structime] = []
            ispf_autosolman_dict[structime].append("ispf_autosolman%s" %(opdidx[8:]))
            
            ilqf_atliqman_dict[structime] = []
            ilqf_atliqman_dict[structime].append("ilqf_atliqman%s" %(opdidx[8:]))
            
            iaul_atlime_dict[structime] = []
            iaul_atlime_dict[structime].append("iaul_atlime%s" %(opdidx[8:]))


        datelist = sorted(datelist)
        
#        keytest = [kk for kk, vv in opsjson.iteritems()]
#        for kid in keytest:
#            print(kid, len(opsjson[kid]))

        for dtidx in range(len(datelist)):
            
            # I will append two keys 
            jx1_year_dict[datelist[dtidx]].append("njx1_year%i" %(dtidx))
            jx1_year_dict[datelist[dtidx]].append("jx1_year%i" %(dtidx))

            jx2_month_dict[datelist[dtidx]].append("njx2_month%i" %(dtidx))
            jx2_month_dict[datelist[dtidx]].append("jx2_month%i" %(dtidx))
            
            jx3_day_dict[datelist[dtidx]].append("njx3_day%i" %(dtidx))
            jx3_day_dict[datelist[dtidx]].append("jx3_day%i" %(dtidx))
            
            jx4_tillid_dict[datelist[dtidx]].append("njx4_tillid%i" %(dtidx))
            jx4_tillid_dict[datelist[dtidx]].append("jx4_tillid%i" %(dtidx))
            
            jx5_tractid_dict[datelist[dtidx]].append("njx5_tractid%i" %(dtidx))
            jx5_tractid_dict[datelist[dtidx]].append("jx5_tractid%i" %(dtidx))
            
            jx6_cropid_dict[datelist[dtidx]].append("njx6_cropid%i" %(dtidx))
            jx6_cropid_dict[datelist[dtidx]].append("jx6_cropid%i" %(dtidx))
            
            jx7_dict[datelist[dtidx]].append("njx7_%i" %(dtidx))
            jx7_dict[datelist[dtidx]].append("jx7_%i" %(dtidx))
            
            opv1_dict[datelist[dtidx]].append("nopv1_%i" %(dtidx))
            opv1_dict[datelist[dtidx]].append("opv1_%i" %(dtidx))
            
            opv2_dict[datelist[dtidx]].append("nopv2_%i" %(dtidx))
            opv2_dict[datelist[dtidx]].append("opv2_%i" %(dtidx))
            
            opv3_dict[datelist[dtidx]].append("nopv3_%i" %(dtidx))
            opv3_dict[datelist[dtidx]].append("opv3_%i" %(dtidx))
            
            opv4_dict[datelist[dtidx]].append("nopv4_%i" %(dtidx))
            opv4_dict[datelist[dtidx]].append("opv4_%i" %(dtidx))
            
            opv5_dict[datelist[dtidx]].append("nopv5_%i" %(dtidx))
            opv5_dict[datelist[dtidx]].append("opv5_%i" %(dtidx))
            
            opv6_dict[datelist[dtidx]].append("nopv6_%i" %(dtidx))
            opv6_dict[datelist[dtidx]].append("opv6_%i" %(dtidx))
            
            opv7_dict[datelist[dtidx]].append("nopv7_%i" %(dtidx))
            opv7_dict[datelist[dtidx]].append("opv7_%i" %(dtidx))
            
            opv8_dict[datelist[dtidx]].append("nopv8_%i" %(dtidx))
            opv8_dict[datelist[dtidx]].append("opv8_%i" %(dtidx))
       
        
            operationid_dict[datelist[dtidx]].append("noperationid%i" %(dtidx))
            operationid_dict[datelist[dtidx]].append("operationid%i" %(dtidx))
            
            lun_landuseno_dict[datelist[dtidx]].append("nlun_landuseno%i" %(dtidx))
            lun_landuseno_dict[datelist[dtidx]].append("lun_landuseno%i" %(dtidx))
            
            iaui_autoirr_dict[datelist[dtidx]].append("niaui_autoirr%i" %(dtidx))
            iaui_autoirr_dict[datelist[dtidx]].append("iaui_autoirr%i" %(dtidx))
            
            iauf_autofert_dict[datelist[dtidx]].append("niauf_autofert%i" %(dtidx))
            iauf_autofert_dict[datelist[dtidx]].append("iauf_autofert%i" %(dtidx))
            
            iamf_automanualdepos_dict[datelist[dtidx]].append("niamf_automanualdepos%i" %(dtidx))
            iamf_automanualdepos_dict[datelist[dtidx]].append("iamf_automanualdepos%i" %(dtidx))
            
            ispf_autosolman_dict[datelist[dtidx]].append("nispf_autosolman%i" %(dtidx))
            ispf_autosolman_dict[datelist[dtidx]].append("ispf_autosolman%i" %(dtidx))
            
            ilqf_atliqman_dict[datelist[dtidx]].append("nilqf_atliqman%i" %(dtidx))
            ilqf_atliqman_dict[datelist[dtidx]].append("ilqf_atliqman%i" %(dtidx))
            
            iaul_atlime_dict[datelist[dtidx]].append("niaul_atlime%i" %(dtidx))
            iaul_atlime_dict[datelist[dtidx]].append("iaul_atlime%i" %(dtidx))

        
        for dtidx1 in range(len(datelist)):
            # I wil append two keys datelist[dtidx]
            oldkey = jx1_year_dict[datelist[dtidx1]][0]
            newkey = jx1_year_dict[datelist[dtidx1]][1]
            opsjson["jx1_year"][newkey] = opsjson["jx1_year"][oldkey]
            del(opsjson["jx1_year"][oldkey])

            oldkey = jx2_month_dict[datelist[dtidx1]][0]
            newkey = jx2_month_dict[datelist[dtidx1]][1]
            opsjson["jx2_month"][newkey] = opsjson["jx2_month"][oldkey]
            del(opsjson["jx2_month"][oldkey])

            oldkey = jx3_day_dict[datelist[dtidx1]][0]
            newkey = jx3_day_dict[datelist[dtidx1]][1]
            opsjson["jx3_day"][newkey] = opsjson["jx3_day"][oldkey]
            del(opsjson["jx3_day"][oldkey])

            oldkey = jx4_tillid_dict[datelist[dtidx1]][0]
            newkey = jx4_tillid_dict[datelist[dtidx1]][1]
            opsjson["jx4_tillid"][newkey] = opsjson["jx4_tillid"][oldkey]
            del(opsjson["jx4_tillid"][oldkey])

            oldkey = jx5_tractid_dict[datelist[dtidx1]][0]
            newkey = jx5_tractid_dict[datelist[dtidx1]][1]
            opsjson["jx5_tractid"][newkey] = opsjson["jx5_tractid"][oldkey]
            del(opsjson["jx5_tractid"][oldkey])

            oldkey = jx6_cropid_dict[datelist[dtidx1]][0]
            newkey = jx6_cropid_dict[datelist[dtidx1]][1]
            opsjson["jx6_cropid"][newkey] = opsjson["jx6_cropid"][oldkey]
            del(opsjson["jx6_cropid"][oldkey])

            oldkey = jx7_dict[datelist[dtidx1]][0]
            newkey = jx7_dict[datelist[dtidx1]][1]
            opsjson["jx7"][newkey] = opsjson["jx7"][oldkey]
            del(opsjson["jx7"][oldkey])

            oldkey = opv1_dict[datelist[dtidx1]][0]
            newkey = opv1_dict[datelist[dtidx1]][1]
            opsjson["opv1"][newkey] = opsjson["opv1"][oldkey]
            del(opsjson["opv1"][oldkey])

            oldkey = opv2_dict[datelist[dtidx1]][0]
            newkey = opv2_dict[datelist[dtidx1]][1]
            opsjson["opv2"][newkey] = opsjson["opv2"][oldkey]
            del(opsjson["opv2"][oldkey])

            oldkey = opv3_dict[datelist[dtidx1]][0]
            newkey = opv3_dict[datelist[dtidx1]][1]
            opsjson["opv3"][newkey] = opsjson["opv3"][oldkey]
            del(opsjson["opv3"][oldkey])

            oldkey = opv4_dict[datelist[dtidx1]][0]
            newkey = opv4_dict[datelist[dtidx1]][1]
            opsjson["opv4"][newkey] = opsjson["opv4"][oldkey]
            del(opsjson["opv4"][oldkey])

            oldkey = opv5_dict[datelist[dtidx1]][0]
            newkey = opv5_dict[datelist[dtidx1]][1]
            opsjson["opv5"][newkey] = opsjson["opv5"][oldkey]
            del(opsjson["opv5"][oldkey])

            oldkey = opv6_dict[datelist[dtidx1]][0]
            newkey = opv6_dict[datelist[dtidx1]][1]
            opsjson["opv6"][newkey] = opsjson["opv6"][oldkey]
            del(opsjson["opv6"][oldkey])

            oldkey = opv7_dict[datelist[dtidx1]][0]
            newkey = opv7_dict[datelist[dtidx1]][1]
            opsjson["opv7"][newkey] = opsjson["opv7"][oldkey]
            del(opsjson["opv7"][oldkey])

            oldkey = opv8_dict[datelist[dtidx1]][0]
            newkey = opv8_dict[datelist[dtidx1]][1]
            opsjson["opv8"][newkey] = opsjson["opv8"][oldkey]
            del(opsjson["opv8"][oldkey])



            oldkey = operationid_dict[datelist[dtidx1]][0]
            newkey = operationid_dict[datelist[dtidx1]][1]
            opsjson["operationid"][newkey] = opsjson["operationid"][oldkey]
            del(opsjson["operationid"][oldkey])

            oldkey = lun_landuseno_dict[datelist[dtidx1]][0]
            newkey = lun_landuseno_dict[datelist[dtidx1]][1]
            opsjson["lun_landuseno"][newkey] = opsjson["lun_landuseno"][oldkey]
            del(opsjson["lun_landuseno"][oldkey])

            oldkey = iaui_autoirr_dict[datelist[dtidx1]][0]
            newkey = iaui_autoirr_dict[datelist[dtidx1]][1]
            opsjson["iaui_autoirr"][newkey] = opsjson["iaui_autoirr"][oldkey]
            del(opsjson["iaui_autoirr"][oldkey])

            oldkey = iauf_autofert_dict[datelist[dtidx1]][0]
            newkey = iauf_autofert_dict[datelist[dtidx1]][1]
            opsjson["iauf_autofert"][newkey] = opsjson["iauf_autofert"][oldkey]
            del(opsjson["iauf_autofert"][oldkey])

            oldkey = iamf_automanualdepos_dict[datelist[dtidx1]][0]
            newkey = iamf_automanualdepos_dict[datelist[dtidx1]][1]
            opsjson["iamf_automanualdepos"][newkey] = opsjson["iamf_automanualdepos"][oldkey]
            del(opsjson["iamf_automanualdepos"][oldkey])

            oldkey = ispf_autosolman_dict[datelist[dtidx1]][0]
            newkey = ispf_autosolman_dict[datelist[dtidx1]][1]
            opsjson["ispf_autosolman"][newkey] = opsjson["ispf_autosolman"][oldkey]
            del(opsjson["ispf_autosolman"][oldkey])

            oldkey = ilqf_atliqman_dict[datelist[dtidx1]][0]
            newkey = ilqf_atliqman_dict[datelist[dtidx1]][1]
            opsjson["ilqf_atliqman"][newkey] = opsjson["ilqf_atliqman"][oldkey]
            del(opsjson["ilqf_atliqman"][oldkey])

            oldkey = iaul_atlime_dict[datelist[dtidx1]][0]
            newkey = iaul_atlime_dict[datelist[dtidx1]][1]
            opsjson["iaul_atlime"][newkey] = opsjson["iaul_atlime"][oldkey]
            del(opsjson["iaul_atlime"][oldkey])
        
   
        
        
        
        for dtidx2 in range(len(datelist)):
            # I wil append two keys datelist[dtidx]
            oldkey = jx1_year_dict[datelist[dtidx2]][1]
            newkey = jx1_year_dict[datelist[dtidx2]][2]
            opsjson["jx1_year"][newkey] = opsjson["jx1_year"][oldkey]
            del(opsjson["jx1_year"][oldkey])

            oldkey = jx2_month_dict[datelist[dtidx2]][1]
            newkey = jx2_month_dict[datelist[dtidx2]][2]
            opsjson["jx2_month"][newkey] = opsjson["jx2_month"][oldkey]
            del(opsjson["jx2_month"][oldkey])

            oldkey = jx3_day_dict[datelist[dtidx2]][1]
            newkey = jx3_day_dict[datelist[dtidx2]][2]
            opsjson["jx3_day"][newkey] = opsjson["jx3_day"][oldkey]
            del(opsjson["jx3_day"][oldkey])

            oldkey = jx4_tillid_dict[datelist[dtidx2]][1]
            newkey = jx4_tillid_dict[datelist[dtidx2]][2]
            opsjson["jx4_tillid"][newkey] = opsjson["jx4_tillid"][oldkey]
            del(opsjson["jx4_tillid"][oldkey])

            oldkey = jx5_tractid_dict[datelist[dtidx2]][1]
            newkey = jx5_tractid_dict[datelist[dtidx2]][2]
            opsjson["jx5_tractid"][newkey] = opsjson["jx5_tractid"][oldkey]
            del(opsjson["jx5_tractid"][oldkey])

            oldkey = jx6_cropid_dict[datelist[dtidx2]][1]
            newkey = jx6_cropid_dict[datelist[dtidx2]][2]
            opsjson["jx6_cropid"][newkey] = opsjson["jx6_cropid"][oldkey]
            del(opsjson["jx6_cropid"][oldkey])

            oldkey = jx7_dict[datelist[dtidx2]][1]
            newkey = jx7_dict[datelist[dtidx2]][2]
            opsjson["jx7"][newkey] = opsjson["jx7"][oldkey]
            del(opsjson["jx7"][oldkey])

            oldkey = opv1_dict[datelist[dtidx2]][1]
            newkey = opv1_dict[datelist[dtidx2]][2]
            opsjson["opv1"][newkey] = opsjson["opv1"][oldkey]
            del(opsjson["opv1"][oldkey])

            oldkey = opv2_dict[datelist[dtidx2]][1]
            newkey = opv2_dict[datelist[dtidx2]][2]
            opsjson["opv2"][newkey] = opsjson["opv2"][oldkey]
            del(opsjson["opv2"][oldkey])

            oldkey = opv3_dict[datelist[dtidx2]][1]
            newkey = opv3_dict[datelist[dtidx2]][2]
            opsjson["opv3"][newkey] = opsjson["opv3"][oldkey]
            del(opsjson["opv3"][oldkey])

            oldkey = opv4_dict[datelist[dtidx2]][1]
            newkey = opv4_dict[datelist[dtidx2]][2]
            opsjson["opv4"][newkey] = opsjson["opv4"][oldkey]
            del(opsjson["opv4"][oldkey])

            oldkey = opv5_dict[datelist[dtidx2]][1]
            newkey = opv5_dict[datelist[dtidx2]][2]
            opsjson["opv5"][newkey] = opsjson["opv5"][oldkey]
            del(opsjson["opv5"][oldkey])

            oldkey = opv6_dict[datelist[dtidx2]][1]
            newkey = opv6_dict[datelist[dtidx2]][2]
            opsjson["opv6"][newkey] = opsjson["opv6"][oldkey]
            del(opsjson["opv6"][oldkey])

            oldkey = opv7_dict[datelist[dtidx2]][1]
            newkey = opv7_dict[datelist[dtidx2]][2]
            opsjson["opv7"][newkey] = opsjson["opv7"][oldkey]
            del(opsjson["opv7"][oldkey])

            oldkey = opv8_dict[datelist[dtidx2]][1]
            newkey = opv8_dict[datelist[dtidx2]][2]
            opsjson["opv8"][newkey] = opsjson["opv8"][oldkey]
            del(opsjson["opv8"][oldkey])


            oldkey = operationid_dict[datelist[dtidx2]][1]
            newkey = operationid_dict[datelist[dtidx2]][2]
            opsjson["operationid"][newkey] = opsjson["operationid"][oldkey]
            del(opsjson["operationid"][oldkey])

            oldkey = lun_landuseno_dict[datelist[dtidx2]][1]
            newkey = lun_landuseno_dict[datelist[dtidx2]][2]
            opsjson["lun_landuseno"][newkey] = opsjson["lun_landuseno"][oldkey]
            del(opsjson["lun_landuseno"][oldkey])

            oldkey = iaui_autoirr_dict[datelist[dtidx2]][1]
            newkey = iaui_autoirr_dict[datelist[dtidx2]][2]
            opsjson["iaui_autoirr"][newkey] = opsjson["iaui_autoirr"][oldkey]
            del(opsjson["iaui_autoirr"][oldkey])

            oldkey = iauf_autofert_dict[datelist[dtidx2]][1]
            newkey = iauf_autofert_dict[datelist[dtidx2]][2]
            opsjson["iauf_autofert"][newkey] = opsjson["iauf_autofert"][oldkey]
            del(opsjson["iauf_autofert"][oldkey])

            oldkey = iamf_automanualdepos_dict[datelist[dtidx2]][1]
            newkey = iamf_automanualdepos_dict[datelist[dtidx2]][2]
            opsjson["iamf_automanualdepos"][newkey] = opsjson["iamf_automanualdepos"][oldkey]
            del(opsjson["iamf_automanualdepos"][oldkey])

            oldkey = ispf_autosolman_dict[datelist[dtidx2]][1]
            newkey = ispf_autosolman_dict[datelist[dtidx2]][2]
            opsjson["ispf_autosolman"][newkey] = opsjson["ispf_autosolman"][oldkey]
            del(opsjson["ispf_autosolman"][oldkey])

            oldkey = ilqf_atliqman_dict[datelist[dtidx2]][1]
            newkey = ilqf_atliqman_dict[datelist[dtidx2]][2]
            opsjson["ilqf_atliqman"][newkey] = opsjson["ilqf_atliqman"][oldkey]
            del(opsjson["ilqf_atliqman"][oldkey])

            oldkey = iaul_atlime_dict[datelist[dtidx2]][1]
            newkey = iaul_atlime_dict[datelist[dtidx2]][2]
            opsjson["iaul_atlime"][newkey] = opsjson["iaul_atlime"][oldkey]
            del(opsjson["iaul_atlime"][oldkey])

        return opsjson
        
    
    def addcovercrops(self, 
                       COVERCROPS, 
                       opsjson,
                       mgt2ops
                       ):
        
        # This requires only adding two lines on the management files
        # To do this, I first need to identify the planting date and 
        # harvest dates of the current operations
        from datetime import date, timedelta
        # Loop through all operations 
        # Some variables will need to be defined as flags.

        # Loop through the length of each variables
        # In order to get the cover crop planting date, I need to 
        # get the current dates for planting and kill.
        datelist = {}

        opsyrkeys = [key for key, val in opsjson["jx1_year"].iteritems()]
        
        for yridx1 in range(mgt2ops["rotyrs"]):
            templine = []
            for opyridx in opsyrkeys:
            # jx4_tillid == 451 for kill
            # planting is different, varies with different.
            # Thus, I will continue use the first and last of the 
            # date for planting and kill of cover crops.
            # This ops has been sorted by dates. So the order is good.
                structime = 0
                if opsjson["jx1_year"][opyridx] == yridx1+1:
                    structime = date(2000+int(opsjson["jx1_year"][opyridx]),
                        opsjson["jx2_month"]["jx2_month%s" %(opyridx[8:])],
                        opsjson["jx3_day"]["jx3_day%s" %(opyridx[8:])])
                    templine.append(structime)
            datelist["yr%i" %(yridx1)] = templine  
        
        # This datelist is used to get the minimum date and maximum date
        # of the operation for the normal crop production.
        killtd = timedelta(days=COVERCROPS.cvcropkilldatetd[1])
        # Add cover crop kill date
        opslineno = len(opsyrkeys)
        for yridx in range(mgt2ops["rotyrs"]):
            yrdtlst = datelist["yr%i" %(yridx)]*1
            killdate = min(yrdtlst)

            # in each year add two lines, one for kill and one for
            # planting
            opsjson["jx1_year"]["jx1_year%i" %(opslineno+yridx)] = yridx+1
            opsjson["jx2_month"]["jx2_month%i" 
                   %(opslineno+yridx)] = (killdate-killtd).month
            opsjson["jx3_day"]["jx3_day%i"
                   %(opslineno+yridx)] = (killdate-killtd).day          
            opsjson["jx4_tillid"]["jx4_tillid%i" %(opslineno+yridx)] = 451
            opsjson["jx5_tractid"]["jx5_tractid%i" %(opslineno+yridx)] = 0
            opsjson["jx6_cropid"]["jx6_cropid%i" 
                   %(opslineno+yridx)] = COVERCROPS.cvcropplant[1]
            opsjson["jx7"]["jx7_%i" %(opslineno+yridx)] = 0
            opsjson["opv1"]["opv1_%i" 
                   %(opslineno+yridx)] = 0
            opsjson["opv2"]["opv2_%i" %(opslineno+yridx)] = 0
            opsjson["opv3"]["opv3_%i" %(opslineno+yridx)] = 0
            opsjson["opv4"]["opv4_%i" %(opslineno+yridx)] = 0
            opsjson["opv5"]["opv5_%i" %(opslineno+yridx)] = 0
            opsjson["opv6"]["opv6_%i" %(opslineno+yridx)] = 0
            opsjson["opv7"]["opv7_%i" %(opslineno+yridx)] = 0
            opsjson["opv8"]["opv8_%i" %(opslineno+yridx)] = 0
        
        # Adding plant operation
        opsyrkeys = [key for key, val in opsjson["jx1_year"].iteritems()]
        planttd = timedelta(days=COVERCROPS.cvcropplantdatetd[1])
        opslineno = len(opsyrkeys)
        for yridx3 in range(mgt2ops["rotyrs"]):
            # in each year add two lines, one for kill and one for
            # planting
            yrdtlst = datelist["yr%i" %(yridx3)]*1   
            plantdate = max(yrdtlst)
            opsjson["jx1_year"]["jx1_year%i" %(opslineno+yridx3)] = yridx3+1
            opsjson["jx2_month"]["jx2_month%i" 
                   %(opslineno+yridx3)] = (plantdate+planttd).month
            opsjson["jx3_day"]["jx3_day%i"
                   %(opslineno+yridx3)] = (plantdate+planttd).day  
            opsjson["jx4_tillid"]["jx4_tillid%i" %(opslineno+yridx3)] = 139
            opsjson["jx5_tractid"]["jx5_tractid%i" %(opslineno+yridx3)] = 24
            opsjson["jx6_cropid"]["jx6_cropid%i" 
                   %(opslineno+yridx3)] = COVERCROPS.cvcropplant[1]
            opsjson["jx7"]["jx7_%i" %(opslineno+yridx3)] = 0
            opsjson["opv1"]["opv1_%i" 
                   %(opslineno+yridx3)] = 1300
            opsjson["opv2"]["opv2_%i" %(opslineno+yridx3)] = 0
            opsjson["opv3"]["opv3_%i" %(opslineno+yridx3)] = 0
            opsjson["opv4"]["opv4_%i" %(opslineno+yridx3)] = 0
            opsjson["opv5"]["opv5_%i" %(opslineno+yridx3)] = 0
            opsjson["opv6"]["opv6_%i" %(opslineno+yridx3)] = 0
            opsjson["opv7"]["opv7_%i" %(opslineno+yridx3)] = 0
            opsjson["opv8"]["opv8_%i" %(opslineno+yridx3)] = 0

        # Reorder the operation orders by dates
        jx1_year_dict = {}
        jx2_month_dict = {}
        jx3_day_dict = {}
        jx4_tillid_dict = {}
        jx5_tractid_dict = {}
        jx6_cropid_dict = {}
        jx7_dict = {}
        opv1_dict = {}
        opv2_dict = {}
        opv3_dict = {}
        opv4_dict = {}
        opv5_dict = {}
        opv6_dict = {}
        opv7_dict = {}
        opv8_dict = {}
        
        datelist = []
        
        structime = 0
        
        # Loop through the length of each variables
        for opdidx in range(len(opsjson["jx1_year"])):
            # First get a datetime object.
            # Since we do not have a year, a dummy 2000 
            # was used. 
            # The last line was 17 without dates, the day
            # will be 0. Thus, 
            # it was assigned as Dec 31 as the last day
            structime = date(2000+int(opsjson["jx1_year"]["jx1_year%i" %(opdidx)]),
                opsjson["jx2_month"]["jx2_month%i" %(opdidx)],
                opsjson["jx3_day"]["jx3_day%i" %(opdidx)])
            
            if structime in datelist:
                opsjson["jx3_day"]["jx3_day%i" %(
                        opdidx)] = int(opsjson["jx3_day"][
                        "jx3_day%i" %(opdidx)]) + 1
                        
            structime = date(2000+int(opsjson["jx1_year"]["jx1_year%i" %(opdidx)]),
                opsjson["jx2_month"]["jx2_month%i" %(opdidx)],
                opsjson["jx3_day"]["jx3_day%i" %(opdidx)])
            
            datelist.append(structime)
            
            jx1_year_dict[structime] = []
            jx1_year_dict[structime].append("jx1_year%i" %(opdidx))
            
            jx2_month_dict[structime] = []
            jx2_month_dict[structime].append("jx2_month%i" %(opdidx))
            
            jx3_day_dict[structime] = []
            jx3_day_dict[structime].append("jx3_day%i" %(opdidx))
            
            jx4_tillid_dict[structime] = []
            jx4_tillid_dict[structime].append("jx4_tillid%i" %(opdidx))
            
            jx5_tractid_dict[structime] = []
            jx5_tractid_dict[structime].append("jx5_tractid%i" %(opdidx))
            
            jx6_cropid_dict[structime] = []
            jx6_cropid_dict[structime].append("jx6_cropid%i" %(opdidx))
            
            jx7_dict[structime] = []
            jx7_dict[structime].append("jx7_%i" %(opdidx))
            
            opv1_dict[structime] = []
            opv1_dict[structime].append("opv1_%i" %(opdidx))
            
            opv2_dict[structime] = []
            opv2_dict[structime].append("opv2_%i" %(opdidx))
            
            opv3_dict[structime] = []
            opv3_dict[structime].append("opv3_%i" %(opdidx))
            
            opv4_dict[structime] = []
            opv4_dict[structime].append("opv4_%i" %(opdidx))
            
            opv5_dict[structime] = []
            opv5_dict[structime].append("opv5_%i" %(opdidx))
            
            opv6_dict[structime] = []
            opv6_dict[structime].append("opv6_%i" %(opdidx))
            
            opv7_dict[structime] = []
            opv7_dict[structime].append("opv7_%i" %(opdidx))
            
            opv8_dict[structime] = []
            opv8_dict[structime].append("opv8_%i" %(opdidx))

        datelist = sorted(datelist)
        
        for dtidx in range(len(datelist)):
            # I will append two keys 
            jx1_year_dict[datelist[dtidx]].append("njx1_year%i" %(dtidx))
            jx1_year_dict[datelist[dtidx]].append("jx1_year%i" %(dtidx))

            jx2_month_dict[datelist[dtidx]].append("njx2_month%i" %(dtidx))
            jx2_month_dict[datelist[dtidx]].append("jx2_month%i" %(dtidx))
            
            jx3_day_dict[datelist[dtidx]].append("njx3_day%i" %(dtidx))
            jx3_day_dict[datelist[dtidx]].append("jx3_day%i" %(dtidx))
            
            jx4_tillid_dict[datelist[dtidx]].append("njx4_tillid%i" %(dtidx))
            jx4_tillid_dict[datelist[dtidx]].append("jx4_tillid%i" %(dtidx))
            
            jx5_tractid_dict[datelist[dtidx]].append("njx5_tractid%i" %(dtidx))
            jx5_tractid_dict[datelist[dtidx]].append("jx5_tractid%i" %(dtidx))
            
            jx6_cropid_dict[datelist[dtidx]].append("njx6_cropid%i" %(dtidx))
            jx6_cropid_dict[datelist[dtidx]].append("jx6_cropid%i" %(dtidx))
            
            jx7_dict[datelist[dtidx]].append("njx7_%i" %(dtidx))
            jx7_dict[datelist[dtidx]].append("jx7_%i" %(dtidx))
            
            opv1_dict[datelist[dtidx]].append("nopv1_%i" %(dtidx))
            opv1_dict[datelist[dtidx]].append("opv1_%i" %(dtidx))
            
            opv2_dict[datelist[dtidx]].append("nopv2_%i" %(dtidx))
            opv2_dict[datelist[dtidx]].append("opv2_%i" %(dtidx))
            
            opv3_dict[datelist[dtidx]].append("nopv3_%i" %(dtidx))
            opv3_dict[datelist[dtidx]].append("opv3_%i" %(dtidx))
            
            opv4_dict[datelist[dtidx]].append("nopv4_%i" %(dtidx))
            opv4_dict[datelist[dtidx]].append("opv4_%i" %(dtidx))
            
            opv5_dict[datelist[dtidx]].append("nopv5_%i" %(dtidx))
            opv5_dict[datelist[dtidx]].append("opv5_%i" %(dtidx))
            
            opv6_dict[datelist[dtidx]].append("nopv6_%i" %(dtidx))
            opv6_dict[datelist[dtidx]].append("opv6_%i" %(dtidx))
            
            opv7_dict[datelist[dtidx]].append("nopv7_%i" %(dtidx))
            opv7_dict[datelist[dtidx]].append("opv7_%i" %(dtidx))
            
            opv8_dict[datelist[dtidx]].append("nopv8_%i" %(dtidx))
            opv8_dict[datelist[dtidx]].append("opv8_%i" %(dtidx))
       
        
        for dtidx1 in range(len(datelist)):
            # I wil append two keys datelist[dtidx]
            
            oldkey = jx1_year_dict[datelist[dtidx1]][0]
            newkey = jx1_year_dict[datelist[dtidx1]][1]
            opsjson["jx1_year"][newkey] = opsjson["jx1_year"][oldkey]
            del(opsjson["jx1_year"][oldkey])

            oldkey = jx2_month_dict[datelist[dtidx1]][0]
            newkey = jx2_month_dict[datelist[dtidx1]][1]
            opsjson["jx2_month"][newkey] = opsjson["jx2_month"][oldkey]
            del(opsjson["jx2_month"][oldkey])

            oldkey = jx3_day_dict[datelist[dtidx1]][0]
            newkey = jx3_day_dict[datelist[dtidx1]][1]
            opsjson["jx3_day"][newkey] = opsjson["jx3_day"][oldkey]
            del(opsjson["jx3_day"][oldkey])

            oldkey = jx4_tillid_dict[datelist[dtidx1]][0]
            newkey = jx4_tillid_dict[datelist[dtidx1]][1]
            opsjson["jx4_tillid"][newkey] = opsjson["jx4_tillid"][oldkey]
            del(opsjson["jx4_tillid"][oldkey])

            oldkey = jx5_tractid_dict[datelist[dtidx1]][0]
            newkey = jx5_tractid_dict[datelist[dtidx1]][1]
            opsjson["jx5_tractid"][newkey] = opsjson["jx5_tractid"][oldkey]
            del(opsjson["jx5_tractid"][oldkey])

            oldkey = jx6_cropid_dict[datelist[dtidx1]][0]
            newkey = jx6_cropid_dict[datelist[dtidx1]][1]
            opsjson["jx6_cropid"][newkey] = opsjson["jx6_cropid"][oldkey]
            del(opsjson["jx6_cropid"][oldkey])

            oldkey = jx7_dict[datelist[dtidx1]][0]
            newkey = jx7_dict[datelist[dtidx1]][1]
            opsjson["jx7"][newkey] = opsjson["jx7"][oldkey]
            del(opsjson["jx7"][oldkey])

            oldkey = opv1_dict[datelist[dtidx1]][0]
            newkey = opv1_dict[datelist[dtidx1]][1]
            opsjson["opv1"][newkey] = opsjson["opv1"][oldkey]
            del(opsjson["opv1"][oldkey])

            oldkey = opv2_dict[datelist[dtidx1]][0]
            newkey = opv2_dict[datelist[dtidx1]][1]
            opsjson["opv2"][newkey] = opsjson["opv2"][oldkey]
            del(opsjson["opv2"][oldkey])

            oldkey = opv3_dict[datelist[dtidx1]][0]
            newkey = opv3_dict[datelist[dtidx1]][1]
            opsjson["opv3"][newkey] = opsjson["opv3"][oldkey]
            del(opsjson["opv3"][oldkey])

            oldkey = opv4_dict[datelist[dtidx1]][0]
            newkey = opv4_dict[datelist[dtidx1]][1]
            opsjson["opv4"][newkey] = opsjson["opv4"][oldkey]
            del(opsjson["opv4"][oldkey])

            oldkey = opv5_dict[datelist[dtidx1]][0]
            newkey = opv5_dict[datelist[dtidx1]][1]
            opsjson["opv5"][newkey] = opsjson["opv5"][oldkey]
            del(opsjson["opv5"][oldkey])

            oldkey = opv6_dict[datelist[dtidx1]][0]
            newkey = opv6_dict[datelist[dtidx1]][1]
            opsjson["opv6"][newkey] = opsjson["opv6"][oldkey]
            del(opsjson["opv6"][oldkey])

            oldkey = opv7_dict[datelist[dtidx1]][0]
            newkey = opv7_dict[datelist[dtidx1]][1]
            opsjson["opv7"][newkey] = opsjson["opv7"][oldkey]
            del(opsjson["opv7"][oldkey])

            oldkey = opv8_dict[datelist[dtidx1]][0]
            newkey = opv8_dict[datelist[dtidx1]][1]
            opsjson["opv8"][newkey] = opsjson["opv8"][oldkey]
            del(opsjson["opv8"][oldkey])


        
        for dtidx2 in range(len(datelist)):
            # I wil append two keys datelist[dtidx]
            oldkey = jx1_year_dict[datelist[dtidx2]][1]
            newkey = jx1_year_dict[datelist[dtidx2]][2]
            opsjson["jx1_year"][newkey] = opsjson["jx1_year"][oldkey]
            del(opsjson["jx1_year"][oldkey])

            oldkey = jx2_month_dict[datelist[dtidx2]][1]
            newkey = jx2_month_dict[datelist[dtidx2]][2]
            opsjson["jx2_month"][newkey] = opsjson["jx2_month"][oldkey]
            del(opsjson["jx2_month"][oldkey])

            oldkey = jx3_day_dict[datelist[dtidx2]][1]
            newkey = jx3_day_dict[datelist[dtidx2]][2]
            opsjson["jx3_day"][newkey] = opsjson["jx3_day"][oldkey]
            del(opsjson["jx3_day"][oldkey])

            oldkey = jx4_tillid_dict[datelist[dtidx2]][1]
            newkey = jx4_tillid_dict[datelist[dtidx2]][2]
            opsjson["jx4_tillid"][newkey] = opsjson["jx4_tillid"][oldkey]
            del(opsjson["jx4_tillid"][oldkey])

            oldkey = jx5_tractid_dict[datelist[dtidx2]][1]
            newkey = jx5_tractid_dict[datelist[dtidx2]][2]
            opsjson["jx5_tractid"][newkey] = opsjson["jx5_tractid"][oldkey]
            del(opsjson["jx5_tractid"][oldkey])

            oldkey = jx6_cropid_dict[datelist[dtidx2]][1]
            newkey = jx6_cropid_dict[datelist[dtidx2]][2]
            opsjson["jx6_cropid"][newkey] = opsjson["jx6_cropid"][oldkey]
            del(opsjson["jx6_cropid"][oldkey])

            oldkey = jx7_dict[datelist[dtidx2]][1]
            newkey = jx7_dict[datelist[dtidx2]][2]
            opsjson["jx7"][newkey] = opsjson["jx7"][oldkey]
            del(opsjson["jx7"][oldkey])

            oldkey = opv1_dict[datelist[dtidx2]][1]
            newkey = opv1_dict[datelist[dtidx2]][2]
            opsjson["opv1"][newkey] = opsjson["opv1"][oldkey]
            del(opsjson["opv1"][oldkey])

            oldkey = opv2_dict[datelist[dtidx2]][1]
            newkey = opv2_dict[datelist[dtidx2]][2]
            opsjson["opv2"][newkey] = opsjson["opv2"][oldkey]
            del(opsjson["opv2"][oldkey])

            oldkey = opv3_dict[datelist[dtidx2]][1]
            newkey = opv3_dict[datelist[dtidx2]][2]
            opsjson["opv3"][newkey] = opsjson["opv3"][oldkey]
            del(opsjson["opv3"][oldkey])

            oldkey = opv4_dict[datelist[dtidx2]][1]
            newkey = opv4_dict[datelist[dtidx2]][2]
            opsjson["opv4"][newkey] = opsjson["opv4"][oldkey]
            del(opsjson["opv4"][oldkey])

            oldkey = opv5_dict[datelist[dtidx2]][1]
            newkey = opv5_dict[datelist[dtidx2]][2]
            opsjson["opv5"][newkey] = opsjson["opv5"][oldkey]
            del(opsjson["opv5"][oldkey])

            oldkey = opv6_dict[datelist[dtidx2]][1]
            newkey = opv6_dict[datelist[dtidx2]][2]
            opsjson["opv6"][newkey] = opsjson["opv6"][oldkey]
            del(opsjson["opv6"][oldkey])

            oldkey = opv7_dict[datelist[dtidx2]][1]
            newkey = opv7_dict[datelist[dtidx2]][2]
            opsjson["opv7"][newkey] = opsjson["opv7"][oldkey]
            del(opsjson["opv7"][oldkey])

            oldkey = opv8_dict[datelist[dtidx2]][1]
            newkey = opv8_dict[datelist[dtidx2]][2]
            opsjson["opv8"][newkey] = opsjson["opv8"][oldkey]
            del(opsjson["opv8"][oldkey])


        return opsjson


    def addfilterstrip(self, 
                       FILTERSTRIPS, 
                       json_sub):
            
        # The operation of adding a filter strip includes
        # simulating the filter strip as a separate watershed
        # So, first, I will add another subarea
        json_sub["subarea2"]={}
        json_sub["subarea2"]["model_setup"]={}
        json_sub["subarea2"]["model_setup"]["subid_snum"]= json_sub["subarea1"]["model_setup"]["subid_snum"]
        json_sub["subarea2"]["model_setup"]["description_title"]=json_sub["subarea1"]["model_setup"]["description_title"]
        json_sub["subarea2"]["model_setup"]["owner_id"]=json_sub["subarea1"]["model_setup"]["owner_id"]
        json_sub["subarea2"]["model_setup"]["nvcn"]=json_sub["subarea1"]["model_setup"]["nvcn"]
        json_sub["subarea2"]["model_setup"]["outflow_release_method_isao"]=json_sub["subarea1"]["model_setup"]["outflow_release_method_isao"]
        
        json_sub["subarea2"]["geographic"]={}
        json_sub["subarea2"]["geographic"]["wsa_ha"]=json_sub["subarea1"]["geographic"]["wsa_ha"]
        json_sub["subarea2"]["geographic"]["latitude_xct"]=json_sub["subarea1"]["geographic"]["latitude_xct"]
        json_sub["subarea2"]["geographic"]["longitude_yct"]=json_sub["subarea1"]["geographic"]["longitude_yct"]
        json_sub["subarea2"]["geographic"]["avg_upland_slplen_splg"]=json_sub["subarea1"]["geographic"]["avg_upland_slplen_splg"]
        json_sub["subarea2"]["geographic"]["avg_upland_slp"]=json_sub["subarea1"]["geographic"]["avg_upland_slp"]
        json_sub["subarea2"]["geographic"]["uplandmanningn_upn"]=json_sub["subarea1"]["geographic"]["uplandmanningn_upn"]

        json_sub["subarea2"]["geographic"]["channellength_chl"]=json_sub["subarea1"]["geographic"]["channellength_chl"]
        json_sub["subarea2"]["geographic"]["channelslope_chs"]=json_sub["subarea1"]["geographic"]["channelslope_chs"]
        # For agricultural land, I will use excavated or dredged, and
        # not maintained. 
        json_sub["subarea2"]["geographic"]["channelmanningn_chn"]=json_sub["subarea1"]["geographic"]["channelmanningn_chn"]
        json_sub["subarea2"]["geographic"]["channel_depth_chd"]=json_sub["subarea1"]["geographic"]["channel_depth_chd"]
        # Reach is between where channel starts or enters the subarea
        # and leaves the subarea. For extreme or field simulation here,
        # we use same value as chl.
        json_sub["subarea2"]["geographic"]["reach_length_rchl"]=json_sub["subarea1"]["geographic"]["reach_length_rchl"]
        json_sub["subarea2"]["geographic"]["reach_depth_rchd"]=json_sub["subarea1"]["geographic"]["reach_depth_rchd"]
        json_sub["subarea2"]["geographic"]["reach_bottom_width_rcbw"]=json_sub["subarea1"]["geographic"]["reach_bottom_width_rcbw"]
        json_sub["subarea2"]["geographic"]["reach_top_width_rctw"] =json_sub["subarea1"]["geographic"]["reach_top_width_rctw"]
        json_sub["subarea2"]["geographic"]["reach_slope_rchs"]=json_sub["subarea1"]["geographic"]["reach_slope_rchs"]
        json_sub["subarea2"]["geographic"]["reach_manningsn_rchn"]=json_sub["subarea1"]["geographic"]["reach_manningsn_rchn"]
        json_sub["subarea2"]["geographic"]["reach_uslec_rchc"]=json_sub["subarea1"]["geographic"]["reach_uslec_rchc"]
        json_sub["subarea2"]["geographic"]["reach_uslek_rchk"] =json_sub["subarea1"]["geographic"]["reach_uslek_rchk"]
        json_sub["subarea2"]["geographic"]["reach_floodplain_rfpw"]=json_sub["subarea1"]["geographic"]["reach_floodplain_rfpw"]
        json_sub["subarea2"]["geographic"]["reach_floodplain_length_rfpl"]=json_sub["subarea1"]["geographic"]["reach_floodplain_length_rfpl"]
        json_sub["subarea2"]["geographic"]["rch_ksat_adj_factor_sat1"]=json_sub["subarea1"]["geographic"]["rch_ksat_adj_factor_sat1"]

        # This will override that value specified in the ops file.
        # In other words, if I have different values for different tillage, the 
        # values will be modified to this value. If it is set to zero,
        # LUN will not be modified.
        json_sub["subarea2"]["land_use_type"]={}
        json_sub["subarea2"]["land_use_type"]["land_useid_luns"]=json_sub["subarea1"]["land_use_type"]["land_useid_luns"]
        json_sub["subarea2"]["land_use_type"]["standing_crop_residue_stdo"]=json_sub["subarea1"]["land_use_type"]["standing_crop_residue_stdo"]

        json_sub["subarea2"]["soil"]={}
        json_sub["subarea2"]["soil"]["soilid"]=json_sub["subarea1"]["soil"]["soilid"]

        json_sub["subarea2"]["management"]={}
        json_sub["subarea2"]["management"]["opeartionid_iops"]=int(json_sub["subarea1"]["management"]["opeartionid_iops"])+1
        json_sub["subarea2"]["management"]["min_days_automow_imw"]=json_sub["subarea1"]["management"]["min_days_automow_imw"]
        json_sub["subarea2"]["management"]["min_days_autonitro_ifa"]=json_sub["subarea1"]["management"]["min_days_autonitro_ifa"]
        json_sub["subarea2"]["management"]["liming_code_lm"]=json_sub["subarea1"]["management"]["liming_code_lm"]
        json_sub["subarea2"]["management"]["furrow_dike_code_ifd"]=json_sub["subarea1"]["management"]["furrow_dike_code_ifd"]
        json_sub["subarea2"]["management"]["fd_water_store_fdsf"]=json_sub["subarea1"]["management"]["fd_water_store_fdsf"]
        json_sub["subarea2"]["management"]["autofert_lagoon_idf1"]=json_sub["subarea1"]["management"]["autofert_lagoon_idf1"]
        json_sub["subarea2"]["management"]["auto_manure_feedarea_idf2"]=json_sub["subarea1"]["management"]["auto_manure_feedarea_idf2"]
        json_sub["subarea2"]["management"]["auto_commercial_p_idf3"]=json_sub["subarea1"]["management"]["auto_commercial_p_idf3"]
        json_sub["subarea2"]["management"]["auto_commercial_n_idf4"]=json_sub["subarea1"]["management"]["auto_commercial_n_idf4"]
        json_sub["subarea2"]["management"]["auto_solid_manure_idf5"]=json_sub["subarea1"]["management"]["auto_solid_manure_idf5"]
        json_sub["subarea2"]["management"]["auto_commercial_k_idf6"]= json_sub["subarea1"]["management"]["auto_commercial_k_idf6"]
        json_sub["subarea2"]["management"]["nstress_trigger_auton_bft"]=json_sub["subarea1"]["management"]["nstress_trigger_auton_bft"]
        json_sub["subarea2"]["management"]["auton_rate_fnp4"]=json_sub["subarea1"]["management"]["auton_rate_fnp4"]
        json_sub["subarea2"]["management"]["auton_manure_fnp5"]=json_sub["subarea1"]["management"]["auton_manure_fnp5"]
        json_sub["subarea2"]["management"]["max_annual_auton_fmx"]= json_sub["subarea1"]["management"]["max_annual_auton_fmx"]

        json_sub["subarea2"]["drainage"]={}
        json_sub["subarea2"]["drainage"]["drainage_depth_idr"]=json_sub["subarea1"]["drainage"]["drainage_depth_idr"]
        json_sub["subarea2"]["drainage"]["drain_days_end_w_stress_drt"]=json_sub["subarea1"]["drainage"]["drain_days_end_w_stress_drt"]

        json_sub["subarea2"]["grazing"]={}
        json_sub["subarea2"]["grazing"]["feeding_area_ii"]= "1"
        json_sub["subarea2"]["grazing"]["manure_app_area_iapl"]= "0.00"
        json_sub["subarea2"]["grazing"]["feedarea_pile_autosolidmanure_rate_fnp2"]= "0.00"
        json_sub["subarea2"]["grazing"]["herds_eligible_forgrazing_ny1"]= "1"
        json_sub["subarea2"]["grazing"]["herds_eligible_forgrazing_ny2"]= "0.00"
        json_sub["subarea2"]["grazing"]["herds_eligible_forgrazing_ny3"]= "0.010"
        json_sub["subarea2"]["grazing"]["herds_eligible_forgrazing_ny4"]= "0.00"
        json_sub["subarea2"]["grazing"]["herds_eligible_forgrazing_ny5"]= "0.00"
        json_sub["subarea2"]["grazing"]["herds_eligible_forgrazing_ny6"]= "0.00"
        json_sub["subarea2"]["grazing"]["herds_eligible_forgrazing_ny7"]= "0.00"
        json_sub["subarea2"]["grazing"]["herds_eligible_forgrazing_ny8"]= "0.00"
        json_sub["subarea2"]["grazing"]["herds_eligible_forgrazing_ny9"]= "0.00"
        json_sub["subarea2"]["grazing"]["herds_eligible_forgrazing_ny10"]= "0.00"
        json_sub["subarea2"]["grazing"]["grazing_limit_herd_xtp1"]= "1"
        json_sub["subarea2"]["grazing"]["grazing_limit_herd_xtp2"]= "0.00"
        json_sub["subarea2"]["grazing"]["grazing_limit_herd_xtp3"]= "0.010"
        json_sub["subarea2"]["grazing"]["grazing_limit_herd_xtp4"]= "0.00"
        json_sub["subarea2"]["grazing"]["grazing_limit_herd_xtp5"]= "0.00"
        json_sub["subarea2"]["grazing"]["grazing_limit_herd_xtp6"]= "0.00"
        json_sub["subarea2"]["grazing"]["grazing_limit_herd_xtp7"]= "0.00"
        json_sub["subarea2"]["grazing"]["grazing_limit_herd_xtp8"]= "0.00"
        json_sub["subarea2"]["grazing"]["grazing_limit_herd_xtp9"]= "0.00"
        json_sub["subarea2"]["grazing"]["grazing_limit_herd_xtp10"]= "0.00"

        json_sub["subarea2"]["weather"]={}
        json_sub["subarea2"]["weather"]["daily_wea_stnid_iwth"]=json_sub["subarea1"]["weather"]["daily_wea_stnid_iwth"]
        json_sub["subarea2"]["weather"]["begin_water_in_snow_sno"]= "0.00"

        json_sub["subarea2"]["wind_erosion"]={}
        json_sub["subarea2"]["wind_erosion"]["azimuth_land_slope_amz"]= "0"
        json_sub["subarea2"]["wind_erosion"]["field_widthkm"]= "0.00"
        json_sub["subarea2"]["wind_erosion"]["field_lenthkm_fl"]= "0"
        json_sub["subarea2"]["wind_erosion"]["angel_of_fieldlength_angl"]= "0.00"

        json_sub["subarea2"]["water_erosion"]={}
        json_sub["subarea2"]["water_erosion"]["usle_p_pec"]= "1.00"
        
        json_sub["subarea2"]["flood_plain"]={}
        json_sub["subarea2"]["flood_plain"]["flood_plain_frac_ffpq"]= "0.02"
        json_sub["subarea2"]["flood_plain"]["fp_ksat_adj_factor_fps1"]= "1.00"

        json_sub["subarea2"]["urban"]={}
        json_sub["subarea2"]["urban"]["urban_frac_urbf"]= "0.00"

        json_sub["subarea2"]["reservoir"]={}
        json_sub["subarea2"]["reservoir"]["elev_emers_rsee"]= "0"
        json_sub["subarea2"]["reservoir"]["res_area_emers_rsae"]= "0.00"
        json_sub["subarea2"]["reservoir"]["runoff_emers_rsve"]= "0"
        json_sub["subarea2"]["reservoir"]["elev_prins_rsep"]= "0.00"
        json_sub["subarea2"]["reservoir"]["res_area_prins_rsap"]= "0"
        json_sub["subarea2"]["reservoir"]["runoff_prins_rsvp"]= "0.00"
        json_sub["subarea2"]["reservoir"]["ini_res_volume_rsv"]= "0"
        json_sub["subarea2"]["reservoir"]["avg_prins_release_rate_rsrr"]="0.00"
        json_sub["subarea2"]["reservoir"]["ini_sed_res_rsys"]= "0.00"
        json_sub["subarea2"]["reservoir"]["ini_nitro_res_rsyn"]= "0"
        json_sub["subarea2"]["reservoir"]["hydro_condt_res_bottom_rshc"]= "0.00"
        json_sub["subarea2"]["reservoir"]["time_sedconc_tonormal_rsdp"]= "0"
        json_sub["subarea2"]["reservoir"]["bd_sed_res_rsbd"]= "0.00"

        json_sub["subarea2"]["pond"]={}
        json_sub["subarea2"]["pond"]["frac_pond_pcof"]= "0"
        json_sub["subarea2"]["pond"]["frac_lagoon_dalg"]= "0.00"
        json_sub["subarea2"]["pond"]["lagoon_vol_ratio_vlgn"]= "0.00"
        json_sub["subarea2"]["pond"]["wash_water_to_lagoon_coww"]= "0"
        json_sub["subarea2"]["pond"]["time_reduce_lgstorage_nom_ddlg"]= "0.00"
        json_sub["subarea2"]["pond"]["ratio_liquid_manure_to_lg_solq"]= "0"
        json_sub["subarea2"]["pond"]["frac_safety_lg_design_sflg"]= "0.00"

        json_sub["subarea2"]["buffer"]={}
        json_sub["subarea2"]["buffer"]["frac_buffer_bcof"]= "0.00"
        json_sub["subarea2"]["buffer"]["buffer_flow_len_bffl"]= "0.00"

        json_sub["subarea2"]["irrigation"]={}
        json_sub["subarea2"]["irrigation"]["regidity_irrig_nirr"]= "0.00"
        json_sub["subarea2"]["irrigation"]["irrigation_irr"]= "0"
        json_sub["subarea2"]["irrigation"]["min_days_btw_autoirr_iri"]= "0.00"
        json_sub["subarea2"]["irrigation"]["waterstress_triger_irr_bir"]= "0"
        json_sub["subarea2"]["irrigation"]["irr_lost_runoff_efi"]= "0.00"
        json_sub["subarea2"]["irrigation"]["max_annual_irri_vol_vimx"]= "0.00"
        json_sub["subarea2"]["irrigation"]["min_single_irrvol_armn"]= "0"
        json_sub["subarea2"]["irrigation"]["max_single_irrvol_armx"]= "0.00"
        json_sub["subarea2"]["irrigation"]["factor_adj_autoirr_firg"]= "0"
        json_sub["subarea2"]["irrigation"]["subareaid_irrwater_irrs"]= "0.00"

        json_sub["subarea2"]["point_source"]={}
        json_sub["subarea2"]["point_source"]["point_source_ipts"]= "0.00"

        # Then Updating the corresponding variables as required
        # by the manual
        json_sub["subarea2"]["water_erosion"]["usle_p_pec"]= FILTERSTRIPS.FS_PEC
        uplandslope = json_sub["subarea2"]["geographic"]["avg_upland_slp"]
        json_sub["subarea2"]["geographic"]["avg_upland_slp"
            ]= FILTERSTRIPS.FS_SLPfactor*float(uplandslope)
        json_sub["subarea2"]["geographic"]["avg_upland_slplen_splg"]=FILTERSTRIPS.FS_SPLG
        json_sub["subarea2"]["geographic"]["uplandmanningn_upn"] = FILTERSTRIPS.FS_UPN
        json_sub["subarea2"]["geographic"]["channelslope_chs"
            ]= FILTERSTRIPS.FS_SLPfactor*float(uplandslope)
        json_sub["subarea2"]["geographic"]["channelmanningn_chn"]=FILTERSTRIPS.FS_CHN
        json_sub["subarea2"]["geographic"]["reach_slope_rchs"]= FILTERSTRIPS.FS_SLPfactor*float(uplandslope)
        json_sub["subarea2"]["geographic"]["reach_depth_rchd"]=FILTERSTRIPS.FS_RCHD
        json_sub["subarea2"]["geographic"]["reach_bottom_width_rcbw"]=FILTERSTRIPS.FS_RCBW
        json_sub["subarea2"]["geographic"]["reach_top_width_rctw"]=FILTERSTRIPS.FS_RCTW
        json_sub["subarea2"]["geographic"]["reach_manningsn_rchn"]=FILTERSTRIPS.FS_RCHN
        json_sub["subarea2"]["geographic"]["reach_uslec_rchc"]=FILTERSTRIPS.FS_RCHC
        json_sub["subarea2"]["geographic"]["reach_uslek_rchk"]=FILTERSTRIPS.FS_RCHK
        json_sub["subarea2"]["geographic"]["reach_floodplain_rfpw"]=FILTERSTRIPS.FS_SPLG
        json_sub["subarea2"]["geographic"]["reach_floodplain_length_rfpl"]=FILTERSTRIPS.FS_RFPL
        json_sub["subarea2"]["flood_plain"]["flood_plain_frac_ffpq"]=FILTERSTRIPS.FS_FFPQ
        json_sub["subarea2"]["land_use_type"]["land_useid_luns"]=FILTERSTRIPS.FS_LUNS

        operationid = json_sub["subarea1"]["management"]["opeartionid_iops"]
        json_sub["subarea2"]["management"]["opeartionid_iops"]= operationid+1

        # It is not mentioned in the area what area should be contributed to the 
        # subarea. We need setup the subarea areas contributed to filter strip.
        # The area is set in the input files.
        area = json_sub["subarea1"]["geographic"]["wsa_ha"]*1
        json_sub["subarea2"]["geographic"]["wsa_ha"]=area*FILTERSTRIPS.FS_AreaFrac
        json_sub["subarea1"]["geographic"]["wsa_ha"]=area*(1-FILTERSTRIPS.FS_AreaFrac)

        # Pay attention to the units
        # area in unit of ha
        # field length = in km, actually the width of the field
        field_len = area*FILTERSTRIPS.FS_AreaFrac/FILTERSTRIPS.FS_width*10
        
        import math
        channel_len2 = math.sqrt(math.pow(field_len,
                                  2)+math.pow(FILTERSTRIPS.FS_RCHL,2))
        json_sub["subarea2"]["geographic"]["reach_length_rchl"]= FILTERSTRIPS.FS_RCHL
        json_sub["subarea2"]["geographic"]["channellength_chl"]=channel_len2

        # After gettin the field length, we can update the channel lengths of the 
        # first variable
        channel_len1=json_sub["subarea1"]["geographic"]["channellength_chl"]*1
        json_sub["subarea1"]["geographic"]["channellength_chl"]=channel_len1-FILTERSTRIPS.FS_RCHL
        json_sub["subarea1"]["geographic"]["reach_length_rchl"]=channel_len1-FILTERSTRIPS.FS_RCHL
    
        return json_sub
    

    #######################################################
    def updateopscomforfilterstrip(self, fidopscom, hruidx, hrunolist):
        fidopscom.writelines("%5i\tOP%sfs.OPC\n" %(hruidx+2,
                                              hrunolist[hruidx]))
        
        
        
        
    def generate_filterstrip_json(self, FILTERSTRIPS, opsjson_orig): 
        
        # This function will actually write the ops files
        # Filter strips should meet the following criteria:
        # 1. Shall be permanently designated plantings and are not 
        #    part of the adjacent crop rotation.
        # 2. I shall meet the format of the ops json and continue use
        #    the function
        # I will use the original ops json template
        # The first step is to delete all original lines, and then
        # generate new lines
        
        opsjson = opsjson_orig.copy()
        
        # Get all keys for the first level
        key_l1 = [key1 for key1, value1 in opsjson.iteritems()]
        
        # Get the ops length of 
        totalopsln = len(opsjson["jx6_cropid"])

        # delete current lines and only keep one line.
        # First, delete two keys, which are not dictionary.
        key_l1.remove("mgtkey")
        key_l1.remove("mgtname")
        key_l1.remove("operationid")
        key_l1.remove("lun_landuseno")        
        key_l1.remove("iaui_autoirr")
        key_l1.remove("iauf_autofert")        
        key_l1.remove("iamf_automanualdepos")
        key_l1.remove("ispf_autosolman")        
        key_l1.remove("ilqf_atliqman")
        key_l1.remove("iaul_atlime")
        key_l1.remove("manningn")

        
        for keyl1 in key_l1:
            for opsidx in range(1, totalopsln):
                tempkey = 0
                if keyl1[-1].isdigit():
                    tempkey = '%s_%i' %(str(keyl1), opsidx)
                    del opsjson[keyl1][tempkey]
                else:
                    tempkey = r'%s%i' %(str(keyl1), opsidx)
                    del opsjson[keyl1][tempkey]
            
        # The next step is to add lines for cover crops
        # Line 1
        opsjson["jx1_year"]["jx1_year0"] = 1
        opsjson["jx2_month"]["jx2_month0"] = 1
        opsjson["jx3_day"]["jx3_day0"] = 1  
        opsjson["jx4_tillid"]["jx4_tillid0"] = 139
        opsjson["jx5_tractid"]["jx5_tractid0"] = 24
        opsjson["jx6_cropid"]["jx6_cropid0"] = FILTERSTRIPS.FS_Crop
        opsjson["jx7"]["jx7_0"] = 0
        opsjson["opv1"]["opv1_0"] = 1300
        opsjson["opv2"]["opv2_0"] = 0
        opsjson["opv3"]["opv3_0"] = 0
        opsjson["opv4"]["opv4_0"] = 0
        opsjson["opv5"]["opv5_0"] = 0
        opsjson["opv6"]["opv6_0"] = 0
        opsjson["opv7"]["opv7_0"] = 0
        opsjson["opv8"]["opv8_0"] = 0

#        opsjson["jx1_year"]["jx1_year1"] = yridx3+1
#        opsjson["jx2_month"]["jx2_month1"] = (plantdate+td).month
#        opsjson["jx3_day"]["jx3_day1"] = (plantdate+td).day  
#        opsjson["jx4_tillid"]["jx4_tillid1"] = 139
#        opsjson["jx5_tractid"]["jx5_tractid1"] = 24
#        opsjson["jx6_cropid"]["jx6_cropid1"] = COVERCROPS.cvcropplant[1]
#        opsjson["jx7"]["jx7_1"] = 0
#        opsjson["opv1"]["opv1_1"] = 1300
#        opsjson["opv2"]["opv2_1"] = 0
#        opsjson["opv3"]["opv3_1"] = 0
#        opsjson["opv4"]["opv4_1"] = 0
#        opsjson["opv5"]["opv5_1"] = 0
#        opsjson["opv6"]["opv6_1"] = 0
#        opsjson["opv7"]["opv7_1"] = 0
#        opsjson["opv8"]["opv8_1"] = 0

        
        return opsjson
        
        
        
        
       