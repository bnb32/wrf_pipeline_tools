#!/bin/bash

#if [ $# -ne 3 ]; then echo "usage $0: case start_yr end_yr"; exit 1; fi

#SYEAR=$2
#EYEAR=$3
CASE="forced"
DIR=~/PROJ_WRF/${CASE}
DIFF_FILE=~/PROJ_WRF/ctrl/T_sfc/chunks/T_sfc_ctrl_1000_1009.nc
EXTRACT=0
AVERAGE=0
SUBTRACT=1

if [ ! -d ${DIR}/T_sfc ]; then mkdir -p ${DIR}/T_sfc; fi
if [ ! -d ${DIR}/T_sfc/chunks ]; then mkdir -p ${DIR}/T_sfc/chunks; fi
if [ ! -d ${DIR}/T_sfc/diffs ]; then mkdir -p ${DIR}/T_sfc/diffs; fi

SYEARS=(1213)
EYEARS=(1223)
#SYEARS=(1213 1258 1274 1284 1452 1600 1641 1761 1809 1815)
#EYEARS=(1223 1274 1283 1294 1461 1609 1650 1770 1818 1825)

for i in $(seq 0 0); do
    if [ ${EXTRACT} -eq 1 ]; then
        for year in $(seq ${SYEARS[i]} ${EYEARS[i]}); do
            YDIR=${DIR}/${year}
            if [ -d ${YDIR} ]; then
                for month in $(seq -f "%02g" 1 12); do
                    INFILE=${YDIR}/wrfpost_${CASE}_${year}_${month}.nc 
                    OUTFILE=${DIR}/T_sfc/T_sfc_${CASE}_${year}_${month}.nc
                    ncks -v T_sfc_monthly ${INFILE} ${OUTFILE}
                done
            fi
        done
    fi
    
    if [ ${AVERAGE} -eq 1 ]; then
        FILES=`eval ls ${DIR}/T_sfc/T_sfc_${CASE}_{${SYEARS[i]}..${EYEARS[i]}}_{01..12}.nc`
        OUTFILE=${DIR}/T_sfc/chunks/T_sfc_${CASE}_${SYEARS[i]}_${EYEARS[i]}.nc
	ncea -O ${FILES} ${OUTFILE}    
    fi

    if [ ${SUBTRACT} -eq 1 ]; then
        INFILE=${DIR}/T_sfc/chunks/T_sfc_${CASE}_${SYEARS[i]}_${EYEARS[i]}.nc
	OUTFILE=${DIR}/T_sfc/diffs/T_sfc_${CASE}_${SYEARS[i]}_${EYEARS[i]}_diff.nc
        ncdiff -O -v T_sfc_monthly ${INFILE} ${DIFF_FILE} ${OUTFILE}     
    fi
done
