#! /bin/bash

if [ $# -eq 4 ]; then CASE=$1; YEAR=$2; MONTH=$3; SHIFT=$4
elif [[ -z ${CASE} ]] || [[ -z ${YEAR} ]] || 
     [[ -z ${MONTH} ]]; [[ -z ${SHIFT} ]]; then
    echo usage $0: case year month shift; exit 1; fi

DAYS=(31 28 31 30 31 30 31 31 30 31 30 31)
CDAYS=(0 31 59 90 120 151 181 212 243 273 304 334 365)

source ~/RUNWORKFLOW/pipeline_env_info.sh ${CASE}

#WRF_IN_DIR=${WRF_OUT_DIR}/${YEAR}/output
WRF_IN_DIR=${PROJ_WRF}/${YEAR}
WRF_IN_FILE=`ls ${WRF_IN_DIR}/wrfout_*.nc 2>/dev/null`
WRF_OUT_PREF=wrfout_${CASE}_${YEAR}_${MONTH}
WRF_POST_PREF=wrfpost_${CASE}_${YEAR}_${MONTH}
START_TIME=$((4*${CDAYS[$((${MONTH#0}-1))]}-SHIFT))
END_TIME=$((4*${CDAYS[$((${MONTH#0}))]}-1-SHIFT))

S_TIMES=(${START_TIME} $((START_TIME+4*7)) $((START_TIME+4*14)) $((START_TIME+4*21)))
E_TIMES=($((START_TIME+4*7-1)) $((START_TIME+4*14-1)) $((START_TIME+4*21-1)) ${END_TIME})

split_month() {
    
    IN_FILE=`ls -1q ${WRF_IN_DIR}/wrfout_*.nc 2>/dev/null`
    IN_DIR=${WRF_IN_DIR}

    if [ ${#IN_FILE} -gt 0 ]; then
        for i in $(seq 1 4); do
            OUT_FILE=${WRF_OUT_PREF}_${i}.nc
            if ! file_exists ${IN_DIR}/${OUT_FILE} &&
               ! file_exists ${IN_DIR}/${WRF_POST_PREF}_${i}.nc; then
                print_line "processing ${IN_FILE}"
                print_line "creating ${OUT_FILE}"
                ncks -d Time,${S_TIMES[i-1]},${E_TIMES[i-1]} \
                    ${IN_FILE} ${IN_DIR}/${OUT_FILE} 
                check_exit "error creating ${OUT_FILE}"
            else print_line "${OUT_FILE} or ${WRF_POST_PREF}_${i}.nc already exists"; fi
        done
    else print_line "no wrfout file ${CASE} ${YEAR}"; fi

}    

convert_month() {
    
    IN_DIR=${WRF_IN_DIR}

    for i in $(seq 1 4); do
        IN_FILE=${WRF_OUT_PREF}_${i}.nc
        OUT_FILE=${WRF_POST_PREF}_${i}.nc
    if file_exists ${IN_DIR}/${IN_FILE}; then
        if ! file_exists ${IN_DIR}/${OUT_FILE}; then
            print_line "processing ${IN_FILE}"
            print_line "creating ${OUT_FILE}"
            ncl "dir_in=\"${IN_DIR}\"" "dir_out=\"${IN_DIR}\"" "file_in=\"${IN_FILE}\"" "file_out=\"${OUT_FILE}\"" ${NCL_CONV_DIR}/wrfout_to_cf.ncl
            check_exit "error creating ${OUT_FILE}"
	    print_line "finished ${OUT_FILE}"; rm ${IN_DIR}/${IN_FILE}
        else print_line "${OUT_FILE} already exists"
	rm ${IN_DIR}/${IN_FILE}; 
	fi
    else print_line "no monthly wrfout file ${CASE} ${YEAR} ${MONTH} ${i}"; fi
    done
}

split_month
convert_month
