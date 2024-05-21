#! /bin/bash
#SBATCH -p debug
#SBATCH -t 01:00:00
#SBATCH -c 1
#SBATCH --mem=60G
#SBATCH -J flux
#SBATCH -o slurm_o/flux_o
#SBATCH -e slurm_e/flux_e

###############################################################################
# Usage                                                                       #
#                                                                             #
# bash Analysis.sh                                                            #
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

    if [ -e data/0${d}/west.h5 ] ; then

        cd data/0${d}/

        # Remove the files and folders from previous flux runs
        rm -rf west.cfg
        rm -rf fluxAnalysis

        # cp -pf $CURRENT/fluxAnalysis/WEST_CFG_TEMPLATE/cumulative/west.cfg . 

        # w_ipa -ao 

        # rm -rf west.cfg

        cp -pf $CURRENT/fluxAnalysis/WEST_CFG_TEMPLATE/interval_avg/west.cfg .
        w_assign -W west.h5 --config-from-file --scheme interval_avg --serial
        # Since the assign.h5 file are created inside the fluxAnalysis/interval
        # as per the SCHEME in the west.cfg, we need to cd into that dir and
        # run w_direct in it
        cd fluxAnalysis/interval_avg/
        w_direct all -a assign.h5 -W ../../west.h5 --evolution blocked --step-iter 10

        # w_ipa -ao 

        cd $CURRENT
    fi
done
