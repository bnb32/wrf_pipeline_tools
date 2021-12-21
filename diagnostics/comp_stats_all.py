#!/usr/bin/python
 
###############################################################################
#
#
###############################################################################

import numpy as np
import sys,os,subprocess
from diag_functions import *
from plot_functions import *
import matplotlib.pyplot as plt
import pandas as pd
from comp_stats_data import *
from volcInfo import getVolcInfo
import argparse
from confidence_interval import conInterval
from scipy import stats
import seaborn as sns
#sns.set_theme()


DIR="/glade/scratch/cmc542/tmp/bbenton"

parser = argparse.ArgumentParser(description='Plot and find volcanoes')
parser.add_argument('-number',default=50,type=int)
parser.add_argument('-region',default="all",choices=["north","south","all"])
parser.add_argument('-print_data',default=False,action='store_true')
parser.add_argument('-nrun',default=9)
parser.add_argument('-run_control',default=False,action='store_true')
args = parser.parse_args()

strengths,start_years,erup_lats=getVolcInfo(args.number,args.region)
start_years = [int(x) for x in start_years]

erup_num = len(strengths)

nrun=args.nrun
print_data=args.print_data
run_control=args.run_control

tcfilename2 = "%s/TSTORMS_OUTPUT/ctrl/WRF/run_%s/traj_out_ctrl_950_1104_%s" %(DIR,nrun,nrun)

start_years=[x for x in start_years]
end_years=[x+1 for x in start_years]

weights=[2-x/max(strengths) for x in strengths] 

s_years=[]
e_years=[]
e_lats=[]

#strengths=[strengths[i]*(1.0-abs(erup_lats[i]-4.0)/15.0) for i in range(len(strengths))]

str_sort=sorted(strengths)

for x in str_sort:
    idx=(np.abs(np.array(strengths)-x)).argmin()
    s_years.append(start_years[idx])
    e_years.append(end_years[idx])
    e_lats.append(erup_lats[idx])

start_years=s_years
end_years=e_years
strengths=str_sort
erup_lats=e_lats

forced_yrs=0
for i in range(len(start_years)):
    forced_yrs+=end_years[i]-start_years[i]+1

tcdir="%s/TSTORMS_OUTPUT/forced/WRF/run_%s" %(DIR,nrun)

lmon=5;rmon=11
llat=0.0;rlat=25.0
llon=-100.0;rlon=-50.0
lwind=0.0;rwind=40.0
lpress=1020.0;rpress=980.0
ltime=0.0;rtime=120.0
lpdi=55000;rpdi=9000000
lace=2500;race=37500
min_lat = 0;max_lat = 55;lat_res = 1    
min_lon = -135;max_lon = 10;lon_res = 3
#min_wind = 10.0;max_wind = 100.0;wind_res = 3.0
min_wind = 10.0;max_wind = 70.0;wind_res = 1.0
#min_press = 850.0;max_press = 1020.0;press_res = 3.0
min_press = 950.0;max_press = 1020.0;press_res = 1.0
tstep = 6*60*60
#min_pdi = 55000.0*tstep; max_pdi = 2000000.0*tstep
min_pdi = 0.0*tstep; max_pdi = 2000000.0*tstep
pdi_res = (max_pdi-min_pdi)/100

min_ace = 0*2500.0*10**(-4); max_ace = 40000.0*10**(-4)
ace_res = (max_ace-min_ace)/100

#dur_days = 15
dur_days = 7

avg_store=[]
diff_store=[]
rat_store=[]

ref_syear=950
ref_eyear=1104
ctrl_yrs=ref_eyear-ref_syear+1
ref_avg=1

ref_dir="%s/TSTORMS_OUTPUT/ctrl/WRF/run_%s" %(DIR,nrun)

filename = DIR+"/TSTORMS_OUTPUT/forced/WRF/run_%s/traj_out_forced_%s_%s_%s"

