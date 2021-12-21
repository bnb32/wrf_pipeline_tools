#!/usr/bin/python
 
###############################################################################
#
#
###############################################################################

import numpy,sys,os

from diag_functions import *

from plot_functions import *

import matplotlib.pyplot as plt

import argparse

#---------- Get Arguments ------------------------------------------

parser = argparse.ArgumentParser(description='Plot diagnostics comparison')
parser.add_argument('-file1',default="/glade/u/home/bbenton/20XXWRF/DATA/TSTORMS_OUTPUT/erai_30km/WRF/run_9/traj_out_erai_1995_2005_9")
parser.add_argument('-file2',default="/glade/u/home/bbenton/20XXWRF/IBTRACS_DATA/TSTORMS_OUTPUT/ibtracs_v3/traj_out_ibtracs_v3_1995_2005")
parser.add_argument('-start_year',default=1995,type=int)
parser.add_argument('-end_year',default=2005,type=int)
parser.add_argument('-fig_name',default="erai_vs_ibtracs_diags")
args = parser.parse_args()

tcfilename = args.file1
compfile = args.file2
figname = args.fig_name
start_year = args.start_year
end_year = args.end_year

#---------- diag params -------------------#

min_lat = 0;max_lat = 55;lat_res = 1    
min_lon = -135;max_lon = 10;lon_res = 3
min_wind = 10.0;max_wind = 100.0;wind_res = 3.0
min_press = 850.0;max_press = 1020.0;press_res = 3.0

tstep = 6*60*60
min_pdi = 0.0; max_pdi = 1000000.0*tstep
pdi_res = (max_pdi-min_pdi)/50

min_ace = 0.0; max_ace = 100000.0*10**(-4)
ace_res = (max_ace-min_ace)/50

#dur_days = 15
dur_days = 15

year_avg = 3
ref_syear = 1000
ref_eyear = 1100

title = "Storm Number ( "+str(start_year)+"-"+str(end_year)+" )"

outer_grid = gridspec.GridSpec(1,3,wspace=0.3,hspace=0.3)

fig = plot_num_fig(tcfilename,start_year,end_year,
                 min_lat,max_lat,lat_res,min_lon,max_lon,lon_res,
		 min_wind,max_wind,wind_res,min_press,max_press,press_res,
		 dur_days,min_pdi,max_pdi,pdi_res,
         min_ace,max_ace,ace_res,outer_grid[0])

fig = plot_pval_fig(tcfilename,compfile,start_year,end_year,year_avg,
                 ref_syear,ref_eyear,
                 min_lat,max_lat,lat_res,min_lon,max_lon,lon_res,
		 min_wind,max_wind,wind_res,min_press,max_press,press_res,
		 dur_days,outer_grid[1],fig)

fig = plot_num_fig(compfile,ref_syear,ref_eyear,
                 min_lat,max_lat,lat_res,min_lon,max_lon,lon_res,
		 min_wind,max_wind,wind_res,min_press,max_press,press_res,
		 dur_days,outer_grid[2],fig)


all_axes = fig.get_axes()

for i in range(len(all_axes)):
    ax = all_axes[i]
    if i == 0:
        title = "Storm Number\n( Forced: "+str(start_year)+"-"+str(end_year)+" )"
        ax.text(1.3,1.4,title,size=8,horizontalalignment='center',transform=ax.transAxes)
    if i == 8:
        title = "P Value\n( "+str(start_year)+"-"+str(end_year)+" )"
        ax.text(1.3,1.4,title,size=8,horizontalalignment='center',transform=ax.transAxes)
    if i == 15:
        title = "Storm Number\n( Control: "+str(start_year)+"-"+str(end_year)+" )"
        ax.text(1.3,1.4,title,size=8,horizontalalignment='center',transform=ax.transAxes)

	
plt.savefig(figname+"_stats.png",bbox_inches='tight',dpi=600)
