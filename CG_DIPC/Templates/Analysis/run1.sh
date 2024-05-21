#! /bin/bash

conda deactivate
conda activate westpa2-loos

# Make directories to dump the slurm outputs and error files
mkdir -p slurm_o
mkdir -p slurm_e

# # Run initial data pull from the WE simulation and make cv evolution .pdf files.
echo "Run initial data pull from the WE simulation and make cv evolution .pdf files."
sbatch west2pdist.sh
echo "Done!"

# # Process the pdist.h5 
echo "Process the pdist.h5" 
sbatch pdist2data.sh
echo "Done!"

# Flux Analysis : Calculate the flux and state populations.
echo "Flux Analysis"
sbatch flux.sh
echo "Flux Analysis : Prepping assign.h5 and direct.h5 files (1/2)"
sbatch flux2.sh
echo "Flux Analysis : Calculating state population and flux (2/2)"
