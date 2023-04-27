#!/bin/bash
#SBATCH --partition=gpu -C K20X
#SBATCH --gres=gpu:2
#SBATCH --time=120:00:00
#SBATCH --job-name=WESTPA_RUN
#SBATCH --output=WESTPA_RUN.out
#SBATCH --error=WESTPA_RUN.err
#SBATCH --nodes=1
#SBATCH --cpus-per-task=24

###############################################################################
#                                                                             #
# run.sh                                                                      #
#                                                                             #
# Runs the weighted ensemble TEST simulation. Make sure you ran init.sh first!#
#                                                                             #
###############################################################################

############################### GENERAL SETUP ################################# 

# Set shell option to print commands and their arguments as they are executed.
set -x

# Make sure environment is set else exit
cd $SLURM_SUBMIT_DIR
source env.sh || exit 1

# Print out a sorted list of all the environmental variables
env | sort

# Run w_run
# Please note that this script is optimized for the K20Xm GPUs at CIRC, U of R
# NOTE : You need to change the n-workers parameter with the $NUM_OF_LOCAL_GPUS
# in a given node. For the K20Xm, it is 2 GPUS per node. This version is better
# when the work is more GPU dependent than CPUs.
w_run \
    --work-manager=processes \
    --n-workers=2 \
    "$@" \
    &> ${LOGDIR}/west-$SLURM_JOBID.log &