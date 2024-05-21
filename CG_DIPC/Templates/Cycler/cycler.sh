#! /bin/bash 

# Check if halt file exists
if [[ -f halt ]]
then
    echo "Exiting..." && exit 0
fi

# Set up environmental variables
NODES=$(echo $SLURM_NNODES)
CPT=$(echo $SLURM_JOB_CPUS_PER_NODE)
JOBID=$(echo $SLURM_JOB_ID)
JOBNAME=$(echo $SLURM_JOB_NAME)

# Get prefix & iteration
META=`echo $JOBNAME | cut -d'-' -f3`
PREFIX=`echo $JOBNAME | cut -d'-' -f1`
ITERATION=`echo $JOBNAME | cut -d'-' -f2`
ITERATION=`echo $ITERATION | cut -d'-' -f1`
PREVITER=$((ITERATION - 1))
NEXTITER=$((ITERATION + 1))
echo "Jobname:" $JOBNAME

# Check that files from previous iteration exist
checkpoint=$(echo $PREFIX"_"$PREVITER".cpt")
restart=$(echo $PREFIX"_"$PREVITER".tpr")
trajectory=$(echo $PREFIX"_"$PREVITER".xtc")
log_file=$(echo $PREFIX"_"$PREVITER".log")
# trr_file=$(echo $PREFIX"_"$PREVITER".trr")
edr_file=$(echo $PREFIX"_"$PREVITER".edr")

gro_file=$(echo $PREFIX".gro")
mdp_file=$(echo $PREFIX".mdp")

# if [[ ! -e "$trr_file" ]]
# then
    # echo ".trr FILE!!An error occurred in iteration "$PREVITER". Exiting..." && exit 0
# fi

if [[ ! -e "$mdp_file" ]]
then
    echo "MD Parameter file(.mdp)!!!An error occurred in iteration "$PREVITER". Exiting..." && exit 0
fi

if [[ ! -e "$gro_file" ]]
then
    echo "GRO File!!!An error occurred in iteration "$PREVITER". Exiting..." && exit 0
fi

if [[ "$ITERATION" != "1" ]] && [[ ! -e "$restart" ]]
then
    echo "RESTART!!!An error occurred in iteration "$PREVITER". Exiting..." && exit 0
fi

if [[ "$ITERATION" != "1" ]] && [[ ! -e "$checkpoint" ]]
then
    echo "CHECK POINT!!An error occurred in iteration "$PREVITER". Exiting..." && exit 0
fi

if [[ "$ITERATION" != "1" ]] && [[ ! -e "$trajectory" ]]
then
    echo "TRAJ!!An error occurred in iteration "$PREVITER". Exiting..." && exit 0
fi

if [[ "$ITERATION" != "1" ]] && [[ ! -e "$log_file" ]]
then
    echo "LOG FILE!!An error occurred in iteration "$PREVITER". Exiting..." && exit 0
fi

if [[ "$ITERATION" != "1" ]] && [[ ! -e "$edr_file" ]]
then
    echo ".edr FILE!!An error occurred in iteration "$PREVITER". Exiting..." && exit 0
fi

# Submit next job
NEXTJOBN=$(echo ${PREFIX}-${NEXTITER})
BNEXTJOB=$(echo $NEXTJOBN})

if [[ -v META ]]
then
    NEXTJOBN=$(echo ${NEXTJOBN}-$META)
fi

echo "Nodes:" $NODES "CPT:" $CPT "JobID:" $JOBID
echo "Partition:" $PARTITION "Time limit:" $TIMELIMIT "Memory:" $MEM "Driver:" $DRIVER
echo "Prefix:" $PREFIX "Current teration:" $ITERATION "Next iteration:" $NEXTITER

# sbatch --partition $PARTITION --time $TIMELIMIT -c $CPT -C "V100|K80" --overcommit --gres gpu:$NODES --mem $MEM --job-name $NEXTJOBN --dependency afterany:$JOBID --error $NEXTJOBN.err --output $NEXTJOBN.out $DRIVER
sbatch --partition $PARTITION --time $TIMELIMIT -c $CPT --overcommit --gres gpu:$NODES --mem $MEM --job-name $NEXTJOBN --dependency afterany:$JOBID --error $NEXTJOBN.err --output $NEXTJOBN.out $DRIVER

# Start current job
dhm=$(date +%k%M) # date hour minute
scontrol show jobid -dd $SLURM_JOB_ID > slurm-${SLURM_JOB_ID}_${dhm}.jobinfo
nvidia-smi -q -g 0 -d UTILIZATION > nvidia-${SLURM_JOB_ID}_${dhm}.jobinfo

module load gromacs/2020.3/b2

gmx grompp -f ${PREFIX}.mdp -o ${PREFIX}_${ITERATION}.tpr -c ${PREFIX}.gro -r ref_system_centered.pdb -t $checkpoint -p system.top -n index.ndx

gmx mdrun -nt $CPT -deffnm ${PREFIX}_${ITERATION} -cpt 360 -maxh 48

exit 0
