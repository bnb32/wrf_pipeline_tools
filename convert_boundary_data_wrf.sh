#! /bin/bash

if [[ $# -eq 3 ]] && [[ ("$1" = "ctrl") || ("$1" = "forced") ]]; then 
    CASE=$1; YEAR=$2; EXT_FLAG=$3;
elif [[ $# -eq 4 ]] && [[ "$1" = "erai" ]]; then    
    CASE=$1; YEAR=$2; EXT_FLAG=$3; MONTH=$4
elif [[ ! -z ${CASE} ]] && [[ ! -z ${YEAR} ]] && 
     [[ ! -z ${EXT_FLAG} ]] && [[ ! -z ${MONTH} ]] && 
     [[ "$CASE" = "erai" ]]; then :
elif [[ ! -z ${CASE} ]] && [[ ! -z ${YEAR} ]] && 
     [[ ! -z ${EXT_FLAG} ]] && [[ -z ${MONTH} ]] && 
     [[ ("$CASE" = "ctrl") || ("$CASE" = "forced") ]]; then :
elif [[ -z ${CASE} ]] || [[ -z ${YEAR} ]] || 
     [[ -z ${EXT_FLAG} ]] || [[ -z ${MONTH} ]]; then
    echo "usage $0: case year ext_flag month (for erai)"; exit 1; fi

source ~/RUNWORKFLOW/pipeline_env_info.sh ${CASE} ${YEAR}

extract_wrf_data() {

    OUTDIR=${CESM_WRF_DIR}/${YEAR}; make_dir $OUTDIR

    rm -f ${OUTDIR}/*.tmp
    
    # cam output
    if ! file_exists ${OUTDIR}/cam_out.nc; then 
    cp ${CESM_DIR}/${YEAR}/${ATM_FILE_YEAR} ${OUTDIR}/cam_out.nc
    ncrename -v TS,ts -v Z3,PHIS ${OUTDIR}/cam_out.nc; fi
    if ! file_exists ${OUTDIR}/atmos_ta.nc; then
    ncks -v T,hyai,hybi ${OUTDIR}/cam_out.nc ${OUTDIR}/atmos_ta.nc; fi
    if ! file_exists ${OUTDIR}/atmos_ua.nc; then
    ncks -v U ${OUTDIR}/cam_out.nc ${OUTDIR}/atmos_ua.nc; fi
    if ! file_exists ${OUTDIR}/atmos_va.nc; then
    ncks -v V ${OUTDIR}/cam_out.nc ${OUTDIR}/atmos_va.nc; fi
    if ! file_exists ${OUTDIR}/atmos_hus.nc; then
    ncks -v Q ${OUTDIR}/cam_out.nc ${OUTDIR}/atmos_hus.nc; fi
    if ! file_exists ${OUTDIR}/atmos_ps.nc; then
    ncks -v PS ${OUTDIR}/cam_out.nc ${OUTDIR}/atmos_ps.nc; fi
    if ! file_exists ${OUTDIR}/atmos_ts_1.nc; then
    ncks -v ts ${OUTDIR}/cam_out.nc ${OUTDIR}/atmos_ts_1.nc; fi
    rm ${OUTDIR}/cam_out.nc
    
    # land output
    if ! file_exists ${OUTDIR}/lnd_out.nc; then 
    cp ${CESM_DIR}/${YEAR}/${LND_FILE_YEAR} ${OUTDIR}/lnd_out.nc
    ncrename -v landmask,LANDMASK -v TSOI,tsl -v SOILLIQ,mrlsl ${OUTDIR}/lnd_out.nc
    ncap2 -O -s "snw=1000*SNOWDP" ${OUTDIR}/lnd_out.nc -o ${OUTDIR}/lnd_out.nc
    ncatted -O -a units,snw,o,c,"kg/m2" ${OUTDIR}/lnd_out.nc
    ncatted -O -a long_name,snw,o,c,"snow water equivalent" ${OUTDIR}/lnd_out.nc; fi

    if ! file_exists ${OUTDIR}/atmos_snw_1.nc; then 
    ncks -v snw ${OUTDIR}/lnd_out.nc ${OUTDIR}/atmos_snw_1.nc; fi
    if ! file_exists ${OUTDIR}/atmos_tsl_1.nc; then 
    ncks -v tsl ${OUTDIR}/lnd_out.nc ${OUTDIR}/atmos_tsl_1.nc; fi
    if ! file_exists ${OUTDIR}/atmos_mrlsl_1.nc; then 
    ncks -v mrlsl ${OUTDIR}/lnd_out.nc ${OUTDIR}/atmos_mrlsl_1.nc; fi
    rm ${OUTDIR}/lnd_out.nc
    
    # ocean output
    if ! file_exists ${OUTDIR}/ocn_out.nc; then 
    cp ${CESM_DIR}/${YEAR}/${OCN_FILE_YEAR} ${OUTDIR}/ocn_out.nc
    ncap2 -O -s "tos=SST+273.15f" ${OUTDIR}/ocn_out.nc -o ${OUTDIR}/ocn_out.nc
    ncatted -O -a units,tos,o,c,"K" ${OUTDIR}/ocn_out.nc; fi
    if ! file_exists ${OUTDIR}/atmos_tos_1.nc; then 
    ncks -v tos ${OUTDIR}/ocn_out.nc ${OUTDIR}/atmos_tos_1.nc; fi
    rm ${OUTDIR}/ocn_out.nc
    
    # ice output
    if ! file_exists ${OUTDIR}/ice_out.nc; then 
    cp ${CESM_DIR}/${YEAR}/${ICE_FILE_YEAR} ${OUTDIR}/ice_out.nc; fi
    if ! file_exists ${OUTDIR}/atmos_sic_1.nc; then 
    ncks -v aice_d ${OUTDIR}/ice_out.nc ${OUTDIR}/atmos_sic_1.nc; fi
    rm ${OUTDIR}/ice_out.nc

}

if is_cesm_case $CASE; then

    if [ "${EXT_FLAG}" = "1" ]; then extract_wrf_data; fi    
    
    CINT_DIR=${ROOT_DIR}/CINT_CONV; IN_DIR=${CESM_WRF_DIR}/${YEAR}
    
    make_dir ${CINT_DIR}
    if [ ! -f ${CINT_DIR}/${WRF_CONV_FILE} ]; then
        cp ${NCL_CONV_DIR}/${WRF_CONV_FILE} ${CINT_DIR}/${WRF_CONV_FILE}
    fi    
    if [ ! -f ${CINT_DIR}/atmos_zsfc.nc ]; then
        ln -sf ${SCRIPT_DIR}/Invariant_Data/${TOPO_FILE} ${CINT_DIR}/atmos_zsfc.nc
    fi
    if [ ! -f ${CINT_DIR}/atmos_lmask.nc ]; then
        ln -sf ${SCRIPT_DIR}/Invariant_Data/${LFRAC_FILE} ${CINT_DIR}/atmos_lmask.nc
    fi
    if [ ! -f ${CINT_DIR}/${MAP_FILE} ]; then
        cp ${SCRIPT_DIR}/Invariant_Data/${MAP_FILE} ${CINT_DIR}/${MAP_FILE}
    fi
    
    cd ${CINT_DIR}
    
    print_line "extracting cesm intermediate files: ${CASE} ${YEAR}"
    ncl "case=\"${CASE}\"" "year=\"${YEAR}\"" "dir_in=\"${IN_DIR}\"" ${CINT_DIR}/${WRF_CONV_FILE} 
    check_exit "error extracting cesm intermediate files: ${CASE} ${YEAR}"
    
fi
    
if is_erai_case $CASE; then

    EINT_DIR=${ROOT_DIR}/EINT_CONV; OUT_DIR=${WRF_INT_DIR}/${YEAR}
    DAYS=(31 28 31 30 31 30 31 31 30 31 30 31)
    
    make_dir ${EINT_DIR}
    if [ ! -f ${EINT_DIR}/${ERAI_CONV_FILE} ]; then
        cp ${NCL_CONV_DIR}/${ERAI_CONV_FILE} ${EINT_DIR}/${ERAI_CONV_FILE}
    fi
    
    if [ ! -f ${EINT_DIR}/${LFRAC_FILE} ]; then
        ln -sf ${SCRIPT_DIR}/Invariant_Data/${LFRAC_FILE} ${EINT_DIR}/${LFRAC_FILE}
    fi
    
    if [ ! -f ${EINT_DIR}/${TOPO_FILE} ]; then
        ln -sf ${SCRIPT_DIR}/Invariant_Data/${TOPO_FILE} ${EINT_DIR}/${TOPO_FILE}
    fi
    
    cd ${EINT_DIR}
    
    print_line "extracting erai intermediate files: ${YEAR} ${MONTH}"
    for ((DAY=1; DAY<=$((${DAYS[MONTH-1]})); DAY++)); do
        for ((TSTEP=0; TSTEP<=3; TSTEP++)); do
            HOUR=$((6*TSTEP))
    	ncl year=${YEAR} month=${MONTH} day=${DAY} hour=${HOUR} "outDIR=\"${OUT_DIR}\"" "execDIR=\"${EINT_DIR}\"" ${EINT_DIR}/${ERAI_CONV_FILE}
    	check_exit "error extracting erai intermediate files: ${YEAR} ${MONTH} ${DAY}"
        done
    done

fi
