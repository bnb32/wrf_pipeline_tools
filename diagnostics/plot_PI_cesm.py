#     
#import os
import numpy as np
import Ngl, Nio
from scipy import stats
#from plot_functions import get_PI_frac

def get_PI_frac(PI_ctrl,PI_forced):
    #return PI_forced[:,:]/PI_ctrl[:,:]-1.0
    return np.sqrt(PI_forced[:,:]/PI_ctrl[:,:])-1.0

def t_test(data1,data2):
    dat1 = np.histogram(np.asarray(data1)/float(np.sum(data1)),500)[0]
    dat2 = np.histogram(np.asarray(data2)/float(np.sum(data2)),500)[0]

    #[Dval, pval] = stats.ttest_rel(dat1,dat2)
    [Dval, pval] = stats.ttest_ind(dat1,dat2)

    return [Dval,pval]

data_dir="/glade/p/cesm/community/cesmLME/CESM-CAM5-LME/atm/proc/tseries/monthly/%s/"
ctrl_file="b.e11.BLMTRC5CN.f19_g16.850forcing.003.cam.h0.%s.085001-184912.nc"
forced_file1="b.e11.BLMTRC5CN.f19_g16.007.cam.h0.%s.085001-184912.nc"
forced_file2="b.e11.BLMTRC5CN.f19_g16.007.cam.h0.%s.185001-200512.nc"

s_num=50

s_ctrl=950
e_ctrl=1100

min_lat=5
max_lat=55
min_lon=-130
max_lon=10

rows=5
cols=2

def get_lat_lon_cesm():
     ll_file=Nio.open_file(data_dir %("T") + ctrl_file %("T"));
     lat=ll_file.variables["lat"].get_value()
     lon=ll_file.variables["lon"].get_value()
     for i in range(len(lon)):
         if lon[i]>180.0: lon[i]-=360.0

     return lat,lon



lat,lon=get_lat_lon_cesm()

min_lat_idx=(np.abs(lat-min_lat)).argmin()
max_lat_idx=(np.abs(lat-max_lat)).argmin()
min_lon_idx=(np.abs(lon-min_lon)).argmin()
max_lon_idx=(np.abs(lon-max_lon)).argmin()

lat=lat[min_lat_idx:max_lat_idx+1]
lon=np.concatenate((lon[min_lon_idx:],lon[0:max_lon_idx+1]),axis=0)

def yidx(s_year,fs_year):
    return (s_year-fs_year)*12-1

def get_PI_chunk_cesm(case,s_year,e_year):
    if case=="ctrl":
        T_file=Nio.open_file(data_dir %("T") + ctrl_file %("T"));
        LH_file=Nio.open_file(data_dir %("LHFLX") + ctrl_file %("LHFLX"));
        fs_year=850
    if case=="forced" and e_year < 1850:
        T_file=Nio.open_file(data_dir %("T") + forced_file1 %("T"));
        LH_file=Nio.open_file(data_dir %("LHFLX") + forced_file1 %("LHFLX"));
        fs_year=850
    if case=="forced" and e_year >= 1850:        
        T_file=Nio.open_file(data_dir %("T") + forced_file2 %("T"));
        LH_file=Nio.open_file(data_dir %("LHFLX") + forced_file2 %("LHFLX"));
        fs_year=1850

    T1=T_file.variables["T"][yidx(s_year,fs_year):yidx(e_year,fs_year)+1,:,min_lat_idx:max_lat_idx+1,0:max_lon_idx+1]
    T2=T_file.variables["T"][yidx(s_year,fs_year):yidx(e_year,fs_year)+1,:,min_lat_idx:max_lat_idx+1,min_lon_idx:]

    T=np.concatenate((T2,T1),axis=3)
    T_sfc=T[:,29,:,:]
    T_top=T[:,12,:,:]
    
    LH1=LH_file.variables["LHFLX"][yidx(s_year,fs_year):yidx(e_year,fs_year)+1,min_lat_idx:max_lat_idx+1,0:max_lon_idx+1]
    LH2=LH_file.variables["LHFLX"][yidx(s_year,fs_year):yidx(e_year,fs_year)+1,min_lat_idx:max_lat_idx+1,min_lon_idx:]

    LH=np.concatenate((LH2,LH1),axis=2)
    
    PI=(T_sfc-T_top)/T_sfc*LH
    PI_dist=np.zeros((e_year-s_year+1,PI.shape[1],PI.shape[2]))

    PI_mean=(np.mean(T_sfc,axis=0)-np.mean(T_top,axis=0))/np.mean(T_sfc,axis=0)*np.mean(LH,axis=0)

    for i in range(e_year-s_year+1):
        PI_dist[i,:,:]=np.mean(PI[i*12:(i+1)*12,:,:],axis=0)
    PI_dist*=(1/float(e_year-s_year+1))

    return [PI_mean,PI_dist]

