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

if len(sys.argv) < 2:
    print "usage "+sys.argv[0]+": <case> <nrun>"
    sys.exit(1)
else:
    case = sys.argv[1]
    nrun = sys.argv[2]
    figname = case+"_tracks_all_"+str(nrun)+".pdf"


#---------- Setup Plotting  ------------------------------------------

#
#  Open a workstation and specify a different color map.
#
wkres = Ngl.Resources()
cmap = numpy.array([[1.,1.,1.],[0.,0.,0.], \
		    [0.2,0.8,1.],[0.4,1.,.8], \
		    [1.,1.,0.4],[1.,.7,0.2], \
		    [1.,0.5,0.],[1.,0.2,0.], \
		    [0.7,0.,0.]],'f')
wkres.wkColorMap = cmap
wks_type = "pdf"
wks = Ngl.open_wks(wks_type,figname,wkres)

#---------- Get storm tracks  ------------------------------------------

data = get_all_data(case,nrun)

ranges = [ "1213-1223",
           "1258-1274", 
           "1274-1283", 
           "1284-1294", 
           "1452-1461", 
           "1600-1609", 
           "1641-1650", 
           "1761-1770", 
           "1809-1818", 
           "1815-1825" ] 

# set up plot
resources = Ngl.Resources()
resources.nglFrame   = False       
resources.nglDraw   = False
resources.mpFillOn   = True
resources.mpLabelsOn = False
resources.mpOutlineOn = True
resources.mpLandFillColor = "grey"
resources.mpOceanFillColor = "blue"
resources.mpGridAndLimbOn = False
resources.vpXF       = 0.05
resources.vpYF       = 0.95
resources.vpWidthF   = 0.95
resources.vpHeightF  = 0.90
resources.tmXBTickStartF = -75
resources.tmXBTickEndF = -25
resources.tmYROn  = True
resources.tmXTOn  = True
resources.tmXBLabelFontHeightF = 0.02
resources.tmYLLabelFontHeightF = 0.02
resources.mpLimitMode = "LatLon"
resources.mpMinLonF = -140
resources.mpMaxLonF = 20
resources.mpMinLatF = -5
resources.mpMaxLatF = 60
resources.mpProjection = "CylindricalEquidistant"

# draw legend
txres = Ngl.Resources()
txres.txFontHeightF = 0.015
txres.txFontColor   =  1
txres.txFont        = 22

xleg = [0.07,0.19,0.32,0.44,0.57,0.7,0.83]
xtxt = [0.12,0.24,0.36,0.49,0.61,0.74,0.87]
yleg = [0.17,0.17,0.17,0.17,0.17,0.17,0.17]
ytxt = [0.17,0.17,0.17,0.17,0.17,0.17,0.17]
labels = ["TD","TS","Cat1","Cat2","Cat3","Cat4","Cat5"]

gxres = Ngl.Resources()
gxres.gsMarkerIndex = 16

for i in range(0,7):
    gxres.gsMarkerColor = 2+i
    Ngl.polymarker_ndc(wks,0.05+xleg[i],-0.15+yleg[i],gxres)
    Ngl.text_ndc(wks,labels[i],0.05+xtxt[i],-0.15+ytxt[i],txres)

#
#  Draw the trajectories.
#
pres = Ngl.Resources()        # polyline resources
pres.gsLineThicknessF = 2               # line thickness
pres.gsLineColor = "grey"
mres  = Ngl.Resources()                        # marker resources
mres.gsMarkerSizeF  = .0015        # marker size
mres.gsMarkerIndex = 16 # filled circle

plots = []
for k in range(10):
    resources.tiMainString = "Storm Tracks "+ranges[k]
    mplot = Ngl.map(wks,resources)    # Draw map.
    plots.append(mplot)

# loop through trajectories
for k in range(10):
    [tracks]=data[k]
    for i in range(len(tracks)):
    	nt = len(tracks[i][0])
    
    	for j in range(nt-1):
    	    x = tracks[i][0][j]
    	    y = tracks[i][1][j]
    	    w = tracks[i][2][j]
    	    p = tracks[i][3][j]
    
    	    x_pair = tracks[i][0][j:j+2]
    	    y_pair = tracks[i][1][j:j+2]
    	    
    
    	    if 10.0 <= w < 17.0: pres.gsLineColor = 2
    	    if 17.0 <= w < 32.0: pres.gsLineColor = 3
    	    if 32.0 <= w < 42.0: pres.gsLineColor = 4 
    	    if 42.0 <= w < 49.0: pres.gsLineColor = 5 
    	    if 49.0 <= w < 58.0: pres.gsLineColor = 6 
    	    if 58.0 <= w < 70.0: pres.gsLineColor = 7 
    	    if 70.0 <= w: pres.gsLineColor = 8
    	    
    	    # draw polyline
    	    Ngl.add_polyline(wks,plots[k],x_pair,y_pair,pres)
    #Ngl.frame(wks)
    #del mplot

panelres = Ngl.Resources()
panelres.nglPanelYWhiteSpacePercent = 5
panelres.nglPanelXWhiteSpacePercent = 3
panelres.nglPanelTop = 0.975
panelres.nglPanelBottom = 0.08

Ngl.panel(wks,plots[0:10],[5,2],panelres)

Ngl.end()

