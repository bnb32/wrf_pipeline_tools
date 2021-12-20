** wrf_pipeline_tools to run wrf on cheyenne **

Four main scripts are:

(1) run_wrf_pipeline.sh
(2) run_wrf_pre_pipeline.sh
(3) run_wrf_diag_pipeline.sh
(4) run_wrf_batch.py

(1) run_wrf_pipeline.sh calls (2) and (4) and runs the entire pipeline
from fetching cesm data from HPSS to converting cesm data to intermediate
format for WPS, to running WRF, and to extracting only the needed fields 
from WRF output for storm tracking and drought analysis. This script takes an
argument <stride> which selects how many parallel WRF sims to run. This script also includes all immediate post-processing routines on WRF output before sending to TSTORMS 

(2) run_wrf_pre_pipeline.sh calls minor scripts to do all preprocessing 
needed before running WPS. The main script called by (2) is the ncl conversion
script to write out intermediate WPS files. This script also performs checks for
whether cesm data is needed from HPSS, whether the cesm data has been converted into
the format needed for WPS intermediate conversion, and whether WPS intermediate 
data has already been written. This script takes an argument <nrun> which
allows WRF intermediate conversion to be run in parallel. The WPS intermediate
conversion is submitted to the queue on cheyenne.

(3) run_wrf_diag_pipeline.sh calls all diagnostics oriented routines. This includes running TSTORMS, plotting output, appending new figures to diagnostics.tex, compiling the tex file, and uploading to google drive.

(4) run_wrf_batch.py runs the entire WPS/WRF routine, including geogrid, metgrid,
real, and wrf. This script uses the templates seen in batch_templates to submit
jobs through PBS to cheyenne and setup namelists. These templates are edited upon 
running and copied into the required directories. This script also takes an 
argument <nrun> so that multiple WRF runs can happen simultaneously. On running 
WPS_nrun and WRF_nrun are created and routines are run from those directories. 

You need to have the following nc files in an "Invariant_Data" directory:

(1) "/gpfs/fs1/p/cesmdata/cseg/ncl/map_gx1v6_to_fv1.9x2.5_bilin_da_090296.nc"
(2) "/gpfs/fs1/p/cesmdata/cseg/inputdata/lnd/clm2/griddata/fracdata_1.9x2.5_gx1v6_c090206.nc"
(3) "/gpfs/fs1/p/cesmdata/cseg/inputdata/atm/cam/topo/USGS-gtopo30_1.9x2.5_remap_c050602.nc"
  
Also need to have WRF and WPS directories in `${DIR_HOME}`.  
