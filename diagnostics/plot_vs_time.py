#!/usr/bin/python
 
###############################################################################
#
#
###############################################################################

#
# MODULES
#
#import Numeric,sys,os
import numpy,sys,os

from diag_functions import *

import matplotlib.pyplot as plt


#---------- Get Arguments ------------------------------------------

if len(sys.argv) < 2:
    print "usage: plot_vs_time.py <infile> <outfile>"
    sys.exit(1)
else:
    tcfilename = sys.argv[1]
    figname = sys.argv[2]


#---------- Setup Plotting  ------------------------------------------


#---------- Get storm tracks  ------------------------------------------

[tracks] = read_trajectories(tcfilename)

plt.title("Intensity vs Time")
plt.ylabel("Wind Speed (m/s)")
plt.xlabel("Time (hrs)")

# loop through trajectories
#for i in range(len(tracks)):
for i in range(2):
    nt = len(tracks[i][0])

    time = []
    wind = []

    for j in range(nt-1):
	x = tracks[i][0][j]
	y = tracks[i][1][j]
	w = tracks[i][2][j]
	p = tracks[i][3][j]

        time.append(6.0*j)
	wind.append(w)

    plt.plot(time,wind)

plt.savefig(figname)


