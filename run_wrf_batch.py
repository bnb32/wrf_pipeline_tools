import sys,os,subprocess,numpy
import calendar
from string import Template
from datetime import datetime
from  math import ceil
from  math import floor
#import urllib2, cookielib

#----------------------------------------------------------------------------------
#-------------------------Edit Fields in this section only-------------------------
#----------------------------------------------------------------------------------

#Domain (input as an int ex. input 175W as -175, 10S as -10, 35N as 35, etc.)
leftlon = -100
#leftlon = -125
rightlon = -20
#rightlon = 5
bottomlat = 5
#bottomlat = 5
toplat = 45
#toplat = 60

#Resolution as string in meters
resolution = "10000"
#resolution = "30000"

#Time domain (format as "YYYY,MM,DD")
#start_mon = "01"
#end_mon = "12"
#start_day = "01"
#end_day = "31"

if len(sys.argv) < 7:
    print "usage: run_wrf_batch.py <case> <year> <nrun> <start_mon> <end_mon> <start_day> <end_day>"
    sys.exit(1)
else:
    case = sys.argv[1]
    start_yr = end_yr = sys.argv[2]
    nrun = sys.argv[3]
    start_mon=sys.argv[4]
    end_mon=sys.argv[5]
    start_day=sys.argv[6]
    end_day=sys.argv[7]

if start_mon=="01" and end_mon=="12" and start_day=="01" and end_day=="31":
    run_full_year=True
else:
    run_full_year=False

if case == "erai":

    file_name_pref = "ERAI_WRF_"
    exp_id = case + "_" + start_yr
    file_name = file_name_pref + start_yr

else:

    file_name_pref = "CESM_WRF_"
    exp_id = case + "_" + start_yr
    file_name = file_name_pref + case + "_" + start_yr

#User Directory (parent directory to WPS and WRF/test/em_real directories) as string
#Should also be the parent directory to RUNWORKFLOW and templates directories
DIR_USER = "/glade/scratch/bbenton/20XXWRF"
DIR_HOME = "/glade/u/home/bbenton/20XXWRF"
DIR_WRF = DIR_USER + "/WRF_" + nrun
DIR_WPS = DIR_USER + "/WPS_" + nrun
DIR_TEMPLATES = DIR_USER + "/RUNWORKFLOW/batch_templates"

#Input file directory as string
DIR_INPUT = "/glade/scratch/bbenton/20XXWRF/WRF_INT_OUTPUT/" + case + "/" + start_yr

#Output directory as string
DIR_OUTPUT = "/glade/scratch/bbenton/20XXWRF/WRF_OUTPUT/" + case + "/" + start_yr + "/output"

#Project Code as string
project_code = "UCOR0023"

#Interval hours from incoming files
#is usually "06" if GFS
interval_hours = "06" #for incoming files

#account for three digit years - changes namelist entries
if int(start_yr) < 1000: start_yr="0"+start_yr
if int(end_yr) < 1000: end_yr="0"+end_yr

start_time = start_yr + "," + start_mon + "," + start_day
end_time = end_yr + "," + end_mon + "," + end_day



#----------------------------------------------------------------------------------
#-------------------------Do not edit code below this line-------------------------
#----------------------------------------------------------------------------------

def check_wrf_wps_dirs():

    if not (os.path.isfile(DIR_WPS+"/geogrid.exe") and os.path.isfile(DIR_WPS+"/metgrid.exe")):
        subprocess.call("rm -rf "+DIR_WPS, shell=True)
        subprocess.call("cp -r "+DIR_HOME+"/WPS "+ DIR_WPS, shell=True)
    
    if not (os.path.isfile(DIR_WRF+"/test/em_real/real.exe") and os.path.isfile(DIR_WRF+"/test/em_real/wrf.exe")):
        subprocess.call("rm -rf "+DIR_WRF, shell=True)
        subprocess.call("cp -r "+DIR_HOME+"/WRF "+ DIR_WRF, shell=True)


#-------------------------Setting up time, domain and namelists-------------------


#takes in a longitude value as an int and returns in string form
def formatLon(intlon):
	if(intlon<0):
		strlon = str(intlon)[1:]+"W"
	else:
		strlon = str(intlon)+"E"
	return strlon

#takes in a latitude value as an int and returns in string form	
def formatLat(intlat):
	if(intlat<0):
		strlat = str(intlat)[1:]+"S"
	else:
		strlat = str(intlat)+"N"
	return strlat

dx = resolution
dy = resolution


