#!/usr/bin/python
 
###############################################################################
#
# functions for use in various diagnostics
#
###############################################################################

import sys,os,string,subprocess
import numpy as np
from scipy import stats
import cmath

ranges=["1213_1223","1258_1274","1274_1283","1284_1294","1452_1461",
        "1600_1609","1641_1650","1761_1770","1809_1818","1815_1825"]

def normed(x):
    return np.asarray(x)/float(np.sum(x))

def get_samp_stats(filename,command,tcdir,ref_avgs,ref_stds,nrun,
                   yr_bins,start_years,end_years,
                   min_lat,max_lat,lat_res,min_lon,max_lon,lon_res,
                   min_wind,max_wind,wind_res,min_press,max_press,
                   press_res,dur_days,lmon,rmon,llat,rlat,llon,rlon,
                   lwind,rwind,lpress,rpress,ltime,rtime,lpdi,rpdi,lace,race,min_pdi,max_pdi,pdi_res,min_ace,max_ace,ace_res):


    print(start_years)
    print(end_years)

    avg_store=[]
    diff_store=[]
    rat_store=[]
    
    start_year=start_years[0]
    end_year=end_years[0]
    
    tcfilename1 = filename %(nrun,start_year,end_year,nrun)
    
    cmd = command %(tcfilename1,start_year,end_year,tcdir,tcfilename1)
    
    subprocess.call(cmd,shell=True)
    
    [months,monthly_num1,
    years1,yearly_num1,
    lats,lat_num1,
    lons,lon_num1,
    intsys,intsy_num1,
    press,pres_num1,
    durs,wdurd_num1,
    pdurd_num1,
    pdis,pdi_num1,
    aces,ace_num1] = get_all_diags(tcfilename1,start_year,end_year,
                                     min_lat,max_lat,lat_res,
                                         min_lon,max_lon,lon_res,
                                         min_wind,max_wind,wind_res,
                                         min_press,max_press,press_res,
                                         dur_days,
                                         min_pdi,max_pdi,pdi_res,min_ace,max_ace,ace_res)
    
    avgs1 = get_all_avgs(months,monthly_num1,years1,yearly_num1,
                         lats,lat_num1,lons,lon_num1,intsys,intsy_num1,
                         press,pres_num1,durs,wdurd_num1,pdurd_num1,pdis,pdi_num1,aces,ace_num1)
    
    pnum1 = get_all_percents(months,monthly_num1,lmon,rmon,
                             lats,lat_num1,llat,rlat,
                             lons,lon_num1,llon,rlon,
                             intsys,intsy_num1,lwind,rwind,
                             press,pres_num1,lpress,rpress,
                             durs,wdurd_num1,pdurd_num1,
                             ltime,rtime,lpdi,rpdi,lace,race,pdis,pdi_num1,aces,ace_num1)
    avgs_all=np.concatenate((avgs1,pnum1),axis=0)
    
    diffs=avgs_all-ref_avgs
    rats=np.divide(diffs,ref_stds)
    avg_store.append(avgs_all)
    diff_store.append(diffs)
    rat_store.append(rats)
    
    year_num=[]
    for x in yearly_num1:
        year_num.append(x)

    for i in range(1,len(start_years)):
        start_year=start_years[i]
        end_year=end_years[i]

        tcfilename1 = filename %(nrun,start_year,end_year,nrun)
    
        cmd= command %(tcfilename1,start_year,end_year,tcdir,tcfilename1)
    
        subprocess.call(cmd,shell=True)
    
           
        [months,monthly_num,
         years,yearly_num,
         lats,lat_num,
         lons,lon_num,
         intsys,intsy_num,
         press,pres_num,
         durs,wdurd_num,
         pdurd_num,
         pdis,pdi_num,
         aces,ace_num] = get_all_diags(tcfilename1,start_year,end_year,
                                     min_lat,max_lat,lat_res,
                                         min_lon,max_lon,lon_res,
                                         min_wind,max_wind,wind_res,
                                         min_press,max_press,press_res,
                                         dur_days,
                                         min_pdi,max_pdi,pdi_res,min_ace,max_ace,ace_res)



        monthly_num1+=monthly_num
        lat_num1+=lat_num
        lon_num1+=lon_num
        intsy_num1+=intsy_num
        pres_num1+=pres_num
        wdurd_num1+=wdurd_num
        pdurd_num1+=pdurd_num
        pdi_num1+=pdi_num
        ace_num1+=ace_num
        for x in yearly_num:
            year_num.append(x)
    
                
        avgs1 = get_all_avgs(months,monthly_num,years,yearly_num,
                             lats,lat_num,lons,lon_num,intsys,intsy_num,
                             press,pres_num,durs,wdurd_num,pdurd_num,pdis,pdi_num,aces,ace_num)
        
        pnum1 = get_all_percents(months,monthly_num,lmon,rmon,
                                 lats,lat_num,llat,rlat,
                                 lons,lon_num,llon,rlon,
                                 intsys,intsy_num,lwind,rwind,
                                 press,pres_num,lpress,rpress,
                                 durs,wdurd_num,pdurd_num,
                                 ltime,rtime,lpdi,rpdi,lace,race,pdis,pdi_num,aces,ace_num)
        avgs_all=np.concatenate((avgs1,pnum1),axis=0)
        
        diffs=avgs_all-ref_avgs
        rats=np.divide(diffs,ref_stds)
        avg_store.append(avgs_all)
        diff_store.append(diffs)
        rat_store.append(rats)

    monthly_num=monthly_num1.copy()
    #yearly_num=np.histogram(year_num,yr_bins)[0]
    yearly_num=year_num
    lat_num=lat_num1.copy()
    lon_num=lon_num1.copy()
    intsy_num=intsy_num1.copy()
    pres_num=pres_num1.copy()
    wdurd_num=wdurd_num1.copy()
    pdurd_num=pdurd_num1.copy()
    pdi_num=pdi_num1.copy()
    ace_num=ace_num1.copy()

    return [avg_store,diff_store,rat_store,monthly_num,yearly_num,lat_num,
            lon_num,intsy_num,pres_num,wdurd_num,pdurd_num,months,lats,lons,
            press,intsys,durs,pdis,pdi_num,aces,ace_num]