command = "if [ ! -f %s ]; then for ((year=%s; year<=%s; year++)); do filename=%s/$year/traj_out_forced_$year; if [ -f $filename ]; then cat $filename >> %s; fi; done; fi"

if run_control:

    [ref_stds,ref_avgs,ref_mons,ref_years,ref_lats,ref_lons,ref_ints,ref_press,ref_wdurds,ref_pdurds,ref_pdi,ref_ace]=get_ref_stats(tcfilename2,ref_dir,ref_syear,ref_eyear,ref_avg,
                      lmon,rmon,llat,rlat,llon,rlon,lwind,rwind,lpress,
    		  rpress,ltime,rtime,min_lat,max_lat,lat_res,
    		  min_lon,max_lon,lon_res,min_wind,max_wind,
    		  wind_res,min_press,max_press,press_res,dur_days,lpdi,rpdi,lace,race,min_pdi,max_pdi,pdi_res,min_ace,max_ace,ace_res)
    
    print("ref_stds=%s"%ref_stds)
    print("ref_avgs=%s"%ref_avgs)
    print("ref_mons=%s"%ref_mons)
    print("ref_years=%s"%ref_years)
    print("ref_lats=%s"%ref_lats)
    print("ref_lons=%s"%ref_lons)
    print("ref_ints=%s"%ref_ints)
    print("ref_press=%s"%ref_press)
    print("ref_wdurds=%s"%ref_wdurds)
    print("ref_pdurds=%s"%ref_pdurds)
    print("ref_pdi=%s"%ref_pdi)
    print("ref_ace=%s"%ref_ace)
    
    [months,monthly_num2,
    years2,yearly_num2,
    lats,lat_num2,
    lons,lon_num2,
    intsys,intsy_num2,
    press,pres_num2,
    durs,wdurd_num2,
    pdurd_num2,
    pdis,pdi_num2,
    aces,ace_num2] = get_all_diags(tcfilename2,ref_syear,ref_eyear,
                                     min_lat,max_lat,lat_res,
            			     min_lon,max_lon,lon_res,
            			     min_wind,max_wind,wind_res,
            			     min_press,max_press,press_res,
            			     dur_days,min_pdi,max_pdi,pdi_res,min_ace,max_ace,ace_res)
    
    [monthly_num2,
    yearly_num2,
    lat_num2,
    lon_num2,
    intsy_num2,
    pres_num2,
    wdurd_num2,
    pdurd_num2,
    pdi_num2,
    ace_num2] = get_ref_dists(tcfilename2,ref_dir,ref_syear,ref_eyear,ref_avg,
                                     min_lat,max_lat,lat_res,
            			     min_lon,max_lon,lon_res,
            			     min_wind,max_wind,wind_res,
            			     min_press,max_press,press_res,
            			     dur_days,
                             min_pdi,max_pdi,pdi_res,
                             min_ace,max_ace,ace_res)
    
    
    yn2_hist=np.histogram(yearly_num2,bins=30)
    #yearly_num2=yn2_hist[0]
    
    print("yr_bins=%s"%list(yn2_hist[1]))
    print("monthly_num2=%s"%list(monthly_num2))
    print("yearly_num2=%s"%list(yearly_num2))
    print("lat_num2=%s"%list(lat_num2))
    print("lon_num2=%s"%list(lon_num2))
    print("intsy_num2=%s"%list(intsy_num2))
    print("pres_num2=%s"%list(pres_num2))
    print("wdurd_num2=%s"%list(wdurd_num2))
    print("pdurd_num2=%s"%list(pdurd_num2))
    print("pdi_num2=%s"%list(pdi_num2))
    print("ace_num2=%s"%list(ace_num2))
    
    exit()

