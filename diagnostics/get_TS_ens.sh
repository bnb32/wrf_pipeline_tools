#!/bin/bash

DAT_DIR=/glade/p_old/cesmLME/CESM-CAM5-LME/atm/proc/tseries/monthly/TS
PREF=b.e11.BLMTRC5CN.f19_g16
DIR=~/PROJ_WRF/forced/TS

if [ ! -d $DIR ]; then mkdir -p $DIR; fi

for i in $(seq -f "%03g" 1 13); do
    ncks -v TS ${DAT_DIR}/${PREF}.${i}.cam.h0.TS.085001-184912.nc ${DIR}/TS_${i}_0850_1849.nc
done

