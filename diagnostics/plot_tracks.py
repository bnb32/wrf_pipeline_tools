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
    figname = tcfilename+"_tracks.pdf"


#---------- Setup Plotting  ------------------------------------------

#
#  Open a workstation and specify a different color map.
#
wkres = Ngl.Resources()
#wkres.wkColorMap = "default"
cmap = numpy.array([[1.,1.,1.],[0.,0.,0.], \
		    [0.2,0.8,1.],[0.4,1.,.8], \
		    [1.,1.,0.4],[1.,.7,0.2], \
		    [1.,0.5,0.],[1.,0.2,0.], \
		    [0.7,0.,0.]],'f')
wkres.wkColorMap = cmap
#wks_type = "x11"
wks_type = "pdf"
#wkres.wkOrientation = "landscape"
wks = Ngl.open_wks(wks_type,figname,wkres)
#wks_map = Ngl.open_wks(wks_type,"example",wkres)
#Ngl.draw_colormap(wks_map)

#---------- Get storm tracks  ------------------------------------------

[tracks] = read_trajectories(tcfilename)

# set up plot
resources = Ngl.Resources()
resources.nglFrame   = False         # don't advance frame
resources.vpWidthF   = 0.95          # make map bigger
resources.vpHeightF  = 0.95
resources.mpLimitMode = "LatLon"

resources.mpFillOn   = True
resources.mpLabelsOn = True
resources.mpOutlineOn = True
#resources.mpLandFillColor = "green"
#resources.mpOceanFillColor = "blue"
resources.mpLandFillColor = "grey"
resources.mpOceanFillColor = "white"
resources.mpGridAndLimbOn = False
resources.vpXF       = 0.05
resources.vpYF       = 0.95
resources.vpWidthF   = 0.95
resources.vpHeightF  = 0.95
resources.tmXBTickStartF = -75
resources.tmXBTickEndF = -25
resources.tmYROn  = True
resources.tmXTOn  = True
resources.tmXBLabelFontHeightF = 0.02
resources.tmYLLabelFontHeightF = 0.02
resources.mpLimitMode = "LatLon"
resources.mpMinLonF = -100
resources.mpMaxLonF = -60
resources.mpMinLatF = 0
resources.mpMaxLatF = 40
#resources.mpMinLonF = -140
#resources.mpMaxLonF = 20
#resources.mpMinLatF = -5
#resources.mpMaxLatF = 60
resources.mpProjection = "CylindricalEquidistant"
map = Ngl.map(wks,resources)    # Draw map.

#
#  Main title.
#
txres = Ngl.Resources()
txres.txFontHeightF = 0.025
txres.txFontColor   =  1
txres.txFont        = 22
Ngl.text_ndc(wks,"Hurricane Katrina",0.52,0.85,txres)

# draw legend

yl=0.09

xleg = [0.07,0.19,0.32,0.44,0.57,0.7,0.83]
xtxt = [0.12,0.24,0.36,0.49,0.61,0.74,0.87]
yleg = [yl,yl,yl,yl,yl,yl,yl]
ytxt = [yl,yl,yl,yl,yl,yl,yl]
labels = ["TD","TS","Cat1","Cat2","Cat3","Cat4","Cat5"]

txres.txFontHeightF = 0.015

gxres = Ngl.Resources()
gxres.gsMarkerIndex = 16

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
pres.gsLineThicknessF = 6               # line thickness
pres.gsLineColor = "grey"
mres  = Ngl.Resources()                        # marker resources
mres.gsMarkerSizeF  = .0015        # marker size
mres.gsMarkerIndex = 16 # filled circle

# loop through trajectories
for i in range(len(tracks)):
	nt = len(tracks[i][0])

#	x_all = tracks[i][0][0:nt]
#	y_all = tracks[i][1][0:nt]

        #Ngl.polyline(wks,map,x_all,y_all,pres)
	
	for j in range(nt-1):
		x = tracks[i][0][j]
		y = tracks[i][1][j]
		w = tracks[i][2][j]
		p = tracks[i][3][j]

		x_pair = tracks[i][0][j:j+2]
		y_pair = tracks[i][1][j:j+2]
		
		#print x, y, w, p

		#if p > 980.0: mres.gsMarkerColor = 4 
		#if 980.0 > p > 965.0: mres.gsMarkerColor = 5 
		#if 965.0 > p > 945.0: mres.gsMarkerColor = 6
		#if 945.0 > p > 920.0: mres.gsMarkerColor = 7 
		#if p < 920.0: mres.gsMarkerColor = 8 
		
		
	##	if w < 17.0: mres.gsMarkerColor = 2
	##	if 17.0 <= w < 32.0: mres.gsMarkerColor = 3
	##	if 32.0 <= w < 42.0: mres.gsMarkerColor = 4 
	##	if 42.0 <= w < 49.0: mres.gsMarkerColor = 5 
	##	if 49.0 <= w < 58.0: mres.gsMarkerColor = 6 
	##	if 58.0 <= w < 70.0: mres.gsMarkerColor = 7 
	##	if 70.0 <= w: mres.gsMarkerColor = 8

	        if 10.0 <= w < 17.0: pres.gsLineColor = 2
		if 17.0 <= w < 32.0: pres.gsLineColor = 3
		if 32.0 <= w < 42.0: pres.gsLineColor = 4 
		if 42.0 <= w < 49.0: pres.gsLineColor = 5 
		if 49.0 <= w < 58.0: pres.gsLineColor = 6 
		if 58.0 <= w < 70.0: pres.gsLineColor = 7 
		if 70.0 <= w: pres.gsLineColor = 8
		
		# Draw polymarkers at each point
		#Ngl.polymarker(wks,map,[x],[y],mres) 

		# draw polyline
		Ngl.polyline(wks,map,x_pair,y_pair,pres)

	
Ngl.frame(wks)

#---------- Clean up ------------------------------------------

# (not really necessary, but a good practice).

del map
del resources
del mres
del pres
# others...

Ngl.end()

