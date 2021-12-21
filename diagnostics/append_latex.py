#!/usr/bin/python
 
###############################################################################
#
#
###############################################################################

import numpy,sys,os

from diag_functions import *

import matplotlib.pyplot as plt

import pandas

#---------- Get Arguments ------------------------------------------

if len(sys.argv) < 4:
    print "usage "+sys.argv[0]+": <infile1> <infile2> <start_year> <end_year>"
    sys.exit(1)
else:
    tcfilename1 = sys.argv[1]
    tcfilename2 = sys.argv[2]
    start_year = int(sys.argv[3])
    end_year = int(sys.argv[4])


#---------- diag params -------------------#

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

#---------- run diagnostics  ----------------#   

# data set 1

[months,monthly_num1] = get_month_number(tcfilename1,start_year,end_year)
[years,yearly_num1] = get_year_number(tcfilename1,start_year,end_year)
[lats,lat_num1] = get_lat_number(tcfilename1,start_year,end_year,min_lat,max_lat,lat_res)
[lons,lon_num1] = get_lon_number(tcfilename1,start_year,end_year,min_lon,max_lon,lon_res)
[intsys,intsy_num1] = get_wind_number(tcfilename1,start_year,end_year,min_wind,max_wind,wind_res)
[press,pres_num1] = get_press_number(tcfilename1,start_year,end_year,min_press,max_press,press_res)
[durs,wdurd_num1] = get_wind_decay_number(tcfilename1,start_year,end_year,dur_days)
[durs,pdurd_num1] = get_press_decay_number(tcfilename1,start_year,end_year,dur_days)

# data set 2

[months,monthly_num2] = get_month_number(tcfilename2,start_year,end_year)
[years,yearly_num2] = get_year_number(tcfilename2,start_year,end_year)
[lats,lat_num2] = get_lat_number(tcfilename2,start_year,end_year,min_lat,max_lat,lat_res)
[lons,lon_num2] = get_lon_number(tcfilename2,start_year,end_year,min_lon,max_lon,lon_res)
[intsys,intsy_num2] = get_wind_number(tcfilename2,start_year,end_year,min_wind,max_wind,wind_res)
[press,pres_num2] = get_press_number(tcfilename2,start_year,end_year,min_press,max_press,press_res)
[durs,wdurd_num2] = get_wind_decay_number(tcfilename2,start_year,end_year,dur_days)
[durs,pdurd_num2] = get_press_decay_number(tcfilename2,start_year,end_year,dur_days)


#----------------plotting---------------------#

avgs1 = numpy.zeros(9)
avgs1[0] = avg_hori(months,monthly_num1)
avgs1[1] = avg_hori(years,yearly_num1)
avgs1[2] = avg_vert(years,yearly_num1)
avgs1[3] = avg_hori(lats,lat_num1)
avgs1[4] = avg_hori(lons,lon_num1)
avgs1[5] = avg_hori(intsys,intsy_num1)
avgs1[6] = avg_hori(press,pres_num1)
avgs1[7] = avg_hori(durs,wdurd_num1)
avgs1[8] = avg_hori(durs,pdurd_num1)

avgs2 = numpy.zeros(9)
avgs2[0] = avg_hori(months,monthly_num2)
avgs2[1] = avg_hori(years,yearly_num2)
avgs2[2] = avg_vert(years,yearly_num2)
avgs2[3] = avg_hori(lats,lat_num2)
avgs2[4] = avg_hori(lons,lon_num2)
avgs2[5] = avg_hori(intsys,intsy_num2)
avgs2[6] = avg_hori(press,pres_num2)
avgs2[7] = avg_hori(durs,wdurd_num2)
avgs2[8] = avg_hori(durs,pdurd_num2)

avg_tdiff = total_uncert(avgs1,avgs2)

pnum1 = numpy.zeros(7)
pnum2 = numpy.zeros(7)
pdiff = numpy.zeros(7)
avg_diff = numpy.zeros(9)


pmonth1 = percent_in(months,monthly_num1,5,11)
pmonth2 = percent_in(months,monthly_num2,5,11)

plat1 = percent_in(lats,lat_num1,0.0,25.0)
plat2 = percent_in(lats,lat_num2,0.0,25.0)