def run_namelist_setup(run_full_year=True):

    #radius of earth times 2*pi/360
    earth_rad=6367470.
    convert_factor = 2.*3.14159265/360.*earth_rad
    
    londistance = (360. - (leftlon - rightlon)) * convert_factor if leftlon > rightlon else abs(leftlon-rightlon)*convert_factor
    e_we = str(int(floor(londistance/int(dx))))
    latdistance = abs(toplat-bottomlat)*convert_factor
    e_sn = str(int(floor(latdistance/int(dy))))
    lonmiddle = (leftlon+rightlon)/2. if leftlon < rightlon else ((leftlon+rightlon)/2. + 180. if (leftlon+rightlon)/2. <= 0 else ((leftlon+rightlon)/2. - 180.)) 
    ref_lon = str(lonmiddle)
    latmiddle = (toplat+bottomlat)/2.
    ref_lat = str(latmiddle)
    
    stand_lon = ref_lon
    
    truelat1 = ref_lat
    truelat2 = "0.0"
    geog_data_res = '10m'
    
    lonW = formatLon(leftlon)
    lonE = formatLon(rightlon)
    latS = formatLat(bottomlat)
    latN = formatLat(toplat)
    
    #findDomain(leftlon,rightlon,bottomlat,toplat,resolution)
    
    startyear,startmonth,startday = start_time.split(",", 2)
    starthour = "00"
    startmin = "00"
    startsec = "00"
    
    endyear, endmonth, endday = end_time.split(",", 2)
    endhour = "18"
    #endhour = "00"
    endmin = "00"
    endsec = "00"
    
    timeDict ={'year':startyear,'month':startmonth, 'day':startday, 'hour':starthour, 'min':startmin, 'sec':startsec}
    time_template = Template("$year-$month-$day _$hour:$min:$sec")
    
    if not os.path.exists(DIR_OUTPUT):
        os.makedirs(DIR_OUTPUT)
    
    try:	
        with open(DIR_TEMPLATES + '/template_namelist.wps', 'r') as namelistwps:
    		NAMELIST_WPS = namelistwps.read()
        with open(DIR_TEMPLATES + '/template_namelist.input', 'r') as namelistwrf:
    		NAMELIST_WRF = namelistwrf.read()
        with open(DIR_TEMPLATES + '/template_rungeogrid.csh', 'r') as rungeogrid:
    		RUN_GEOGRID = rungeogrid.read()
        with open(DIR_TEMPLATES + '/template_runmetgrid.csh', 'r') as runmetgrid:
    		RUN_METGRID = runmetgrid.read()
        with open(DIR_TEMPLATES + '/template_runreal.csh', 'r') as runreal:
    		RUN_REAL = runreal.read()
        with open(DIR_TEMPLATES + '/template_runwrf.csh', 'r') as runwrf:
    		RUN_WRF = runwrf.read()
    
    except:
        print 'Error reading template files'
        exit()
    
    #namelists
    #%PREFIX%
    prefix = " prefix = '" + file_name + "',"
    
    #%FGNAME%
    fg_name = " fg_name = '" + file_name + "'"
    
    
    #%DATES%
    starttime = time_template.substitute(timeDict).replace(" ", "")
    wps_dates = " start_date = '" + starttime + "' \n"
    
    wrf_dates = ' start_year = '
    wrf_dates = wrf_dates + timeDict['year']
    wrf_dates = wrf_dates + ',\n start_month = '
    wrf_dates = wrf_dates + timeDict['month']
    wrf_dates = wrf_dates + ',\n start_day = '
    wrf_dates = wrf_dates + timeDict['day']
    wrf_dates = wrf_dates + ',\n start_hour = '
    wrf_dates = wrf_dates + timeDict['hour']
    wrf_dates = wrf_dates + ',\n start_minute = '
    wrf_dates = wrf_dates + '00, '
    wrf_dates = wrf_dates + '\n start_second = '
    wrf_dates = wrf_dates + '00, \n'
    
    timeDict['year'] = endyear
    timeDict['month'] = endmonth
    timeDict['day'] = endday
    timeDict['hour'] = endhour
    endtime = time_template.substitute(timeDict).replace(" ", "")
    wps_dates += " end_date = \'" + endtime + "' \n"
    
    wrf_dates += ' end_year = '
    wrf_dates = wrf_dates + timeDict['year']
    wrf_dates = wrf_dates + ',\n end_month = '
    wrf_dates = wrf_dates + timeDict['month']
    wrf_dates = wrf_dates + ',\n end_day = '
    wrf_dates = wrf_dates + timeDict['day']
    wrf_dates = wrf_dates + ',\n end_hour = '
    wrf_dates = wrf_dates + timeDict['hour']
    wrf_dates = wrf_dates + ',\n end_minute = '
    wrf_dates = wrf_dates + endmin
    wrf_dates = wrf_dates + '\n end_second = '
    wrf_dates = wrf_dates + endsec + ', \n'
    
    interval_seconds = int(interval_hours)*3600
    wps_dates += " interval_seconds = " + str(interval_seconds) + ""
    wrf_dates += " interval_seconds = " + str(interval_seconds) + ","
    
    #%TIMESTEP%
    #time_step should be 6 times dx (in km)
    #only multiply by 3 because of cfl errors
    time_step = int(dx)/1000
    time_step = time_step*3
    #time_step = int(time_step*1.5)
    wrf_timestep = " time_step = " + str(time_step) + ",\n"
    
    
    #%GEOS%
    wps_geos = " dx = " + dx + ",\n"
    wps_geos += " dy = " + dy + ",\n"
    wps_geos += " e_we = " + e_we + ",\n"
    wps_geos += " e_sn = " + e_sn + ",\n"
    wps_geos += " ref_lat = " + ref_lat + ",\n"
    wps_geos += " ref_lon = " + ref_lon + ",\n"
    wps_geos += " truelat1 = " + truelat1 + ",\n"
    wps_geos += " truelat2 = " + truelat2 + ",\n"
    wps_geos += " stand_lon = " + stand_lon + ","
    
    wrf_geos = " e_we = " + e_we + ",\n"
    wrf_geos += " e_sn = " + e_sn + ",\n"
    
    
    #%GEOS2%
    #if(int(startyear)>2004):
    #	wrf_geos2 = " num_metgrid_soil_levels = 4" + ",\n"
    #else:
    #	wrf_geos2 = " num_metgrid_soil_levels = 2" + ",\n"
    wrf_geos2 = " dx = " + dx + ",\n"
    wrf_geos2 += " dy = " + dy + ",\n"
    
    #%RUNTIME%
    if run_full_year:
    
        run_d = 364
        run_h = 18
        run_m = 0
        run_s = 0
   
    else:
        runstart =datetime(int(startyear), int(startmonth), int(startday), int(starthour), int(startmin), int(startsec))
        runend = datetime(int(endyear), int(endmonth), int(endday), int(endhour), int(endmin), int(endsec))
        runtime = runend - runstart
        run_d = runtime.days
        run_h = divmod(runtime.seconds, 3600)
        run_m = divmod(run_h[1], 60)
        run_s = run_m[1]
        run_h = run_h[0]
	run_m = run_m[0]

    wrf_runtime = " run_days = " + str(run_d) + ",\n"
    wrf_runtime += " run_hours = " + str(run_h) + ",\n"
    wrf_runtime += " run_minutes = " + str(run_m) + ",\n"
    wrf_runtime += " run_seconds = " + str(run_s) + ","
   
    #.csh files
    
    #%NAME%
    csh_name = exp_id
    
    #%DIRECTORY%
    csh_wps_dir = DIR_WPS
    
    csh_wrf_dir = DIR_WRF+"/test/em_real"
    
    #%TASKS%
    total_tasks = float(e_we) * float(e_sn) * 30.
    total_tasks = total_tasks/100000.
    total_tasks = int(ceil(total_tasks/15.0))+1
    total_tasks = total_tasks * 15
    
    runwrf_tasks = str(total_tasks)
    
    #%LINK%
    runmet_link = "ln -sf " + DIR_WPS+"/met_em* " + DIR_WRF+"/test/em_real"
    
    #%OUTPUT%
    os.chdir(DIR_OUTPUT)
    #EnsembleNum = int(len([name for name in os.listdir('.') if os.path.isfile(name)])) 
    #while(len(str(EnsembleNum))<3):
    #		EnsembleNum = "0" + str(EnsembleNum)
    #filename = "wrfout_"+EnsembleNum+"_"+start_time.replace(",","")+"-"+end_time.replace(",","")+"."+lonW+"-to-"+lonE+"."+latS+"-to-"+latN+".nc"
    filename = "wrfout_"+start_time.replace(",","")+"-"+end_time.replace(",","")+"."+lonW+"-to-"+lonE+"."+latS+"-to-"+latN+".nc"
    
    runwrf_output = "mv wrfout_d01_"+starttime+ " " + filename + "\n"
    runwrf_output += "mv " + filename + " " + DIR_OUTPUT + "\n"
    runwrf_output += "mv wrfrst_d01_*" + " " + DIR_OUTPUT + "\n"
    runwrf_output += "mkdir " + DIR_OUTPUT+"/../info\n"
    runwrf_output += "mv rsl.* " + DIR_OUTPUT+"/../info\n"
    runwrf_output += "cp namelist.input " + DIR_OUTPUT+"\n"
    
    
    with open('namelist.wps', 'w') as namelistwps:
    	namelistwps.write(NAMELIST_WPS.replace('%DATES%', wps_dates).replace('%GEOS%', wps_geos).replace('%PREFIX%', prefix).replace('%FGNAME%', fg_name))
    	namelistwps.close()
    with open('namelist.input', 'w') as namelistwrf:
    	namelistwrf.write(NAMELIST_WRF.replace('%DATES%', wrf_dates).replace('%TIMESTEP%', wrf_timestep).replace('%GEOS%', wrf_geos).replace('%RUNTIME%', wrf_runtime).replace('%GEOS2%', wrf_geos2))
    	namelistwrf.close()
    with open('rungeogrid.csh', 'w') as rungeo:
    	rungeo.write(RUN_GEOGRID.replace('%PROJECTCODE%', project_code).replace('%NAME%', exp_id).replace('%DIRECTORY%', csh_wps_dir))
    	rungeo.close()
    with open('runmetgrid.csh', 'w') as runmet:
    	runmet.write(RUN_METGRID.replace('%PROJECTCODE%', project_code).replace('%NAME%', exp_id).replace('%DIRECTORY%', csh_wps_dir).replace('%LINK%', runmet_link))
    	runmet.close()
    with open('runreal.csh', 'w') as runreal:
    	runreal.write(RUN_REAL.replace('%PROJECTCODE%', project_code).replace('%NAME%', exp_id).replace('%DIRECTORY%', csh_wrf_dir))
    	runreal.close()	
    with open('runwrf.csh', 'w') as runwrf:
    	runwrf.write(RUN_WRF.replace('%PROJECTCODE%', project_code).replace('%NAME%', exp_id).replace('%DIRECTORY%', csh_wrf_dir).replace('%TASKS%', runwrf_tasks).replace('%OUTPUT%', runwrf_output))
    	runwrf.close()
    
    #move namelist.wps into the WPS directory and namelist.input into the em_real directory
    subprocess.call(["mv", "namelist.wps", DIR_WPS])
    subprocess.call(["mv", "rungeogrid.csh", DIR_WPS])
    subprocess.call(["mv", "runmetgrid.csh", DIR_WPS])
    subprocess.call(["mv", "namelist.input", DIR_WRF+"/test/em_real"])
    subprocess.call(["mv", "runreal.csh", DIR_WRF+"/test/em_real"])
    subprocess.call(["mv", "runwrf.csh", DIR_WRF+"/test/em_real"])
    
    [os.remove(os.path.join(DIR_WRF+"/test/em_real",f)) for f in os.listdir(DIR_WRF+"/test/em_real") if f.startswith("met_em.")]



