#!/usr/bin/python

#
# MODULES
#
import numpy,sys,os

import string

def read_trajectories(filename):

    tcfilepath = os.path.join(sys.prefix, filename)
    tcfile = open(tcfilepath)

    all_tracks = []
    all_lon = []
    all_lat = []
    while (1):
        line = tcfile.readline()
        elems = string.split(line)

	#print line
	#print elems
        
        try:
            # get track length
            tclength = int(elems[1])
	   
	    #print "\nStorm Length = %d\n" %  tclength
            
            track_lon = []
            track_lat = []
	    track_wind = []
	    track_pressure = []
	    track_year = []
	    track_month = []
	    track_day = []
	    track_hr = []
            for i in range(tclength):
                line = tcfile.readline()
                elems = string.split(line)

                # get lat and lon coordinates at each point
                try:
                    #lat = 90.0 + float(elems[0])
                    lon = float(elems[0])
                    lat = float(elems[1])
		    wind = float(elems[2])
		    pressure = float(elems[3])
		    year = int(elems[4])
	    	    month = int(elems[5])
	    	    day = int(elems[6])
	    	    hour = int(elems[7])


                    track_lat.append(lat)
                    track_lon.append(lon)
		    track_wind.append(wind)
		    track_pressure.append(pressure)
		    track_year.append(year)
		    track_month.append(month)
		    track_day.append(day)
		    track_hr.append(hour)

                except:
                    pass

            # store or plot track
            all_tracks.append(numpy.array([track_lon,track_lat,track_wind,track_pressure,track_year,track_month,track_day,track_hr]))

            # print track_lon
            # print track_lat

            #all_lon = concatenate((all_lon, Numeric.array(track_lon)),1)
            #all_lat = concatenate((all_lat, Numeric.array(track_lat)),1)
            
        except:
            pass
        if not line:
            break

    tcfile.close()

    #ntracks = len(all_tracks)
    #print "\nTotal: %d tracks\n" % (ntracks)

    #return [all_lon, all_lat]
    
    return [all_tracks]


