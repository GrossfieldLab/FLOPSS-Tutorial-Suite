#! /bin/bash
#SBATCH -p standard
#SBATCH -t 04:00:00
#SBATCH -c 1
#SBATCH -J west2pdist
#SBATCH -o slurm_o/west2pdist_o
#SBATCH -e slurm_e/west2pdist_e

###############################################################################
# Usage                                                                       #
#                                                                             #
# bash Analysis.sh                                                            #
#                                                                             #
###############################################################################

# For DEBUGGING purposes, uncomment the following line
# set -x

CURRENT=$PWD
WEFOLDER=../

###############################################################################
#             1. CREATING DIRS AND COPYING west.h5 FILES FOR ANALYSIS         #
###############################################################################

BINEXPR=$(echo $(python3 binGenerator.py --binRange "(0, 1)" --Num_bins_plusOne 101))

for d in 01 02 03 04
do

    if [ -e ${WEFOLDER}/$d/west.h5 ] ; then

        mkdir -pv data/${d}
        rsync -av ${WEFOLDER}/${d}/west.h5 data/${d}/

        cd data/${d}/

        rm -f *.pdf *.dat
        rm pdist.h5

        w_pdist -b "[${BINEXPR}]" --serial

        plothist evolution pdist.h5 -o evolution.pdf

        cd $CURRENT
    fi
done
