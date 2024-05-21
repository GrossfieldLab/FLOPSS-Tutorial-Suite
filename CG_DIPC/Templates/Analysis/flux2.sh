#! /bin/bash
#SBATCH -p debug
#SBATCH -t 01:00:00
#SBATCH -c 1
#SBATCH --mem=60G
#SBATCH -J flux2
#SBATCH -o slurm_o/flux2_o
#SBATCH -e slurm_e/flux2_e

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
    cd data/0${d}/fluxAnalysis/interval_avg/

    python3 ${CURRENT}/fluxAnalysis/get_statePopulation.py --directFile=direct.h5
    python3 ${CURRENT}/fluxAnalysis/get_stateToStateFlux.py --directFile=direct.h5
    python3 ${CURRENT}/fluxAnalysis/get_stateTargetFlux.py --directFile=direct.h5

    cd $CURRENT
done
