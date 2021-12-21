#!/usr/bin/python
 
###############################################################################
#
#
###############################################################################

import numpy,sys,os,subprocess

from diag_functions import *

from plot_functions import *

import matplotlib.pyplot as plt

import pandas

#---------- Get Arguments ------------------------------------------
'''
if len(sys.argv) < 5:
    print "usage "+sys.argv[0]+": <case> <nrun> <start_year> <end_year> <year_avg>"
    sys.exit(1)
else:
    case=sys.argv[1]
    nrun=sys.argv[2]
    start_year = int(sys.argv[3])
    end_year = int(sys.argv[4])
    year_avg=int(sys.argv[5])
    tcfilename1 = "/glade/u/home/bbenton/TSTORMS_OUTPUT/%s/WRF/run_%s/traj_out_%s_%s_%s_%s" %(case,nrun,case,start_year,end_year,nrun)
    #tcfilename2 = "/glade/u/home/bbenton/TSTORMS_OUTPUT/ctrl/WRF/run_4/traj_out_ctrl_all_4"
    tcfilename2 = "/glade/u/home/bbenton/TSTORMS_OUTPUT/ibtracs/WRF/run_1/traj_out_ibtracs"
'''

start_year=1995
end_year=2005
tcfilename1 = "/glade/u/home/bbenton/20XXWRF/TSTORMS_OUTPUT/ibtracs_v3/traj_out_ibtracs_v3_1995_2005"
tcfilename2 = "/glade/u/home/bbenton/DATA/TSTORMS_OUTPUT/erai_30km/WRF/run_9/traj_out_erai_1995_2005_9"
year_avg=1

'''
tcdir="/glade/u/home/bbenton/TSTORMS_OUTPUT/%s/WRF/run_%s" %(case,nrun)
cmd="if [ ! -f %s ]; then for ((year=%s; year<=%s; year++)); do filename=%s/$year/traj_out_%s_$year; if [ -f $filename ]; then cat $filename >> %s; fi; done; fi" %(tcfilename1,start_year,end_year,tcdir,case,tcfilename1)

subprocess.call(cmd,shell=True)
'''

#---------- diag params -------------------#

lmon=5
rmon=11

llat=0.0
rlat=25.0

llon=-100.0
rlon=-50.0

lwind=0.0
rwind=40.0

lpress=1020.0
rpress=980.0

ltime=0.0
rtime=100.0

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

#ref_syear = 1000
#ref_eyear = 1100
ref_syear=1995
ref_eyear=2005

#---------- run diagnostics  ----------------#   


fig = plot_pval_fig(tcfilename1,tcfilename2,start_year,end_year,year_avg,ref_syear,
                  ref_eyear, min_lat,max_lat,lat_res,min_lon,max_lon,lon_res,
		  min_wind,max_wind,wind_res,min_press,max_press,press_res,dur_days)

#plt.savefig(tcfilename1+"_pvals.pdf")

# reference data set
[months,monthly_num2,
 years2,yearly_num2,
 lats,lat_num2,
 lons,lon_num2,
 intsys,intsy_num2,
 press,pres_num2,
 durs,wdurd_num2,
 pdurd_num2] = get_all_diags(tcfilename2,ref_syear,ref_eyear,
                             min_lat,max_lat,lat_res,
			     min_lon,max_lon,lon_res,
			     min_wind,max_wind,wind_res,
			     min_press,max_press,press_res,
			     dur_days)

# data set 1

pm_vals=[]
pw_vals=[]
plat_vals=[]
plon_vals=[]
pp_vals=[]
pwdur_vals=[]
ppdur_vals=[]
years=[]

year_range = end_year-start_year+1

#print("year_range: "+str(year_range))

