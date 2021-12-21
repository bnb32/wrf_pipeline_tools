#!/bin/bash

import Ngl,Nio
import numpy as np
import sys,subprocess,os

sst_arr=[]
ts_arr=[]

dir_in="/glade/u/home/bbenton/PROJ_WRF/ctrl/1000"
files = [f for f in os.listdir(dir_in) if f.startswith("wrfpost")]
files.sort()

for i in range(0,12):#len(files)):

    file_in=files[i]
    f=Nio.open_file(dir_in+"/"+file_in)

    sst_avg=np.mean(f.variables["SST_monthly"].get_value())
    #sst_avg=np.mean(f.variables["T_sfc_monthly"].get_value())
    #sst_arr.append(sst_avg)
    sst_arr.append(sst_avg)

print(sst_arr)
print(np.mean(sst_arr))