[avg_store,diff_store,rat_store,monthly_num,yearly_num,lat_num,
 lon_num,intsy_num,pres_num,wdurd_num,pdurd_num,months,lats,lons,press,intsys,durs,pdis,pdi_num,aces,ace_num]=get_samp_stats(filename,command,tcdir,ref_avgs,ref_stds,nrun,yr_bins,start_years,end_years,min_lat,max_lat,lat_res,min_lon,max_lon,lon_res,min_wind,max_wind,wind_res,min_press,max_press,press_res,dur_days,lmon,rmon,llat,rlat,llon,rlon,lwind,rwind,lpress,rpress,ltime,rtime,lpdi,rpdi,lace,race,min_pdi,max_pdi,pdi_res,min_ace,max_ace,ace_res)

monthly_num=monthly_num/float(forced_yrs)
monthly_num2=np.asarray(monthly_num2)/float(ctrl_yrs)
yearly_num=yearly_num#/float(forced_yrs)#float(np.sum(yearly_num))
yearly_num2=np.asarray(yearly_num2)#/float(ctrl_yrs)#float(np.sum(yearly_num2))
lat_num=lat_num/float(forced_yrs)
lat_num2=np.asarray(lat_num2)/float(ctrl_yrs)
lon_num=lon_num/float(forced_yrs)
lon_num2=np.asarray(lon_num2)/float(ctrl_yrs)
intsy_num=intsy_num/float(forced_yrs)
intsy_num2=np.asarray(intsy_num2)/float(ctrl_yrs)
pres_num=pres_num/float(forced_yrs)
pres_num2=np.asarray(pres_num2)/float(ctrl_yrs)
wdurd_num=wdurd_num/float(forced_yrs)
wdurd_num2=np.asarray(wdurd_num2)/float(ctrl_yrs)
pdurd_num=pdurd_num/float(forced_yrs)
pdurd_num2=np.asarray(pdurd_num2)/float(ctrl_yrs)
pdi_num=pdi_num/float(forced_yrs)
pdi_num2=np.asarray(pdi_num2)/float(ctrl_yrs)
ace_num=ace_num/float(forced_yrs)
ace_num2=np.asarray(ace_num2)/float(ctrl_yrs)

'''

monthly_num=normed(monthly_num)
monthly_num2=normed(monthly_num2)
yearly_num=normed(yearly_num)#/float(forced_yrs)#float(np.sum(yearly_num))
yearly_num2=normed(yearly_num2)#/float(ctrl_yrs)#float(np.sum(yearly_num2))
lat_num=normed(lat_num)
lat_num2=normed(lat_num2)
lon_num=normed(lon_num)
lon_num2=normed(lon_num2)
intsy_num=normed(intsy_num)
intsy_num2=normed(intsy_num2)
pres_num=normed(pres_num)
pres_num2=normed(pres_num2)
wdurd_num=normed(wdurd_num)
wdurd_num2=normed(wdurd_num2)
pdurd_num=normed(pdurd_num)
pdurd_num2=normed(pdurd_num2)
'''

mons_rat=[rat_store[x][0] for x in range(len(rat_store))]
yrs_rat=[rat_store[x][1] for x in range(len(rat_store))]
lats_rat=[rat_store[x][2] for x in range(len(rat_store))]
lons_rat=[rat_store[x][3] for x in range(len(rat_store))]
intsys_rat=[rat_store[x][4] for x in range(len(rat_store))]
press_rat=[rat_store[x][5] for x in range(len(rat_store))]
wdurs_rat=[rat_store[x][6] for x in range(len(rat_store))]
pdurs_rat=[rat_store[x][7] for x in range(len(rat_store))]
pdi_rat=[rat_store[x][8] for x in range(len(rat_store))]
ace_rat=[rat_store[x][9] for x in range(len(rat_store))]

pmons_rat=[rat_store[x][10] for x in range(len(rat_store))]
plats_rat=[rat_store[x][11] for x in range(len(rat_store))]
plons_rat=[rat_store[x][12] for x in range(len(rat_store))]
pints_rat=[rat_store[x][13] for x in range(len(rat_store))]
ppress_rat=[rat_store[x][14] for x in range(len(rat_store))]
pwdurs_rat=[rat_store[x][15] for x in range(len(rat_store))]
ppdurs_rat=[rat_store[x][16] for x in range(len(rat_store))]
ppdi_rat=[rat_store[x][17] for x in range(len(rat_store))]
pace_rat=[rat_store[x][18] for x in range(len(rat_store))]

