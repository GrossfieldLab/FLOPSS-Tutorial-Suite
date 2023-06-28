#!/bin/sh
#
# env.sh
#
# This script defines environment variables that are used by other shell
# scripts, both when setting up the simulation and when running the simulation.

############################# GENERAL SETUP #################################### 

# Purge all the existing modules
# module purge

# This is our local scratch, where we'll store files during the dynamics.
export NODELOC=$LOCAL
export USE_LOCAL_SCRATCH=1

################################ GROMACS #######################################

# Loading the prebuilt GROMACS module - For Cluster Run 
module load gromacs/2020.3/b2

# Set environmental variable for GROMACS
export GMX=$(which gmx)

############################## WESTPA & LOOS ###################################

# Activating prebuilt conda env with LOOS and westpa2
conda activate westpa2-loos

# Check for LOOS in python3
if ! python3 -c "import loos"; then
    echo "loos module can't be imported in python3"
    echo "Make sure you have loos properly installed in your conda env"
    exit 1
fi

# Set up python environment for westpa
export WEST_PYTHON=$(which python)

################################ WE SETUP ######################################

# Explicitly name our simulation root directory.
# In this case, $WESR_SIM_ROOT is essentially $SLURM_SUBMIT_DIR
if [[ -z "$WEST_SIM_ROOT" ]]; then
  export WEST_SIM_ROOT="$PWD"
fi

# Set the simulation name.
export SIM_NAME=$(basename $WEST_SIM_ROOT)
echo "simulation $SIM_NAME root is $WEST_SIM_ROOT"

# Set Log directory
export LOGDIR=${WEST_SIM_ROOT}/job_logs