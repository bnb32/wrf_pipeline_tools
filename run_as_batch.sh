#!/bin/bash

if [ $# -ne 4 ]; then echo "usage $0: function batch_id time args"; exit 1; fi

FUNC=$1; NAME=$2; TIME=$3; ARGS=$4

cd ~/RUNWORKFLOW/logs
qsub -N ${NAME} -A UCOR0023 -l "$TIME" -q regular -j oe -m abe -M bnb.chey.mon@gmail.com -l select=1:ncpus=1:mpiprocs=1 -S /bin/bash -v $ARGS $FUNC