def z_transform(x,t_step,N):
    z=[]
    phase=0
    div=2*cmath.pi/N
    for l in range(N):
        phase=l*div
        val=0
        for m in range(len(x)):
            val+=x[m]*cmath.exp(m*t_step*1j*phase)
        z.append(val)
    return z        

def get_ref_dists(filename,ref_dir,start_yr,end_yr,avg_yr,
                  min_lat,max_lat,lat_res,
                  min_lon,max_lon,lon_res,min_wind,max_wind,
                  wind_res,min_press,max_press,press_res,dur_days,min_pdi,max_pdi,pdi_res,min_ace,max_ace,ace_res):

    cmd="if [ ! -f %s ]; then for ((year=%s; year<=%s; year++)); do filename=%s/$year/traj_out_ctrl_$year; if [ -f $filename ]; then cat $filename >> %s; fi; done; fi" %(filename,start_yr,end_yr,ref_dir,filename)
    subprocess.call(cmd,shell=True)

    year_num=[]
    ref_syear=start_yr
    ref_eyear=ref_syear+avg_yr-1
    
    [months,monthly_num,
    years2,yearly_num,
    lats,lat_num,
    lons,lon_num,
    intsys,intsy_num,
    press,pres_num,
    durs,wdurd_num,
    pdurd_num,
    pdis,pdi_num,
    aces,ace_num] = get_all_diags(filename,ref_syear,ref_eyear,
                                 min_lat,max_lat,lat_res,
                                 min_lon,max_lon,lon_res,
                                 min_wind,max_wind,wind_res,
                                 min_press,max_press,press_res,
                                 dur_days,min_pdi,max_pdi,pdi_res,min_ace,max_ace,ace_res)
    for x in yearly_num:
        year_num.append(x)

    for i in range(ref_eyear,end_yr-avg_yr+1):
        ref_syear=i
        ref_eyear=ref_syear+avg_yr-1
    
        [months,monthly_num2,
         years2,yearly_num2,
         lats,lat_num2,
         lons,lon_num2,
         intsys,intsy_num2,
         press,pres_num2,
         durs,wdurd_num2,
         pdurd_num2,
         pdis,pdi_num2,
         aces,ace_num2] = get_all_diags(filename,ref_syear,ref_eyear,
                                 min_lat,max_lat,lat_res,
                                 min_lon,max_lon,lon_res,
                                 min_wind,max_wind,wind_res,
                                 min_press,max_press,press_res,
                                 dur_days,min_pdi,max_pdi,pdi_res,min_ace,max_ace,ace_res)
                             
        monthly_num+=monthly_num2
        lat_num+=lat_num2
        lon_num+=lon_num2
        intsy_num+=intsy_num2
        pres_num+=pres_num2
        wdurd_num+=wdurd_num2
        pdurd_num+=pdurd_num2
        pdi_num+=pdi_num2
        ace_num+=ace_num2
        for x in yearly_num2:
            year_num.append(x)            


    return [monthly_num,
            year_num,
            lat_num,
            lon_num,
            intsy_num,
            pres_num,
            wdurd_num,
            pdurd_num,
            pdi_num,
            ace_num]