mons_avg=[avg_store[x][0] for x in range(len(avg_store))]
yrs_avg=[avg_store[x][1] for x in range(len(avg_store))]
lats_avg=[avg_store[x][2] for x in range(len(avg_store))]
lons_avg=[avg_store[x][3] for x in range(len(avg_store))]
intsys_avg=[avg_store[x][4] for x in range(len(avg_store))]
press_avg=[avg_store[x][5] for x in range(len(avg_store))]
wdurs_avg=[avg_store[x][6] for x in range(len(avg_store))]
pdurs_avg=[avg_store[x][7] for x in range(len(avg_store))]
pdi_avg=[avg_store[x][8] for x in range(len(avg_store))]
ace_avg=[avg_store[x][9] for x in range(len(avg_store))]

pmons_avg=[avg_store[x][9] for x in range(len(avg_store))]
plats_avg=[avg_store[x][10] for x in range(len(avg_store))]
plons_avg=[avg_store[x][11] for x in range(len(avg_store))]
pints_avg=[avg_store[x][12] for x in range(len(avg_store))]
ppress_avg=[avg_store[x][13] for x in range(len(avg_store))]
pwdurs_avg=[avg_store[x][14] for x in range(len(avg_store))]
ppdurs_avg=[avg_store[x][15] for x in range(len(avg_store))]
ppdi_avg=[avg_store[x][16] for x in range(len(avg_store))]
pace_avg=[avg_store[x][17] for x in range(len(avg_store))]


print("\nks-tests")
print("month & %s & %s \\\\" %(round(ks_test(monthly_num,monthly_num2)[0],3),round(ks_test(monthly_num,monthly_num2)[1],2)))

#why is this not summing to 1 for the 10 erups?
print("yearly num & %s & %s \\\\" %(round(ks_test(yearly_num,yearly_num2)[0],3),round(ks_test(yearly_num,yearly_num2)[1],2)))
print("lats & %s & %s \\\\" %(round(ks_test(lat_num,lat_num2)[0],3),round(ks_test(lat_num,lat_num2)[1],2)))
print("lons & %s & %s \\\\" %(round(ks_test(lon_num,lon_num2)[0],3),round(ks_test(lon_num,lon_num2)[1],2)))
print("max wind & %s & %s \\\\" %(round(ks_test(intsy_num,intsy_num2)[0],3),round(ks_test(intsy_num,intsy_num2)[1],2)))
print("min press & %s & %s \\\\" %(round(ks_test(pres_num,pres_num2)[0],3),round(ks_test(pres_num,pres_num2)[1],2)))
print("w-life & %s & %s \\\\" %(round(ks_test(wdurd_num,wdurd_num2)[0],3),round(ks_test(wdurd_num,wdurd_num2)[1],2)))
print("p-life & %s & %s \\\\" %(round(ks_test(pdurd_num,pdurd_num2)[0],3),round(ks_test(pdurd_num,pdurd_num2)[1],2)))
print("pdi & %s & %s \\\\" %(round(ks_test(pdi_num,pdi_num2)[0],3),round(ks_test(pdi_num,pdi_num2)[1],2)))
print("ace & %s & %s \\\\" %(round(ks_test(ace_num,ace_num2)[0],3),round(ks_test(ace_num,ace_num2)[1],2)))


print("\nanderson-darling tests")
print("\nmonth: ")
print(and_test(monthly_num,monthly_num2))
print("\nyearly num: ")
print(and_test(yearly_num,yearly_num2))
print("\nlats: ")
print(and_test(lat_num,lat_num2))
print("\nlons: ")
print(and_test(lon_num,lon_num2))
print("\nmax wind: ")
print(and_test(intsy_num,intsy_num2))
print("\nmax press: ")
print(and_test(pres_num,pres_num2))
print("\nw-life: ") 
print(and_test(wdurd_num,wdurd_num2))
print("\np-life: ")
print(and_test(pdurd_num,pdurd_num2))
print("\npdi: ")
print(and_test(pdi_num,pdi_num2))
print("\nace: ")
print(and_test(ace_num,ace_num2))