for i in range(year_range):
    calc_year = start_year+i
    years.append(calc_year)
    [start_idx,end_idx] = running_range(year_range,year_avg,i)
    syr = start_idx+start_year
    eyr = end_idx+start_year

    #print("start_year: "+str(syr))
    #print("end_year: "+str(eyr))

    [months,monthly_num1,
     years1,yearly_num1,
     lats,lat_num1,
     lons,lon_num1,
     intsys,intsy_num1,
     press,pres_num1,
     durs,wdurd_num1,
     pdurd_num1] = get_all_diags(tcfilename1,syr,eyr,
                                 min_lat,max_lat,lat_res,
    			         min_lon,max_lon,lon_res,
    			         min_wind,max_wind,wind_res,
    			         min_press,max_press,press_res,
    			         dur_days)
    
    [ Pm, Pw, Plat, Plon, 
      Pp, Pwdur, Ppdur ] = get_all_ks_tests(monthly_num1,monthly_num2,
                                            intsy_num1,intsy_num2,
    				            lat_num1,lat_num2,
    					    lon_num1,lon_num2,
    					    pres_num1,pres_num2,
    					    wdurd_num1,wdurd_num2,
    					    pdurd_num1,pdurd_num2)
    pm_vals.append(Pm)							    
    pw_vals.append(Pw)							    
    plat_vals.append(Plat)							    
    plon_vals.append(Plon)							    
    pp_vals.append(Pp)							    
    pwdur_vals.append(Pwdur)							    
    ppdur_vals.append(Ppdur)							    



[months,monthly_num1,
 years1,yearly_num1,
 lats,lat_num1,
 lons,lon_num1,
 intsys,intsy_num1,
 press,pres_num1,
 durs,wdurd_num1,
 pdurd_num1] = get_all_diags(tcfilename1,start_year,end_year,
                             min_lat,max_lat,lat_res,
    			     min_lon,max_lon,lon_res,
    			     min_wind,max_wind,wind_res,
    			     min_press,max_press,press_res,
    			     dur_days)

avgs1 = get_all_avgs(months,monthly_num1,years1,yearly_num1,
                     lats,lat_num1,lons,lon_num1,intsys,intsy_num1,
		     press,pres_num1,durs,wdurd_num1,pdurd_num1)

avgs2 = get_all_avgs(months,monthly_num2,years2,yearly_num2,
                     lats,lat_num2,lons,lon_num2,intsys,intsy_num2,
		     press,pres_num2,durs,wdurd_num2,pdurd_num2)

pnum1 = get_all_percents(months,monthly_num1,lmon,rmon,
                         lats,lat_num1,llat,rlat,
			 lons,lon_num1,llon,rlon,
			 intsys,intsy_num1,lwind,rwind,
		         press,pres_num1,lpress,rpress,
			 durs,wdurd_num1,pdurd_num1,
			 ltime,rtime)

pnum2 = get_all_percents(months,monthly_num2,lmon,rmon,
                         lats,lat_num2,llat,rlat,
			 lons,lon_num2,llon,rlon,
			 intsys,intsy_num2,lwind,rwind,
		         press,pres_num2,lpress,rpress,
			 durs,wdurd_num2,pdurd_num2,
			 ltime,rtime)

pm_std = numpy.std(pm_vals)
pm_mean = numpy.mean(pm_vals)
pw_std = numpy.std(pw_vals)
pw_mean = numpy.mean(pw_vals)
plat_std = numpy.std(plat_vals)
plat_mean = numpy.mean(plat_vals)
plon_std = numpy.std(plon_vals)
plon_mean = numpy.mean(plon_vals)
pp_std = numpy.std(pp_vals)
pp_mean = numpy.mean(pp_vals)
pwdur_std = numpy.std(pwdur_vals)
pwdur_mean = numpy.mean(pwdur_vals)
ppdur_std = numpy.std(ppdur_vals)
ppdur_mean = numpy.mean(ppdur_vals)

pmeans=[pm_mean,pw_mean,plat_mean,plon_mean,pp_mean,pwdur_mean,ppdur_mean]
pstds=[pm_std,pw_std,plat_std,plon_std,pp_std,pwdur_std,ppdur_std]

pvals = [ Pm, Pw, Plat, Plon, Pp, Pwdur, Ppdur ] = get_all_ks_tests(monthly_num1,monthly_num2,
                                                            intsy_num1,intsy_num2,
							    lat_num1,lat_num2,
							    lon_num1,lon_num2,
							    pres_num1,pres_num2,
							    wdurd_num1,wdurd_num2,
							    pdurd_num1,pdurd_num2)


print_diff_table(avgs1,avgs2,pnum1,pnum2,start_year,end_year)
print_ks_table(pvals,pmeans,pstds)
