#     
import os, numpy
import Ngl, Nio

#
case="forced"
exp="wrf"

if exp=="wrf":
    dat_dir="~/PROJ_WRF/%s_mixed/T_sfc/diffs" %(case)
if exp=="cesm":
    #dat_dir="~/PROJ_WRF/%s_mixed/T_sfc/diffs" %(case)
    dat_dir="~/PROJ_WRF/%s/SST" %(case)

if case=="forced":

    s_years=[1213,1258,1274,1284,1452,1600,1641,1761,1809,1815]
    e_years=[1223,1274,1283,1294,1461,1609,1650,1770,1818,1825]
    cols=2-len(s_years)%2
    rows=int(len(s_years)/cols)

if case=="ctrl":
    s_years=[1000]
    e_years=[1100]
    rows=1
    cols=1


titles=[]
for i in range(len(s_years)):
    titles.append("SST Anomaly %s-%s" %(s_years[i],e_years[i]))

data={}
for i in range(len(s_years)):
    if exp=="wrf":
        data["dat"+str(i+1)]=dat_dir+"/T_sfc_%s_%s_%s_diff.nc" %(case,s_years[i],e_years[i])
    if exp=="cesm":
        data["dat"+str(i+1)]=dat_dir+"/SST_%s_%s_%s_diff.nc" %(case,s_years[i],e_years[i])


files={}
for i in range(len(s_years)):
    files["f"+str(i+1)]=Nio.open_file(data["dat"+str(i+1)])

temp=[]
for i in range(len(s_years)):
    if exp=="wrf":
        temp.append(files["f"+str(i+1)].variables["T_sfc_monthly"][0,:,:])
    if exp=="cesm":
        temp.append(files["f"+str(i+1)].variables["SST"][:,:])


lat  = files["f1"].variables["lat"][:]
lon  = files["f1"].variables["lon"][:]

rlist = Ngl.Resources()

wks_type = "pdf"
wks = Ngl.open_wks(wks_type,"T_sfc_diff_%s_%s_mixed" %(case,exp),rlist)

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
resources.mpMinLatF      = 0.0 #float(min(lat))
resources.mpMaxLatF      = 55.0 #float(max(lat))
resources.mpMinLonF      = -130.0 #float(min(lon))
resources.mpMaxLonF      = 10.0 #float(max(lon))
resources.mpProjection = "CylindricalEquidistant"
resources.pmLabelBarDisplayMode = "Never"

resources.cnLevelSelectionMode = "ManualLevels"
resources.cnMinLevelValF       = -5
resources.cnMaxLevelValF       = 5
resources.cnLevelSpacingF      = 0.25
resources.mpPerimOn       = True

plot = []
for i in range(len(s_years)):
    resources.tiMainString = titles[i]
    plot.append(Ngl.contour_map(wks,temp[i],resources))

panelres = Ngl.Resources()
panelres.nglPanelYWhiteSpacePercent = 5.
panelres.nglPanelXWhiteSpacePercent = 3.
panelres.nglPanelLabelBar                 = True 
panelres.nglPanelLabelBarWidthF           = 0.700 
panelres.nglPanelTop                      = 0.975
panelres.nglPanelFigureStrings            = ["A","B","C","D","E","F","G","H","I","J"]
panelres.nglPanelFigureStringsJust        = "BottomRight"

Ngl.panel(wks,plot[0:len(s_years)],[rows,cols],panelres)

Ngl.end()

