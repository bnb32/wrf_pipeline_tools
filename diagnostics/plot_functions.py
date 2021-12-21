#!/bin/python

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import Ngl,Nio

from diag_functions import *

def get_PI_year(case, year):
    data_dir="~/PROJ_WRF/%s/%s/"
    post_file="wrfpost_%s_%s_%s.nc"
    tstorms_file="wrf_tstorms_%s_%s.nc"
    temp_pfile=Nio.open_file(data_dir %(case,year) + post_file %(case,year,"01"))
    temp_tfile=Nio.open_file(data_dir %(case,year) + tstorms_file %(case,year))
    T_200=np.mean(temp_tfile.variables["T200"].get_value(),axis=0)[:,:]
    T_sfc=np.mean(temp_pfile.variables["T_sfc_monthly"].get_value(),axis=0)[:,:]
    LH=np.mean(temp_pfile.variables["LH_monthly"].get_value(),axis=0)[:,:]
    #T_2m=np.mean(temp_pfile.variables["T_2m_daily"].get_value(),axis=0)[:,:]
    F_up=np.mean(temp_pfile.variables["LW_u_monthly"].get_value(),axis=0)[:,:]+np.mean(temp_pfile.variables["SW_u_monthly"].get_value(),axis=0)[:,:]
    F_down=np.mean(temp_pfile.variables["LW_d_monthly"].get_value(),axis=0)[:,:]+np.mean(temp_pfile.variables["SW_d_monthly"].get_value(),axis=0)[:,:]
    #P_sfc=np.mean(temp_pfile.variables["p_sfc_monthly"].get_value(),axis=0)[:,:]
    #V_sfc=np.sqrt(np.mean(temp_tfile.variables["UBOT"].get_value(),axis=0)[:,:]**2+np.mean(temp_tfile.variables["VBOT"].get_value(),axis=0)[:,:]**2)
    for i in range(2,13):
        if i<10: month="0"+str(i)
        else: month=str(i)
        temp_pfile=Nio.open_file(data_dir %(case,year) + post_file %(case,year,month))
        T_sfc+=np.mean(temp_pfile.variables["T_sfc_monthly"].get_value(),axis=0)[:,:]
        LH+=np.mean(temp_pfile.variables["LH_monthly"].get_value(),axis=0)[:,:]
        #T_2m+=np.mean(temp_pfile.variables["T_2m_daily"].get_value(),axis=0)[:,:]
        F_up+=np.mean(temp_pfile.variables["LW_u_monthly"].get_value(),axis=0)[:,:]+np.mean(temp_pfile.variables["SW_u_monthly"].get_value(),axis=0)[:,:]
        F_down+=np.mean(temp_pfile.variables["LW_d_monthly"].get_value(),axis=0)[:,:]+np.mean(temp_pfile.variables["SW_d_monthly"].get_value(),axis=0)[:,:]
        #P_sfc+=np.mean(temp_pfile.variables["p_sfc_monthly"].get_value(),axis=0)[:,:]

    T_sfc[:,:]=T_sfc[:,:]/12.0
    F_down[:,:]=F_down[:,:]/12.0
    F_up[:,:]=F_up[:,:]/12.0
    #P_sfc[:,:]=P_sfc[:,:]/12.0
    LH[:,:]=LH[:,:]/12.0
    #T_2m[:,:]=T_2m/12.0
    #return (T_sfc[:,:]-T_200[:,:])/T_sfc[:,:]*LH[:,:]
    #return (T_sfc[:,:]-T_200[:,:])/T_sfc[:,:]*(T_sfc[:,:]-T_2m[:,:])
    #return (T_sfc[:,:]-T_200[:,:])/(P_sfc[:,:]*V_sfc[:,:])*(F_down[:,:]-F_up[:,:])
    return (T_sfc[:,:]-T_200[:,:])/T_200[:,:]*(F_down[:,:]-F_up[:,:]+LH[:,:])
    

    

def get_lat_lon(case,year):
    data_dir="~/PROJ_WRF/%s/%s/"
    post_file="wrfpost_%s_%s_%s.nc"
    tstorms_file="wrf_tstorms_%s_%s.nc"

    temp_pfile=Nio.open_file(data_dir %(case,year) + post_file %(case,year,"01"))
    lat=temp_pfile.variables["lat"].get_value()[:]
    lon=temp_pfile.variables["lon"].get_value()[:]
    return lat,lon

def get_PI_chunk(case,start,end):
    PI_tmp=get_PI_year(case,start)
    for i in range(start+1,end+1):
        PI_tmp+=get_PI_year(case,i)
    return PI_tmp[:,:]/float(end-start+1)

