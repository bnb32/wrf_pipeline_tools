#     
import os
import numpy as np
import Ngl, Nio
from plot_functions import *

data_dir="~/PROJ_WRF/%s/%s/"
post_file="wrfpost_%s_%s_%s.nc"
tstorms_file="wrf_tstorms_%s_%s.nc"

s_num=0
e_num=10

s_ctrl=1000
e_ctrl=1100

lat_max=221
lon_max=480

rows=5
cols=2

start_years=[1188, 1213, 1232, 1258, 1268, 1275, 1284, 1307, 1316, 1328, 1341, 1358, 1370, 1381, 1416, 1452, 1459, 1474, 1480, 1503, 1512, 1526, 1534, 1584, 1593, 1600, 1619, 1641, 1673, 1693, 1711, 1719, 1729, 1738, 1756, 1762, 1794, 1796, 1809, 1815, 1831, 1835, 1862, 1883, 1886, 1903, 1911, 1925, 1963, 1976]

strengths=[0.0002844205, 0.0039387355, 0.0013156489, 0.018610299, 0.0014670904, 0.00577007, 0.0042582103, 0.00011168822, 0.00017321129, 0.0011022617, 0.0027219066, 0.00010316961, 0.0002691743, 0.0004988108, 0.00069950486, 0.01123978, 0.0012253568, 0.00031424107, 0.00039538497, 9.6238095e-05, 0.00023723794, 0.0001980713, 0.0003649701, 0.0013540474, 0.0009029704, 0.0035108852, 0.0004950247, 0.0035000157, 0.0012742055, 0.0025623553, 0.0003653527, 0.0017625, 0.0006352736, 0.00032004144, 0.00041724482, 0.004875931, 0.00017844126, 0.0003748809, 0.003996972, 0.0080638705, 0.0009511905, 0.0027239982, 0.00041456614, 0.0016446952, 0.00018493412, 0.00036901433, 0.00061599945, 0.00034734656, 0.0014599211, 0.00025356218]

s_years=[]


str_sort=sorted(strengths)
str_sort=str_sort[s_num:e_num]
for x in str_sort:
    idx=(np.abs(np.array(strengths)-x)).argmin()
    s_years.append(start_years[idx])

e_years=[x+1 for x in s_years]

titles=[]
for i in range(len(s_years)):
    titles.append("PI Anomaly %s-%s" %(s_years[i],e_years[i]))


'''
PI_ctrl=get_PI_chunk("ctrl",s_ctrl,e_ctrl)
PI_ctrl.dump("pi_ctrl_array_fdfu_lh")
exit()
'''

PI_ctrl=np.load("pi_ctrl_array_fdfu_lh")
PI_ctrl=PI_ctrl[0:lat_max,0:lon_max]

lat,lon=get_lat_lon("ctrl",s_ctrl)
temp=[]
temp_avg=get_PI_chunk("forced",s_years[0],e_years[0])[0:lat_max,0:lon_max]
print(s_years[0])
for i in range(1,len(s_years)):
    print(s_years[i])
    temp_avg+=get_PI_chunk("forced",s_years[i],e_years[i])[0:lat_max,0:lon_max]
temp_avg=get_PI_frac(PI_ctrl,temp_avg[:,:]/float(len(s_years)))

for i in range(len(s_years)):
   temp.append(get_PI_frac(PI_ctrl,get_PI_chunk("forced",s_years[i],e_years[i])[:lat_max,0:lon_max]))
   
rlist = Ngl.Resources()

wks_type = "pdf"
wks = Ngl.open_wks(wks_type,"PI_diff_%s" %s_num,rlist)
wks_avg = Ngl.open_wks(wks_type,"PI_diff_%s_avg" %s_num,rlist)

resources = Ngl.Resources()
resources.nglDraw  = False
resources.nglFrame   = False   
resources.cnFillOn        = True
resources.cnFillPalette   = "BlueYellowRed"
resources.cnLinesOn       = False
resources.cnLineLabelsOn  = False

## Scalar field resources
resources.sfXArray        = lon
resources.sfYArray        = lat

# Map resources

resources.mpFillDrawOrder        = "PostDraw"
resources.mpLandFillColor        = "Gray"
resources.mpOceanFillColor       = "Transparent"
resources.mpInlandWaterFillColor = "Transparent"
resources.mpGridMaskMode         = "MaskLand"
#del resources.tiMainString

resources.vpWidthF   = 0.95
resources.vpHeightF  = 0.95
resources.mpLimitMode = "LatLon"

resources.mpFillOn   = True
resources.mpLabelsOn = False
resources.mpOutlineOn = True
resources.mpGridAndLimbOn = False
resources.tmXBLabelFontHeightF = 0.02
resources.tmYLLabelFontHeightF = 0.02
resources.mpMinLatF      = 5.0 #float(min(lat))
resources.mpMaxLatF      = 55.0 #float(max(lat))
resources.mpMinLonF      = -130.0 #float(min(lon))
resources.mpMaxLonF      = 10.0 #float(max(lon))
resources.mpProjection = "CylindricalEquidistant"
resources.pmLabelBarDisplayMode = "Never"

resources.cnLevelSelectionMode = "ManualLevels"
resources.cnMinLevelValF       = -0.05
resources.cnMaxLevelValF       = 0.05
resources.cnLevelSpacingF      = 0.01
resources.mpPerimOn       = True

resources_avg = resources

plot = []
plot_avg=[]
for i in range(len(s_years)):
    resources.tiMainString = titles[i]
    plot.append(Ngl.contour_map(wks,temp[i],resources))

resources_avg.tiMainString = "PI Average Anomaly"
plot_avg.append(Ngl.contour_map(wks_avg,temp_avg,resources_avg))

panelres = Ngl.Resources()
panelres.nglPanelYWhiteSpacePercent = 5.
panelres.nglPanelXWhiteSpacePercent = 3.
panelres.nglPanelLabelBar                 = True 
panelres.nglPanelLabelBarWidthF           = 0.700 
panelres.nglPanelTop                      = 0.975
panelres.nglMaximize=True

panelres_avg=panelres
panelres_avg.nglMaximize=True

panelres.nglPanelFigureStrings            = ["A","B","C","D","E","F","G","H","I","J"]
panelres.nglPanelFigureStringsJust        = "BottomRight"

Ngl.panel(wks,plot[0:int(rows*cols)],[rows,cols],panelres)
Ngl.panel(wks_avg,plot_avg,[1,1],panelres_avg)

print("avg PI diff")
print(np.mean(temp_avg[:,:]))

Ngl.end()

