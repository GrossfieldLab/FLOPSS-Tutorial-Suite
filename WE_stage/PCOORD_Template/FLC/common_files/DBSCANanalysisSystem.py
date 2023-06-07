#!/usr/bin/env python3
'''
Example:
    python3 DBSCANanalysisSystem.py --model 1DIPC.psf
                                    --traj fixed_1DIPC_100.dcd
                                    --parameter param.dat > output
'''

# Importing functional modules
import loos
import loos.pyloos
import sys
import argparse
import numpy as np
import miscFuncs.loosFuncs as lf

def dbscanAnalysisSystem(fmodel, ftrajectory, fparam):

    # Parsing the arguments into variables
    model = loos.createSystem(fmodel)
    trajectory = loos.pyloos.Trajectory(ftrajectory, model)

    # Reading rFile
    rFileLipids, rAvgLipids, minSample = lf.rFileReader(fparam)

    # Converting model into dictionary
    lipidContainer, system, lipidList = lf.segs2pyDicts(model,
                                                        rFileLipids)

    totalNum = len(system)
    totalFrames = len(trajectory)
    clusterCount= np.zeros((totalFrames,))
    clusterLipids2Total= np.zeros((totalFrames,))
    coreLipids2Total = np.zeros((totalFrames,))
    outlierLipids2Total = np.zeros((totalFrames,))
    silhouette_CoefficentDict = {}

    frameCounter = 0
    for frame in trajectory:

        box = frame.periodicBox()

        # Initializing key Counter
        C = 0
        coreCount = 0
        boundaryCount = 0
        outlierCount = 0
        silhouette_Coefficent = []

        # Extracting lipids to calculate centroids from the container dict
        for value in lipidContainer.values():

            # Collecting radius cutoff from rFile
            rCut = float(rAvgLipids[C])
            min_samples = int(minSample[C])
            keyCoreLipids = []
            keyBoundaryLipids = []

            Up, Lo = lf.leafletLipidSeparator(value)
            nClustUp, nCoreUp, nBoundUp, nNoiseUp, silhoUp = lf.lsDBSCAN(Up,
                                                                        rCut,
                                                                        min_samples,
                                                                        box,
                                                                        True)
            keyCoreLipids.extend(nCoreUp)
            keyBoundaryLipids.extend(nBoundUp)

            nClustLo, nCoreLo, nBoundLo, nNoiseLo, silhoLo = lf.lsDBSCAN(Lo,
                                                                        rCut,
                                                                        min_samples,
                                                                        box,
                                                                        True)
            keyCoreLipids.extend(nCoreLo)
            keyBoundaryLipids.extend(nBoundLo)

            # Worst Silhouette Coefficent of both
            silhouette_Coefficent.append(min(silhoUp, silhoLo))

            clusterCount[frameCounter] += (nClustUp + nClustLo)
            coreCount += np.sum(keyCoreLipids)
            boundaryCount += np.sum(keyBoundaryLipids)
            outlierCount += (nNoiseUp + nNoiseLo)

            # Updating key Counter
            C += 1

        coreLipids2Total[frameCounter] = coreCount/totalNum
        clusterLipids2Total[frameCounter] = (coreCount+boundaryCount)/totalNum
        outlierLipids2Total[frameCounter] = outlierCount/totalNum
        silhouette_CoefficentDict[frameCounter] = silhouette_Coefficent

        if __name__ == "__main__":
            print(clusterCount[frameCounter],
                coreLipids2Total[frameCounter],
                clusterLipids2Total[frameCounter],
                outlierLipids2Total[frameCounter],
                "\t".join(map(str, silhouette_Coefficent)))

        frameCounter += 1

    return(clusterCount,
        coreLipids2Total,
        clusterLipids2Total,
        outlierLipids2Total,
        silhouette_CoefficentDict)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model",
                        dest="model",
                        help="Structure to use")
    parser.add_argument("--traj",
                        dest="trajectory",
                        help="Trajectory to use")
    parser.add_argument("--parameter",
                        dest="parameter",
                        help="Parameter File")
    args = parser.parse_args()

    # Printing out header for output file
    headerList = lf.seg2pyList(args.parameter)
    header = "# " + " ".join(sys.argv)
    header2 = "# Parameters : " + "\t".join(headerList)
    header3 = "# Cluster-count\tCore lipid to total lipid\t\
        Cluster lipids to total lipids\t\
        Outlier lipids to total lipids\t\
        Silhouette Coefficent for lipid species"
    print(header, flush=True)
    print(header2, flush=True)
    print(header3, flush=True)

    dbscanAnalysisSystem(fmodel=args.model,
                         ftrajectory=args.trajectory,
                         fparam=args.parameter)