def get_ref_stats(filename,ref_dir,start_yr,end_yr,avg_yr,
                  lmon,rmon,llat,rlat,llon,rlon,lwind,rwind,lpress,
                  rpress,ltime,rtime,min_lat,max_lat,lat_res,
                  min_lon,max_lon,lon_res,min_wind,max_wind,
                  wind_res,min_press,max_press,press_res,dur_days,lpdi,rpdi,lace,race,min_pdi,max_pdi,pdi_res,min_ace,max_ace,ace_res):
    
    ref_mons=[]
    ref_years=[]
    ref_lats=[]
    ref_lons=[]
    ref_ints=[]
    ref_press=[]
    ref_wdurds=[]
    ref_pdi=[]
    ref_ace=[]
    ref_pdurds=[]
    ref_pmons=[]
    ref_plats=[]
    ref_plons=[]
    ref_pints=[]
    ref_ppress=[]
    ref_pwdurds=[]
    ref_ppdurds=[]
    ref_ppdi=[]
    ref_pace=[]

    cmd="if [ ! -f %s ]; then for ((year=%s; year<=%s; year++)); do filename=%s/$year/traj_out_ctrl_$year; if [ -f $filename ]; then cat $filename >> %s; fi; done; fi" %(filename,start_yr,end_yr,ref_dir,filename)
    subprocess.call(cmd,shell=True)

    for i in range(start_yr,end_yr-avg_yr+1):
        ref_syear=i
        ref_eyear=ref_syear+avg_yr-1
    
        [months,monthly_num2,
         years2,yearly_num2,
         lats,lat_num2,
         lons,lon_num2,
         intsys,intsy_num2,
         press,pres_num2,
         durs,wdurd_num2,
         pdurd_num2,
         pdis,pdi_num2,
         aces,ace_num2] = get_all_diags(filename,ref_syear,ref_eyear,
                                 min_lat,max_lat,lat_res,
                                 min_lon,max_lon,lon_res,
                                 min_wind,max_wind,wind_res,
                                 min_press,max_press,press_res,
                                 dur_days,
                                 min_pdi,max_pdi,pdi_res,
                                 min_ace,max_ace,ace_res)
    
        avgs2 = get_all_avgs(months,monthly_num2,years2,yearly_num2,
                         lats,lat_num2,lons,lon_num2,intsys,intsy_num2,
                         press,pres_num2,durs,wdurd_num2,pdurd_num2,pdis,pdi_num2,aces,ace_num2)
    
    
    
        pnum2 = get_all_percents(months,monthly_num2,lmon,rmon,
                             lats,lat_num2,llat,rlat,
                             lons,lon_num2,llon,rlon,
                             intsys,intsy_num2,lwind,rwind,
                             press,pres_num2,lpress,rpress,
                             durs,wdurd_num2,pdurd_num2,
                             ltime,rtime,lpdi,rpdi,lace,race,pdis,pdi_num2,aces,ace_num2)             
    
        ref_mons.append(avgs2[0])
        ref_years.append(avgs2[1])
        ref_lats.append(avgs2[2])
        ref_lons.append(avgs2[3])
        ref_ints.append(avgs2[4])
        ref_press.append(avgs2[5])
        ref_wdurds.append(avgs2[6])
        ref_pdurds.append(avgs2[7])
        ref_pdi.append(avgs2[8])
        ref_ace.append(avgs2[9])
        ref_pmons.append(pnum2[0])
        ref_plats.append(pnum2[1])
        ref_plons.append(pnum2[2])
        ref_pints.append(pnum2[3])
        ref_ppress.append(pnum2[4])
        ref_pwdurds.append(pnum2[5])
        ref_ppdurds.append(pnum2[6])
        ref_ppdi.append(pnum2[7])
        ref_pace.append(pnum2[8])
    
    ref_stds=[np.std(ref_mons),np.std(ref_years),np.std(ref_lats),np.std(ref_lons),np.std(ref_ints),np.std(ref_press),np.std(ref_wdurds),np.std(ref_pdurds),np.std(ref_pdi),np.std(ref_ace),np.std(ref_pmons),np.std(ref_plats),np.std(ref_plons),np.std(ref_pints),np.std(ref_ppress),np.std(ref_pwdurds),np.std(ref_ppdurds),np.std(ref_ppdi),np.std(ref_pace)]
    
    ref_avgs=[np.mean(ref_mons),np.mean(ref_years),np.mean(ref_lats),np.mean(ref_lons),np.mean(ref_ints),np.mean(ref_press),np.mean(ref_wdurds),np.mean(ref_pdurds),np.mean(ref_pdi),np.mean(ref_ace),np.mean(ref_pmons),np.mean(ref_plats),np.mean(ref_plons),np.mean(ref_pints),np.mean(ref_ppress),np.mean(ref_pwdurds),np.mean(ref_ppdurds),np.mean(ref_ppdi),np.mean(ref_pace)]        

    return [ref_stds,ref_avgs,ref_mons,ref_years,ref_lats,ref_lons,ref_ints,
            ref_press,ref_wdurds,ref_pdurds,ref_pdi,ref_ace]


def sig_calc(val,a):
    gnum=0; lnum=0
    for x in a:
        if val>=x: gnum+=1
        if val<x: lnum+=1
    return [float(lnum)/float(len(a)),float(gnum)/float(len(a))]        

def read_trajectories(filename):

    tcfilepath = os.path.join(sys.prefix, filename)
    tcfile = open(tcfilepath)

    all_tracks = []
    all_lon = []
    all_lat = []
    while (1):
        line = tcfile.readline()
        elems = line.split()#string.split(line)
        
        try:
            tclength = int(elems[1])
            
            track_lon = []
            track_lat = []
            track_wind = []
            track_pressure = []
            track_year = []
            track_month = []
            track_day = []
            track_hr = []
            for i in range(tclength):
                line = tcfile.readline()
                elems = line.split()
		#elems = string.split(line)

                try:
                    lon = float(elems[0])
                    lat = float(elems[1])
                    wind = float(elems[2])
                    pressure = float(elems[3])
                    year = int(elems[4])
                    month = int(elems[5])
                    day = int(elems[6])
                    hour = int(elems[7])


                    track_lat.append(lat)
                    track_lon.append(lon)
                    track_wind.append(wind)
                    track_pressure.append(pressure)
                    track_year.append(year)
                    track_month.append(month)
                    track_day.append(day)
                    track_hr.append(hour)

                except:
                     pass

            all_tracks.append(np.array([track_lon,track_lat,track_wind,track_pressure,track_year,track_month,track_day,track_hr]))
        
        except:
            pass
        if not line:
            break

    tcfile.close()
    return [all_tracks]

