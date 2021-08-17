#!/bin/csh
#PBS -N %NAME%_real
#PBS -A %PROJECTCODE% 
#PBS -l walltime=03:00:00
#PBS -q regular
#PBS -j oe
#PBS -m abe
#PBS -M bnb.chey.mon@gmail.com
#PBS -l select=1:ncpus=32:mpiprocs=32
cd %DIRECTORY%
###mpiexec_mpt -n 64 ./real.exe
###mpiexec_mpt dplace -s 1 ./real.exe
mpiexec_mpt ./real.exe
exit
