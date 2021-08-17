#!/bin/bash

if [ $# -ne 6 ]; then echo usage $0: case year start_mon end_mon start_day end_day; exit 1; fi

CASE=$1; YEAR=$2
S_MON=$3; E_MON=$4
S_DAY=$5; E_DAY=$6

source ~/RUNWORKFLOW/pipeline_env_info.sh ${CASE} ${YEAR}

is_cesm_data() {
    if [ ! -f ${CESM_DIR}/${YEAR}/${ATM_FILE_YEAR} ] ||
       [ ! -f ${CESM_DIR}/${YEAR}/${LND_FILE_YEAR} ] ||
       [ ! -f ${CESM_DIR}/${YEAR}/${OCN_FILE_YEAR} ] ||
       [ ! -f ${CESM_DIR}/${YEAR}/${ICE_FILE_YEAR} ]; then
       print_line "no cesm data: ${CASE} ${YEAR}"; return 1; else 
       print_line "have cesm data: ${CASE} ${YEAR}"; return 0; fi
}

is_wrf_pre_data() {
    if [ ! -f ${CESM_WRF_DIR}/${YEAR}/atmos_ta.nc ] ||
       [ ! -f ${CESM_WRF_DIR}/${YEAR}/atmos_ua.nc ] ||
       [ ! -f ${CESM_WRF_DIR}/${YEAR}/atmos_va.nc ] ||
       [ ! -f ${CESM_WRF_DIR}/${YEAR}/atmos_hus.nc ] ||
       [ ! -f ${CESM_WRF_DIR}/${YEAR}/atmos_ps.nc ] ||
       [ ! -f ${CESM_WRF_DIR}/${YEAR}/atmos_ts_1.nc ] ||
       [ ! -f ${CESM_WRF_DIR}/${YEAR}/atmos_snw_1.nc ] ||
       [ ! -f ${CESM_WRF_DIR}/${YEAR}/atmos_mrlsl_1.nc ] ||
       [ ! -f ${CESM_WRF_DIR}/${YEAR}/atmos_mrlsl_1.nc ] ||
       [ ! -f ${CESM_WRF_DIR}/${YEAR}/atmos_tos_1.nc ] ||
       [ ! -f ${CESM_WRF_DIR}/${YEAR}/atmos_sic_1.nc ]; then
       print_line "no wrf pre data: ${CASE} ${YEAR}"; return 1; else 
       print_line "have wrf pre data: ${CASE} ${YEAR}"; return 0; fi
}         

is_wrf_int_data() {
    
    if [ ! -d ${WRF_INT_DIR}/${YEAR} ]; then
       print_line "no wrf int data: ${CASE} ${YEAR}"; return 1
    elif [ `ls -1q ${WRF_INT_DIR}/${YEAR}/* 2>/dev/null | wc -l` -lt 1460 ]; then
       print_line "no wrf int data: ${CASE} ${YEAR}"; return 1
    else   
       print_line "have wrf int data: ${CASE} ${YEAR}"; return 0; fi
}

is_cesm_tstorms_data() {
    if [ ! -f ${CESM_TSTORMS_DIR}/tstorms_input_${CASE}_${YEAR}.nc ]; then
       print_line "no cesm tstorms data: ${CASE} ${YEAR}"; return 1; else 
       print_line "have cesm tstorms data: ${CASE} ${YEAR}"; return 0; fi
}       
  
remove_big_files() {
    if dir_exists ${CESM_DIR}/${YEAR}; then
        print_line "removing cesm files: ${CASE} ${YEAR}"
        rm -r ${CESM_DIR}/${YEAR}; fi
    check_exit "error removing cesm files: ${CASE} ${YEAR}"
    if dir_exists ${CESM_WRF_DIR}/${YEAR}; then
        print_line "removing pre wrf files: ${CASE} ${YEAR}"
        rm -r ${CESM_WRF_DIR}/${YEAR}; fi
    check_exit "error removing pre wrf files: ${CASE} ${YEAR}"
 
}

get_cesm_data() {
    
    print_line "getting cesm data: ${CASE} ${YEAR}"
    make_dir ${CESM_DIR}/${YEAR}   
    cd ${CESM_DIR}/${YEAR}

    if [ ! -f ${CESM_DIR}/${YEAR}/${ATM_FILE_YEAR} ]; then
        print_line "fetching cam file: ${CASE} ${YEAR}"
        hpss_run "hsi cget ${ATM_DIR}/${ATM_FILE_YEAR}"
	check_exit "error getting cam file: ${CASE} ${YEAR}"
	print_line "done getting cam file: ${CASE} ${YEAR}"; fi

    if [ ! -f ${CESM_DIR}/${YEAR}/${LND_FILE_YEAR} ]; then
        print_line "fetching clm file: ${CASE} ${YEAR}"
        hpss_run "htar -xv -m -f ${LND_DIR}/${LND_FILE_TAR} ${LND_FILE_YEAR}" 
	check_exit "error getting clm file: ${CASE} ${YEAR}"
	print_line "done getting clm file: ${CASE} ${YEAR}"; fi
    
    if [[ `ls -1q ${CESM_DIR}/${YEAR}/${OCN_FILE} | wc -l` -lt 12 ]] &&
       [[ ! -f ${CESM_DIR}/${YEAR}/${OCN_FILE_YEAR} ]]; then
        print_line "fetching pop file: ${CASE} ${YEAR}"
	hpss_run "htar -xv -m -f ${OCN_DIR}/${OCN_FILE_TAR} ${OCN_FILE}"
	check_exit "error getting pop file: ${CASE} ${YEAR}"
	print_line "done getting pop file: ${CASE} ${YEAR}"; fi
    
    if [[ `ls -1q ${CESM_DIR}/${YEAR}/${ICE_FILE} | wc -l` -lt 12 ]] &&
       [[ ! -f ${CESM_DIR}/${YEAR}/${ICE_FILE_YEAR} ]]; then
        print_line "fetching cice file: ${CASE} ${YEAR}"
        hpss_run "htar -xv -m -f ${ICE_DIR}/${ICE_FILE_TAR} ${ICE_FILE}"
	check_exit "error getting cice file: ${CASE} ${YEAR}"
	print_line "done getting cice file: ${CASE} ${YEAR}"; fi

    if ! file_exists ${OCN_FILE_YEAR}; then
        cdo mergetime ${OCN_FILE} ${OCN_FILE_YEAR}; fi
    if ! file_exists ${ICE_FILE_YEAR}; then
        cdo mergetime ${ICE_FILE} ${ICE_FILE_YEAR}; fi
    
    shopt -s extglob; `rm -f ${CESM_DIR}/${YEAR}/!(*00000.nc)`

    if file_exists ${ATM_FILE_YEAR} &&
       file_exists ${LND_FILE_YEAR} &&
       file_exists ${OCN_FILE_YEAR} &&
       file_exists ${ICE_FILE_YEAR}; then
       print_line "done getting cesm data: ${CASE} ${YEAR}"
    else
       print_line "error getting cesm data: ${CASE} ${YEAR}"
       exit 1
    fi   

}

extract_wrf_int_files_batch() {
    
    print_line "submitting convert wrf intermediate files: ${CASE} ${YEAR}"
    bash ${SCRIPT_DIR}/run_as_batch.sh "${SCRIPT_DIR}/convert_boundary_data_wrf.sh" "pre_${CASE}_${YEAR}" "walltime=02:00:00" "CASE=${CASE},YEAR=${YEAR},EXT_FLAG=0"     
    check_exit "error submitting convert wrf intermediate files: ${CASE} ${YEAR}"

}

extract_erai_int_files_batch() {
    
    print_line "extracting wrf intermediate files: ${CASE} ${YEAR}"
    for((MONTH=$((10#${S_MON})); MONTH<=$((10#${E_MON})); MONTH++)); do
        bash ${SCRIPT_DIR}/run_as_batch.sh "${SCRIPT_DIR}/convert_boundary_data_wrf.sh" "pre_${CASE}_${YEAR}_${MONTH}" "walltime=02:00:00" "CASE=$CASE,YEAR=$YEAR,EXT_FLAG=0,MONTH=$MONTH"
    done       
    check_exit "error extracting wrf intermediate files: ${CASE} ${YEAR}"

}

extract_convert_wrf_files_batch() {
    
    print_line "submitting convert and extract wrf files: ${CASE} ${YEAR}"
    bash ${SCRIPT_DIR}/run_as_batch.sh "${SCRIPT_DIR}/convert_boundary_data_wrf.sh" "pre_${CASE}_${YEAR}" "walltime=02:00:00" "CASE=${CASE},YEAR=${YEAR},EXT_FLAG=1"     
    check_exit "error submitting convert and extract wrf files: ${CASE} ${YEAR}"

}

extract_cesm_tstorms_data() {

    print_line "extracting tstorms input from cesm data: ${CASE} ${YEAR}"
    ncl "fin=\"${CESM_DIR}/${YEAR}/${ATM_FILE_YEAR}\"" "case=\"${CASE}\"" "year=\"${YEAR}\"" ${NCL_CONV_DIR}/convert_cesm_to_tstorms.ncl > /dev/null
    check_exit "error extracting tstorms input: ${CASE} ${YEAR}"
    print_line "done extracting tstorms input from cesm data: ${CASE} ${YEAR}"

}

if qstat_exists "pre_${CASE}_${YEAR}"; then
print_line "pre wrf already running: ${CASE} ${YEAR}"
exit 0; fi

if [ "${CASE}" = "erai" ]; then
    if is_wrf_int_data; then :
    else extract_erai_int_files_batch; fi
else
    if is_wrf_int_data; then :
    elif is_wrf_pre_data; then extract_wrf_int_files_batch;
    elif is_cesm_data; then extract_convert_wrf_files_batch;
    else get_cesm_data; extract_convert_wrf_files_batch; fi

    #if is_cesm_tstorms_data; then exit 0
    #else extract_cesm_tstorms_data &
    #exit 0; fi
fi    