def get_all_files(case,nrun):
    
    files = []
    dir_in = "/glade/u/home/bbenton/TSTORMS_OUTPUT/"+case+"/WRF/run_"+str(nrun)
    
    for i in range(len(ranges)):
        filename = dir_in+"/traj_out_"+case+"_"+ranges[i]+"_"+str(nrun)
        files.append(filename)

    return files        

def get_all_data(case,nrun):
    
    data = []
    dir_in = "/glade/u/home/bbenton/TSTORMS_OUTPUT/"+case+"/WRF/run_"+str(nrun)
    
    for i in range(len(ranges)):
        filename = dir_in+"/traj_out_"+case+"_"+ranges[i]+"_"+str(nrun)
        data.append(read_trajectories(filename))

    return data        

def get_year_chunk(filename,start_year,end_year):
    
    [tracks] = read_trajectories(filename)
    
    tracks_cut = []

    for i in range(len(tracks)):
        if (start_year <= tracks[i][4][0] <= end_year):
            tracks_cut.append(tracks[i])

    return [tracks_cut]
    


def get_month_number(filename,start_year,end_year):

    [tracks] = get_year_chunk(filename,start_year,end_year)

    year_range = end_year-start_year+1
    month_num = np.zeros((12))
    months = [1,2,3,4,5,6,7,8,9,10,11,12]

    for i in range(len(tracks)):
        month = int(tracks[i][5][0])
        month_num[month-1]=1+month_num[month-1]

    month_num=month_num/year_range
    return [months, month_num]


def get_year_number(filename,start_year,end_year):    
    
    [tracks] = get_year_chunk(filename,start_year,end_year)
    
    years = []
    year_range = end_year-start_year+1
    
    for i in range(year_range):
        years.append(int(start_year+i))

    year_num = np.zeros((year_range))

    for i in range(len(tracks)):
        year = int(tracks[i][4][0])
        year_num[year-start_year]=1+year_num[year-start_year]

    return [years, year_num]

def get_lat_number(filename,start_year,end_year,min_lat,max_lat,lat_res):    
    
    [tracks] = get_year_chunk(filename,start_year,end_year)
    
    lat_range = int((max_lat-min_lat)/lat_res)
    year_range = end_year-start_year+1
    
    lat_num = np.zeros((lat_range))
    lats = []

    for i in range(lat_range):
        lats.append(min_lat+i*lat_res)

    for i in range(len(tracks)):
        count=0
        lat=0
        for j in range(len(tracks[i][1][:])):
            lat_tmp = tracks[i][1][j]
            if min_lat < lat_tmp < max_lat:
                lat+=lat_tmp; count+=1
        if count > 0: 
            lat=lat/float(count)    
            #lat = np.average(tracks[i][1][:])
            lat_idx = (np.abs(lats[:]-lat)).argmin()
            lat_num[lat_idx]=1+lat_num[lat_idx]

    lat_num=lat_num/year_range
    return [lats, lat_num]
   
def get_lon_number(filename,start_year,end_year,min_lon,max_lon,lon_res):    
    
    [tracks] = get_year_chunk(filename,start_year,end_year)
    
    lon_range = int((max_lon-min_lon)/lon_res)
    year_range = end_year-start_year+1
    
    lon_num = np.zeros((lon_range))
    lons = []

    for i in range(lon_range):
        lons.append(min_lon+i*lon_res)

    for i in range(len(tracks)):
        count=0
        lon=0
        for j in range(len(tracks[i][0][:])):
            lon_tmp = tracks[i][0][j]
            if min_lon < lon_tmp < max_lon:
                lon+=lon_tmp; count+=1
        if count > 0:
            lon=lon/float(count)
            #lon = np.average(tracks[i][0][:])
            lon_idx = (np.abs(lons[:]-lon)).argmin()
            lon_num[lon_idx]=1+lon_num[lon_idx]

    lon_num=lon_num/year_range
    return [lons, lon_num]

def get_pdi_number(filename,start_year,end_year,min_pdi,max_pdi,pdi_res):

    [tracks] = get_year_chunk(filename,start_year,end_year)
    
    pdi_range = int((max_pdi-min_pdi)/pdi_res)
    year_range = end_year-start_year+1
    
    pdi_num = np.zeros((pdi_range))
    pdis = []

    for i in range(pdi_range):
        pdis.append(min_pdi+i*pdi_res)

    tstep = 6*60*60
    min_pdi_val = np.sum(tracks[0][2][:]**3*tstep)
    max_pdi_val = min_pdi_val
    for i in range(len(tracks)):
        pdi_val = np.sum(tracks[i][2][:]**3*tstep)
        if pdi_val>max_pdi_val: max_pdi_val=pdi_val
        if pdi_val<min_pdi_val: min_pdi_val=pdi_val
        
        pdi_idx = (np.abs(pdis[:]-pdi_val)).argmin()
        pdi_num[pdi_idx]=1+pdi_num[pdi_idx]

    #print("max_pdi_val: %s" %(max_pdi_val))
    #print("min_pdi_val: %s" %(min_pdi_val))
    pdi_num=pdi_num/year_range
    return [pdis, pdi_num]

