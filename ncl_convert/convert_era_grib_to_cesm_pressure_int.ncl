;***********************************************************************************
; NCL script to convert monthly ERA-I (ds627.0) data to Intermedate file format
;
;***********************************************************************************
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/contrib/cd_string.ncl"
begin


;***********************************************************************************
; Where do we get the data - here we assume the data is on the NCAR /glade drive
; if your data is elsewhere - make a change here
  ERAI_DIR = "/gpfs/fs1/collections/rda/data/ds627.0/ei.oper.an."      ; data will be either in "pl" or "sfc" - used later


if ( .not. isvar("IM_root_name") ) then
  IM_root_name = "ERAI_WRF_"+year
end if


if ( .not. isvar("outDIR") ) then
  outDIR = "OUTPUT"
end if


;***********************************************************************************
; Don't change anything below this line
;***********************************************************************************
;***********************************************************************************

; Which levels do we to extract from the ERA-I data. Much match the ones from CESM
  CLEVS = (/ 1000.0, 975.0, 950.0, 925.0, 900.0, 850.0, 800.0, 750.00, 700.0, 650.0, 600.0, 550.0, 500.0, 450.0, 400.0, 350.0, 300.0, 250.0, 200.0, 150.0, 100.0, 70.0, 50.0, 30.0, 20.0, 10.0 /)
  nlev = dimsizes(CLEVS)

; We need to know the dimensions of the CESM data for interploation
  nlat     = 96
  nlon     = 144

; Set the IM header information 
; These MUCH be the same as for the CESM data - so get the settings from there

  opt = True
  opt@map_source             = "ERAI Average on CESM Grid"
  opt@projection             = 0
  opt@startloc               = "SWCORNER"
  opt@startlon               = 0.0
  opt@startlat               = -90.0
  opt@deltalon               = 2.5
  opt@deltalat               = 0.942408
  opt@deltalat               = 1.894737
  opt@is_wind_earth_relative = False