def get_PI_frac(PI_ctrl,PI_forced):
    #return PI_forced[:,:]/PI_ctrl[:,:]-1.0
    return np.sqrt(PI_forced[:,:]/PI_ctrl[:,:])-1.0

def plot_num_fig(tcfilename1,tcfilename2,start_year,end_year,
                 min_lat,max_lat,lat_res,min_lon,max_lon,lon_res,
                 min_wind,max_wind,wind_res,min_press,max_press,press_res,
                 dur_days,min_pdi,max_pdi,pdi_res,min_ace,max_ace,ace_res, 
                 outer_grid=gridspec.GridSpec(1,1,wspace=0.0,hspace=0.0)[0],
                 fig=plt.figure(1), title=None):

                     
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
                                     dur_days,min_pdi,max_pdi,pdi_res,
                                     min_ace,max_ace,ace_res)
    [months,monthly_num2,
         years,yearly_num2,
         lats,lat_num2,
         lons,lon_num2,
         intsys,intsy_num2,
         press,pres_num2,
         durs,wdurd_num2,
         pdurd_num2,
         pdis,pdi_num2,
         aces,ace_num2] = get_all_diags(tcfilename2,start_year,end_year,
                                     min_lat,max_lat,lat_res,
                                     min_lon,max_lon,lon_res,
                                     min_wind,max_wind,wind_res,
                                     min_press,max_press,press_res,
                                     dur_days,min_pdi,max_pdi,pdi_res,
                                     min_ace,max_ace,ace_res)

