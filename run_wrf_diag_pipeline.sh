#!/bin/bash

if [ $# -ne 7 ]; then 
echo usage $0: case start_yr end_yr nrun tstorms_flag append_flag compile_flag
exit 1; fi

CASE=$1
START_YR=$2
END_YR=$3
NRUN=$4
TFLAG=$5
AFLAG=$6
CFLAG=$7

source ~/RUNWORKFLOW/pipeline_env_info.sh $CASE

YR_AVG=3
IBTRACS_FILE=~/TSTORMS_OUTPUT/ibtracs/WRF/run_1/traj_out_ibtracs_all_1
TRAJ_FILE=${TSTORMS_OUT_DIR}/WRF/run_${NRUN}/traj_out_${CASE}_${START_YR}_${END_YR}_${NRUN}
DIAGS_FIG=${FIG_DIR}/${CASE}_${START_YR}_${END_YR}_${NRUN}_diags.pdf
TRACKS_FIG=${FIG_DIR}/${CASE}_${START_YR}_${END_YR}_${NRUN}_tracks.pdf
WAVG_FIG=${FIG_DIR}/${CASE}_${START_YR}_${END_YR}_${NRUN}_wavg.pdf
DENSITY_FIG=${FIG_DIR}/${CASE}_${START_YR}_${END_YR}_${NRUN}_density.pdf
RAVG_FIG=${FIG_DIR}/${CASE}_${START_YR}_${END_YR}_${NRUN}_run_avgs.pdf
RAVG_PCENT_FIG=${FIG_DIR}/${CASE}_${START_YR}_${END_YR}_${NRUN}_run_avgs_pcent.pdf
PVALS_FIG=${FIG_DIR}/${CASE}_${START_YR}_${END_YR}_${NRUN}_pvals.pdf
DIAGS_CAP="$CASE diags-${NRUN} $START_YR-$END_YR" 
TRACKS_CAP="$CASE tracks-${NRUN} $START_YR-$END_YR"

combine_wrf_traj_out() {
    DIR=${TSTORMS_OUT_DIR}
    RAW_FILE=${DIR}/WRF/run_${NRUN}/traj_out_${CASE}_${START_YR}_${END_YR}_${NRUN}
    FILT_FILE=${DIR}/WRF/run_${NRUN}/traj_filt_out_${CASE}_${START_YR}_${END_YR}_${NRUN}

    if [ -f ${RAW_FILE} ]; then rm ${RAW_FILE}; fi    
    if [ -f ${FILT_FILE} ]; then rm ${FILT_FILE}; fi    

    print_line "combining traj files: ${CASE} ${START_YR} ${END_YR} ${NRUN}"
    for ((YEAR=${START_YR}; YEAR<=${END_YR}; YEAR++)); do
        TRAJ_RAW=${DIR}/WRF/run_${NRUN}/${YEAR}/traj_out_${CASE}_${YEAR} 
        TRAJ_FILT=${DIR}/WRF/run_${NRUN}/${YEAR}/traj_filt_out_${CASE}_${YEAR} 
        if [ -f ${TRAJ_RAW} ]; then cat ${TRAJ_RAW} >> ${RAW_FILE}; fi
        if [ -f ${TRAJ_FILT} ]; then cat ${TRAJ_FILT} >> ${FILT_FILE}; fi
    done
    check_exit "error combining traj files: $CASE $START_YR $END_YR $NRUN"
}

make_plots() {
    print_line "making plots: ${CASE} ${START_YR} ${END_YR}"
    python ${DIAG_DIR}/plot_number.py $TRAJ_FILE $START_YR $END_YR
    check_exit "error plotting diagnostics: $CASE $START_YR $END_YR $NRUN"
    python ${DIAG_DIR}/plot_tracks.py $TRAJ_FILE
    check_exit "error plotting tracks: $CASE $START_YR $END_YR $NRUN"
    python ${DIAG_DIR}/comp_run_avgs.py ${TRAJ_FILE} ${START_YR} ${END_YR}
    check_exit "error plotting/computing running avgs: $CASE $START_YR $END_YR $NRUN"
    python ${DIAG_DIR}/comp_stats.py ${CASE} ${NRUN} ${START_YR} ${END_YR} ${YR_AVG}
    check_exit "error plotting/computing pvals: $CASE $START_YR $END_YR $NRUN"
    
    #python ${DIAG_DIR}/plot_wavg.py $TRAJ_FILE
    #check_exit "error plotting wind avg: $CASE $START_YR $END_YR $NRUN"
    #python ${DIAG_DIR}/plot_density.py $TRAJ_FILE
    #check_exit "error plotting density: $CASE $START_YR $END_YR $NRUN"
}

trim_plots() {
    print_line "trimming plots: ${CASE} ${START_YR} ${END_YR}"
    trim_fig ${TRAJ_FILE}_diags.pdf ${TRAJ_FILE}_diags.pdf
    check_exit "error trimming diag plot: $CASE $START_YR $END_YR $NRUN"
    trim_fig ${TRAJ_FILE}_tracks.pdf ${TRAJ_FILE}_tracks.pdf
    check_exit "error trimming track plot: $CASE $START_YR $END_YR $NRUN"
    trim_fig ${TRAJ_FILE}_run_avgs.pdf ${TRAJ_FILE}_run_avgs.pdf
    check_exit "error trimming run avg plot: $CASE $START_YR $END_YR $NRUN"
    trim_fig ${TRAJ_FILE}_run_avgs_pcent.pdf ${TRAJ_FILE}_run_avgs_pcent.pdf
    check_exit "error trimming run avg pcent plot: $CASE $START_YR $END_YR $NRUN"
    trim_fig ${TRAJ_FILE}_pvals.pdf ${TRAJ_FILE}_pvals.pdf
    check_exit "error trimming pvals plot: $CASE $START_YR $END_YR $NRUN"

    #trim_fig ${TRAJ_FILE}_wavg.pdf ${TRAJ_FILE}_wavg.pdf
    #check_exit "error trimming wavg plot: $CASE $START_YR $END_YR $NRUN"
    #trim_fig ${TRAJ_FILE}_density.pdf ${TRAJ_FILE}_density.pdf
    #check_exit "error trimming density plot: $CASE $START_YR $END_YR $NRUN"
}

copy_plots() {
    print_line "copying plots to fig directory: ${CASE} ${START_YR} ${END_YR} ${NRUN}"
    cp ${TRAJ_FILE}_diags.pdf ${DIAGS_FIG}
    check_exit "error copying diags plot to fig dir: $CASE $START_YR $END_YR $NRUN"
    cp ${TRAJ_FILE}_tracks.pdf ${TRACKS_FIG}
    check_exit "error copying tracks plot to fig dir: $CASE $START_YR $END_YR $NRUN"
    cp ${TRAJ_FILE}_run_avgs.pdf ${RAVG_FIG}
    check_exit "error copying run_avgs plot to fig dir: $CASE $START_YR $END_YR $NRUN"
    cp ${TRAJ_FILE}_run_avgs_pcent.pdf ${RAVG_PCENT_FIG}
    check_exit "error copying run_avgs_pcent plot to fig dir: $CASE $START_YR $END_YR $NRUN"
    cp ${TRAJ_FILE}_pvals.pdf ${PVALS_FIG}
    check_exit "error copying pvals plot to fig dir: $CASE $START_YR $END_YR $NRUN"
    #cp ${TRAJ_FILE}_wavg.pdf ${WAVG_FIG}
    #check_exit "error copying wavg plot to fig dir: $CASE $START_YR $END_YR $NRUN"
    #cp ${TRAJ_FILE}_density.pdf ${DENSITY_FIG}
    #check_exit "error copying density plot to fig directory: $CASE $START_YR $END_YR $NRUN"
}

append_plots() {
    DIAG_FILE=${WRITEUP_DIR}/diagnostics.tex
    APPEND_FILE=${WRITEUP_DIR}/fig_append_template.tex
    OUT_FILE=${WRITEUP_DIR}/diags_temp.tex
    
    FIG_1=${DIAGS_FIG}; CAP_1="${DIAGS_CAP}"
    FIG_2=${TRACKS_FIG}; CAP_2="${TRACKS_CAP}"
    
    print_line "appending figures: ${CASE} ${START_YR} ${END_YR} ${NRUN}"
    head -n -2 ${DIAG_FILE} > ${OUT_FILE}
    cat ${APPEND_FILE} >> ${OUT_FILE}
    check_exit "error appending figures: $CASE $START_YR $END_YR $NRUN"
    
    sed -i -e "s#fig_1#${FIG_1}#g" ${OUT_FILE}
    sed -i -e "s#cap_1#${CAP_1}#g" ${OUT_FILE}
    sed -i -e "s#fig_2#${FIG_2}#g" ${OUT_FILE}
    sed -i -e "s#cap_2#${CAP_2}#g" ${OUT_FILE}
    
    mv ${OUT_FILE} ${DIAG_FILE}
    check_exit "error overwriting ${DIAG_FILE}"
}

append_latex() {
    DIAG_FILE=${WRITEUP_DIR}/diagnostics.tex
    APPEND_FILE=${WRITEUP_DIR}/temp_${NRUN}.tex
    OUT_FILE=${WRITEUP_DIR}/diags_temp.tex

    print_line "appending latex file: ${TRAJ_FILE} ${START_YR} ${END_YR}"
    head -n -2 ${DIAG_FILE} > ${OUT_FILE}
    python ${DIAG_DIR}/append_latex.py ${TRAJ_FILE} ${IBTRACS_FILE} ${START_YR} ${END_YR} > ${APPEND_FILE}

    sed -i -e "s#fig_1#${FIG_1}#g" ${APPEND_FILE}
    sed -i -e "s#cap_1#${CAP_1}#g" ${APPEND_FILE}
    sed -i -e "s#fig_2#${FIG_2}#g" ${APPEND_FILE}
    sed -i -e "s#cap_2#${CAP_2}#g" ${APPEND_FILE}

    cat ${APPEND_FILE} >> ${OUT_FILE}
    check_exit "error appending latex: $CASE $START_YR $END_YR $NRUN"

    mv ${OUT_FILE} ${DIAG_FILE}; rm ${APPEND_FILE}
    check_exit "error overwriting ${DIAG_FILE}"

}

run_tstorms() {
    for ((YEAR=$START_YR; YEAR<=$END_YR; YEAR++)); do
        if [ -d ${PROJ_WRF}/${YEAR} ]; then
	    print_line "running tstorms: ${CASE} ${YEAR}"
            bash ${SCRIPT_DIR}/run_as_batch.sh "${SCRIPT_DIR}/run_tstorms.sh" "tstorms_${CASE}_${YEAR}" "walltime=02:00:00" "CASE=$CASE,YEAR=$YEAR,NRUN=$NRUN,CESM_FLAG=0"
            check_exit "error submitting tstorms run: ${CASE} ${YEAR}"
        fi
    done
}

if [ "$TFLAG" = "1" ]; then run_tstorms; fi #qstat_wait "tstorms"; fi

#combine_wrf_traj_out
#make_plots
#trim_plots
#copy_plots
#append_plots

if [ "$AFLAG" = "1" ]; then append_latex; fi

if [ "$CFLAG" = "1" ]; then cd ${WRITEUP_DIR}; bash compile_tex.sh diagnostics; fi    