def get_sig_array(PI_dist,temp_dist):
    lat_dim=PI_dist.shape[1]
    lon_dim=PI_dist.shape[2]
    sig_array=np.zeros((lat_dim,lon_dim))
    for i in range(lat_dim):
        for j in range(lon_dim):
            pdist_tmp=PI_dist[:,i,j]
            tdist_tmp=temp_dist[:,i,j]
            [dval,pval]=t_test(pdist_tmp,tdist_tmp)
            sig_array[i,j]=pval
    return sig_array            


start_years=[1188, 1213, 1232, 1258, 1268, 1275, 1284, 1307, 1316, 1328, 1341, 1358, 1370, 1381, 1416, 1452, 1459, 1474, 1480, 1503, 1512, 1526, 1534, 1584, 1593, 1600, 1619, 1641, 1673, 1693, 1711, 1719, 1729, 1738, 1756, 1762, 1794, 1796, 1809, 1815, 1831, 1835, 1862, 1883, 1886, 1903, 1911, 1925, 1963, 1976]

strengths=[0.0002844205, 0.0039387355, 0.0013156489, 0.018610299, 0.0014670904, 0.00577007, 0.0042582103, 0.00011168822, 0.00017321129, 0.0011022617, 0.0027219066, 0.00010316961, 0.0002691743, 0.0004988108, 0.00069950486, 0.01123978, 0.0012253568, 0.00031424107, 0.00039538497, 9.6238095e-05, 0.00023723794, 0.0001980713, 0.0003649701, 0.0013540474, 0.0009029704, 0.0035108852, 0.0004950247, 0.0035000157, 0.0012742055, 0.0025623553, 0.0003653527, 0.0017625, 0.0006352736, 0.00032004144, 0.00041724482, 0.004875931, 0.00017844126, 0.0003748809, 0.003996972, 0.0080638705, 0.0009511905, 0.0027239982, 0.00041456614, 0.0016446952, 0.00018493412, 0.00036901433, 0.00061599945, 0.00034734656, 0.0014599211, 0.00025356218]

s_years=[]


str_sort=sorted(strengths)
str_sort=str_sort[-s_num:]
for x in str_sort:
    idx=(np.abs(np.array(strengths)-x)).argmin()
    s_years.append(start_years[idx])

e_years=[x+1 for x in s_years]

titles=[]
for i in range(len(s_years)):
    titles.append("PI Anomaly %s-%s" %(s_years[i],e_years[i]))

'''
[PI_ctrl,PI_dist]=get_PI_chunk_cesm("ctrl",s_ctrl,e_ctrl)
PI_ctrl.dump("pi_ctrl_array_cesm")
PI_dist.dump("pi_ctrl_dist_cesm")
exit()
'''

PI_ctrl=np.load("pi_ctrl_array_cesm",allow_pickle=True)
PI_dist=np.load("pi_ctrl_dist_cesm",allow_pickle=True)

temp=[]
[temp_avg,temp_dist]=get_PI_chunk_cesm("forced",s_years[0],e_years[0]);
print(s_years[0])

for i in range(1,len(s_years)):
    print(s_years[i])
    [tavg,tdist]=get_PI_chunk_cesm("forced",s_years[i],e_years[i]);
    temp_avg+=tavg
    temp_dist=np.concatenate((temp_dist,tdist),axis=0)

temp_avg=get_PI_frac(PI_ctrl,temp_avg[:,:]/float(len(s_years)))

for i in range(len(s_years)):
   temp.append(get_PI_frac(PI_ctrl,get_PI_chunk_cesm("forced",s_years[i],e_years[i])[0]));

sig_array=get_sig_array(PI_dist,temp_dist)   
   
rlist = Ngl.Resources()