#----------------plotting---------------------#

    fig_rows=5
    fig_cols=2

    plt.rc('font',size=7)
    plt.rc('axes', titlesize=7)

    inner_grid = gridspec.GridSpecFromSubplotSpec(fig_rows, fig_cols,
                  subplot_spec=outer_grid, wspace=0.6, hspace=0.9)

    if title: fig.suptitle(title)

    ax = plt.Subplot(fig,inner_grid[0])
    #ax.bar(months,monthly_num,1,align='center')
    l1,l2=ax.plot(months,monthly_num/np.sum(monthly_num),'r',months,monthly_num2/np.sum(monthly_num2),'b')
    fig.add_subplot(ax)
    #plt.annotate(r'$\mu=$'+str(avg_hori(months,monthly_num)), \
    #         xy=(0.05,0.75),xycoords='axes fraction')
    plt.title("Month")
    plt.xlim([1,12])

    ax = plt.Subplot(fig,inner_grid[1])
    #ax.bar(years,yearly_num,1,align='center')
    ax.plot(years,yearly_num,'r',years,yearly_num2,'b')
    fig.add_subplot(ax)
    #plt.annotate(r'$\mu_{num}=$'+str(avg_vert(years,yearly_num)), \
     #        xy=(0.05,0.75),xycoords='axes fraction')
    #plt.annotate(r'$\mu_{year}=$'+str(avg_hori(years,yearly_num)), \
    #         xy=(0.05,0.55),xycoords='axes fraction')
    plt.title("Year")
    plt.xlim([start_year,end_year])

    ax = plt.Subplot(fig,inner_grid[2])
    #ax.bar(lats,lat_num,lat_res,align='center')
    ax.plot(lats,lat_num/np.sum(lat_num),'r',lats,lat_num2/np.sum(lat_num2),'b')
    fig.add_subplot(ax)
    #plt.annotate(r'$\mu=$'+str(avg_hori(lats,lat_num)), \
    #             xy=(0.05,0.75),xycoords='axes fraction')
    plt.title("Latitude")
    plt.xlim([min_lat,max_lat])
    
    ax = plt.Subplot(fig,inner_grid[3])
    #ax.bar(lons,lon_num,lon_res,align='center')
    ax.plot(lons,lon_num/np.sum(lon_num),'r',lons,lon_num2/np.sum(lon_num2),'b')
    fig.add_subplot(ax)
    #plt.annotate(r'$\mu=$'+str(avg_hori(lons,lon_num)), \
    #             xy=(0.05,0.75),xycoords='axes fraction')
    plt.title("Longitude")
    plt.xlim([min_lon,max_lon])
    
    ax = plt.Subplot(fig,inner_grid[4])
    #ax.bar(intsys,intsy_num,int((max_wind-min_wind)/len(intsys)),align='center')
    ax.plot(intsys,intsy_num/np.sum(intsy_num),'r',intsys,intsy_num2/np.sum(intsy_num2),'b')
    fig.add_subplot(ax)
    #plt.annotate(r'$\mu=$'+str(avg_hori(intsys,intsy_num)), \
    #             xy=(0.05,0.75),xycoords='axes fraction')
    plt.title("Wind Speed (m/s)")
    plt.xlim([min_wind,max_wind])
    
    ax = plt.Subplot(fig,inner_grid[5])
    #ax.bar(press,pres_num,int((max_press-min_press)/len(press)),align='center')
    ax.plot(press[::-1],pres_num[::-1]/np.sum(pres_num[::-1]),'r',press[::-1],pres_num2[::-1]/np.sum(pres_num2[::-1]),'b')
    fig.add_subplot(ax)
    #plt.annotate(r'$\mu=$'+str(avg_hori(press,pres_num)), \
    #             xy=(0.05,0.75),xycoords='axes fraction')
    plt.title("Pressure (mb)")
    plt.xlim([min_press,max_press])
    
    ax = plt.Subplot(fig,inner_grid[6])
    #ax.bar(durs,wdurd_num,6,align='center')
    ax.plot(durs,wdurd_num/np.sum(wdurd_num),'r',durs,wdurd_num2/np.sum(wdurd_num2),'b')
    fig.add_subplot(ax)
    #plt.annotate(r'$\mu=$'+str(avg_hori(durs,wdurd_num)), \
     #            xy=(0.05,0.75),xycoords='axes fraction')
    plt.title("Wind Life (hrs)")
    plt.xlim([0,6*len(wdurd_num)])
    
    ax = plt.Subplot(fig,inner_grid[7])
    #ax.bar(durs,pdurd_num,6,align='center')
    ax.plot(durs,pdurd_num/np.sum(pdurd_num),'r',durs,pdurd_num2/np.sum(pdurd_num2),'b')
    fig.add_subplot(ax)
    #plt.annotate(r'$\mu=$'+str(avg_hori(durs,pdurd_num)), \
    #             xy=(0.05,0.75),xycoords='axes fraction')
    plt.title("Press Life (hrs)")
    plt.xlim([0,6*len(pdurd_num)])

    ax = plt.Subplot(fig,inner_grid[8])
    ax.plot(pdis,pdi_num/np.sum(pdi_num),'r',pdis,pdi_num2/np.sum(pdi_num2),'b')
    fig.add_subplot(ax)
    plt.title("PDI ($m^3/s^2$)")
    plt.xlim([min_pdi,max_pdi-5*pdi_res])
    plt.ticklabel_format(axis="x", style="sci", scilimits=(0,0))
    
    ax = plt.Subplot(fig,inner_grid[9])
    ax.plot(aces,ace_num/np.sum(ace_num),'r',aces,ace_num2/np.sum(ace_num2),'b')
    fig.add_subplot(ax)
    plt.title("ACE ($m^2/s^2$)")
    plt.xlim([min_ace,max_ace-5*ace_res])
    #plt.ticklabel_format(axis="x", style="sci", scilimits=(0,0))

    fig.legend((l1,l2),('ERAI','IBTrACS'),'upper left')
    
    print("ERAI")
    print("month avg: %s" %(avg_hori(months,monthly_num)))
    print("yearly num avg: %s" %(avg_vert(years,yearly_num)))
    print("lat avg: %s" %(avg_hori(lats,lat_num)))
    print("lon avg: %s" %(avg_hori(lons,lon_num)))
    print("max wind avg: %s" %(avg_hori(intsys,intsy_num)))
    print("min press avg: %s" %(avg_hori(press,pres_num)))
    print("w-life avg: %s" %(avg_hori(durs,wdurd_num)))
    print("p-life avg: %s" %(avg_hori(durs,pdurd_num)))
    print("pdi avg: %s" %(avg_hori(pdis,pdi_num)))
    print("ace avg: %s" %(avg_hori(aces,ace_num)))

    print("IBTRACS")
    print("month avg: %s" %(avg_hori(months,monthly_num2)))
    print("yearly num avg: %s" %(avg_vert(years,yearly_num2)))
    print("lat avg: %s" %(avg_hori(lats,lat_num2)))
    print("lon avg: %s" %(avg_hori(lons,lon_num2)))
    print("max wind avg: %s" %(avg_hori(intsys,intsy_num2)))
    print("min press avg: %s" %(avg_hori(press,pres_num2)))
    print("w-life avg: %s" %(avg_hori(durs,wdurd_num2)))
    print("p-life avg: %s" %(avg_hori(durs,pdurd_num2)))
    print("pdi avg: %s" %(avg_hori(pdis,pdi_num2)))
    print("ace avg: %s" %(avg_hori(aces,ace_num2)))

    return fig