'''

print("\nmonth avg: %s" %(np.mean(mons_avg)))
print("yearly num avg: %s" %(np.mean(yrs_avg)))
print("lat avg: %s" %(np.mean(lats_avg)))
print("lon avg: %s" %(np.mean(lons_avg)))
print("max wind avg: %s" %(np.mean(intsys_avg)))
print("min press avg: %s" %(np.mean(press_avg)))
print("w-life avg: %s" %(np.mean(wdurs_avg)))
print("p-life avg: %s" %(np.mean(pdurs_avg)))
'''

forced_avgs=[avg_hori(months,monthly_num),np.mean(yrs_avg),avg_hori(lats,lat_num), avg_hori(lons,lon_num), avg_hori(intsys,intsy_num), avg_hori(press,pres_num), avg_hori(durs,wdurd_num), avg_hori(durs,pdurd_num),avg_hori(pdis,pdi_num),avg_hori(aces,ace_num)]

print("\nforced avgs")
print("month avg: %s" %(avg_hori(months,monthly_num)))
print("yearly num avg: %s" %(np.mean(yrs_avg)))
print("lat avg: %s" %(avg_hori(lats,lat_num)))
print("lon avg: %s" %(avg_hori(lons,lon_num)))
print("max wind avg: %s" %(avg_hori(intsys,intsy_num)))
print("min press avg: %s" %(avg_hori(press,pres_num)))
print("w-life avg: %s" %(avg_hori(durs,wdurd_num)))
print("p-life avg: %s" %(avg_hori(durs,pdurd_num)))
print("pdi avg: %s" %(avg_hori(pdis,pdi_num)))
print("ace avg: %s" %(avg_hori(aces,ace_num)))

print("\nctrl avgs")
print("month avg: %s" %(ref_avgs[0]))
print("yearly num avg: %s" %(ref_avgs[1]))
print("lat avg: %s" %(ref_avgs[2]))
print("lon avg: %s" %(ref_avgs[3]))
print("max wind avg: %s" %(ref_avgs[4]))
print("min press avg: %s" %(ref_avgs[5]))
print("w-life avg: %s" %(ref_avgs[6]))
print("p-life avg: %s" %(ref_avgs[7]))
print("pdi avg: %s" %(ref_avgs[8]))
print("ace avg: %s" %(ref_avgs[9]))

print("\ntotal diff: %s" %(total_uncert(forced_avgs,ref_avgs[0:10])))