;***********************************************************************************
; Set up the required IM header information
  FIELD_T          = "TT"
  UNITS_T          = "K"
  DESC_T           = "Temperature"

  FIELD_U          = "UU"
  UNITS_U          = "m s-1"
  DESC_U           = "Zonal Wind Speed"

  FIELD_V          = "VV"
  UNITS_V          = "m s-1"
  DESC_V           = "Meridional Wind Speed"

  FIELD_Q          = "SPECHUMD"
  UNITS_Q          = "kg kg-1"
  DESC_Q           = "Specific Humidity"

  FIELD_R          = "RH"
  UNITS_R          = "%"
  DESC_R           = "Relative Humidity"

  FIELD_Z          = "GHT"
  UNITS_Z          = "m"
  DESC_Z           = "Geopotential Height"

  FIELD_SLP        = "PMSL"
  UNITS_SLP        = "Pa"
  DESC_SLP         = "Sea level pressure"
  XLVL_SLP         = 201300.

  FIELD_PS         = "PSFC"
  UNITS_PS         = "Pa"
  DESC_PS          = "Surface pressure"

  FIELD_U10        = "UU"
  UNITS_U10        = "m s-1"
  DESC_U10         = "10 m Zonal Wind Speed"

  FIELD_V10        = "VV"
  UNITS_V10        = "m s-1"
  DESC_V10         = "10 m Meridional Wind Speed"

  FIELD_T2         = "TT"
  UNITS_T2         = "K"
  DESC_T2          = "2 m Temperature"

  FIELD_Q2         = "SPECHUMD"
  UNITS_Q2         = "kg kg-1"
  DESC_Q2          = "2 m Specific Humidity"

  FIELD_R2         = "RH"
  UNITS_R2         = "%"
  DESC_R2          = "2 m Relative Humidity"

  FIELD_SNOWW6     = "SNOW"
  UNITS_SNOWW6     = "kg m-2"
  DESC_SNOWW6      = "Water Equivalent of Accum Snow Depth"

  FIELD_TSKIN6     = "SKINTEMP"
  UNITS_TSKIN6     = "K"
  DESC_TSKIN6      = "Skin Temperature"

  FIELD_TAVGSFCMON = "TAVGSFC"
  UNITS_TAVGSFCMON = "K"
  DESC_TAVGSFCMON  = "Daily mean of surface air temperature"

  FIELD_SST6       = "SST"
  UNITS_SST6       = "K"
  DESC_SST6        = "Sea Surface Temperature"

  FIELD_ICE6       = "SEAICE"
  UNITS_ICE6       = "fraction"
  DESC_ICE6        = "Sea-Ice-Fraction"

  FIELD_TSOIL1_6   = "ST000010"
  UNITS_TSOIL1_6   = "K"
  DESC_TSOIL1_6    = "Soil Temperature 0-10 cm layer"

  FIELD_TSOIL2_6   = "ST010040"
  UNITS_TSOIL2_6   = "K"
  DESC_TSOIL2_6    = "Soil Temperature 10-40 cm layer"

  FIELD_TSOIL3_6   = "ST040100"
  UNITS_TSOIL3_6   = "K"
  DESC_TSOIL3_6    = "Soil Temperature 40-100 cm layer"

  FIELD_TSOIL4_6   = "ST100200"
  UNITS_TSOIL4_6   = "K"
  DESC_TSOIL4_6    = "Soil Temperature 100-200 cm layer"

  FIELD_MSOIL1_6   = "SM000010"
  UNITS_MSOIL1_6   = "fraction"
  DESC_MSOIL1_6    = "Soil Moisture 0-10 cm layer"

  FIELD_MSOIL2_6   = "SM010040"
  UNITS_MSOIL2_6   = "fraction"
  DESC_MSOIL2_6    = "Soil Moisture 10-40 cm layer"

  FIELD_MSOIL3_6   = "SM040100"
  UNITS_MSOIL3_6   = "fraction"
  DESC_MSOIL3_6    = "Soil Moisture 40-100 cm layer"

  FIELD_MSOIL4_6   = "SM100200"
  UNITS_MSOIL4_6   = "fraction"
  DESC_MSOIL4_6    = "Soil Moisture 100-200 cm layer"

  FIELD_LMASK      ="LANDSEA"
  UNITS_LMASK      ="proprtn"
  DESC_LMASK       ="Land/Sea Flag; 0=Ocean; 1=Land"

  FIELD_ZSFC       ="SOILHGT"
  UNITS_ZSFC       ="m"
  DESC_ZSFC        ="Terrain Elevation"


;***********************************************************************************