def get_ace_number(filename,start_year,end_year,min_ace,max_ace,ace_res):

    [tracks] = get_year_chunk(filename,start_year,end_year)
    
    ace_range = int((max_ace-min_ace)/ace_res)
    year_range = end_year-start_year+1
    
    ace_num = np.zeros((ace_range))
    aces = []

    for i in range(ace_range):
        aces.append(min_ace+i*ace_res)

    min_ace_val = np.sum(tracks[0][2][:]**2*10**(-4))
    max_ace_val = min_ace_val
    for i in range(len(tracks)):
        ace_val = np.sum(tracks[i][2][:]**2*10**(-4))
        if ace_val>max_ace_val: max_ace_val=ace_val
        if ace_val<min_ace_val: min_ace_val=ace_val
        
        ace_idx = (np.abs(aces[:]-ace_val)).argmin()
        ace_num[ace_idx]=1+ace_num[ace_idx]
    
    #print("max_ace_val: %s" %(max_ace_val))
    #print("min_ace_val: %s" %(min_ace_val))
    ace_num=ace_num/year_range
    return [aces, ace_num]


def get_wind_number(filename,start_year,end_year,min_wind,max_wind,wind_res):

    [tracks] = get_year_chunk(filename,start_year,end_year)
    
    wind_range = int((max_wind-min_wind)/wind_res)
    year_range = end_year-start_year+1
    
    wind_num = np.zeros((wind_range))
    winds = []

    for i in range(wind_range):
        winds.append(min_wind+i*wind_res)

    for i in range(len(tracks)):
        wind_max = np.max(tracks[i][2][:])
        wind_idx = (np.abs(winds[:]-wind_max)).argmin()
        wind_num[wind_idx]=1+wind_num[wind_idx]

    wind_num=wind_num/year_range
    return [winds, wind_num]

def get_press_number(filename,start_year,end_year,min_press,max_press,press_res):

    [tracks] = get_year_chunk(filename,start_year,end_year)
    
    press_range = int((max_press-min_press)/press_res)
    
    year_range = end_year-start_year+1
    
    press_num = np.zeros((press_range))
    pressures = []

    for i in range(press_range):
        pressures.append(max_press-i*press_res)

    for i in range(len(tracks)):
        press_min = np.min(tracks[i][3][:])
        if len(str(press_min).split('.')[0]) <= 2: press_min=100.0*press_min
        press_idx = (np.abs(pressures[:]-press_min)).argmin()
        if (press_min > 0.0): press_num[press_idx]=1+press_num[press_idx]

    press_num=press_num/year_range
    return [pressures, press_num]

def get_wind_decay_number(filename,start_year,end_year,day_num):

    [tracks] = get_year_chunk(filename,start_year,end_year)

    year_range = end_year-start_year+1
    wdur_num = np.zeros((4*day_num)) 
    durs = []

    for i in range(4*day_num):
        durs.append(6*i)

    for i in range(len(tracks)):
        dur_all = len(tracks[i][0])
        max_wind = np.max(tracks[i][2][:])
        mean_wind = np.mean(tracks[i][2][:])
        mw_idx = (tracks[i][2][:]).argmax()
        dw_idx = (np.abs(tracks[i][2][mw_idx:dur_all]-mean_wind)).argmin()
        wdur_decay = np.abs(mw_idx-dw_idx)+1
        if wdur_decay > len(wdur_num)-1:
            wdur_num[len(wdur_num)-1] = wdur_num[len(wdur_num)-1]+1
        else:
            wdur_num[wdur_decay] = wdur_num[wdur_decay]+1

    wdur_num=wdur_num/year_range
    return [durs, wdur_num]

def get_press_decay_number(filename,start_year,end_year,day_num):

    [tracks] = get_year_chunk(filename,start_year,end_year)

    year_range = end_year-start_year+1
    pdur_num = np.zeros((4*day_num)) 
    durs = []

    for i in range(4*day_num):
        durs.append(6*i)

    for i in range(len(tracks)):
        dur_all = len(tracks[i][0])
        min_press = np.min(tracks[i][3][:])
        mean_press = np.mean(tracks[i][3][:])
        mp_idx = (tracks[i][3][:]).argmin()
        dp_idx = (np.abs(tracks[i][3][mp_idx:dur_all]-mean_press)).argmin()
        pdur_decay = np.abs(mp_idx-dp_idx)+1
        
        if (min_press > 0.0):
            if pdur_decay > len(pdur_num)-1:
                pdur_num[len(pdur_num)-1] = pdur_num[len(pdur_num)-1]+1
            else:
                pdur_num[pdur_decay] = pdur_num[pdur_decay]+1

    pdur_num=pdur_num/year_range
    return [durs, pdur_num]