'''
print("\nmonth diff: %s" %(np.mean(mons_rat)))
print("yearly num diff: %s" %(np.mean(yrs_rat)))
print("lat diff: %s" %(np.mean(lats_rat)))
print("lon diff: %s" %(np.mean(lons_rat)))
print("max wind diff: %s" %(np.mean(intsys_rat)))
print("min press diff: %s" %(np.mean(press_rat)))
print("w-life diff: %s" %(np.mean(wdurs_rat)))
print("p-life diff: %s" %(np.mean(pdurs_rat)))
'''
print("\nmonth diff: %s" %((avg_hori(months,monthly_num)-ref_avgs[0])/ref_stds[0]))
print("yearly num diff: %s" %((np.mean(yrs_avg)-ref_avgs[1])/ref_stds[1]))
print("lat diff: %s" %((avg_hori(lats,lat_num)-ref_avgs[2])/ref_stds[2]))
print("lon diff: %s" %((avg_hori(lons,lon_num)-ref_avgs[3])/ref_stds[3]))
print("max wind diff: %s" %((avg_hori(intsys,intsy_num)-ref_avgs[4])/ref_stds[4]))
print("min press diff: %s" %((avg_hori(press,pres_num)-ref_avgs[5])/ref_stds[5]))
print("w-life diff: %s" %((avg_hori(durs,wdurd_num)-ref_avgs[6])/ref_stds[6]))
print("p-life diff: %s" %((avg_hori(durs,pdurd_num)-ref_avgs[7])/ref_stds[7]))
print("pdi diff: %s" %((avg_hori(pdis,pdi_num)-ref_avgs[8])/ref_stds[8]))
print("ace diff: %s" %((avg_hori(aces,ace_num)-ref_avgs[9])/ref_stds[9]))
'''
print("\nmonth sig: %s" %(sig_calc(np.mean(mons_avg),ref_mons)))
print("yearly num sig: %s" %(sig_calc(np.mean(yrs_avg),ref_years)))
print("lat sig: %s" %(sig_calc(np.mean(lats_avg),ref_lats)))
print("lon sig: %s" %(sig_calc(np.mean(lons_avg),ref_lons)))
print("max wind sig: %s" %(sig_calc(np.mean(intsys_avg),ref_ints)))
print("min press sig: %s" %(sig_calc(np.mean(press_avg),ref_press)))
print("w-life sig: %s" %(sig_calc(np.mean(wdurs_avg),ref_wdurds)))
print("p-life sig: %s" %(sig_calc(np.mean(pdurs_avg),ref_pdurds)))
'''

print("\nsig calcs")
print("month & %s & %s \\\\" %(round(sig_calc(avg_hori(months,monthly_num),ref_mons)[0],3),round(sig_calc(avg_hori(months,monthly_num),ref_mons)[1],3)))
print("yearly num & %s & %s \\\\" %(round(sig_calc(np.mean(yrs_avg),ref_years)[0],3),round(sig_calc(np.mean(yrs_avg),ref_years)[1],3)))
print("lats & %s & %s \\\\" %(round(sig_calc(avg_hori(lats,lat_num),ref_lats)[0],3),round(sig_calc(avg_hori(lats,lat_num),ref_lats)[1],3)))
print("lons & %s & %s \\\\" %(round(sig_calc(avg_hori(lons,lon_num),ref_lons)[0],3),round(sig_calc(avg_hori(lons,lon_num),ref_lons)[1],3)))
print("max wind & %s & %s \\\\" %(round(sig_calc(avg_hori(intsys,intsy_num),ref_ints)[0],3),round(sig_calc(avg_hori(intsys,intsy_num),ref_ints)[1],3)))
print("min press & %s & %s \\\\" %(round(sig_calc(avg_hori(press,pres_num),ref_press)[0],3),round(sig_calc(avg_hori(press,pres_num),ref_press)[1],3)))
print("w-life & %s & %s \\\\" %(round(sig_calc(avg_hori(durs,wdurd_num),ref_wdurds)[0],3),round(sig_calc(avg_hori(durs,wdurd_num),ref_wdurds)[1],3)))
print("p-life & %s & %s \\\\" %(round(sig_calc(avg_hori(durs,pdurd_num),ref_pdurds)[0],3),round(sig_calc(avg_hori(durs,pdurd_num),ref_pdurds)[1],3)))
print("pdi & %s & %s \\\\" %(round(sig_calc(avg_hori(pdis,pdi_num),ref_pdi)[0],3),round(sig_calc(avg_hori(pdis,pdi_num),ref_pdi)[1],3)))
print("ace & %s & %s \\\\" %(round(sig_calc(avg_hori(aces,ace_num),ref_ace)[0],3),round(sig_calc(avg_hori(aces,ace_num),ref_ace)[1],3)))

