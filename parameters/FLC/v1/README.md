### Context


This set of parameter is based on the refined version of FLOPSS (please refer
here). 

The parameters: radius and number of nearest neighbours are calculated for
a DPPC-DIPC_CHOL bilayer system consisting of 1944 total lipids. Four replicas
of this system was simulated at 298K, 323K, 333K, 353K, 373K and 423K. Now we
set a range for radius (5A to 60A) and number of nearest numbers (5 to 60) and
checked the corresponding value of FLC across all the temperature runs.

We used a HMM model to find hidden states (upto 5) and the took the state difference
between extreme states. We filtered out all the parameter files that did not
resulted in a state difference of 0.5. Next, we rank the parameter files that
are most consistent across all temperature replicas. Then we sorted them based
on the ones that produce maximum state differences. If there's a tie, we go
with the one that does has least num of neighbours (to reduce the neighbor
search cost), if that's a tie, we go with the least radius.

This process was done for each lipid species and the corresponding refined
values are used in parameter file
