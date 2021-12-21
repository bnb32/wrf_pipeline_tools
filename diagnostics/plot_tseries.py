#!/bin/python

import numpy as np
import matplotlib.pyplot as plt
import Ngl,Nio
import sys

#if len(sys.argv)<2: print("case,exp"); exit()
#else: case=sys.argv[1]; exp=sys.argv[2]

case="forced"
#exp="cesm"


lat_min=0.0
lat_max=57.5
lon_min=-100.0
lon_max=10.0

if case=="forced":
    s_years=[1213]#,1258,1274,1284,1452,1600,1641,1761,1809,1815]
    e_years=[1223]#,1274,1283,1294,1461,1609,1650,1770,1818,1825]

if case=="ctrl":
    s_years=[1000]
    e_years=[1009]

cols=2-len(s_years)%2
rows=int(len(s_years)/cols)

int_dat=[294.5891,
294.3944,
294.5567,
294.4318,
294.5257,
294.6812,
294.8867,
294.8929,
294.6867,
294.6723,
294.6832]

def get_tavg(case,exp,s_year,e_year):

    if exp=="cesm":
        dat_dir="~/PROJ_WRF/%s/SST" %(case)
    if exp=="wrf":
        dat_dir="~/PROJ_WRF/%s/T_sfc" %(case)
    
    temp=[]
    data={}
    files={}
    if exp=="cesm":
        data["dat"]=dat_dir+"/SST_%s_%s_%s.nc" %(case,s_year,e_year)
        
        files["f"]=Nio.open_file(data["dat"])
        
        lat2d  = files["f"].variables["TLAT"]

	lat = lat2d[:,0]
	lat_min_idx=(np.abs(lat-lat_min)).argmin()
        lat_max_idx=(np.abs(lat-lat_max)).argmin()

        lon2d  = files["f"].variables["TLONG"]
        lon = lon2d[0,:]

	for i in range(len(lon)):
	    if lon[i]>180.0: lon[i]=-(360-lon[i])
        lon_min_idx=(np.abs(lon-lon_min)).argmin()
        lon_max_idx=(np.abs(lon-lon_max)).argmin()

        #print(lon_min_idx)
	#print(lon_max_idx)
        #print(lon[lon_min_idx:lon_max_idx])
	#exit()

        for i in range((e_year-s_year)+1):
	    #T_avg = np.mean(files["f"].variables["TS"][12*i:12*(i+1),lat_min_idx:lat_max_idx,:])
            T_avg = np.mean(files["f"].variables["SST"][12*i:12*(i+1),0,lat_min_idx:lat_max_idx,:])+273.15
            temp.append(T_avg)
    
    if exp=="wrf":
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
            T_avg = np.mean(files["f_%s" %(i)].variables["T_sfc_monthly"][0,lat_min_idx:lat_max_idx,:])
            temp.append(T_avg)
        
        tmp_avg=[]
        for i in range(int(len(temp)/12)):
            tmp_avg.append(np.mean(temp[12*i:12*(i+1)]))
	temp=tmp_avg    

    return temp	

fig=plt.figure(1)
plt.rc('font',size=8)

#ctrl_vals=get_tavg("ctrl",1000,1009)
#ctrl_val=np.mean(ctrl_vals)

for i in range(len(s_years)):
    plt.subplot(rows,cols,i+1)
    plt.plot(get_tavg(case,"cesm",s_years[i],e_years[i]))
    plt.plot(get_tavg(case,"wrf",s_years[i],e_years[i]))
    plt.plot(int_dat)
    plt.title("SST %s %s-%s" %(case,s_years[i],e_years[i]))

plt.subplots_adjust(top=0.9,bottom=0.15,left=0.20,right=0.90,hspace=1.2,wspace=0.5)  
plt.savefig("%s_SST_avgs.pdf" %(case))

