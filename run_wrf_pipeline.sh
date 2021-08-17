#!/bin/bash

if [ $# -lt 5 ]; then
    echo "usage $0: case start_year end_year stride nstart (start_mon end_mon start_day end_day)-optional"
    exit 1
fi

CASE=$1
START_YEAR=$2
END_YEAR=$3
STRIDE=$4
NDIV=$(((END_YEAR-START_YEAR)/STRIDE))
NSTART=$5
S_MON=$6
E_MON=$7
S_DAY=$8
E_DAY=$9

DAY_ARR=(31 28 31 30 31 30 31 31 30 31 30 31)

WRFOUT_PREF=wrfout_*.nc

source ~/RUNWORKFLOW/pipeline_env_info.sh ${CASE}

is_full_year() {
    if [[ ! -z ${S_MON} ]] && [[ ! -z ${E_MON} ]] &&
       [[ ! -z ${S_DAY} ]] && [[ ! -z ${E_DAY} ]]; then
       return 1
    else return 0
    fi
}

if is_full_year; then S_MON="01"; E_MON="12"; S_DAY="01"; E_DAY="31"; fi

if [[ $((10#${S_MON})) -lt 10 ]]; then S_MON=$(printf %02d $((10#${S_MON}))); fi
if [[ $((10#${E_MON})) -lt 10 ]]; then E_MON=$(printf %02d $((10#${E_MON}))); fi
if [[ $((10#${S_DAY})) -lt 10 ]]; then S_DAY=$(printf %02d $((10#${S_DAY}))); fi
if [[ $((10#${E_DAY})) -lt 10 ]]; then E_DAY=$(printf %02d $((10#${E_DAY}))); fi

if [[ $((10#${E_MON}-10#${S_MON})) -lt 0 ]]; then 
echo "incorrect month inputs"; exit 1; fi

T_STEPS=0
for MONTH in $(seq $((10#${S_MON})) $((10#${E_MON}))); do
    if [[ $MONTH -eq $((10#${S_MON})) ]]; then DAYS=$((DAY_ARR[MONTH-1]-S_DAY+1))
    elif [[ $MONTH -eq $((10#${E_MON})) ]]; then DAYS=$((E_DAY))
    else DAYS=$((DAY_ARR[MONTH-1])); fi
    TMP=$((4*DAYS))
    T_STEPS=$((T_STEPS+TMP))
done

SHIFT=0
for MONTH in $(seq 1 $((10#${S_MON}))); do
    if [[ $MONTH -eq $((10#${S_MON})) ]]; then DAYS=$((S_DAY-1))
    else DAYS=$((DAY_ARR[MONTH-1])); fi
    TMP=$((4*DAYS))
    SHIFT=$((SHIFT+TMP))
done

is_wrf_complete() {
    WRF_IN_FILE=`ls -1q ${2}/${WRFOUT_PREF} 2>/dev/null | head -n 1`

    if [[ ! ${WRF_IN_FILE} ]]; then
        print_line "no wrfout file in ${2}: ${CASE} ${1}"; return 1
    else
        print_line "have wrfout file in ${2}: ${CASE} ${1}"
	NTIMES=`ncdump -h ${WRF_IN_FILE} | grep "Time = UNLIMITED"`
	NTIMES=${NTIMES//[^0-9]/}
        #if [[ ${NTIMES} -lt 1456 ]]; then
        if [[ ${NTIMES} -lt $((T_STEPS-1)) ]]; then
	    print_line "wrfout file not complete: ${CASE} ${1}"; 
	    print_line "${NTIMES} time steps only"; return 1
	else 
	    print_line "wrfout file complete: ${CASE} ${1}"; 
	    print_line "${NTIMES} time steps"; return 0; fi
    fi
}    

run_pre_wrf() {
    print_line "running pre wrf: ${CASE} ${1} ${S_MON} ${E_MON} ${S_DAY} ${E_DAY}"
    bash ${SCRIPT_DIR}/run_wrf_pre_pipeline.sh ${CASE} ${1} ${S_MON} ${E_MON} ${S_DAY} ${E_DAY}
    check_exit "error running pre wrf: ${CASE} ${1} ${S_MON} ${E_MON} ${S_DAY} ${E_DAY}"
}   

run_wrf() {
    print_line "running wrf: ${CASE} ${1} ${S_MON} ${E_MON} ${S_DAY} ${E_DAY}"
    python ${SCRIPT_DIR}/run_wrf_batch.py ${CASE} ${1} ${2} ${S_MON} ${E_MON} ${S_DAY} ${E_DAY}
    check_exit "error running wrf: ${CASE} ${1} ${S_MON} ${E_MON} ${S_DAY} ${E_DAY}"
}  

is_wrf_int_data() {
    if ! dir_exists ${WRF_INT_DIR}/${1}; then
       print_line "no wrf int data: ${CASE} ${1}";
       return 1
    
    elif [ `ls -1q ${WRF_INT_DIR}/${1} | wc -l` -lt ${T_STEPS} ]; then
       print_line "no wrf int data: ${CASE} ${1}"; 
       return 1
    
    else   
       print_line "have wrf int data: ${CASE} ${1}"; return 0; fi
}

remove_big_files() {   
    if dir_exists ${CESM_DIR}/${1}; then
        print_line "removing cesm files: ${CASE} ${1}"
        rm -r ${CESM_DIR}/${1}; fi
    check_exit "error removing cesm files: ${CASE} ${1}"
    if dir_exists ${CESM_WRF_DIR}/${1}; then
        print_line "removing pre wrf files: ${CASE} ${1}"
        rm -r ${CESM_WRF_DIR}/${1}; fi
    check_exit "error removing pre wrf files: ${CASE} ${1}"
}

is_all_split_or_converted() {
    WRF_IN_DIR=${PROJ_WRF}/${1}
    for MONTH in $(seq -f "%02g" $((10#${S_MON})) $((10#${E_MON}))); do
        if ! file_exists ${WRF_IN_DIR}/wrfout_${CASE}_${1}_${MONTH}.nc &&
           ! file_exists ${WRF_IN_DIR}/wrfpost_${CASE}_${1}_${MONTH}.nc
	   then print_line "no monthly data in proj dir: ${CASE} ${1}"
	   return 1; fi
    done
    print_line "have monthly data in proj dir: ${CASE} ${1}"
    return 0
}       

is_all_converted() {
    WRF_IN_DIR=${PROJ_WRF}/${1}
    for MONTH in $(seq -f "%02g" $((10#${S_MON})) $((10#${E_MON}))); do
        for i in $(seq 1 4); do
	    if ! file_exists ${WRF_IN_DIR}/wrfpost_${CASE}_${1}_${MONTH}_${i}.nc
	    then return 1; fi
        done
    done
    print_line "monthly data converted: ${CASE} ${1}"
    return 0
}

remove_big_wrf() {
    WRF_IN_DIR=${PROJ_WRF}/${1}
    if is_all_converted ${1}; then
        if [ $(ls ${WRF_IN_DIR}/${WRFOUT_PREF} 2>/dev/null) ]; then
	    BIG_FILE=`ls ${WRF_IN_DIR}/${WRFOUT_PREF}`
            print_line "removing wrfout file: ${CASE} ${1}"; rm ${BIG_FILE}
	    print_line "removing restart and info files: ${CASE} ${1}"
	    rm -f ${WRF_OUT_DIR}/${1}/output/*
	    rm -f ${WRF_OUT_DIR}/${1}/info/*
	    check_exit "error removing extra wrf files: ${CASE} ${1}"
	else print_line "already removed extra wrf files: ${CASE} ${1}"; fi
	if dir_exists ${WRF_INT_DIR}/${1}; then
	    print_line "removing wrf int files: ${CASE} ${1}"
	    rm -r ${WRF_INT_DIR}/${1}
	    check_exit "error removing wrf int files: ${CASE} ${1}"
	else print_line "already removed wrf int files: ${CASE} ${1}"; fi
    else print_line "error splitting and converting: ${CASE} ${1}"; exit 1; fi
}


run_get_wrf_month() {
    for MONTH in $(seq -f "%02g" $((10#${S_MON})) $((10#${E_MON}))); do
        print_line "converting ${CASE} ${1} ${MONTH}"
        bash ${SCRIPT_DIR}/run_as_batch.sh "${SCRIPT_DIR}/get_wrf_month.sh" "post_${CASE}_${1}_${MONTH}" "walltime=01:30:00" "CASE=${CASE},YEAR=${1},MONTH=${MONTH},SHIFT=${SHIFT}"
        check_exit "error submitting convert job $CASE $1 $MONTH"
    done
}

run_post_wrf() {
    WRF_IN_DIR=${PROJ_WRF}/${1}
    if is_wrf_complete ${1} ${WRF_IN_DIR} && 
       ! is_all_converted ${1}; then 
        print_line "running post wrf: ${CASE} ${1}"
        run_get_wrf_month ${1}
	check_exit "error running post wrf: ${CASE} ${1}"
    elif is_all_converted ${1}; then
        print_line "post wrf already done: ${CASE} ${1}"
    else print_line "error running wrf: ${CASE} ${1}"; exit 1; fi
}

move_wrfout() {
    WRF_IN_FILE=`ls ${WRF_OUT_DIR}/${1}/output/${WRFOUT_PREF} 2>/dev/null | head -n 1`
    WRF_PROJ_DIR=${PROJ_WRF}/${1}
    make_dir ${PROJ_WRF}/${1}
    if [[ $(ls ${WRF_PROJ_DIR}/${WRFOUT_PREF} 2>/dev/null | head -n 1) ]]; then
        print_line "wrfout file already moved: ${CASE} ${1}"	
    elif [ ${#WRF_IN_FILE} -ne 0 ]; then
	print_line "moving wrfout to proj dir: ${CASE} ${1}"
	#mv ${WRF_IN_FILE} ${PROJ_WRF}/${1}
	slurm_run "dav" "mv ${WRF_IN_FILE} ${PROJ_WRF}/${1}"
	check_exit "error moving wrfout file: ${CASE} ${1}"
        print_line "moved wrfout to proj dir: ${CASE} ${1}"
	NAMELIST_FILE=${WRF_OUT_DIR}/${1}/output/namelist.input 
	if file_exists ${NAMELIST_FILE}; then
	    mv ${NAMELIST_FILE} ${PROJ_WRF}/${1}; fi
    elif is_all_converted ${1}; then
        print_line "post wrf and move already done: ${CASE} ${1}"
    else print_line "error running wrf: ${CASE} ${1}"; exit 1; fi
}

make_tstorms_year() {
    WRFPOST_YEAR=${PROJ_WRF}/${1}/wrfpost_${CASE}_${1}.nc
    TSTORMS_YEAR=${PROJ_WRF}/${1}/wrf_tstorms_${CASE}_${1}.nc
    if is_all_converted ${1}; then
	if ! file_exists ${WRFPOST_YEAR}; then
	    print_line "combining monthly files: ${CASE} ${1}"
	    ncrcat -d time,0, ${PROJ_WRF}/${1}/*.nc ${WRFPOST_YEAR}; fi
	if ! file_exists ${TSTORMS_YEAR}; then
            print_line "creating tstorms file: ${CASE} ${1}"
	    ncks -v Z1000,Z200,U850,V850,UBOT,VBOT,T500,T200,PSL ${WRFPOST_YEAR} ${TSTORMS_YEAR}
	    if file_exists ${TSTORMS_YEAR}; then rm ${WRFPOST_YEAR}; fi
        else print_line "tstorms file already exists: ${CASE} ${1}"; fi
    else print_line "waiting for full conversion: ${CASE} ${1}"; fi	
}

is_complete_moved_split_or_converted() {
    if is_wrf_complete ${1} ${WRF_OUT_DIR}/${1}/output ||
       is_wrf_complete ${1} ${PROJ_WRF}/${1} ||
       is_all_split_or_converted ${1}; then
       return 0; else return 1; fi
}

clean_month() {
    WRF_IN_DIR=${PROJ_WRF}/${1}
    
    for i in $(seq 1 4); do
        WRF_POST_FILE=wrfpost_${CASE}_${1}_${2}_${i}.nc
        WRF_TEMP_FILE=wrfpost_${CASE}_${1}_${2}_${i}_tmp.nc
        FILE_IN=${WRF_IN_DIR}/${WRF_POST_FILE}
        if [ `ncdump -h ${FILE_IN} | grep "float Z1000(" | wc -l` -ne 0 ]; then
            ncks -O -x -v Z1000,Z200,U850,V850,T500,T200 ${FILE_IN} \
            -o ${WRF_IN_DIR}/${WRF_TEMP_FILE}
            check_exit "error cleaning wrf file: ${CASE} ${1} ${2}"
            mv ${WRF_IN_DIR}/${WRF_TEMP_FILE} ${WRF_IN_DIR}/${WRF_POST_FILE}
        else print_line "already cleaned wrf file: ${CASE} ${1} ${2}"; fi
    done

}

tstorms_file_exists() {
    WRF_IN_DIR=${PROJ_WRF}/${1}
    if file_exists ${WRF_IN_DIR}/wrf_tstorms_${CASE}_${1}.nc; then
    return 0; else print_line "tstorms file absent: ${CASE} ${1}"
    return 1; fi

}

clean_year() {
    rm -f ${PROJ_WRF}/${1}/*.tmp
    if tstorms_file_exists ${1}; then 
        print_line "cleaning files: ${CASE} ${1}"
        for MONTH in $(seq -f "%02g" $((10#${S_MON})) $((10#${E_MON}))); do
    	    clean_month ${1} ${MONTH}
    	    check_exit "error cleaning file: ${CASE} ${1} ${MONTH}"
        done
	print_line "cleaned files: ${CASE} ${1}"
    else exit 1; fi  

}

run_all_post_proc() {

    START_IN=$1; CHUNK_IN=$2
    for ((YEAR=${START_IN}; YEAR<=$((START_IN+CHUNK_IN-1)); YEAR++)); do
	move_wrfout $YEAR & sleep 1.0
    done

    while slurm_exists || pgrep_exists "srun"; do sleep 1.0; done
    
    for ((YEAR=${START_IN}; YEAR<=$((START_IN+CHUNK_IN-1)); YEAR++)); do
        run_post_wrf $YEAR
    done

    qstat_chunk_wait "post_${CASE}" ${START_IN} $((START_IN+CHUNK_IN-1))
     
    for ((YEAR=${START_IN}; YEAR<=$((START_IN+CHUNK_IN-1)); YEAR++)); do
        remove_big_wrf $YEAR
    done
    
    for ((YEAR=${START_IN}; YEAR<=$((START_IN+CHUNK_IN-1)); YEAR++)); do
        make_tstorms_year $YEAR & sleep 0.1
    done
    
    while pgrep_exists "ncks" || pgrep_exists "ncrcat"; do sleep 1.0; done

    for ((YEAR=${START_IN}; YEAR<=$((START_IN+CHUNK_IN-1)); YEAR++)); do
        clean_year $YEAR &
    done
    
}

run_all_pre_proc() {
    START_IN=$1; CHUNK_IN=$2
    for ((YEAR=${START_IN}; YEAR<=$((START_IN+CHUNK_IN-1)); YEAR++)); do
	print_line "checking for output before pre-processing: $CASE $YEAR"
	if ! is_complete_moved_split_or_converted ${YEAR} &&
	   ! is_wrf_int_data ${YEAR}; then
	    run_pre_wrf ${YEAR}; sleep 1.0
	fi
    done

    #while slurm_exists; do sleep 1.0; done
    # while pgrep_exists "cdo" || pgrep_exists "mergetime"; do sleep 1.0; done
}

run_all_wrf() {
    START_IN=$1; CHUNK_IN=$2
    for ((j=0; j<=$((CHUNK_IN-1)); j++)); do
        YEAR=$((START_IN+j))

	print_line "checking for output before running wrf: $CASE $YEAR"
	if ! is_complete_moved_split_or_converted ${YEAR} &&
	   ! qstat_exists "${CASE}_${YEAR}_wrf"; then
	    if is_wrf_int_data ${YEAR}; then
	        remove_big_files ${YEAR}
		run_wrf ${YEAR} $((NSTART+j))
            else
	        print_line "error getting wrf int data: ${CASE} ${YEAR}"
	        print_line "exiting wrf: ${CASE} ${YEAR}"
	        exit 1 
            fi
	elif qstat_exists "${CASE}_${YEAR}_wrf"; then
	    print_line "wrf currently running: ${CASE} ${YEAR}"
	fi
    done
}

print_line "running on host: ${HOSTNAME}"

for i in $(seq 0 $NDIV); do
    
    for j in $(seq 0 2); do
        START[j]=$((START_YEAR+(i+j-1)*STRIDE))
	END[j]=$((START[j]+STRIDE-1))
        if [ ${END[j]} -gt ${END_YEAR} ]; then END[j]=${END_YEAR}; fi
        CHUNK[j]=$((END[j]-START[j]+1))
    done

    if [[ ($i -eq 0) && ($i -ne $NDIV) ]]; then
         run_all_pre_proc ${START[1]} ${CHUNK[1]}
         qstat_chunk_wait "pre_${CASE}" ${START[1]} ${END[1]}
         run_all_wrf ${START[1]} ${CHUNK[1]}
         run_all_pre_proc ${START[2]} ${CHUNK[2]}

    elif [[ ($i -eq 0) && ($i -eq $NDIV) ]]; then
         run_all_pre_proc ${START[1]} ${CHUNK[1]}
         qstat_chunk_wait "pre_${CASE}" ${START[1]} ${END[1]}
         run_all_wrf ${START[1]} ${CHUNK[1]}
    
    elif [ $i -eq $NDIV ]; then
         run_all_wrf ${START[1]} ${CHUNK[1]}

    else 
         run_all_wrf ${START[1]} ${CHUNK[1]}
         run_all_pre_proc ${START[2]} ${CHUNK[2]}
    fi

    qstat_chunk_wait "${CASE}" ${START[1]} ${END[1]} "wrf"
    qstat_chunk_wait "post_${CASE}" ${START[0]} ${END[0]}
    run_all_post_proc ${START[1]} ${CHUNK[1]} &
    sleep 10.0

done   

while qstat_exists "post" || slurm_exists || pgrep_exists "mv" || 
      pgrep_exists "ncks" || pgrep_exists "ncrcat" || pgrep_exists "rm";
      do sleep 10.0; done

print_line "finished running wrf pipeline: $CASE $START_YEAR $END_YEAR"
