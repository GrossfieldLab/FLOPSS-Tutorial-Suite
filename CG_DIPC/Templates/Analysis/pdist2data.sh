#! /bin/bash
#SBATCH -p debug
#SBATCH -t 01:00:00
#SBATCH -c 1
#SBATCH -J pdist2data
#SBATCH -o slurm_o/pdist2data_o
#SBATCH -e slurm_e/pdist2data_e

###############################################################################
# Usage                                                                       #
#                                                                             #
# bash Plot.sh                                                                #
#                                                                             #
###############################################################################

# For DEBUGGING purposes, uncomment the following line
# set -x

CURRENT=$PWD

###############################################################################
#             1. CREATING DIRS AND COPYING west.h5 FILES FOR ANALYSIS         #
###############################################################################

for d in 1 2 3 4
do
    cd data/0${d}/
    iterstart=1
    iterstop=500
    interval=10

    STOP=$(echo "$(($iterstop - $(($iterstart-1)))) / $interval" | bc)

        for j in $(seq 0 $(($STOP-1)))
        do
            STARTiter=$(($iterstart+$(($j*$interval))))
            STOPiter=$(($(($iterstart+$(($(($j+1))*$interval))))-1))
            echo "${STARTiter} - ${STOPiter}"
            echo "plothist average pdist.h5 --first-iter $STARTiter --last-iter $STOPiter --text-output=average_${STARTiter}-${STOPiter}.dat"
            plothist average pdist.h5 --first-iter $STARTiter --last-iter $STOPiter --text-output=average_${STARTiter}-${STOPiter}.dat
        done
    cd $CURRENT
done