def avg_hori(x,y):
    avg = 0
    norm = 0
    for i in range(len(y)):
        avg = avg + y[i]*x[i]
        norm = norm + y[i]

    if float(norm)>0:
        avg = float(avg)/float(norm)
    return round(avg,2)

def avg_vert(x,y):
    avg = 0
    norm = len(y)
    for i in range(len(y)):
        avg = avg + y[i]

    if float(norm)>0:
        avg = float(avg)/float(norm)
    return round(avg,2)

def uncert(x,y):
    diff = np.abs(y-x)
    diff = diff/(0.5*(np.abs(x+y)))
    return diff

def total_uncert(x,y):
    tdiff = 0
    norm = len(y)
    for i in range(len(y)):
        tdiff = tdiff + uncert(x[i],y[i])
    tdiff = tdiff/norm
    return tdiff

def total_diff(x,y):
    tdiff = 0
    norm = len(y)
    for i in range(len(y)):
        tdiff = tdiff + np.abs(x[i]-y[i])
    tdiff = tdiff/norm
    return tdiff

def percent_in(x,y,lx,rx):
    arr = np.asarray(x)
    lidx = (np.abs(arr[:]-lx)).argmin()
    ridx = (np.abs(arr[:]-rx)).argmin()
    num_btwn = 0
    num_total = 0
    for i in range(ridx-lidx+1):
        num_btwn = num_btwn + y[lidx+i]
    for i in range(len(y)):
        num_total = num_total + y[i]
    return num_btwn/num_total

def pad_num(x):
    str_num = '{0:12g}'.format(round(x,12))
    return str_num

def avg_time(track):
    avg_yr = np.mean(track[4])
    avg_mon = np.mean(track[5])
    avg_day = np.mean(track[6])
    avg_hr = np.mean(track[7])
    return [avg_yr,avg_mon,avg_day,avg_hr]

def avg_place(track):
    avg_lon = np.mean(track[0])
    avg_lat = np.mean(track[1])
    return [avg_lon,avg_lat]

def avg_track(track):
    avg_track = np.concatenate([avg_place(track),avg_time(track)])
    return avg_track

def find_track(track,filename):

    cand_matches = []
    match = []
    loc_diffs = []
    [tracks] = read_trajectories(filename)

    for i in range(len(tracks)):
        cand_track = avg_track(tracks[i])
        if ((np.sqrt((track[0]-cand_track[0])**2+
                        (track[1]-cand_track[1])**2) < 8.0) and
            (np.abs(track[2]-cand_track[2]) < 1.0) and
            (np.abs(track[3]-cand_track[3]) < 2.0) and
            (np.abs(track[4]-cand_track[4]) < 10.0)):
             cand_matches.append(np.array(cand_track))

    if len(cand_matches) > 0:
        for i in range(len(cand_matches)):
            cand_track = cand_matches[i]
            diff = np.sqrt((track[0]-cand_track[0])**2+
                              (track[1]-cand_track[1])**2)
            loc_diffs.append(diff)

    if len(loc_diffs) > 0:
        match_idx = (np.abs(loc_diffs)).argmin()
        match.append(np.array(cand_matches[match_idx]))

    return match        

def track_match_all(filename1,filename2):

    [tracks1] = read_trajectories(filename1)
    [tracks2] = read_trajectories(filename2)

    #total_num = len(tracks2)
    total_num = (len(tracks2)+len(tracks1))/2.0
    counter = 0
    
    if len(tracks1) < len(tracks2):
        for i in range(len(tracks1)):
            track = avg_track(tracks1[i])
            match = find_track(track,filename2)
            if len(match) > 0: counter = counter+1
    else:
        for i in range(len(tracks2)):
            track = avg_track(tracks2[i])
            match = find_track(track,filename1)
            if len(match) > 0: counter = counter+1

    pcent_match = float(counter)/float(total_num)        
    return pcent_match

def running_avg(data,avg_yrs):
    avgs = []
    for i in range(len(data)):
        start_idx = int(i-avg_yrs/2)
        end_idx = start_idx + avg_yrs
        if ((end_idx > len(data)) or (start_idx < 0)):
            start_idx = 0
            end_idx = len(data)
        avgs.append(np.mean(data[start_idx:end_idx]))
    return avgs

def running_range(total_len,avg_len,idx):
    start_idx = int(idx-avg_len/2)
    end_idx = start_idx + avg_len
    if ((end_idx > total_len) or (start_idx < 0)):
        #start_idx = 0
        #end_idx = total_len
        start_idx = idx
        end_idx = idx+1
        
    return [ start_idx, end_idx ]        

def ks_test(data1,data2):
    dat1 = np.histogram(np.asarray(data1)/float(np.sum(data1)),500)[0]
    dat2 = np.histogram(np.asarray(data2)/float(np.sum(data2)),500)[0]

    [Dval, pval] = stats.ks_2samp(dat1,dat2)

    return [Dval,pval]

def and_test(data1,data2):
    dat1 = np.histogram(np.asarray(data1)/float(np.sum(data1)),500)[0]
    dat2 = np.histogram(np.asarray(data2)/float(np.sum(data2)),500)[0]

    return stats.anderson_ksamp([dat1,dat2])

