;***********************************************************************************
; NCL script to convert IBTracs netcdf data to tstorms format for diagnostics 
;
;***********************************************************************************
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/contrib/cd_string.ncl"
begin

;***********************************************************************************

;year=1995
in_dir="~/scratch/20XXWRF/IBTRACS_DATA"
in_file="Year."+year+".ibtracs_wmo.v03r10.nc"
;out_dir="/glade/u/home/bbenton/scratch/20XXWRF/TSTORMS_OUTPUT/ibtracs/"+year
out_file="traj_out_ibtracs_"+year
fout=out_dir+"/"+out_file

system("mkdir -p " + out_dir)
system("rm -f "+fout)

tracks = addfile(in_dir+"/"+in_file,"r")

lat = (tracks->lat_wmo)*0.01
lon = (tracks->lon_wmo)*0.01
wind = (tracks->wind_wmo)*0.5144*0.1
pres = (tracks->pres_wmo)*0.1
time_int = (tracks->time_wmo)
time_int@calendar = "julian"
time_int@units = "days since 1858-11-17 00:00:00"
time = cd_calendar(time_int,0)
num_steps = tracks->numObs
storm_id = tracks->storm_sn
basin_id = tracks->genesis_basin
total_storms = dimsizes(storm_id(:,0))

; output in following format:
; for a given storm track
; start no_steps year month day hour
; for following steps
; lon lat wind pressure year month day hour


do snum=0,total_storms-1
    ;print(pres(snum,:num_steps(snum)-1))
    if((basin_id(snum) .eq. 0) .or. (basin_id(snum) .eq. 3)) then
        output_head = [/(/"start "+num_steps(snum)+" "+time(snum,0,0)+ \
               " "+time(snum,0,1)+" "+time(snum,0,2)+" "+time(snum,0,3)/)/]   
        write_table(fout,"a",output_head,"%s")
        do step_num=0,num_steps(snum)-1
            output_line = [/(/lon(snum,step_num)+" "+lat(snum,step_num)+ \
	           " "+wind(snum,step_num)+" "+pres(snum,step_num)+ \
		   " "+time(snum,step_num,0)+" "+time(snum,step_num,1)+ \
		   " "+time(snum,step_num,2)+" "+time(snum,step_num,3)/)/]
            write_table(fout,"a",output_line,"%s")
        end do
    end if
end do    

exit
end
status_exit(1)