; We always need the invariant files - so go ahead and read them in first
  in_ccsm_lmask = addfile(execDIR+"/fracdata_1.9x2.5_gx1v6_c090206.nc","r")  ; static land mask
  CESM_LMASK= int2flt(in_ccsm_lmask->LANDMASK)
  in_ccsm_topo = addfile(execDIR+"/USGS-gtopo30_1.9x2.5_remap_c050602.nc","r")  ; static land mask
  CESM_ZSFC= doubletofloat(in_ccsm_topo->PHIS)/9.81

    First = True
    
    if ( month .lt. 10 ) then
      HDATE2 = year+"-0"+month
    else
      HDATE2 = year+"-"+month
    end if
    if ( day .lt. 10 ) then
      HDATE2 = HDATE2+"-0"+day
    else
      HDATE2 = HDATE2+"-"+day
    end if
    if ( hour .lt. 10 ) then
      HDATE2 = HDATE2+"_0"+hour
    else
      HDATE2 = HDATE2+"_"+hour
    end if
    HDATE = HDATE2+":00:0000000"

    OFILE = IM_root_name+":" + HDATE2                              ; figure the output file name so that we can clobber it
    system ("mkdir -p " + outDIR )                                   ; make the output directories
    system ("rm -f " + OFILE)                                           ; delete the file, so that we don't append to an existing file
    system ("rm -f " + outDIR + "/" + OFILE)                 ; delete the file, so that we don't append to an existing file


    if ( month .lt. 10 ) then
      DATE = tostring(year)+"0"+tostring(month)
      DIR = tostring(year)+"0"+tostring(month)
    else
      DATE = tostring(year)+tostring(month)
      DIR = tostring(year)+tostring(month)
    end if
    if ( day .lt. 10 ) then
      DATE = tostring(DATE)+"0"+tostring(day)
    else
      DATE = tostring(DATE)+tostring(day)
    end if
    if ( hour .lt. 10 ) then
      DATE = tostring(DATE)+"0"+tostring(hour)
    else
      DATE = tostring(DATE)+tostring(hour)
    end if



      print("opening files for " + DATE)
      in1 = addfile(ERAI_DIR+"pl/"+DIR+"/ei.oper.an.pl.regn128sc."+DATE+".grb","r")
      in2 = addfile(ERAI_DIR+"pl/"+DIR+"/ei.oper.an.pl.regn128uv."+DATE+".grb","r")
      in3 = addfile(ERAI_DIR+"sfc/"+DIR+"/ei.oper.an.sfc.regn128sc."+DATE+".grb","r")

        ;vNames1 = getfilevarnames(in1)
        ;nNames1 = dimsizes (vNames1)
        ;print(ERAI_DIR+"pl/"+DIR+"/ei.oper.an.pl.regn128sc."+DATE+".grb")
        ;print(vNames1)
      
        ;vNames2 = getfilevarnames(in2)
        ;nNames2 = dimsizes (vNames2)
        ;print(ERAI_DIR+"pl/"+DIR+"/ei.oper.an.pl.regn128uv."+DATE+".grb")
        ;print(vNames2)
    
        ;vNames3 = getfilevarnames(in3)
        ;nNames3 = dimsizes (vNames3)
        ;print(ERAI_DIR+"sfc/"+DIR+"/ei.oper.an.sfc.regn128sc."+DATE+".grb")
        ;print(vNames3)

        ; Match up ERA levs with ones you want
        ELEVS   = in1->lv_ISBL0
        ;print(ELEVS)
        CLEVSIND = new(nlev,integer)
        do ii = 0,nlev-1
          CLEVSIND(ii) = ind(ELEVS .eq. CLEVS(ii))
        end do
        ;print(CLEVSIND)

        ZSFC = g2fsh_Wrap(in3->Z_GDS4_SFC(::-1,:),(/nlat,nlon/))/9.81

        print("   Get 3D")
        R = g2fsh_Wrap(in1->R_GDS4_ISBL(:,::-1,:),(/nlat,nlon/))
        Q = g2fsh_Wrap(in1->Q_GDS4_ISBL(:,::-1,:),(/nlat,nlon/))
        T = g2fsh_Wrap(in1->T_GDS4_ISBL(:,::-1,:),(/nlat,nlon/))
        Z = g2fsh_Wrap(in1->Z_GDS4_ISBL(:,::-1,:),(/nlat,nlon/))/9.81
        U = g2fsh_Wrap(in2->U_GDS4_ISBL(:,::-1,:),(/nlat,nlon/))
        V = g2fsh_Wrap(in2->V_GDS4_ISBL(:,::-1,:),(/nlat,nlon/))

        print("   Get 2D")
        SLP  = g2fsh_Wrap(in3->MSL_GDS4_SFC(::-1,:),(/nlat,nlon/))
        PS   = g2fsh_Wrap(in3->SP_GDS4_SFC(::-1,:),(/nlat,nlon/))
        U10  = g2fsh_Wrap(in3->10U_GDS4_SFC(::-1,:),(/nlat,nlon/))
        V10  = g2fsh_Wrap(in3->10V_GDS4_SFC(::-1,:),(/nlat,nlon/))
        T2   = g2fsh_Wrap(in3->2T_GDS4_SFC(::-1,:),(/nlat,nlon/))
        D2   = g2fsh_Wrap(in3->2D_GDS4_SFC(::-1,:),(/nlat,nlon/))

        print("   Get SOIL")
        TSOIL1_6 = g2fsh_Wrap(in3->STL1_GDS4_DBLY(::-1,:),(/nlat,nlon/))
        TSOIL2_6 = g2fsh_Wrap(in3->STL2_GDS4_DBLY(::-1,:),(/nlat,nlon/))
        TSOIL3_6 = g2fsh_Wrap(in3->STL3_GDS4_DBLY(::-1,:),(/nlat,nlon/))
        TSOIL4_6 = g2fsh_Wrap(in3->STL4_GDS4_DBLY(::-1,:),(/nlat,nlon/))
        MSOIL1_6 = g2fsh_Wrap(in3->SWVL1_GDS4_DBLY(::-1,:),(/nlat,nlon/))
        MSOIL2_6 = g2fsh_Wrap(in3->SWVL2_GDS4_DBLY(::-1,:),(/nlat,nlon/))
        MSOIL3_6 = g2fsh_Wrap(in3->SWVL3_GDS4_DBLY(::-1,:),(/nlat,nlon/))
        MSOIL4_6 = g2fsh_Wrap(in3->SWVL4_GDS4_DBLY(::-1,:),(/nlat,nlon/))

        print("   Get SEA")
        TSKIN6    = g2fsh_Wrap(in3->SKT_GDS4_SFC(::-1,:),(/nlat,nlon/))
        SST6_TEMP = in3->SSTK_GDS4_SFC(::-1,:)
        ICE6_TEMP = in3->CI_GDS4_SFC(::-1,:)
        SNOWW6    = g2fsh_Wrap(in3->SD_GDS4_SFC(::-1,:),(/nlat,nlon/))*1000.  ; convert from m to kg/m^2
 
        TAVGSFCMON = TSKIN6
	R2 = relhum_ttd(T2,D2,0)
	R2 = R2 < 100.
	R2 = R2 > 0.
	Q2 = mixhum_ptd(PS,D2,2)
	Q2 = Q2 > 0.

	poisson_grid_fill(SST6_TEMP,True,0,2000,0.001,0.6,0)
        SST6 = g2fsh_Wrap(SST6_TEMP,(/nlat,nlon/))
	delete(SST6_TEMP)
	poisson_grid_fill(ICE6_TEMP,True,0,2000,0.001,0.6,0)
        ICE6 = g2fsh_Wrap(ICE6_TEMP,(/nlat,nlon/))
	ICE6 = where(ICE6.lt.0.,0.,ICE6)
	ICE6 = where(ICE6.gt.1.,1.,ICE6)
	delete(ICE6_TEMP)
	SNOWW6 = SNOWW6 > 0.

    ; Adjust T2, TSKIN6, TAVGSFCMON from ERA-Interim interpolated elevation to CESM Elevation
    TOPODIFF = CESM_ZSFC-ZSFC ; take difference in topography between the two datasets
    TSKIN6 = TSKIN6 - TOPODIFF*(0.00649) ; assume International Standard ELR
    TAVGSFCMON = TAVGSFCMON - TOPODIFF*(0.00649) ; assume International Standard ELR
    T2_OLD = T2 ; need this below for psfc correction
    T2 = T2 - TOPODIFF*(0.00649) ; assume International Standard ELR
      
    ; Adjust Psfc using Wallance and Hobbs pg 56: P2=P1*exp[-(z2-z1)/(29.3*Tv)]
	    ; Assume Tv = T(1+0.61*q)
    TV2_AVG = (T2+T2_OLD)/2.*(1.+0.61*Q2) ; average virtual temp
    PS = PS*exp((-1*TOPODIFF)/(29.3*TV2_AVG))

    print(" We are now going to create some IM files for date " + HDATE2)

    opt@date = HDATE

    ; write any non-level variables (including treament of soil temp/moisture profiles as single levels each)
    ; Due to the fact that other programs will read these files, and there we assume the fields to in a in given order,
    ; these order of the writes below are import for this application

    opt@level = 200100.
    wrf_wps_write_int(IM_root_name,FIELD_LMASK,UNITS_LMASK,DESC_LMASK, CESM_LMASK(:,:),opt) 
    wrf_wps_write_int(IM_root_name,FIELD_ZSFC,UNITS_ZSFC,DESC_ZSFC, CESM_ZSFC(:,:),opt) 
    wrf_wps_write_int(IM_root_name,FIELD_TSKIN6,UNITS_TSKIN6,DESC_TSKIN6, TSKIN6(:,:),opt) 
    wrf_wps_write_int(IM_root_name,FIELD_TAVGSFCMON,UNITS_TAVGSFCMON,DESC_TAVGSFCMON, TAVGSFCMON(:,:),opt) 
    wrf_wps_write_int(IM_root_name,FIELD_SST6,UNITS_SST6,DESC_SST6, SST6(:,:),opt) 
    wrf_wps_write_int(IM_root_name,FIELD_ICE6,UNITS_ICE6,DESC_ICE6, ICE6(:,:),opt)
    wrf_wps_write_int(IM_root_name,FIELD_SNOWW6,UNITS_SNOWW6,DESC_SNOWW6, SNOWW6(:,:),opt)
    wrf_wps_write_int(IM_root_name,FIELD_TSOIL1_6,UNITS_TSOIL1_6,DESC_TSOIL1_6, TSOIL1_6(:,:),opt) 
    wrf_wps_write_int(IM_root_name,FIELD_TSOIL2_6,UNITS_TSOIL2_6,DESC_TSOIL2_6, TSOIL2_6(:,:),opt)
    wrf_wps_write_int(IM_root_name,FIELD_TSOIL3_6,UNITS_TSOIL3_6,DESC_TSOIL3_6, TSOIL3_6(:,:),opt)
    wrf_wps_write_int(IM_root_name,FIELD_TSOIL4_6,UNITS_TSOIL4_6,DESC_TSOIL4_6, TSOIL4_6(:,:),opt)
    wrf_wps_write_int(IM_root_name,FIELD_MSOIL1_6,UNITS_MSOIL1_6,DESC_MSOIL1_6, MSOIL1_6(:,:),opt)
    wrf_wps_write_int(IM_root_name,FIELD_MSOIL2_6,UNITS_MSOIL2_6,DESC_MSOIL2_6, MSOIL2_6(:,:),opt)
    wrf_wps_write_int(IM_root_name,FIELD_MSOIL3_6,UNITS_MSOIL3_6,DESC_MSOIL3_6, MSOIL3_6(:,:),opt) 
    wrf_wps_write_int(IM_root_name,FIELD_MSOIL4_6,UNITS_MSOIL4_6,DESC_MSOIL4_6, MSOIL4_6(:,:),opt) 

    opt@level = XLVL_SLP        ; Need a different level for SLP
    wrf_wps_write_int(IM_root_name,FIELD_SLP,UNITS_SLP,DESC_SLP, SLP(:,:),opt) 

    opt@level = 200100.         ; Reset level back to regular surface value
    wrf_wps_write_int(IM_root_name,FIELD_PS,UNITS_PS,DESC_PS, PS(:,:),opt) 
    wrf_wps_write_int(IM_root_name,FIELD_U10,UNITS_U10,DESC_U10, U10(:,:),opt) 	
    wrf_wps_write_int(IM_root_name,FIELD_V10,UNITS_V10,DESC_V10, V10(:,:),opt) 
    wrf_wps_write_int(IM_root_name,FIELD_T2,UNITS_T2,DESC_T2, T2(:,:),opt) 	
    wrf_wps_write_int(IM_root_name,FIELD_R2,UNITS_R2,DESC_R2, R2(:,:),opt) 

    ; Write each level of the 3D fields out separately
    do LEV=0,dimsizes(CLEVS)-1

      opt@level = CLEVS(LEV)*100.
      wrf_wps_write_int(IM_root_name,FIELD_U,UNITS_U,DESC_U, U(CLEVSIND(LEV),:,:),opt)
      wrf_wps_write_int(IM_root_name,FIELD_V,UNITS_V,DESC_V, V(CLEVSIND(LEV),:,:),opt)
      wrf_wps_write_int(IM_root_name,FIELD_T,UNITS_T,DESC_T, T(CLEVSIND(LEV),:,:),opt)
      wrf_wps_write_int(IM_root_name,FIELD_R,UNITS_R,DESC_R, R(CLEVSIND(LEV),:,:),opt)
      wrf_wps_write_int(IM_root_name,FIELD_Z,UNITS_Z,DESC_Z, Z(CLEVSIND(LEV),:,:),opt)

    end do 

    ; move the file to the outDIR directory
      print ("mv " + OFILE + "   " + outDIR + "/.")
      system ("mv " + OFILE + "   " + outDIR + "/.")
      print("  ")

exit
end
status_exit(1)

