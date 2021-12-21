#!/bin/python

import numpy as np
import matplotlib.pyplot as plt
import Ngl,Nio
import sys
from scipy.io import FortranFile
import struct
from array import array

year=1213
case="forced"
pref="/glade/scratch/bbenton/20XXWRF/WRF_INT_OUTPUT/%s/%s/CESM_WRF_%s_%s:%s" %(case,year,case,year,year)
in_file=pref+"-01-01_00"

