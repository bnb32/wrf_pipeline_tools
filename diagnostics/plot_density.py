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

import Nio #  for reading netCDF files

import Ngl
from diag_functions import *


# import Scientific.IO.NetCDF # 

#---------- Get Arguments ------------------------------------------

if len(sys.argv) < 1:
    print "usage "+sys.argv[0]+": <infile>"
    sys.exit(1)
else:
    tcfilename = sys.argv[1]
    figname = tcfilename + "_density.pdf"


#---------- Setup Plotting  ------------------------------------------

minLat = -5
maxLat = 60
minLon = -140
maxLon = 20
LatRes = 1
LonRes = 1

LatBoxNum = (maxLat - minLat)/LatRes
LonBoxNum = (maxLon - minLon)/LonRes
WindNum = 1000

storm_sort = numpy.zeros((LonBoxNum,LatBoxNum,WindNum))

for i in range(LonBoxNum):
    lon = minLon + i*LonRes
    for j in range(LatBoxNum):
        lat = minLat + j*LatRes
	storm_sort[i,j,0] = lon
	storm_sort[i,j,1] = lat

#
#  Open a workstation and specify a different color map.
#
wkres = Ngl.Resources()
cmap = numpy.array([[1.,1.,1.],[0.,0.,0.], \
		    [0.2,0.8,1.],[0.4,1.,.8], \
		    [1.,1.,0.4],[1.,.7,0.2], \
		    [1.,0.5,0.],[1.,0.2,0.], \
		    [.7,0.,0.]],'f')
wkres.wkColorMap = cmap
wks_type = "pdf"
wks = Ngl.open_wks(wks_type,figname,wkres)

#---------- Get storm tracks  ------------------------------------------

[tracks] = read_trajectories(tcfilename)

# set up plot
resources = Ngl.Resources()
resources.nglFrame   = False         # don't advance frame
resources.mpFillOn   = True
resources.mpLabelsOn = True
resources.mpOutlineOn = True
resources.mpLandFillColor = "grey"
resources.mpOceanFillColor = "blue"
resources.mpGridAndLimbOn = False
resources.vpXF       = 0.05
resources.vpYF       = 0.95
resources.vpWidthF   = 0.8
resources.vpHeightF  = 0.8
resources.tmXBTickStartF = -75
resources.tmXBTickEndF = -25
resources.tmYROn  = True
resources.tmXTOn  = True
resources.tmXBLabelFontHeightF = 0.02
resources.tmYLLabelFontHeightF = 0.02
resources.mpLimitMode = "LatLon"
resources.mpMinLonF = minLon
resources.mpMaxLonF = maxLon
resources.mpMinLatF = minLat
resources.mpMaxLatF = maxLat
resources.mpProjection = "CylindricalEquidistant"
map = Ngl.map(wks,resources)    # Draw map.

#
#  Main title.
#
txres = Ngl.Resources()
txres.txFontHeightF = 0.025
txres.txFontColor   =  1
txres.txFont        = 22
Ngl.text_ndc(wks,"Storm Density",0.52,0.75,txres)

# draw legend

num_0 = 0
num_1 = 2
num_2 = 4
num_3 = 6
num_4 = 8
num_5 = 10
num_6 = 12

range1 = "<"+str(num_1)
range2 = str(num_1)+"-"+str(num_2)
range3 = str(num_2)+"-"+str(num_3)
range4 = str(num_3)+"-"+str(num_4)
range5 = str(num_4)+"-"+str(num_5)
range6 = str(num_5)+"-"+str(num_6)
range7 = str(num_6)+"<"

labels = [range1,range2,range3,range4,range5,range6,range7]

txres.txFontHeightF = 0.015

gxres = Ngl.Resources()
gxres.gsMarkerIndex = 16

xleg = [0.07,0.19,0.32,0.44,0.57,0.7,0.83]
xtxt = [0.12,0.24,0.36,0.49,0.61,0.74,0.87]
yleg = [0.17,0.17,0.17,0.17,0.17,0.17,0.17]
ytxt = [0.17,0.17,0.17,0.17,0.17,0.17,0.17]

for i in range(0,7):
    gxres.gsMarkerColor = 2+i
    Ngl.polymarker_ndc(wks,0.05+xleg[i],0.1+yleg[i],gxres)
    Ngl.text_ndc(wks,labels[i],0.05+xtxt[i],0.1+ytxt[i],txres)

del txres
del gxres

#
#  Draw the trajectories.
#
pres = Ngl.Resources()        # polyline resources
pres.gsLineThicknessF = 2               # line thickness
pres.gsLineColor = "grey"
mres  = Ngl.Resources()                        # marker resources
mres.gsMarkerSizeF  = .005        # marker size
mres.gsMarkerIndex = 16 # filled circle


# loop through trajectories
for i in range(len(tracks)):
    nt = len(tracks[i][0])
	
    for j in range(nt-1):
        x = tracks[i][0][j]
	y = tracks[i][1][j]
	w = tracks[i][2][j]
	p = tracks[i][3][j]

	lon_idx = (numpy.abs(storm_sort[:,0,0]-x)).argmin()
	lat_idx = (numpy.abs(storm_sort[0,:,1]-y)).argmin()
	wind_idx = numpy.count_nonzero(storm_sort[lon_idx,lat_idx,2:])

	storm_sort[lon_idx,lat_idx,2+wind_idx] = w


for i in range(LonBoxNum):
    lon = minLon + i*LonRes
    for j in range(LatBoxNum):
        lat = minLat + j*LatRes
	
	storm_num = numpy.count_nonzero(storm_sort[i,j,2:])

	if num_0 < storm_num < num_1: mres.gsMarkerColor = 2
	if num_1 <= storm_num < num_2: mres.gsMarkerColor = 3
	if num_2 <= storm_num < num_3: mres.gsMarkerColor = 4 
	if num_3 <= storm_num < num_4: mres.gsMarkerColor = 5 
	if num_4 <= storm_num < num_5: mres.gsMarkerColor = 6 
	if num_5 <= storm_num < num_6: mres.gsMarkerColor = 7 
	if num_6 <= storm_num: mres.gsMarkerColor = 8

	# Draw polymarkers at each point
	if storm_num > 0: Ngl.polymarker(wks,map,[lon],[lat],mres) 

	# draw polyline
	#Ngl.polyline(wks,map,x_pair,y_pair,pres)

	
Ngl.frame(wks)

#---------- Clean up ------------------------------------------

# (not really necessary, but a good practice).

del map
del resources
del mres
del pres
# others...

Ngl.end()