wks_type = "eps"
rlist.wkPaperHeightF = 14.0;
rlist.wkPaperWidthF = 9.5;
wks = Ngl.open_wks(wks_type,"PI_diff_%s" %s_num,rlist)
rlist_avg = rlist;
rlist_avg.wkOrientation="portrait"
wks_avg = Ngl.open_wks(wks_type,"PI_diff_%s_avg" %s_num,rlist_avg)

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

resources.vpWidthF   = 1.0
resources.vpHeightF  = 1.0
resources.mpLimitMode = "LatLon"

resources.mpFillOn   = True
resources.mpLabelsOn = False
resources.mpOutlineOn = True
resources.mpGridAndLimbOn = False
resources.tmXBLabelFontHeightF = 0.03
resources.tmYLLabelFontHeightF = 0.03
resources.mpMinLatF      = min_lat
resources.mpMaxLatF      = max_lat
resources.mpMinLonF      = min_lon
resources.mpMaxLonF      = max_lon
resources.mpProjection = "CylindricalEquidistant"
resources.pmLabelBarDisplayMode = "Never"

resources.cnLevelSelectionMode = "ManualLevels"
resources.cnMinLevelValF       = -0.05
resources.cnMaxLevelValF       = 0.05
resources.cnLevelSpacingF      = 0.005
resources.mpPerimOn       = True
resources.nglPaperMargin=0.0
resources.nglPaperHeight=14.0
resources.nglPaperWidth=12.5

plot = []
for i in range(len(s_years)):
    resources.tiMainString = titles[i]
    plot.append(Ngl.contour_map(wks,temp[i],resources))

panelres = Ngl.Resources()
panelres.nglPanelYWhiteSpacePercent = 6.
panelres.nglPanelXWhiteSpacePercent = 4.
panelres.nglPanelLabelBar                 = True 
panelres.nglPanelLabelBarWidthF           = 0.700 
panelres.nglPanelTop                      = 1.0
panelres.nglPanelFigureStrings            = ["A","B","C","D","E","F","G","H","I","J"]
panelres.nglPanelFigureStringsJust        = "BottomRight"
panelres.nglPaperMargin=0.0
panelres.nglPaperHeight=14.0
panelres.nglPaperWidth=12.5

#Ngl.panel(wks_avg,plot_avg,[1,1],panelres_avg)
Ngl.panel(wks,plot[0:int(rows*cols)],[rows,cols],panelres)

panelres_avg = Ngl.Resources()
panelres_avg.nglPanelLabelBar = True
panelres_avg.nglPaperMargin=0.0
panelres_avg.nglPaperHeight=12.0
panelres_avg.nglPaperWidth=9.5

plot_avg=[]
resources.tiMainString = "PI Average Anomaly"
map=Ngl.contour_map(wks_avg,temp_avg,resources)

resources = Ngl.Resources()

resources.cnLinesOn       = False
resources.cnLineLabelsOn  = False
## Scalar field resources
resources.sfXArray        = lon
resources.sfYArray        = lat

resources.vpWidthF   = 1.0
resources.vpHeightF  = 1.0

resources.cnFillOn          = True  # Turn on contour level fill.
resources.cnMonoFillColor   = True  # Use one fill color.
resources.cnMonoFillPattern = False # Use multiple fill patterns.
resources.cnLineLabelAngleF = 0. # Draw contour line labels right-side up.
resources.cnLevelSpacingF   = 0.0001
resources.nglDraw  = False  # Don't draw the plot or advance the
resources.nglFrame = False  # frame in the call to Ngl.contour.
resources.nglMaximize = False
resources.pmLabelBarDisplayMode = "Never"    # Turn off label bar.
contour = Ngl.contour(wks_avg, sig_array, resources)  # Create a contour plot.
levels = Ngl.get_float_array(contour,"cnLevels")
patterns = np.zeros((len(levels)+1),'i')

for i in range(len(levels)):
    if (levels[i] > 0.01):
        #patterns[i] = 5
        patterns[i] = -1
    else:
        patterns[i] = -1
patterns[-1]=-1        

rlist = Ngl.Resources()
rlist.cnFillPatterns = patterns
rlist.cnFillScaleF = 1.0
Ngl.set_values(contour,rlist)

#Ngl.frame(wks_avg)

Ngl.overlay(map,contour)
plot_avg.append(map)
Ngl.panel(wks_avg,plot_avg,[1,1],panelres_avg)

print("avg PI diff")
print(np.mean(temp_avg[:,:]))

Ngl.end()

