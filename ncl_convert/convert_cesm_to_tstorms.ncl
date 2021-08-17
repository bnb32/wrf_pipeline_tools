;******************************************************************************
; NCL script to convert CESM data to TSTORMS format
;
;;******************************************************************************

load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/contrib/cd_string.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl" 
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/popRemap.ncl"

begin

  input_file = fin
  out_file = "tstorms_input_" + case + "_" + year + ".nc"
  ;outDIR = "/glade/u/home/bbenton/scratch/20XXWRF/CESM_DATA/forced/2005"
  outDIR = "/glade/u/home/bbenton/scratch/20XXWRF/CESM_DATA/" + case + "/TSTORMS"
  output_file = outDIR + "/" + out_file

  print("input file " + fin)
  print("outDIR: " + outDIR)

;******************************************************************************
; Don't change anything below this line
;******************************************************************************

  mon_days = (/31,28,31,30,31,30,31,31,30,31,30,31/)
  ;m_index = stringtointeger(month)

  ;t_steps = 4*mon_days(m_index-1)-1


;************************************************
; file handling
;************************************************
  system("/bin/rm -f " + output_file)
  
  topo_dir = "/glade/u/home/bbenton/20XXWRF/CESM_to_Int/Invariant_Data"
  topo_file = "USGS-gtopo30_1.9x2.5_remap_c050602.nc"

  print("opening file")
  in_cam   = addfile(input_file,"r") 
  ftopo = addfile(topo_dir + "/" + topo_file,"r")
  fout = addfile(output_file,"c")

;************************************************
; read needed variables from file
;************************************************
  print("read variables in")

  P0 = 0.01*in_cam->P0       
  time = in_cam->time                            
  lon = in_cam->lon
  lat = in_cam->lat
  lev = in_cam->lev

  ntim = dimsizes(time) 
  nlev = dimsizes(lev) 
  nlat  = dimsizes(lat)  
  nlon  = dimsizes(lon)

  T = in_cam->T                               
  U = in_cam->U                          
  V = in_cam->V 
  Z = in_cam->Z3
  PS   = in_cam->PS      
  PSL = in_cam->PSL
  hyam = in_cam->hyam                            
  hybm = in_cam->hybm                      

  PHIS = ftopo->PHIS
  tbot = T(:,nlev-1,:,:)

;************************************************
; convert variables to tstorms format
;************************************************
  print("convert variables")

  lev_p = (/ 1000, 850, 500, 200 /)

  ;ZP = vinth2p(Z,hyam,hybm,lev_p,PS,1,P0,1,True)
  ;UP = vinth2p(U,hyam,hybm,lev_p,PS,1,P0,1,True)
  ;VP = vinth2p(V,hyam,hybm,lev_p,PS,1,P0,1,True)
  ;TP = vinth2p(T,hyam,hybm,lev_p,PS,1,P0,1,True)
  
  ZP = vinth2p_ecmwf(Z,hyam,hybm,lev_p,PS,1,P0,1,True,-1,tbot,PHIS)
  UP = vinth2p_ecmwf(U,hyam,hybm,lev_p,PS,1,P0,1,True,0,tbot,PHIS)
  VP = vinth2p_ecmwf(V,hyam,hybm,lev_p,PS,1,P0,1,True,0,tbot,PHIS)
  TP = vinth2p_ecmwf(T,hyam,hybm,lev_p,PS,1,P0,1,True,1,tbot,PHIS)
  
  Z1000 = ZP(:,0,:,:)
  ;Z1000 = Z(:,nlev-1,:,:)
  Z200 = ZP(:,3,:,:)
  ;UBOT = UP(:,0,:,:)
  UBOT = U(:,nlev-1,:,:)
  ;VBOT = VP(:,0,:,:)
  VBOT = V(:,nlev-1,:,:)
  U850 = UP(:,1,:,:)
  V850 = VP(:,1,:,:)
  T500 = TP(:,2,:,:)
  T200 = TP(:,3,:,:)
  
;************************************************
; write to output
;************************************************
  print("write to output")

  setfileoption(fout,"DefineMode",True)
  
  fAtt = True 
  fAtt@title         = "cesm to tstorms output"  
  fAtt@source_file   =  input_file
  fAtt@Conventions   = "None"  
  fAtt@creation_date = systemfunc ("date")        
  fileattdef( fout, fAtt ) 
  
  dimNames = (/"time", "lat", "lon" /)  
  dimSizes = (/ -1   ,  nlat,  nlon /) 
  dimUnlim = (/ True , False, False /)  
  filedimdef(fout,dimNames,dimSizes,dimUnlim)
  
  filevardef(fout, "time" ,typeof(time),getvardims(time)) 
  ;filevardef(fout, "lev" ,typeof(lev),getvardims(lev))                           
  filevardef(fout, "lat" ,typeof(lat),getvardims(lat))                         
  filevardef(fout, "lon" ,typeof(lon),getvardims(lon))                         
  filevardef(fout, "Z1000" ,typeof(Z1000),getvardims(Z1000))    
  filevardef(fout, "Z200" ,typeof(Z200),getvardims(Z200))          
  filevardef(fout, "U850" ,typeof(U850),getvardims(U850))          
  filevardef(fout, "V850" ,typeof(V850),getvardims(V850))          
  filevardef(fout, "T500" ,typeof(T500),getvardims(T500))          
  filevardef(fout, "T200" ,typeof(T200),getvardims(T200))    
  filevardef(fout, "UBOT" ,typeof(UBOT),getvardims(UBOT))    
  filevardef(fout, "VBOT" ,typeof(VBOT),getvardims(VBOT))    
  filevardef(fout, "PSL" ,typeof(PSL),getvardims(PSL))    
  
  filevarattdef(fout,"time",time)                    
  ;filevarattdef(fout,"lev",lev)                    
  filevarattdef(fout,"lat",lat)                     
  filevarattdef(fout,"lon",lon)                     
  filevarattdef(fout,"Z1000",Z1000)
  filevarattdef(fout,"Z200",Z200)
  filevarattdef(fout,"U850",U850)
  filevarattdef(fout,"V850",V850)
  filevarattdef(fout,"T500",T500)
  filevarattdef(fout,"T200",T200)
  filevarattdef(fout,"UBOT",UBOT)
  filevarattdef(fout,"VBOT",VBOT)
  filevarattdef(fout,"PSL",PSL)
  
  setfileoption(fout,"DefineMode",False)
  
  fout->time   = (/time/)     
  ;fout->lev    = (/lev/)
  fout->lat    = (/lat/)
  fout->lon    = (/lon/) 
  fout->Z1000    = (/Z1000/) 
  fout->Z200    = (/Z200/) 
  fout->U850    = (/U850/) 
  fout->V850    = (/V850/) 
  fout->T500    = (/T500/) 
  fout->T200    = (/T200/) 
  fout->UBOT    = (/UBOT/) 
  fout->VBOT    = (/VBOT/) 
  fout->PSL    = (/PSL/) 

exit
end
status_exit(1)
