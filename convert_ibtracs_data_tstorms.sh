#!/bin/bash

if [ $# -ne 2 ]; then echo usage: $0 start_year end_year; exit 1; fi

source ~/RUNWORKFLOW/pipeline_env_info.sh ibtracs

if [ ! -d ${IBTRACS_DIR} ]; then mkdir -p ${IBTRACS_DIR}; fi

for ((YEAR=$1; YEAR<=$2; YEAR++)); do
    IBTRACS_FILE=${IBTRACS_DIR}/Year.${YEAR}.ibtracs_wmo.v03r10.nc
    if [ ! -f ${IBTRACS_FILE} ]; then
        cd ${IBTRACS_DIR}
        wget ftp://eclipse.ncdc.noaa.gov/pub/ibtracs/v03r10/wmo/netcdf/year/Year.${YEAR}.ibtracs_wmo.v03r10.nc ${IBTRACS_FILE}
    fi
done   

for ((YEAR=$1; YEAR<=$2; YEAR++)); do
    OUT_DIR=${ROOT_DIR}/TSTORMS_OUTPUT/ibtracs/WRF/run_1/${YEAR}
    ncl year=${YEAR} "out_dir=\"${OUT_DIR}\"" ${NCL_CONV_DIR}/convert_ibtracs_to_tstorms_fmt.ncl
done    
