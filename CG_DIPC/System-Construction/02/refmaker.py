#!/usr/bin/env python3
"""
15/10/2020
refmaker.py

Description:
    Replaces the coordinates of the bead selection with the centroid of input pdb. The new pdb can be used as the
    reference file (-r flag in gmx grompp module) for flat bottom restraint implementation.

Usage:
    python3 refmaker.py <.pdb file> <str-name of the bead corresponding to i in .itp definition> output

Example:
    python3 refmaker.py system_centered.pdb "PO4" ref_system_centered.pdb
"""

import sys
import loos

# Creating a LOOS AtomicGroup with pdb
model = loos.createSystem(sys.argv[1])

# Find the centroid of the system
ref = model.centroid()

# Replace only the z coord of bead with centroid z 
for i in range(len(model)):
    if model[i].name() == str(sys.argv[2]):
        update = model[i].coords()
        update.set(update[0],update[1],ref[2])
        model[i].coords(update)

pdbFile = loos.PDB.fromAtomicGroup(model)
outFile = open(str(sys.argv[3]),"w")
outFile.write(str(pdbFile))
outFile.close()