def t_test(data1,data2):
    dat1 = np.histogram(np.asarray(data1)/float(np.sum(data1)),500)[0]
    dat2 = np.histogram(np.asarray(data2)/float(np.sum(data2)),500)[0]

    #[Dval, pval] = stats.ttest_rel(dat1,dat2)
    [Dval, pval] = stats.ttest_ind(dat1,dat2)

    return [Dval,pval]

def get_all_diags(filename,start_year,end_year,
                  min_lat,max_lat,lat_res,
                  min_lon,max_lon,lon_res,
                  min_wind,max_wind,wind_res,
                  min_press,max_press,press_res,
                  dur_days,
                  min_pdi,max_pdi,pdi_res,
                  min_ace,max_ace,ace_res):

    [mons,mnum] = get_month_number(filename,start_year,end_year)
    [yrs,ynum] = get_year_number(filename,start_year,end_year)
    [lats,lat_num] = get_lat_number(filename,start_year,end_year,
                                    min_lat,max_lat,lat_res)
    [lons,lon_num] = get_lon_number(filename,start_year,end_year,
                                    min_lon,max_lon,lon_res)
    [winds,wnum] = get_wind_number(filename,start_year,end_year,
                                   min_wind,max_wind,wind_res)
    [press,pnum] = get_press_number(filename,start_year,end_year,
                                    min_press,max_press,press_res)
    [durs,wdur_num] = get_wind_decay_number(filename,start_year,end_year,
                                            dur_days)
    [durs,pdur_num] = get_press_decay_number(filename,start_year,end_year,
                                             dur_days)   

    [pdis,pdi_num] = get_pdi_number(filename,start_year,end_year,min_pdi,max_pdi,pdi_res)   

    [aces,ace_num] = get_ace_number(filename,start_year,end_year,min_ace,max_ace,ace_res)   

    return [mons,mnum,yrs,ynum,lats,lat_num,lons,lon_num,
            winds,wnum,press,pnum,durs,wdur_num,pdur_num,pdis,pdi_num,aces,ace_num]

def get_all_avgs(mons,mnum,yrs,ynum,lats,lat_num,lons,lon_num,
                 winds,wnum,press,pnum,durs,wdur_num,pdur_num,pdis,pdi_num,aces,ace_num):         

    avgs = np.zeros(10)
    avgs[0] = avg_hori(mons,mnum)
    avgs[1] = avg_vert(yrs,ynum)
    avgs[2] = avg_hori(lats,lat_num)
    avgs[3] = avg_hori(lons,lon_num)
    avgs[4] = avg_hori(winds,wnum)
    avgs[5] = avg_hori(press,pnum)
    avgs[6] = avg_hori(durs,wdur_num)
    avgs[7] = avg_hori(durs,pdur_num)        
    avgs[8] = avg_hori(pdis,pdi_num)        
    avgs[9] = avg_hori(aces,ace_num)        

    return avgs

def get_all_percents(mons,mnum,lmon,rmon,
                     lats,lat_num,llat,rlat,
                     lons,lon_num,llon,rlon,
                     winds,wnum,lwind,rwind,
                     press,pnum,lpress,rpress,
                     durs,wdur_num,pdur_num,
                     ltime,rtime,lpdi,rpdi,
                     lace,race,pdis,pdi_num,
                     aces,ace_num):

    pnums = np.zeros(9)
    pnums[0] = percent_in(mons,mnum,lmon,rmon)
    pnums[1] = percent_in(lats,lat_num,llat,rlat)
    pnums[2] = percent_in(lons,lon_num,llon,rlon)
    pnums[3] = percent_in(press,pnum,lpress,rpress)
    pnums[4] = percent_in(winds,wnum,lwind,rwind)
    pnums[5] = percent_in(durs,wdur_num,ltime,rtime)
    pnums[6] = percent_in(durs,pdur_num,ltime,rtime)
    pnums[7] = percent_in(pdis,pdi_num,lpdi,rpdi)
    pnums[8] = percent_in(aces,ace_num,lace,race)

    return pnums

def get_all_ks_tests(mnum1,mnum2,wnum1,wnum2,lat_num1,lat_num2,
                     lon_num1,lon_num2,pnum1,pnum2,wdur_num1,wdur_num2,
                     pdur_num1,pdur_num2):

    [ Dm, Pm ] = ks_test(mnum1,mnum2)                     
    [ Dw, Pw ] = ks_test(wnum1,wnum2)                     
    [ Dlat, Plat ] = ks_test(lat_num1,lat_num2)                     
    [ Dlon, Plon ] = ks_test(lon_num1,lon_num2)                     
    [ Dp, Pp ] = ks_test(pnum1,pnum2)                     
    [ Dwdur, Pwdur ] = ks_test(wdur_num1,wdur_num2)                     
    [ Dpdur, Ppdur ] = ks_test(pdur_num1,pdur_num2)

    return [ Pm, Pw, Plat, Plon, Pp, Pwdur, Ppdur ]