plon1 = percent_in(lons,lon_num1,-100.0,-50.0)
plon2 = percent_in(lons,lon_num2,-100.0,-50.0)

ppres1 = percent_in(press,pres_num1,1020.0,950.0)
ppres2 = percent_in(press,pres_num2,1020.0,950.0)

pwind1 = percent_in(intsys,intsy_num1,0.0,40.0)
pwind2 = percent_in(intsys,intsy_num2,0.0,40.0)

pwdur1 = percent_in(durs,wdurd_num1,0.0,100.0)
pwdur2 = percent_in(durs,wdurd_num2,0.0,100.0)

ppdur1 = percent_in(durs,pdurd_num1,0.0,100.0)
ppdur2 = percent_in(durs,pdurd_num2,0.0,100.0)

pnum1[0]=pmonth1
pnum1[1]=plat1
pnum1[2]=plon1
pnum1[3]=ppres1
pnum1[4]=pwind1
pnum1[5]=pwdur1
pnum1[6]=ppdur1

pnum2[0]=pmonth2
pnum2[1]=plat2
pnum2[2]=plon2
pnum2[3]=ppres2
pnum2[4]=pwind2
pnum2[5]=pwdur2
pnum2[6]=ppdur2

for i in range(len(avg_diff)):
    avg_diff[i]=uncert(avgs1[i],avgs2[i])

for i in range(len(pdiff)):
    pdiff[i]=uncert(pnum1[i],pnum2[i])

pcent_tdiff = total_uncert(pnum1,pnum2)
comb_diff = (avg_tdiff+pcent_tdiff)/2.0

columnsTitles = ['Metrics','ERAI','IBTrACS','Difference']

table = {'Metrics': ['avg month','avg year','avg year num','avg lat','avg lon',
		     'avg speed m/s', 'avg pressure hPa', '(wind) avg life', 
		     '(pressure) avg life', 'May-Nov', '0N-25N', '100W-50W', 
		     '1020hPa-950hPa', '0m/s-40m/s', '(wind) 0-100hrs', 
		     '(pressure) 0-100hrs'],
         'ERAI': [avgs1[0],avgs1[1],avgs1[2],avgs1[3],avgs1[4],avgs1[5],avgs1[6],
	          avgs1[7],avgs1[8],pnum1[0],pnum1[1],pnum1[2],pnum1[3],pnum1[4],
		  pnum1[5],pnum1[6]], 
	 'IBTrACS': [avgs2[0],avgs2[1],avgs2[2],avgs2[3],avgs2[4],avgs2[5],avgs2[6],
	             avgs2[7],avgs2[8],pnum2[0],pnum2[1],pnum2[2],pnum2[3],pnum2[4],
		     pnum2[5],pnum2[6]],
         'Difference': [avg_diff[0],avg_diff[1],avg_diff[2],avg_diff[3],avg_diff[4],
	 	        avg_diff[5],avg_diff[6],avg_diff[7],avg_diff[8],pdiff[0],
			pdiff[1],pdiff[2],pdiff[3],pdiff[4],pdiff[5],pdiff[6]]}

df = pandas.DataFrame(data=table)
df = df.reindex(columns=columnsTitles)
df_tex = df.to_latex()

print(r"\afterpage{\clearpage%")
print(r"\begin{figure}[!tbp]")
print("\centering")
print(r"\begin{minipage}[b]{0.45\textwidth}")
print(r"\includegraphics[width=\textwidth]{fig_1}")
print(r"\caption{cap_1}")
print(r"\end{minipage}")
print("\hfill")
print(r"\begin{minipage}[b]{0.45\textwidth}")
print(r"\includegraphics[width=\textwidth]{fig_2}")
print(r"\caption{cap_2}")
print(r"\end{minipage}")
print(r"\end{figure}")

print(df.to_latex(index=False))
print(r"\noindent\fbox{\parbox{\textwidth}{%")
print("\centering")
print("total average difference: "+pad_num(avg_tdiff)+r"\\")
print("total percent difference: "+pad_num(pcent_tdiff)+r"\\")
print("composite difference: "+pad_num(comb_diff)+"}}")
print("}")
print("")
print("")
print("")
print("")
print("\end{document}")
