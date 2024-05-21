##########################################################################
#                                                                        #
#  Usage                                                                 # 
#  -----                                                                 # 
#  bash visual_merge.sh PATH                                                  #
#                                                                        # 
##########################################################################

conda activate loos

GMX_PATH=/software/gromacs/2020.3/b2/bin
TRAJ=$1

prefix=$(basename ${TRAJ}/*PC.mdp .mdp)

# A=$(ls ../${prefix}_*.tpr | tail -1)

echo "GMX_PATH/gmx dump -s fake.tpr | gmxdump2pdb.pl --constraints --vsites ${prefix}"

$GMX_PATH/gmx dump -s fake.tpr | gmxdump2pdb.pl --constraints --vsites ${prefix}

echo ""

echo "subsetter --append 1 --regex 1 --skip 1  -C 'resname =~ "PC" || resname == "CHOL"' --reimage=extreme fixed_${prefix} ${prefix}.psf $TRAJ/${prefix}_*.xtc"

echo ""

subsetter --append 1 --regex 1 --skip 1  -C 'resname =~ "PC" || resname == "CHOL"' --reimage=extreme fixed_${prefix} ${prefix}.psf $TRAJ/${prefix}_*.xtc

echo ""
echo " Merge report "
echo "=============="
echo ""

trajinfo fixed_${prefix}.pdb fixed_${prefix}.dcd

# #############################################################################

# echo "merge-traj --downsample-dcd fixed_${prefix}_10.dcd --downsample-rate 10 ${prefix}.psf A.dcd fixed_${prefix}.dcd"

# echo ""

# merge-traj --downsample-dcd fixed_${prefix}_10.dcd --downsample-rate 10 ${prefix}.psf A.dcd fixed_${prefix}.dcd

# echo ""
# echo " Merge report "
# echo "=============="
# echo ""

# trajinfo fixed_${prefix}.pdb fixed_${prefix}_10.dcd

# #############################################################################

echo "merge-traj --downsample-dcd fixed_${prefix}_100.dcd --downsample-rate 100 ${prefix}.psf A.dcd fixed_${prefix}.dcd"

echo ""

merge-traj --downsample-dcd fixed_${prefix}_100.dcd --downsample-rate 100 ${prefix}.psf A.dcd fixed_${prefix}.dcd

echo ""
echo " Merge report "
echo "=============="
echo ""

trajinfo fixed_${prefix}.pdb fixed_${prefix}_100.dcd



# merge-traj --centering-selection 'resname == "CHOL"' $2.psf  $2_fix.dcd $2.pdb --selection-is-split 1 --fix-imaging 1 --postcenter-z 'resname =~ "PC" || resname == "CHOL"'
# frame2pdb $2.psf $2_fix.dcd 0 > $2_fix.pdb