if str(print_data)=="True":
    print("\nerup years: %s\n" %(start_years))
    print("erup strengths: %s\n" %(strengths))
    print("month diff: %s\n" %(mons_rat))
    print("yearly num diff: %s\n" %(yrs_rat))
    print("lat diff: %s\n" %(lats_rat))
    print("lon diff: %s\n" %(lons_rat))
    print("max wind diff: %s\n" %(intsys_rat))
    print("min press diff: %s\n" %(press_rat))
    print("w-life diff: %s\n" %(wdurs_rat))
    print("p-life diff: %s\n" %(pdurs_rat))
    print("pdi diff: %s\n" %(pdi_rat))
    print("ace diff: %s\n" %(ace_rat))

df = pd.DataFrame()
df["strength"]=strengths
df["month"]=mons_rat
df["number"]=yrs_rat
df["lats"]=lats_rat
df["lons"]=lons_rat
df["max wind"]=intsys_rat
df["min press"]=press_rat
df["w-life"]=wdurs_rat
df["p-life"]=pdurs_rat
df["pdi"]=pdi_rat
df["ace"]=ace_rat

sns.heatmap(df.corr())

if args.region=="north":
    plt.savefig("f_vs_c_dists_NH_corrs_%s.png" %(args.number),dpi=300)
elif args.region=="south":
    plt.savefig("f_vs_c_dists_SH_corrs_%s.png" %(args.number),dpi=300)
else:
    plt.savefig("f_vs_c_dists_corrs_%s.png" %(args.number),dpi=300)



def corrInfo(a,b):
    #val = round(np.corrcoef(a,b)[0][1],4)
    coeff, pval = stats.pearsonr(a,b)
    [l90,u90,l85,u85,l80,u80]=conInterval(coeff,len(a))
    return [coeff, pval,
            round(l90,4),round(u90,4),
            round(l85,4),round(u85,4),
            round(l80,4),round(u80,4),
            ]

if len(strengths)>1:
    headers=["coefficient","p-value","l90","u90","l85","u85","l80","u80"]   
    df = pd.DataFrame(columns=headers)
    df.loc["month"]=corrInfo(strengths,mons_rat)
    df.loc["yearly num"]=corrInfo(strengths,yrs_rat)
    df.loc["lats"]=corrInfo(strengths,lats_rat)
    df.loc["lons"]=corrInfo(strengths,lons_rat)
    df.loc["max wind"]=corrInfo(strengths,intsys_rat)
    df.loc["min press"]=corrInfo(strengths,press_rat)
    df.loc["w-life"]=corrInfo(strengths,wdurs_rat)
    df.loc["p-life"]=corrInfo(strengths,pdurs_rat)
    df.loc["pdi"]=corrInfo(strengths,pdi_rat)
    df.loc["ace"]=corrInfo(strengths,ace_rat)

    print(df)

yrs_plot=(np.asarray(yr_bins[:-1])+np.asarray(yr_bins[1:]))
yrs_plot=yrs_plot/2.0

fig_rows=5
fig_cols=2

plt.rc('font',size=7)
plt.rc('axes', titlesize=7)

fig=plt.figure(1)
outer_grid=gridspec.GridSpec(1,1,wspace=0.0,hspace=0.0)[0]
inner_grid = gridspec.GridSpecFromSubplotSpec(fig_rows, fig_cols,
              subplot_spec=outer_grid, wspace=0.6, hspace=0.9)

if args.number>=50:
    title="Storm Distributions (all eruptions)"
else:
    title="Storm Distributions (top %s eruptions)" %(args.number)
if args.region=="north":
    title="NH "+title
elif args.region=="south":
    title="SH "+title    
    
fig.suptitle(title)

ax = plt.Subplot(fig,inner_grid[0])
l1,l2=ax.plot(months,monthly_num/np.sum(monthly_num),'r',months,monthly_num2/np.sum(monthly_num2),'b')
fig.add_subplot(ax)
plt.title("Month")
plt.xlim([1,12])

ax = plt.Subplot(fig,inner_grid[1])
#ax.plot(yrs_plot,np.histogram(yearly_num,bins=30)[0],'r',yrs_plot,np.histogram(yearly_num2,bins=30)[0],'b')
yrs_plot=[n for n in range(len(yearly_num))]

