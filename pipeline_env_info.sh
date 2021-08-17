#!/bin/bash

if [ $# -eq 1 ]; then CASE=$1
elif [ $# -eq 2 ]; then CASE=$1; YEAR=$2
else echo "usage $0: case year (for cesm files)"; return 1; fi


export BLAT="0N"
export TLAT="60N"
export LLON="125W"
export RLON="5E"
export CPU_MAX=15
export PROJID=UCOR0023

export SCRATCH_DIR=/glade/scratch/bbenton
export ROOT_DIR=${SCRATCH_DIR}/20XXWRF
export SCRIPT_DIR=${ROOT_DIR}/RUNWORKFLOW
export DIAG_DIR=${SCRIPT_DIR}/diagnostics
export WRITEUP_DIR=${SCRIPT_DIR}/writeup
export FIG_DIR=${WRITEUP_DIR}/figures
export NCL_CONV_DIR=${SCRIPT_DIR}/ncl_convert
export CESM_DIR=${ROOT_DIR}/CESM_DATA/${CASE}
export IBTRACS_DIR=${ROOT_DIR}/IBTRACS_DATA
export CESM_WRF_DIR=${CESM_DIR}/WRF
export WRF_INT_DIR=${ROOT_DIR}/WRF_INT_OUTPUT/${CASE}
export TSTORMS_RUN_DIR=~/tstorms/scripts
export CESM_TSTORMS_DIR=${CESM_DIR}/TSTORMS
export TSTORMS_OUT_DIR=${ROOT_DIR}/TSTORMS_OUTPUT/${CASE}
export WRF_OUT_DIR=${ROOT_DIR}/WRF_OUTPUT/${CASE}
export PROJ_DIR=/glade/p/univ/ucor0023/bbenton
export PROJ_WRF=${PROJ_DIR}/WRF_OUTPUT/${CASE}
export WRF_CONV_FILE=convert_cesm_hybrid_nc_to_pressure_int.ncl
export ERAI_CONV_FILE=convert_era_grib_to_cesm_pressure_int.ncl
export TOPO_FILE=USGS-gtopo30_1.9x2.5_remap_c050602.nc
#export TOPO_FILE=consistent-topo-fv1.9x2.5_c130424.nc
export LFRAC_FILE=fracdata_1.9x2.5_gx1v6_c090206.nc
export MAP_FILE=map_gx1v6_to_fv1.9x2.5_bilin_da_090206.nc

if [ ! -z ${YEAR} ]; then

    if [ ${#YEAR} -eq 1 ]; then PYEAR=000${YEAR}; fi
    if [ ${#YEAR} -eq 2 ]; then PYEAR=00${YEAR}; fi
    if [ ${#YEAR} -eq 3 ]; then PYEAR=0${YEAR}; fi
    if [ ${#YEAR} -eq 4 ]; then PYEAR=${YEAR}; fi

    START_YEAR=${PYEAR:0:3}0; END_YEAR=${PYEAR:0:3}9
    
    if [ $END_YEAR -gt 2005 ]; then END_YEAR=2005; fi    
    
    if [ "$CASE" = "ctrl" ]; then
    export PREFIX="b.e11.BLMTRC5CN.f19_g16.850forcing.003"
    elif [ "$CASE" = "forced" ]; then
    export PREFIX="b.e11.BLMTRC5CN.f19_g16.007"
    fi
    
    export DATA_DIR="/CCSM/csm/${PREFIX}"
    export ATM_DIR="${DATA_DIR}/atm/hist"
    export LND_DIR="${DATA_DIR}/lnd/hist"
    export OCN_DIR="${DATA_DIR}/ocn/hist"
    export ICE_DIR="${DATA_DIR}/ice/hist"
    export ATM_FILE_YEAR="${PREFIX}.cam.h2.${PYEAR}-01-01-00000.nc"
    export LND_FILE_TAR="${PREFIX}.clm2.h1.${START_YEAR}-${END_YEAR}.tar"
    export LND_FILE_YEAR="${PREFIX}.clm2.h1.${PYEAR}-01-01-00000.nc"
    export OCN_FILE_TAR="${PREFIX}.pop.h.nday1.${START_YEAR}-${END_YEAR}.tar"
    export OCN_FILE_START="${PREFIX}.pop.h.nday1.${PYEAR}"
    export OCN_FILE="${OCN_FILE_START}*.nc"
    export ICE_FILE_TAR="${PREFIX}.cice.h1.${START_YEAR}-${END_YEAR}.tar"
    export ICE_FILE_START="${PREFIX}.cice.h1.${PYEAR}"
    export ICE_FILE="${ICE_FILE_START}*.nc"
    export CESM_DIR="/glade/scratch/bbenton/20XXWRF/CESM_DATA/${CASE}"
    export ICE_FILE_YEAR="${ICE_FILE_START}-01-01-00000.nc"
    export OCN_FILE_YEAR="${OCN_FILE_START}-01-01-00000.nc"

fi


## misc functions
print_line() { echo -e "\n$1\n"; }   

check_exit() { if [ "$?" -ne "0" ]; then print_line "$1"; exit 1; fi }

dir_exists() { if [[ -d $1 ]]; then return 0; else return 1; fi }

file_exists() { if [[ -f $1 ]]; then return 0; else return 1; fi }

make_dir() { if ! dir_exists $1; then mkdir -p $1; fi }

qstat_exists() { 
    if [[ $(qstat -f | awk "/Job_Name/ && /$1/" | wc -l) -gt 0 ]]; then
    return 0; else return 1; fi }

qstat_wait() { while qstat_exists "$1"; do sleep 60.0; done }

pgrep_exists() { 
    if [[ $(pgrep -u ${USER} $1 | wc -l) -gt 0 ]]; then return 0
    else return 1; fi }

year_iter() {
    for ((i=$1; i<=$2; i++)); do
        START=$3; FUNC=$4; BG=$5
	YEAR=$((START + i - 1))
	if [ "$BG" = "0" ]; then $FUNC $YEAR
	elif [ "$BG" = "1" ]; then $FUNC $YEAR &
	fi
	$6; $7; $8; $9
    done	
}

is_cesm_case() {
    if [[ ("$1" = "ctrl" ) || ("$1" = "forced" ) ]]; then return 0
    else return 1; fi
}

is_erai_case() {
    if [[ "$1" = "erai" ]]; then return 0; else return 1; fi
}

var_empty() {
    if [[ -z $1 ]]; then return 0; else return 1; fi
}

trim_fig() {
    convert $1 -flatten -fuzz 1% -trim +repage $2
}

qstat_chunk() {
WORD1=$1; ST_YR=$2; END_YR=$3; WORD2=$4
RET=1
if var_empty $WORD2; then
    for YEAR in $(seq $2 $3); do
        if qstat_exists "${WORD1}_${YEAR}"; then RET=0; fi
    done
else
    for YEAR in $(seq $2 $3); do
        if qstat_exists "${WORD1}_${YEAR}_${WORD2}"; then RET=0; fi
    done
fi
return ${RET}
}

qstat_chunk_wait() {
WORD1=$1; ST_YR=$2; END_YR=$3; WORD2=$4
while qstat_chunk $WORD1 $ST_YR $END_YR $WORD2; do sleep 60.0; done
}

cpu_usage() {
mpstat 10 1 | awk '$12 ~ /[0-9.]+/ { print 100-$12 }' | tail -n -1
}

usage_wait() {
CPU_USE=`cpu_usage`
while [[ ${CPU_USE%.*} -ge ${CPU_MAX} ]]; do sleep 10.0
print_line "high cpu usage $CPU_USE: waiting"; 
CPU_USE=`cpu_usage`; done
}

slurm_run() {
print_line "slurm submission on $1: $2"
salloc -n1 -p $1 --account=${PROJID} -t 01:00:00 srun -n1 --export=HOME,PATH,TERM,SHELL $2 #2>/dev/null 
}

hpss_run() {
print_line "slurm submission on hpss: $1"
exechpss -a $PROJID "$1" 2>/dev/null; sleep 1.0
}

#hpss_run() {
#slurm_run "hpss" "$1"
#}

slurm_wait() {
while [[ $(squeue | grep ${USER}) ]]; do sleep 60.0; done
}

slurm_exists() {
if [[ $(squeue | grep ${USER}) ]] || pgrep_exists "srun"; then return 0; 
else return 1; fi 
}
