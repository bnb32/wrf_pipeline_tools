#!/bin/python

import Nio, Ngl
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import scipy
from scipy.fftpack import fftshift 
import math
from diag_functions import *
import seaborn as sns
sns.set_style('darkgrid')

dir_in="/glade/scratch/cmc542/tmp/bbenton/WRF_OUTPUT/ctrl/%s"
#dir_in = "/glade/u/home/bbenton/PROJ_WRF/ctrl/%s"
file_in = "/wrfpost_ctrl_%s_%s.nc"

ts_series=[]

if False:

    for year in range(950,1105):
        for month in range(1,13):
            if month < 10: month="0"+str(month)
            else: month=str(month)
            dat_in = Nio.open_file(dir_in %(year) + file_in %(year,month))
            dat_in = dat_in.variables["T_sfc_monthly"][0,:,:]
            ts_series.append(np.mean(dat_in))
            #ts_series.append(np.mean(tmp))
    print(ts_series)
    exit()

else:

    f1=open("/glade/u/home/bbenton/20XXWRF/wrf_pipeline_tools/diagnostics/ctrl_ts_series_1000_1105.txt")
    f2=open("/glade/u/home/bbenton/20XXWRF/wrf_pipeline_tools/diagnostics/ctrl_ts_series_950_1105.txt")
    ts_series1=f1.readline().split(",")
    ts_series2=f2.readline().split(",")

ts_series1=[float(x) for x in ts_series1]
ts_series2=[float(x) for x in ts_series2]

tmp1=[]
tmp2=[]
avg_len=6

for i in range(int(len(ts_series1)/avg_len)):
    tmp1.append(np.mean(ts_series1[avg_len*i:avg_len*(i+1)]))
for i in range(int(len(ts_series2)/avg_len)):
    tmp2.append(np.mean(ts_series2[avg_len*i:avg_len*(i+1)]))

ts_series1=tmp1
ts_series2=tmp2

ts_series1=[x-np.mean(ts_series1) for x in ts_series1]
ts_series2=[x-np.mean(ts_series2) for x in ts_series2]



#ps=np.abs(z_transform(ts_series,avg_len/12.0,int(len(ts_series)/2)))**2
ps1=np.abs(np.fft.fft(ts_series1))**2
freqs1=np.fft.fftfreq(len(ts_series1),0.5)
idx1=np.argsort(freqs1)
ps2=np.abs(np.fft.fft(ts_series2))**2
freqs2=np.fft.fftfreq(len(ts_series2),0.5)
idx2=np.argsort(freqs2)

#ps1=[math.log(x) for x in ps1]
#freqs1=[math.log(x) for x in freqs1[:len(freqs1)/2]]

lsize=15
tsize=20

plt.rc('font',size=lsize)
plt.rc('axes',titlesize=tsize)
plt.rc('axes',labelsize=lsize)
plt.rc('xtick',labelsize=lsize)
plt.rc('ytick',labelsize=lsize)

#plt.plot(ps)
#plt.loglog(freqs2[:len(freqs2)/2],ps2[:len(freqs2)/2],'r')

plt.loglog(freqs1[:int(len(freqs1)/2)],ps1[:int(len(freqs1)/2)],'b')


plt.title("Control Power Spectrum")
plt.ylabel("SST Anomaly Magnitude "+r'$(K)$')
plt.xlabel("Frequency "+r'$(yrs^{-1})$')
plt.ylim(top=1000)
plt.ylim(bottom=0.1)
plt.savefig("power_spectrum.png",bbox_inches='tight',pad_inches=0,dpi=300)
#plt.show()
