import os
import Nio
import numpy
from scipy.signal import argrelextrema
import collections


def getVolcInfo(number,region):

    forced_directories=[d for d in os.listdir('/glade/scratch/cmc542/tmp/bbenton/WRF_OUTPUT/forced')]# if os.path.isdir(d)]
    forced_years = [int(d) for d in forced_directories if d !="T_sfc"]
    
    data_dir  = "/glade/p/cesmdata/inputdata/atm/cam/volc"
    data_file = "/IVI2LoadingLatHeight501-2000_L18_c20100518.nc"
    volc_dat = Nio.open_file(data_dir+data_file,"r")
    
    lats = volc_dat.variables["lat"].get_value()
    colmass_tmp = volc_dat.variables["colmass"].get_value()
    
    min_lat_idx = (numpy.abs(lats+30.0)).argmin()
    max_lat_idx = (numpy.abs(lats-30.0)).argmin()
    
    colmass = [numpy.sum(colmass_tmp[i,min_lat_idx:max_lat_idx]) for i in range(len(colmass_tmp[:,0]))]
    colmass = numpy.array(colmass)
    time = volc_dat.variables["time"].get_value()
    date = volc_dat.variables["date"].get_value()
    erups_dict = {}
    
    max_erups = list(colmass[argrelextrema(colmass, numpy.greater)[0]])
    max_erups.sort()

    for i in range(len(max_erups)):
        idx=(numpy.abs(max_erups[i]-colmass[:])).argmin()
        lat_tmp = lats[(numpy.abs(colmass_tmp[idx,:])).argmax()]
        erups_dict[max_erups[i]]={'time':time[idx],'lat':lat_tmp}
    
    max_erups=[]
    time_erups=[]
    lat_erups=[]
    erups_dict_sorted = collections.OrderedDict(sorted(erups_dict.items()))

    for v in erups_dict_sorted:
        year = erups_dict[v]['time']
        if min(forced_years)<year<1850.0 and ((int(year) in forced_years and int(year)+1 in forced_years) or (int(year)+1 in forced_years and int(year)+2 in forced_years)):
            if region=="north":
                if 40.0>erups_dict[v]['lat']>0.0:
                    max_erups.append(v)
                    time_erups.append(erups_dict[v]['time'])
                    lat_erups.append(erups_dict[v]['lat'])
    
            elif region=="south":
                if -40.0<erups_dict[v]['lat']<0.0:
                    max_erups.append(v)
                    time_erups.append(erups_dict[v]['time'])
                    lat_erups.append(erups_dict[v]['lat'])
            else:
                if -40.0<erups_dict[v]['lat']<40.0:
                    max_erups.append(v)
                    time_erups.append(erups_dict[v]['time'])
                    lat_erups.append(erups_dict[v]['lat'])

    time_erups_tmp=time_erups[-number:]
    time_erups_tmp.sort()
    time_erups_filt=[]
    max_erups_filt=[]
    lat_erups_filt=[]
    
    for i,t in enumerate(time_erups_tmp):
        if True: #i>0 and (t-2)>time_erups_tmp[i-1]:
            for m in erups_dict:
                if erups_dict[m]['time']==t:
                    time_erups_filt.append(t)
                    max_erups_filt.append(m)
                    lat_erups_filt.append(erups_dict[m]['lat'])

    return max_erups_filt,time_erups_filt,lat_erups_filt
