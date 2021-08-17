#!/bin/csh
#PBS -N %NAME%_met
#PBS -A %PROJECTCODE% 
#PBS -l walltime=03:00:00
#PBS -q regular
#PBS -j oe
#PBS -m abe
#PBS -M bnb.chey.mon@gmail.com
#PBS -l select=2:ncpus=36:mpiprocs=36
cd %DIRECTORY%
###mpiexec_mpt -n 64 ./metgrid.exe
###mpiexec_mpt dplace -s 1 ./metgrid.exe
mpiexec_mpt ./metgrid.exe
%LINK%
exit