def print_diff_table(avgs1,avgs2,pnum1,pnum2,start_year,end_year,nrun=None,case=None):

    avg_tdiff = total_uncert(avgs1,avgs2)
    pcent_tdiff = total_uncert(pnum1,pnum2)
    
    avg_diff = np.zeros(len(avgs1))
    pdiff = np.zeros(len(pnum1))
    
    for i in range(len(avg_diff)):
        avg_diff[i]=uncert(avgs1[i],avgs2[i])
    
    for i in range(len(pdiff)):
        pdiff[i]=uncert(pnum1[i],pnum2[i])
    
    comb_diff = (avg_tdiff*len(avg_diff)+pcent_tdiff*len(pdiff))/(len(avg_diff)+len(pdiff))
    
    print("")
    print("run number "+str(nrun)+": "+str(case)+" "+str(start_year)+" "+str(end_year))
    print("total average difference: " +str('{0:4g}'.format(round(avg_tdiff,5))))
    print("total percent difference: " +str('{0:4g}'.format(round(pcent_tdiff,5))))
    print("composite difference: " +str('{0:4g}'.format(round(comb_diff,5))))
    print("")
    print("------------------------------------------------------------------------")
    print(" Metrics                  | Sample       | Reference    | Difference   |")
    print("------------------------------------------------------------------------")
    print("avg month                 | "+pad_num(avgs1[0])+" | "+pad_num(avgs2[0])+" | "+pad_num(avg_diff[0])+" |")
    print("avg yearly number         | "+pad_num(avgs1[1])+" | "+pad_num(avgs2[1])+" | "+pad_num(avg_diff[1])+" |")
    print("avg latitude              | "+pad_num(avgs1[2])+" | "+pad_num(avgs2[2])+" | "+pad_num(avg_diff[2])+" |")
    print("avg longitude             | "+pad_num(avgs1[3])+" | "+pad_num(avgs2[3])+" | "+pad_num(avg_diff[3])+" |")
    print("avg speed                 | "+pad_num(avgs1[4])+" | "+pad_num(avgs2[4])+" | "+pad_num(avg_diff[4])+" |")
    print("avg pressure              | "+pad_num(avgs1[5])+" | "+pad_num(avgs2[5])+" | "+pad_num(avg_diff[5])+" |")
    print("avg life (wind)           | "+pad_num(avgs1[6])+" | "+pad_num(avgs2[6])+" | "+pad_num(avg_diff[6])+" |")
    print("avg life (pressure)       | "+pad_num(avgs1[7])+" | "+pad_num(avgs2[7])+" | "+pad_num(avg_diff[7])+" |")
    print("(months) May-Nov          | "+pad_num(pnum1[0])+" | "+pad_num(pnum2[0])+" | "+pad_num(pdiff[0])+" |")
    print("(latitude) 0N-25N         | "+pad_num(pnum1[1])+" | "+pad_num(pnum2[1])+" | "+pad_num(pdiff[1])+" |")
    print("(longitude) 100W-50W      | "+pad_num(pnum1[2])+" | "+pad_num(pnum2[2])+" | "+pad_num(pdiff[2])+" |")
    print("(pressure hPa) 1020-980   | "+pad_num(pnum1[3])+" | "+pad_num(pnum2[3])+" | "+pad_num(pdiff[3])+" |")
    print("(wind m/s) 0-40           | "+pad_num(pnum1[4])+" | "+pad_num(pnum2[4])+" | "+pad_num(pdiff[4])+" |")
    print("(wind life hrs) 0-100     | "+pad_num(pnum1[5])+" | "+pad_num(pnum2[5])+" | "+pad_num(pdiff[5])+" |")
    print("(pressure life hrs) 0-100 | "+pad_num(pnum1[6])+" | "+pad_num(pnum2[6])+" | "+pad_num(pdiff[6])+" |")
    print("------------------------------------------------------------------------")

def print_ks_table(pvals,pmeans,pstds):

    print("------------------------------------------------------------------------")
    print("                              KS tests")
    print("------------------------------------------------------------------------")
    print(" Metrics                  | P-value      | P-mean       | P-std        |")
    print("------------------------------------------------------------------------")
    print(" month                    | "+pad_num(pvals[0])+" | "+pad_num(pmeans[0])+" | "+pad_num(pstds[0])+" |")
    print(" wind                     | "+pad_num(pvals[1])+" | "+pad_num(pmeans[1])+" | "+pad_num(pstds[1])+" |")
    print(" lat                      | "+pad_num(pvals[2])+" | "+pad_num(pmeans[2])+" | "+pad_num(pstds[2])+" |")
    print(" lon                      | "+pad_num(pvals[3])+" | "+pad_num(pmeans[3])+" | "+pad_num(pstds[3])+" |")
    print(" press                    | "+pad_num(pvals[4])+" | "+pad_num(pmeans[4])+" | "+pad_num(pstds[4])+" |")
    print(" wind life                | "+pad_num(pvals[5])+" | "+pad_num(pmeans[5])+" | "+pad_num(pstds[5])+" |")
    print(" press life               | "+pad_num(pvals[6])+" | "+pad_num(pmeans[6])+" | "+pad_num(pstds[6])+" |")
    print("------------------------------------------------------------------------")