yearly_num2_tmp=[]
stride = int(len(yearly_num2)/len(yearly_num))
for i in range(len(yearly_num)):
    if stride*(i+1)>=len(yearly_num2):
        val=np.mean(yearly_num2[stride*i:])
    else:
        val=np.mean(yearly_num2[stride*i:stride*(i+1)])
    yearly_num2_tmp.append(val)            

ax.plot(yrs_plot,yearly_num,'r',yrs_plot,yearly_num2_tmp,'b')
fig.add_subplot(ax)
plt.title("Years")
#plt.xlim([start_year,end_year])

ax = plt.Subplot(fig,inner_grid[2])
ax.plot(lats,lat_num/np.sum(lat_num),'r',lats,lat_num2/np.sum(lat_num2),'b')
fig.add_subplot(ax)
plt.title("Latitude")
plt.xlim([min_lat,max_lat])

ax = plt.Subplot(fig,inner_grid[3])
ax.plot(lons,lon_num/np.sum(lon_num),'r',lons,lon_num2/np.sum(lon_num2),'b')
fig.add_subplot(ax)
plt.title("Longitude")
plt.xlim([min_lon,max_lon])

ax = plt.Subplot(fig,inner_grid[4])
ax.plot(intsys,intsy_num/np.sum(intsy_num),'r',intsys,intsy_num2/np.sum(intsy_num2),'b')
fig.add_subplot(ax)
plt.title("Wind Speed (m/s)")
plt.xlim([min_wind,max_wind])

ax = plt.Subplot(fig,inner_grid[5])
ax.plot(press[::-1],pres_num[::-1]/np.sum(pres_num[::-1]),'r',press[::-1],pres_num2[::-1]/np.sum(pres_num2[::-1]),'b')
fig.add_subplot(ax)
plt.title("Pressure (mb)")
plt.xlim([min_press,max_press])

ax = plt.Subplot(fig,inner_grid[6])
ax.plot(durs,wdurd_num/np.sum(wdurd_num),'r',durs,wdurd_num2/np.sum(wdurd_num2),'b')
fig.add_subplot(ax)
plt.title("Wind Life (hrs)")
plt.xlim([0,6*len(wdurd_num)-6])

ax = plt.Subplot(fig,inner_grid[7])
ax.plot(durs,pdurd_num/np.sum(pdurd_num),'r',durs,pdurd_num2/np.sum(pdurd_num2),'b')
fig.add_subplot(ax)
plt.title("Press Life (hrs)")
plt.xlim([0,6*len(pdurd_num)-6])

ax = plt.Subplot(fig,inner_grid[8])
ax.plot(pdis,pdi_num/np.sum(pdi_num),'r',pdis,pdi_num2/np.sum(pdi_num2),'b')
fig.add_subplot(ax)
plt.title("PDI ($m^3/s^2$)")
plt.xlim([min_pdi,max_pdi-5*pdi_res])
#plt.xlim([min_pdi,max_pdi])
plt.ticklabel_format(axis="x", style="sci", scilimits=(0,0))

ax = plt.Subplot(fig,inner_grid[9])
ax.plot(aces,ace_num/np.sum(ace_num),'r',aces,ace_num2/np.sum(ace_num2),'b')
fig.add_subplot(ax)
plt.title("ACE ($m^2/s^2$)")
plt.xlim([min_ace,max_ace-5*ace_res])
#plt.xlim([min_ace,max_ace])
#plt.ticklabel_format(axis="x", style="sci", scilimits=(0,0))

fig.legend((l1,l2),('$LME_{forced}$','$LME_{control}$'),'upper left')

if args.region=="north":
    plt.savefig("f_vs_c_dists_NH_%s.png" %(args.number),dpi=300)
elif args.region=="south":
    plt.savefig("f_vs_c_dists_SH_%s.png" %(args.number),dpi=300)
else:
    plt.savefig("f_vs_c_dists_%s.png" %(args.number),dpi=300)

plt.clf()
