#! /bin/bash
#SBATCH -p debug
#SBATCH -t 01:00:00
#SBATCH -c 1
#SBATCH --mem=60G
#SBATCH -J plot
#SBATCH -o slurm_o/plot_o
#SBATCH -e slurm_e/plot_e

CURRENT=$PWD

###############################################################################
#             1. CREATING DIRS AND COPYING west.h5 FILES FOR ANALYSIS         #
###############################################################################

for d in 1 2 3 4
do

    if [ -e data/0${d}/west.h5 ] ; then

        cd data/0${d}/

        python3 $CURRENT/plotScripts/convergence.py --cv FLC --temperature 323 --suffix FLC_323K --plotScale energy --xLo 0 --xUp 1 --yUp 5 --dat_files average_{241,291,341,391,441,491}*.dat
        python3 $CURRENT/plotScripts/plot_fluxProfile.py --suffix DIPC_323K --dat_files fluxAnalysis/interval_avg/*flux_from*.dat
        python3 $CURRENT/plotScripts/plot_statePop.py --suffix DIPC_323K --dat_files fluxAnalysis/interval_avg/*_state_population.dat

        cd $CURRENT
    fi
done
