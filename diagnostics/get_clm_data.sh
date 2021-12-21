#!/bin/bash

START_YEAR=1955
END_YEAR=2005
CASE="ctrl"
DIR=~/scratch/20XXWRF/CESM_DATA/$CASE
OUT_DIR=$DIR/CLM_DATA
LAT=34.0
LONG=247.0

for ((i=$START_YEAR; i<=$END_YEAR; i++)); do
    CAM_FILE=`ls $DIR/$i/*cam*.nc`
    OUT_FILE=clm_data_${CASE}_${i}.nc
    echo "input file: $CAM_FILE"
    echo "output file: $OUT_FILE"
    ncks -d lat,$LAT -d lon,$LONG -O -v T,RELHUM,PS,PRECT,FLDS,FSDS,U,V $CAM_FILE -o $OUT_DIR/$OUT_FILE
    ncap2 -A -s 'UBOT=U(:,29,:,:)' $OUT_DIR/$OUT_FILE
    ncap2 -A -s 'VBOT=V(:,29,:,:)' $OUT_DIR/$OUT_FILE
    ncks -O -x -v U,V $OUT_DIR/$OUT_FILE -o $OUT_DIR/$OUT_FILE
done    