#----------WRF Preprocessing----------

def run_wps():

    os.chdir(DIR_WPS)
    
    #remove any existing intermediate files to avoid confusion
    [os.remove(os.path.join(DIR_WPS,f)) for f in os.listdir(DIR_WPS) if f.startswith("met_em.")]
    [os.remove(os.path.join(DIR_WPS,f)) for f in os.listdir(DIR_WPS) if f.startswith("geogrid.log.")]
    [os.remove(os.path.join(DIR_WPS,f)) for f in os.listdir(DIR_WPS) if f.startswith("metgrid.log.")]
    
    [os.remove(os.path.join(DIR_WPS,f)) for f in os.listdir(DIR_WPS) if f.startswith(file_name_pref)]
    
    #cmd="ln -sf "+DIR_INPUT+"/"+file_name+"\:{"+start_yr+".."+end_yr+"}-{"+start_mon+".."+end_mon+"}-{"+start_day+".."+end_day+"}* "+DIR_WPS
    cmd="ln -sf "+DIR_INPUT+"/"+file_name+"\:* "+DIR_WPS
    subprocess.call(cmd, shell=True)
    
    GEO = subprocess.check_output('qsub -h rungeogrid.csh', shell=True).strip()	
    print "running geogrid.exe"
    print GEO
    MET = subprocess.check_output('qsub -W depend=afterok:%s runmetgrid.csh' %GEO, shell=True).strip()
    print "running metgrid.exe"
    print MET
    return GEO,MET
 
#----------WRF----------#


def run_wrf(GEO,MET):

    os.chdir(DIR_WRF+"/test/em_real")
    [os.remove(os.path.join('.',f)) for f in os.listdir('.') if (f.startswith("wrf") and f.endswith(".out"))]
    
    subprocess.call("rm -f *ctrl*; rm -f *forced*; rm -f *erai*; rm -f wrfout*;", shell=True)
    
    print "calling real.exe"
    REAL = subprocess.check_output('qsub -W depend=afterok:%s runreal.csh' %MET, shell=True).strip()
    print REAL
    
    print "calling wrf.exe"
    WRF = subprocess.check_output('qsub -W depend=afterok:%s runwrf.csh' %REAL, shell=True).strip()
    print WRF
    
    #release geogrid hold
    subprocess.check_output('qrls %s' %GEO, shell=True)


#----------run routine----------#

check_wrf_wps_dirs()
run_namelist_setup(run_full_year)
GEO,MET=run_wps()
run_wrf(GEO,MET)
