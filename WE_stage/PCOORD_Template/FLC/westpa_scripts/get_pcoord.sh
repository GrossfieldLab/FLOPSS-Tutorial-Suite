#!/bin/bash
#
# get_pcoord.sh
#
# This script is run when calculating initial progress coordinates for new
# initial states (istates).  This script is NOT run for calculating the progress
# coordinates of most trajectory segments; that is instead the job of runseg.sh.

# If we are debugging, output a lot of extra information.
if [ -n "$SEG_DEBUG" ] ; then
  set -x
  env | sort
fi

# Make sure we are in the correct directory
cd $WEST_SIM_ROOT/common_files

############################## Progress Coord ################################# 

# Creating a temporary file to store pcoord
TEMP_SYSTEM=$(mktemp)

# Set the arguments for Contacts2D.py and call the script to calculate initial
# progress coordinate.

python3 $WEST_SIM_ROOT/common_files/DBSCANanalysisSystem.py \
    --model $WEST_SIM_ROOT/bstates/model.psf \
    --traj $WEST_STRUCT_DATA_REF \
    --lipid_list $WEST_SIM_ROOT/common_files/lipidList.dat \
    --r $WEST_SIM_ROOT/common_files/avgRcutoff.dat > $TEMP_SYSTEM

cat $TEMP_SYSTEM | tail -n +4 | awk {'print $3'} > $WEST_PCOORD_RETURN

# Clean up
rm -f $TEMP_SYSTEM

cp $WEST_STRUCT_DATA_REF $WEST_TRAJECTORY_RETURN

###############################################################################

if [ -n "$SEG_DEBUG" ] ; then
  head -v $WEST_PCOORD_RETURN
fi
