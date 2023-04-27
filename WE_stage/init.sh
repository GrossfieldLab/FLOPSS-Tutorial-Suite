#!/bin/bash
#SBATCH --partition=gpu-debug
#SBATCH --gres=gpu:1
#SBATCH --time=01:00:00
#SBATCH --mem=15G
#SBATCH --job-name=west_init
#SBATCH --output=west_init.out
#SBATCH --error=west_init.err

# Initialize the WESTPA simulation, creating initial states (istates) and the
# main WESTPA data file, west.h5. 

# If you run this script after starting the simulation, the data you generated
# will be erased!

# Set up simulation environment

source env.sh

# Make sure that seg_logs (log files for each westpa segment), traj_segs (data
# from each trajectory segment), and istates (initial states for starting new
# trajectories for steady state calculation) directories exist and are empty. 

# Since we are running equilibrium runs here, istates have been commented out.

rm -rf traj_segs seg_logs west.h5 system.h5 seg_logs.tar job_logs istates
rm -rf binbounds.txt __pycache__
mkdir -p seg_logs traj_segs job_logs istates


# Set pointer to bstate and tstate (No tstate since we are doing equilibrium runs)
BSTATE_ARGS="--bstate-file $WEST_SIM_ROOT/bstates/bstates.txt"

# Initialize the simulation, creating the main WESTPA data file (west.h5)
# The "$@" lets us take any arguments that were passed to init.sh at the
# command line and pass them along to w_init.

# Run w_init
w_init \
  $BSTATE_ARGS \
  --debug \
  --segs-per-state 4 \
  --work-manager=threads "$@"