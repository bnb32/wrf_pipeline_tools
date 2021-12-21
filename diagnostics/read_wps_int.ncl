;******************************************************************************
; NCL script to convert CESM data to Intermediate file format
;
;;******************************************************************************

load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/contrib/cd_string.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl" 
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/popRemap.ncl"

;sst_mons=new(12,float)

begin

;do mon=1,12

;if(mon.lt.10) then month="0"+tostring(mon) 
;else month=tostring(mon)
;end if

inDIR = "/glade/u/home/bbenton/scratch/20XXWRF/WRF_INT_OUTPUT/" + case + "/" + year
cmd="ls "+inDIR+"/CESM_WRF_"+case+"_"+year+":"+year+"-*" ;+month+"*"

myFiles=systemfunc(cmd)
sst_arr=new(dimsizes(myFiles),float)

do fnum=0,dimsizes(sst_arr)-1
    inFILE=myFiles(fnum)
    slabs=wrf_wps_read_int(inFILE)
    ;print(slabs@field)
    sst_avg=avg(slabs(4,47:77,:))
    ;sst_avg=avg(slabs(3,47:77,:))
    sst_arr(fnum)=sst_avg
end do 

sst_avg=avg(sst_arr)
delete(myFiles)
delete(sst_arr)
print(tofloat(sst_avg))
;sst_mons(mon-1)=sst_avg

;end do

;print(tofloat(avg(sst_mons)))

end  

