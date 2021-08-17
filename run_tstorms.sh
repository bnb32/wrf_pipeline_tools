#!/bin/bash

if [ $# -eq 4 ]; then CASE=$1; YEAR=$2; NRUN=$3; CESM_FLAG=$4
elif [[ -z ${CASE} ]] || [[ -z ${YEAR} ]] || 
     [[ -z ${NRUN} ]] || [[ -z ${CESM_FLAG} ]]; then
    echo usage $0: case year nrun cesm_flag; exit 1; fi

source ~/RUNWORKFLOW/pipeline_env_info.sh ${CASE}

if [ "${CESM_FLAG}" = "0" ]; then

    print_line "running tstorms on wrf data: ${CASE} ${YEAR}"
    ${SCRIPT_DIR}/run_tstorms_general ${PROJ_WRF}/${YEAR}/wrf_tstorms_${CASE}_${YEAR}.nc ${TSTORMS_OUT_DIR}/WRF/run_${NRUN}/${YEAR} ${CASE} ${YEAR}

elif [ "${CESM_FLAG}" = "1" ]; then

    print_line "running tstorms on cesm data: ${CASE} ${YEAR}"
    ${SCRIPT_DIR}/run_tstorms_general ${CESM_TSTORMS_DIR}/tstorms_input_${CASE}_${YEAR}.nc ${TSTORMS_OUT_DIR}/CESM/run_${NRUN}/${YEAR} ${CASE} ${YEAR}

fi

print_line "finished tstorms ${CASE} ${YEAR} ${NRUN}"
