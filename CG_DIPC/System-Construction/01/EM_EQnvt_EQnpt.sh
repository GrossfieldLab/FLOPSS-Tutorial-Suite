#! /bin/bash
#SBATCH -p gpu --gres=gpu:1 
#SBATCH -t 72:00:00
#SBATCH -N 1
#SBATCH -c 16
#SBATCH -J 6_1_DIPC
#SBATCH -o 6_1_DIPC.out
#SBATCH -e 6_1_DIPC.err

module load gromacs/2020.3/b2

# Minimization
export $GMX_MAXCONSTRWARN=-1
# step6.0 - soft-core minimization
gmx grompp -f step6.0_minimization.mdp -o step6.0_minimization.tpr -c system.pdb -r system.pdb -p system.top -n index.ndx
gmx mdrun -nt 16 -deffnm step6.0_minimization

# step6.1
gmx grompp -f step6.1_minimization.mdp -o step6.1_minimization.tpr -c step6.0_minimization.gro -r system.pdb -p system.top -n index.ndx
gmx mdrun -nt 16 -deffnm step6.1_minimization

unset GMX_MAXCONSTRWARN

# Equilibration
cnt=2
cntmax=6

while ((${cnt} <= ${cntmax}))
do
    pcnt=$((cnt-1))
    if (($cnt == 2))
    then
        gmx grompp -f step6.${cnt}_equilibration.mdp -o step6.${cnt}_equilibration.tpr -c step6.${pcnt}_minimization.gro -r system.pdb -p system.top -n index.ndx
    else
        gmx grompp -f step6.${cnt}_equilibration.mdp -o step6.${cnt}_equilibration.tpr -c step6.${pcnt}_equilibration.gro -r system.pdb -p system.top -n index.ndx
    fi
    gmx mdrun -nt 16 -deffnm step6.${cnt}_equilibration
    cnt=$((cnt+1))
done

############################################################
#                 RESTRAINING THE BILAYER                  #
############################################################


## Creating a psf and pdb file for loos to work with : EQ.pdb, EQ.psf
gmx dump -s  step6.6_equilibration.tpr | gmxdump2pdb.pl --constraints --vsites EQ

## Centering the system to center of bilayer 
subsetter -C 'resname =~ "PC" || resname == "CHOL"' --reimage=zealous system_centered EQ.psf step6.6_equilibration.xtc

## Creating reference pdb from the centered pdb
python3 refmaker.py system_centered.pdb "PO4" ref_system_centered.pdb

#############################################################

# Production
gmx grompp -f step7_production.mdp -o step7_production.tpr -c step6.6_equilibration.gro -r ref_system_centered.pdb -p system.top -n index.ndx
gmx mdrun -nt 16 -deffnm step7_production -cpt 60
