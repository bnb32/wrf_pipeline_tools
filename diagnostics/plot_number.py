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

tcfilename1 = args.file1
tcfilename2 = args.file2
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

title = "Storm Distributions ( "+str(start_year)+"-"+str(end_year)+" )"

fig = plot_num_fig(tcfilename1, tcfilename2, start_year,end_year,
                 min_lat,max_lat,lat_res,min_lon,max_lon,lon_res,
		 min_wind,max_wind,wind_res,min_press,max_press,press_res,
		 dur_days,min_pdi,max_pdi,pdi_res,min_ace,max_ace,ace_res,title=title)

plt.savefig(figname,bbox_inches='tight',dpi=300)