def plot_pval_fig(tcfilename1,tcfilename2,start_year,end_year,year_avg,ref_syear,
                  ref_eyear, min_lat,max_lat,lat_res,min_lon,max_lon,lon_res,
                  min_wind,max_wind,wind_res,min_press,max_press,press_res,
                  dur_days, 
                  outer_grid=gridspec.GridSpec(1,1,wspace=0.0,hspace=0.0)[0],
                  fig=plt.figure(1), title=None):



    [months,monthly_num2,
     years2,yearly_num2,
     lats,lat_num2,
     lons,lon_num2,
     intsys,intsy_num2,
     press,pres_num2,
     durs,wdurd_num2,
     pdurd_num2] = get_all_diags(tcfilename2,ref_syear,ref_eyear,
                                 min_lat,max_lat,lat_res,
                                     min_lon,max_lon,lon_res,
                                     min_wind,max_wind,wind_res,
                                     min_press,max_press,press_res,
                                     dur_days)
    
    pm_vals=[]
    pw_vals=[]
    plat_vals=[]
    plon_vals=[]
    pp_vals=[]
    pwdur_vals=[]
    ppdur_vals=[]
    years=[]

    year_range = end_year-start_year+1
    
    for i in range(year_range):
        calc_year = start_year+i
        years.append(calc_year)
        [start_idx,end_idx] = running_range(year_range,year_avg,i)
        syr = start_idx+start_year
        eyr = end_idx+start_year
    
        [months,monthly_num1,
         years1,yearly_num1,
         lats,lat_num1,
         lons,lon_num1,
         intsys,intsy_num1,
         press,pres_num1,
         durs,wdurd_num1,
         pdurd_num1] = get_all_diags(tcfilename1,syr,eyr,
                                     min_lat,max_lat,lat_res,
                                     min_lon,max_lon,lon_res,
                                     min_wind,max_wind,wind_res,
                                     min_press,max_press,press_res,
                                     dur_days)
        
        [ Pm, Pw, Plat, Plon, 
          Pp, Pwdur, Ppdur ] = get_all_ks_tests(monthly_num1,monthly_num2,
                                                intsy_num1,intsy_num2,
                                                lat_num1,lat_num2,
                                                lon_num1,lon_num2,
                                                pres_num1,pres_num2,
                                                wdurd_num1,wdurd_num2,
                                                pdurd_num1,pdurd_num2)
        pm_vals.append(Pm)                                                            
        pw_vals.append(Pw)                                                            
        plat_vals.append(Plat)                                                            
        plon_vals.append(Plon)                                                            
        pp_vals.append(Pp)                                                            
        pwdur_vals.append(Pwdur)                                                            
        ppdur_vals.append(Ppdur)                                                            
    
    #----------------plotting---------------------#
    fig_rows=4
    fig_cols=2

    inner_grid = gridspec.GridSpecFromSubplotSpec(fig_rows, fig_cols,
                  subplot_spec=outer_grid, wspace=0.5, hspace=0.6)
    #inner_grid.update(left=0.2,right=0.9,top=0.9,bottom=0.15)                  
        

   # plt.subplots_adjust(top=0.9,bottom=0.15,left=0.20,right=0.90,hspace=1.0,wspace=0.7)  

    plt.rc('font',size=6)
    plt.rc('axes', titlesize=7)

    if title: plt.suptitle(title)
    ax = plt.Subplot(fig,inner_grid[0])
    ax.plot(years,pm_vals)
    fig.add_subplot(ax)
    plt.title("month")
    plt.ylim(0.0,1.0)

    ax = plt.Subplot(fig,inner_grid[1])
    ax.plot(years,pw_vals)
    fig.add_subplot(ax)
    plt.title("wind")
    plt.ylim(0.0,1.0)
    
    ax = plt.Subplot(fig,inner_grid[2])
    ax.plot(years,plat_vals)
    fig.add_subplot(ax)
    plt.title("lat")
    plt.ylim(0.0,1.0)

    ax = plt.Subplot(fig,inner_grid[3])
    ax.plot(years,plon_vals)
    fig.add_subplot(ax)
    plt.title("lon")
    plt.ylim(0.0,1.0)
    
    ax = plt.Subplot(fig,inner_grid[4])
    ax.plot(years,pp_vals)
    fig.add_subplot(ax)
    plt.title("press")
    plt.ylim(0.0,1.0)

    ax = plt.Subplot(fig,inner_grid[5])
    ax.plot(years,pwdur_vals)
    fig.add_subplot(ax)
    plt.title("w-life")
    plt.ylim(0.0,1.0)
    
    ax = plt.Subplot(fig,inner_grid[6])
    ax.plot(years,ppdur_vals)
    fig.add_subplot(ax)
    plt.title("p-life")
    plt.ylim(0.0,1.0)

    return fig
