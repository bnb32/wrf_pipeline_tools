#!/bin/python
#
import numpy, os
import Nio
import Ngl
import matplotlib.pyplot as plt
import matplotlib.transforms as transforms
from scipy.signal import argrelextrema
import argparse
from volcInfo import getVolcInfo
from confidence_interval import conInterval

parser = argparse.ArgumentParser(description='Plot and find volcanoes')
parser.add_argument('-number',required=True,type=int)
parser.add_argument('-region',default="all",choices=["north","south","all"])
parser.add_argument('-plot',default=False,action='store_true')
args = parser.parse_args()

Number = args.number

vals,times,lats = getVolcInfo(Number,args.region)

print("\nTIMES\n")
print(times) 
print("\nAMOUNTS\n")
print(vals)
print("\nLATITUDES\n")
print(lats)

if args.plot:
    
    fig,ax = plt.subplots()

    plt.rc('font',size=14)
    plt.rc('axes',titlesize=20)
    plt.rc('axes',labelsize=14)
    plt.rc('xtick',labelsize=14)
    plt.rc('ytick',labelsize=8)
    
    plt.locator_params(axis='y',nbins=6)
    
    if args.region=="north":
        plt.title("Volcanic Eruptions (NH)")
    elif args.region=="south":
        plt.title("Volcanic Eruptions (SH)")
    else:
        plt.title("Volcanic Eruptions")

    plt.xlabel("Year")
    plt.ylabel("Aerosol Mass "+r'$(kg/m^2)$')
    #plt.bar(time_erups,max_erups,color="gray")
    plt.bar(times,vals,color="gray")
    vals_sort = vals
    vals_sort.sort()
    plt.axhline(y = vals_sort[-10], color = 'r', linestyle = 'dashed',linewidth=0.35)
    plt.axhline(y = vals_sort[-5], color = 'r', linestyle = 'dashed',linewidth=0.35)
    plt.axhline(y = vals_sort[0], color = 'r', linestyle = 'dashed',linewidth=0.35)
    trans = transforms.blended_transform_factory(
        ax.get_yticklabels()[0].get_transform(), ax.transData)
    ax.text(0,vals_sort[-10], "{:.5f}".format(vals_sort[-10]), 
        color="red", transform=trans,ha="right", va="center", fontsize=6)
    ax.text(0,vals_sort[-5], "{:.5f}".format(vals_sort[-5]), 
        color="red", transform=trans,ha="right", va="center", fontsize=6)
    ax.text(0,vals_sort[0], "{:.5f}".format(vals_sort[0]), 
        color="red", transform=trans,ha="right", va="center", fontsize=6)
    
    yticks = ax.yaxis.get_major_ticks()
    yticks[0].label1.set_visible(False)

    if region=="north":
        plt.savefig("eruptions_plot_NH_%s.png" %(Number),bbox_inches='tight',pad_inches=0.1,dpi=300)
    elif region=="south":
        plt.savefig("eruptions_plot_SH_%s.png" %(Number),bbox_inches='tight',pad_inches=0.1,dpi=300)
    else:    
        plt.savefig("eruptions_plot_%s.png" %(Number),bbox_inches='tight',pad_inches=0.1,dpi=300)
