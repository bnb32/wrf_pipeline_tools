#! /bin/bash

if [ $# -ne 4 ]; then echo usage $0: case start_yr end_yr nrun; exit 1; fi

CASE=$1; ST_YR=$2; END_YR=$3; NRUN=$4

source ~/RUNWORKFLOW/pipeline_env_info.sh ${CASE}

run_trajectory() {
    YEAR=$1
    ${SCRIPT_DIR}/run_trajectory_general ~/TSTORMS_OUTPUT/${CASE}/WRF/run_${NRUN}/${YEAR}/cyclones_out_${CASE}_${YEAR} ~/TSTORMS_OUTPUT/${CASE}/WRF/run_${NRUN}/${YEAR} ${CASE} ${YEAR}
}


for ((year=${ST_YR}; year<=${END_YR}; year++)); do
    run_trajectory ${year} 
done
