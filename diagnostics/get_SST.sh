#!/bin/bash

DIR=~/PROJ_WRF/forced/SST
DAT_DIR=/glade/p_old/cesmLME/CESM-CAM5-LME/ocn/proc/tseries/monthly/SST
PREF=b.e11.BLMTRC5CN.f19_g16.007.pop.h.SST
CPREF=b.e11.BLMTRC5CN.f19_g16.850forcing.003.pop.h.SST

SYEARS=(1213 1258 1274 1284 1452 1600 1641 1761 1809 1815)
EYEARS=(1223 1274 1283 1294 1461 1609 1650 1770 1818 1825)

if [ ! -d ${DIR} ]; then mkdir -p ${DIR}; fi

for ((i=8; i<10; i++)); do

SYR=${SYEARS[i]}
EYR=${EYEARS[i]}

if [[  ${SYR:0:2} -eq 18 ]]; then
COUT_FILE=${DIR}/SST_ctrl_${SYR:0:2}00_${SYR:0:2}49_avg.nc
CTRL_FILE=${DAT_DIR}/${CPREF}.${SYR:0:2}0001-${SYR:0:2}4912.nc 
FORCED_FILE=${DAT_DIR}/${PREF}.${SYR:0:2}0001-${SYR:0:2}4912.nc 
else
COUT_FILE=${DIR}/SST_ctrl_${SYR:0:2}00_${SYR:0:2}99_avg.nc
CTRL_FILE=${DAT_DIR}/${CPREF}.${SYR:0:2}0001-${SYR:0:2}9912.nc 
FORCED_FILE=${DAT_DIR}/${PREF}.${SYR:0:2}0001-${SYR:0:2}9912.nc 
fi
CTRL_FILE=${DAT_DIR}/${CPREF}.100001-109912.nc 
COUT_FILE=${DIR}/SST_ctrl_1000_1099_avg.nc

ncks -O -v SST -d time,$(((SYR-${SYR:0:2}00)*12-1)),$(((EYR-${EYR:0:2}00)*12+10)) ${FORCED_FILE} ${DIR}/SST_forced_${SYR}_${EYR}.nc

ncwa -O -a time,z_t ${DIR}/SST_forced_${SYR}_${EYR}.nc ${DIR}/SST_forced_${SYR}_${EYR}_avg.nc


#if [ ! -f ${COUT_FILE} ]; then
ncwa -O -a time,z_t ${CTRL_FILE} ${COUT_FILE}
#fi

ncdiff -O -v SST ${DIR}/SST_forced_${SYR}_${EYR}_avg.nc ${COUT_FILE} ${DIR}/SST_forced_${SYR}_${EYR}_diff.nc
done
