#!/bin/bash

START=(50 45 40 35 30 25 20 15 10 5)
END=(45 40 35 30 25 20 15 10 5 -50)

for i in $(seq 0 9); do
    python ./comp_stats_all.py ${START[i]} ${END[i]} True > ${START[i]}-${END[i]}_erups_data.txt
    mv ./f_vs_c_dists.pdf ${START[i]}-${END[i]}_erups_dists.pdf
done    
