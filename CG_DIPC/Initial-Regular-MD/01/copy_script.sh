#############################################
#  Usage:                                   #
#       bash copy_script.sh #REPLICANUMBER# #
#############################################

CURRENT=$PWD

for T in 323K 423K
do
    dest=../../Initial-Regular-MD/0${1}/$T
    mkdir -p $dest/

    cp ../../Templates/Production/${T}/step7_production.mdp $dest/
    cp step7_production.cpt $dest/
    cp step7_production.gro $dest/
    cp system.top $dest/
    cp index.ndx $dest/
    cp -r toppar/ $dest/
    cp ref_system_centered.pdb $dest/

    cd $dest/
    mv step7_production.cpt $1"DIPC_0.cpt"
    mv step7_production.mdp $1"DIPC.mdp"
    mv step7_production.gro $1"DIPC.gro"

    cp ../../Templates/Cycler/cycle* .

    cd $CURRENT
done
