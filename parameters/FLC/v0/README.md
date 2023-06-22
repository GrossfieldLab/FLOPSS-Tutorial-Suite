### Context


This set of parameter is based on the first version of FLOPSS (please refer
here). 

The parameters: radius and number of nearest neighbours are calculated for
a DPPC-DIPC_CHOL bilayer system consisting of 1944 total lipids. For each
temperature, xy_rdf is calculated for each species and the first nearest
neighbour shell is determined (the first minimum after the xy_rdf goes above
1). Number of nearest neighbour is taken as 7 (6 + 1 center lipid) with the
assumption that maximum 2D close packing that can be acheived is hexagonal
close packing and the first shell members are eaul to 6. Ofcourse, there is
another assumption of lipids being perfect sphere here. But this is a first
pass.

Since xy_rdf changes as a function of temperature, so does the radius for the
first shell. Hence you can see 2 sets of paramters here, corresponding to 323K
and 423K
