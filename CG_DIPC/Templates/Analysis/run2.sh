#! /bin/bash

# conda deactivate
# conda activate westpa-2020.02

# Sanity check #2
echo "Sanity check #2"
# Flux Analysis : Calculate the flux and state populations.
echo "Flux Analysis : Calculate the flux and state populations.(2/2)"
cd flux_analysis/
bash run.sh
cd ..
echo "Done!(2/2)"

##------------------------------------------------##

# Constructing FES using auxillary variables stored in .h5 file
sbatch OtherFES/Analysis.sh
# bash OtherFES/Analysis_DAPC.sh
# bash OtherFES/Analysis_DIPC.sh
# bash OtherFES/Analysis_POPC.sh

# Combining multiple replica using multi_west
conda deactivate
conda activate westpa-2020.05

#########################################
# WARNING! MIGHT NEED MANUAL INTERVENTION
# CHECK THE COMMENTS INSIDE THE SCRIPT
#########################################
sbatch multi_west/combine.sh
#########################################

bash multi_west/pdist2data_multi.sh

# Make sure you updated the OtherFES/module.py before next step

bash OtherFES/Analysis_multi.sh

##------------------------------------------------##

## Reweighting over other Auxillary coordinate that was not planned
conda deactivate
conda activate westpa-2020.05

# After transfering fakeWE folders into respective directories
# Make the necessary file tree for combining multiple replica
sbatch ReweighOverOtherCVs/makeFileTree.sh

#########################################
# WARNING! MIGHT NEED MANUAL INTERVENTION
# CHECK THE COMMENTS INSIDE THE SCRIPT
#########################################
sbatch ReweighOverOtherCVs/combine.sh
#########################################

bash ReweighOverOtherCVs/pdist2data_multi.sh

# Make sure you updated the ReweighOverOtherCVs/module.py before next step
sbatch OtherFES/Analysis_ReweighOverOtherCVs_multi.sh

##------------------------------------------------##

# Error analysis using derivative-stats

# This section assumes that you have the derivative-stats in your parent dir
# where the Analysis/ dir lies.
# Derivative-stats is available from following:
# https://github.com/lgsmith/derivative-stats

# Also, derivative-stats assumes that FECs have same x bin range.
# However, MAB does not assumes that by default but this can be acheived by
# specifying this in w_pdist stage by BINEXPR. So far this only works for
# 1D pcoords. Our FECs are rectified of this issue.

sbatch errorAnalysis/errorAnalysis.sh
