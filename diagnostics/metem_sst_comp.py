#!/bin/bash

import Ngl,Nio
import numpy as np
import sys,subprocess,os

wrf_sst_arr=[]
wps_sst_arr=[]

wrf_dir_in="/glade/scratch/bbenton/20XXWRF/WRF_0/test/em_real"
wps_dir_in="/glade/scratch/bbenton/20XXWRF/WPS_0"
wps_files = [f for f in os.listdir(wps_dir_in) if f.startswith("met_em.d01")]
wrf_files = [f for f in os.listdir(wrf_dir_in) if f.startswith("wrfinput_d01")]
wps_files.sort()
wrf_files.sort()

for i in range(0,1):#len(files)):

    wrf_file_in=wrf_files[i]
    wrf_f=Nio.open_file(wrf_dir_in+"/"+wrf_file_in+".nc")
    wps_file_in=wps_files[i]
    wps_f=Nio.open_file(wps_dir_in+"/"+wps_file_in)

    #sst_avg=np.mean(f.variables["SST_monthly"].get_value())
    wrf_vals=wrf_f.variables["TSK"].get_value()
    wps_vals=wps_f.variables["TAVGSFC"].get_value()
    #wrf_vals=wrf_vals[0,:,:]
    #wps_vals=wrf_vals[0,:,:]
    wrf_sst_avg=np.mean(wrf_vals[np.nonzero(wps_vals)])
    wps_sst_avg=np.mean(wps_vals[np.nonzero(wps_vals)])
    #sst_arr.append(sst_avg)
    wrf_sst_arr.append(wrf_sst_avg)
    wps_sst_arr.append(wps_sst_avg)

#print(sst_arr)
print(np.mean(wrf_sst_arr))
print(np.mean(wps_sst_arr))
