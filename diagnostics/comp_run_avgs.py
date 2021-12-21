#!/bin/python

import numpy as np
import matplotlib.pyplot as plt
from diag_functions import *
import sys,os

#random_nums = np.random.rand(100,1)

if len(sys.argv) < 3:
    print "usage "+sys.argv[0]+": <infile> <start_year> <end_year>"
    sys.exit(1)
else:
    tcfilename = sys.argv[1]
    start_year = int(sys.argv[2])
    end_year = int(sys.argv[3])
    figname = tcfilename

min_lat = 0
max_lat = 55
lat_res = 1
    
min_lon = -135
max_lon = 10
lon_res = 3

min_wind = 10.0
max_wind = 100.0
wind_res = 3.0

min_press = 850.0
max_press = 1020.0
press_res = 3.0

dur_days = 15
yr_avg = 3

years_total=[]
mon_avgs=[]
year_avgs=[]
lat_avgs=[]
lon_avgs=[]
wind_avgs=[]
press_avgs=[]
wlife_avgs=[]
plife_avgs=[]
mon_pcent=[]
lat_pcent=[]
lon_pcent=[]
press_pcent=[]
wind_pcent=[]
wlife_pcent=[]
plife_pcent=[]

for i in range(end_year-start_year+1):
    year = start_year+i

    [months,monthly_num] = get_month_number(tcfilename,year,year)
    [years,yearly_num] = get_year_number(tcfilename,year,year)
    [lats,lat_num] = get_lat_number(tcfilename,year,year,min_lat,max_lat,lat_res)
    [lons,lon_num] = get_lon_number(tcfilename,year,year,min_lon,max_lon,lon_res)
    [intsys,intsy_num] = get_wind_number(tcfilename,year,year,min_wind,max_wind,wind_res)
    [press,pres_num] = get_press_number(tcfilename,year,year,min_press,max_press,press_res)
    [durs,wdurd_num] = get_wind_decay_number(tcfilename,year,year,dur_days)
    [durs,pdurd_num] = get_press_decay_number(tcfilename,year,year,dur_days)

    years_total.append(year)
    mon_avgs.append(avg_hori(months,monthly_num))
    lat_avgs.append(avg_hori(lats,lat_num))
    lon_avgs.append(avg_hori(lons,lon_num))
    wind_avgs.append(avg_hori(intsys,intsy_num))
    press_avgs.append(avg_hori(press,pres_num))
    wlife_avgs.append(avg_hori(durs,wdurd_num))
    plife_avgs.append(avg_hori(durs,pdurd_num))
    year_avgs.append(avg_vert(years,yearly_num))
    mon_pcent.append(percent_in(months,monthly_num,5,11))
    lat_pcent.append(percent_in(lats,lat_num,0.0,25.0))
    lon_pcent.append(percent_in(lons,lon_num,-100.0,-50.0))
    press_pcent.append(percent_in(press,pres_num,1020.0,980.0))
    wind_pcent.append(percent_in(intsys,intsy_num,0.0,40.0))
    wlife_pcent.append(percent_in(durs,wdurd_num,0.0,100.0))
    plife_pcent.append(percent_in(durs,pdurd_num,0.0,100.0))

mon_avgs=running_avg(mon_avgs,yr_avg)
year_avgs=running_avg(year_avgs,yr_avg)
lat_avgs=running_avg(lat_avgs,yr_avg)
lon_avgs=running_avg(lon_avgs,yr_avg)
wind_avgs=running_avg(wind_avgs,yr_avg)
press_avgs=running_avg(press_avgs,yr_avg)
wlife_avgs=running_avg(wlife_avgs,yr_avg)
plife_avgs=running_avg(plife_avgs,yr_avg)

mon_pcent=running_avg(mon_pcent,yr_avg)
lat_pcent=running_avg(lat_pcent,yr_avg)
lon_pcent=running_avg(lon_pcent,yr_avg)
wind_pcent=running_avg(wind_pcent,yr_avg)
press_pcent=running_avg(press_pcent,yr_avg)
wlife_pcent=running_avg(wlife_pcent,yr_avg)
plife_pcent=running_avg(plife_pcent,yr_avg)


fig_rows=4
fig_cols=2

fig = plt.figure(1)
fig.suptitle("Avg vs Year")

plt.subplot(fig_rows,fig_cols,1)
plt.ylabel("Number")
plt.plot(years_total,year_avgs)

plt.subplot(fig_rows,fig_cols,2)
plt.ylabel("Month")
plt.plot(years_total,mon_avgs)

plt.subplot(fig_rows,fig_cols,3)
plt.ylabel("Lat")
plt.plot(years_total,lat_avgs)

plt.subplot(fig_rows,fig_cols,4)
plt.ylabel("Long")
plt.plot(years_total,lon_avgs)

plt.subplot(fig_rows,fig_cols,5)
plt.ylabel("Wind")
plt.plot(years_total,wind_avgs)

plt.subplot(fig_rows,fig_cols,6)
plt.ylabel("Pressure")
plt.plot(years_total,press_avgs)

plt.subplot(fig_rows,fig_cols,7)
plt.ylabel("Life (wind)")
plt.plot(years_total,wlife_avgs)

plt.subplot(fig_rows,fig_cols,8)
plt.ylabel("Life (pressure)")
plt.plot(years_total,plife_avgs)

plt.subplots_adjust(top=0.9, bottom=0.15, left=0.10, right=0.90, hspace=1.0,
                    wspace=0.40)
plt.savefig(figname+"_run_avgs.pdf",bbox_inches='tight')

fig_rows=3
fig_cols=2

fig = plt.figure(2)
fig.suptitle("Percent vs Year")

plt.subplot(fig_rows,fig_cols,1)
plt.ylabel("May-Nov")
plt.plot(years_total,mon_pcent)

plt.subplot(fig_rows,fig_cols,2)
plt.ylabel("0N-25N")
plt.plot(years_total,lat_pcent)

plt.subplot(fig_rows,fig_cols,3)
plt.ylabel("100W-50W")
plt.plot(years_total,lon_pcent)

plt.subplot(fig_rows,fig_cols,4)
plt.ylabel("0-40m/s")
plt.plot(years_total,wind_pcent)

plt.subplot(fig_rows,fig_cols,5)
plt.ylabel("0-100hrs (wind)")
plt.plot(years_total,wlife_pcent)

plt.subplot(fig_rows,fig_cols,6)
plt.ylabel("0-100hrs (pressure)")
plt.plot(years_total,plife_pcent)

#plt.subplot(fig_rows,fig_cols,7)
#plt.ylabel("1020-980hPa")
#plt.plot(years_total,press_pcent)

plt.subplots_adjust(top=0.9, bottom=0.15, left=0.10, right=0.90, hspace=1.0,
                    wspace=0.40)
plt.savefig(figname+"_run_avgs_pcent.pdf",bbox_inches='tight')
