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

#import Nio #  for reading netCDF files

import Ngl
from diag_functions import *


# import Scientific.IO.NetCDF # 

#---------- Get Arguments ------------------------------------------


if len(sys.argv) < 2:
    print("usage "+sys.argv[0]+": <file1> <file2> ... <fileN> <title>")
    sys.exit(1)
else:
    title = sys.argv[len(sys.argv)-1]
    files={}
    for i in range(1,len(sys.argv)-1):
        files[i-1]=sys.argv[i]
    figname = title.replace(" ","_")+"_tracks"




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
wks_type = "eps"
wks = Ngl.open_wks(wks_type,figname,wkres)

#---------- Get storm tracks  ------------------------------------------


# set up plot
resources = Ngl.Resources()
resources.nglFrame   = False       
resources.nglDraw   = False
resources.mpFillOn   = True
resources.mpLabelsOn = False
resources.mpOutlineOn = True
resources.mpLandFillColor = "grey"
resources.mpOceanFillColor = "white"
resources.mpGridAndLimbOn = False
resources.vpXF       = 0.05
resources.vpYF       = 0.95
resources.vpWidthF   = 0.95
resources.vpHeightF  = 0.90
resources.tmXBTickStartF = -75
resources.tmXBTickEndF = -25
resources.tmYROn  = True
resources.tmXTOn  = True
resources.tmXBLabelFontHeightF = 0.022
resources.tmYLLabelFontHeightF = 0.022
resources.mpLimitMode = "LatLon"
resources.mpMinLonF = -140
resources.mpMaxLonF = 20
resources.mpMinLatF = -5
resources.mpMaxLatF = 60
resources.mpProjection = "CylindricalEquidistant"

# draw title
txres = Ngl.Resources()
txres.txFontHeightF = 0.025
txres.txFontColor   =  1
txres.txFont        = 22
Ngl.text_ndc(wks,title,0.52,0.98,txres)


# draw legend

yl=0.19
scale=0.75
shift=0.10
txres.txFontHeightF = 0.015
xleg = [0.07,0.19,0.31,0.43,0.56,0.69,0.82]
xtxt = [0.12,0.24,0.36,0.49,0.61,0.74,0.87]
for i in range(len(xleg)):
    xleg[i]=shift+scale*xleg[i]
for i in range(len(xtxt)):
    xtxt[i]=shift+scale*xtxt[i]
yleg = [yl,yl,yl,yl,yl,yl,yl]
ytxt = [yl,yl,yl,yl,yl,yl,yl]
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
for k in range(len(files)):
    #if k==0: resources.tiMainString = title
    mplot = Ngl.map(wks,resources)    # Draw map.
    plots.append(mplot)


# loop through trajectories
for k in range(len(files)):
    [tracks]=read_trajectories(files[k])
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
panelres.nglPanelYWhiteSpacePercent = 3
panelres.nglPanelXWhiteSpacePercent = 0
panelres.nglPanelTop = 0.95
panelres.nglPanelBottom = 0.08
panelres.nglPanelFigureStrings = ["A","B","C"]
panelres.nglPanelFigureStringsJust = "BottomRight"
panelres.nglPanelFigureStringsFontHeightF = 0.02

Ngl.panel(wks,plots,[len(files),1],panelres)

Ngl.end()

