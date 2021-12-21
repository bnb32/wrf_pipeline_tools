#!/usr/bin/python
 
###############################################################################
#
#
###############################################################################

import numpy,sys,os

from diag_functions import *

from plot_functions import *

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

import pandas

#---------- Get Arguments ------------------------------------------

if len(sys.argv) < 2:
    print "usage "+sys.argv[0]+": <case> <nrun>"
    sys.exit(1)
else:
    nrun=sys.argv[2]
    case=sys.argv[1]
    tcfilename_ctrl = "/glade/u/home/bbenton/TSTORMS_OUTPUT/ctrl/WRF/run_4/traj_out_ctrl_all_4"

#---------- diag params -------------------#


year_avg=3

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

ref_syear = 1000
ref_eyear = 1100

#---------- run diagnostics  ----------------#   

start_years = [1213,1258,1274,1284,1452,1600,1641,1761,1809,1815]
end_years = [1223,1274,1283,1294,1461,1609,1650,1770,1818,1825]
titles = []

for i in range(10):
    title = "P-values "+str(start_years[i])+"-"+str(end_years[i])
    titles.append(title)

files = get_all_files(case,nrun)

fig_rows=2
fig_cols=2

fig = plt.figure(1)

outer_grid = gridspec.GridSpec(fig_rows, fig_cols, wspace=0.3, hspace=0.3)
#figure,axes = plt.subplots(fig_rows,fig_cols)

#fig = plot_pval_fig(files[0],tcfilename_ctrl,start_years[0],end_years[0],
#                        year_avg,ref_syear,ref_eyear,min_lat,max_lat,
#			lat_res,min_lon,max_lon,lon_res,min_wind,
#			max_wind,wind_res,min_press,max_press,press_res,dur_days,
#			outer_grid,fig,titles[0])
#
for i in range(4):

    fig = plot_pval_fig(files[i],tcfilename_ctrl,start_years[i],end_years[i],
                        year_avg,ref_syear,ref_eyear,min_lat,max_lat,
			lat_res,min_lon,max_lon,lon_res,min_wind,
			max_wind,wind_res,min_press,max_press,press_res,dur_days,
			outer_grid[i],fig,titles[i])



all_axes = fig.get_axes()

for ax in all_axes:
    for sp in ax.spines.values():
        sp.set_visible(True)
    if ax.is_first_row():
        ax.spines['top'].set_visible(False)
    if ax.is_last_row():
        ax.spines['bottom'].set_visible(False)
    if ax.is_first_col():
	ax.spines['left'].set_visible(False)
    if ax.is_last_col():
	ax.spines['right'].set_visible(False)

plt.savefig("all_pvals.pdf")


