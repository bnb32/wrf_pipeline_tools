#!/bin/python

import numpy as np
import matplotlib.pyplot as plt
import Ngl,Nio
import sys


lat_min=0.0
lat_max=55.0
lon_min=-100.0
lon_max=10.0

s_years=[1213,1258,1274,1284,1452,1600,1641,1761,1809,1815]
e_years=[1223,1274,1283,1294,1461,1609,1650,1770,1818,1825]

years=[]
for i in range((1849-850)+1):
    years.append(i+850)

cesm_ctrl="~/PROJ_WRF/ctrl_mixed/T_sfc/chunks/TS_ctrl_1000_1100_avg.nc"
wrf_ctrl="~/PROJ_WRF/ctrl_mixed/T_sfc/chunks/T_sfc_ctrl_1000_1100_avg.nc"

ctrl_file=Nio.open_file(cesm_ctrl)
lat=ctrl_file.variables["lat"][:]
lon=ctrl_file.variables["lon"][:]
lat_min_idx=(np.abs(lat-lat_min)).argmin()
lat_max_idx=(np.abs(lat-lat_max)).argmin()
lon_min_idx=(np.abs(lon-lon_min)).argmin()
lon_max_idx=(np.abs(lon-lon_max)).argmin()
T_cesm_ctrl = np.mean(ctrl_file.variables["TS"][lat_min_idx:lat_max_idx,lon_min_idx:lon_max_idx])

ctrl_file=Nio.open_file(wrf_ctrl)
lat=ctrl_file.variables["lat"][:]
lon=ctrl_file.variables["lon"][:]
lat_min_idx=(np.abs(lat-lat_min)).argmin()
lat_max_idx=(np.abs(lat-lat_max)).argmin()
lon_min_idx=(np.abs(lon-lon_min)).argmin()
lon_max_idx=(np.abs(lon-lon_max)).argmin()
T_wrf_ctrl = np.mean(ctrl_file.variables["T_sfc_monthly"][0,lat_min_idx:lat_max_idx,lon_min_idx:lon_max_idx])

def get_tavg(nrun):

    temp=[]
    data={}
    files={}
    dat_dir="~/PROJ_WRF/forced/TS"
    data["dat"]=dat_dir+"/TS_%s_0850_1849.nc" %(nrun)
    
    files["f"]=Nio.open_file(data["dat"])
    
    lat  = files["f"].variables["lat"][:]
    lat_min_idx=(np.abs(lat-lat_min)).argmin()
    lat_max_idx=(np.abs(lat-lat_max)).argmin()

    lon  = files["f"].variables["lon"][:]
    lon_min_idx=(np.abs(lon-lon_min)).argmin()
    lon_max_idx=(np.abs(lon-lon_max)).argmin()
    
    for i in range((1849-850)+1):
        T_avg = np.mean(files["f"].variables["TS"][12*i:12*(i+1),lat_min_idx:lat_max_idx,lon_min_idx:lon_max_idx])-T_cesm_ctrl
        temp.append(T_avg)

    return temp

def get_tavg_wrf(s_year,e_year):
    
    dat_dir="~/PROJ_WRF/forced_mixed/T_sfc"
    case="forced"
    data={}
    files={}
    temp=[]
    count=0
    for i in range(s_year,e_year+1):
        for j in range(1,13):
            year=str(i); 
    	    if j<10: month="0"+str(j) 
    	    else: month=str(j)
            data["dat_%s" %(count)]=dat_dir+"/T_sfc_%s_%s_%s.nc" %(case,year,month)
            count+=1
    
    for i in range(len(data.keys())):
        files["f_%s" %(i)]=Nio.open_file(data["dat_%s" %(i)])
    
    lat  = files["f_0"].variables["lat"][:]
    lat_min_idx=(np.abs(lat-lat_min)).argmin()
    lat_max_idx=(np.abs(lat-lat_max)).argmin()

    lon  = files["f_0"].variables["lon"][:]
    lon_min_idx=(np.abs(lon-lon_min)).argmin()
    lon_max_idx=(np.abs(lon-lon_max)).argmin()
    
    for i in range(len(files.keys())):
        T_avg = np.mean(files["f_%s" %(i)].variables["T_sfc_monthly"][0,lat_min_idx:lat_max_idx,lon_min_idx:lon_max_idx])
        temp.append(T_avg-T_wrf_ctrl)
    
    tmp_avg=[]
    years=[]
    for i in range(int(len(temp)/12)):
        tmp_avg.append(np.mean(temp[12*i:12*(i+1)]))
	years.append(s_year+i)
    temp=tmp_avg    

    return [years,temp]	


fig=plt.figure(1)
plt.rc('font',size=8)
plt.suptitle("TS avgs 850-1850")
plt.subplot(2,1,1)
for i in range(7,8):
    if i < 10: nrun="00%s" %(i)
    else: nrun="0%s" %(i)
    plt.plot(years,get_tavg(nrun))

plt.subplot(2,1,2)
ys=[]
vs=[]
for i in range(len(s_years)):
    [y,v]=get_tavg_wrf(s_years[i],e_years[i])
    ys=ys+y
    vs=vs+v
years=[]
vals=[]
for i in range((1849-850)+1):
    yr=850+i
    years.append(yr)
    if yr in ys: 
        idx=ys.index(yr)
        vals.append(vs[idx])
    else: vals.append(0)	

plt.plot(years,vals)    
plt.savefig("TS_avgs_exp7.pdf")

