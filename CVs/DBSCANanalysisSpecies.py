#!/usr/bin/env python3
'''
Example:
    python3 DBSCANanalysisSpecies.py --model 1DIPC.psf
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


def dbscanAnalysisSpecies(fmodel, ftrajectory, fparam):

    # Parsing the arguments into variables
    model = loos.createSystem(fmodel)
    trajectory = loos.pyloos.Trajectory(ftrajectory, model)

    # Reading rFile
    rFileLipids, rAvgLipids, minSample = lf.rFileReader(fparam)

    # Converting model into dictionary
    lipidContainer, system, lipidList = lf.segs2pyDicts(model,
                                                        rFileLipids)

    if __name__ == "__main__":
        pass
    else:
        numClustersDict = {}
        core2TotalLipidsDict = {}
        clust2TotalLipidsDict = {}
        outlier2TotalLipidsDict = {}
        meanCorePerClusterDict = {}
        stdCorePerClusterDict = {}
        meanLipidsPerClusterDict = {}
        stdLipidsPerClusterDict = {}
        silhouette_CoefficentDict = {}
        frameCounter = 0

    for frame in trajectory:

        box = frame.periodicBox()

        # Initializing key Counter
        C = 0
        numClusters = []
        core2TotalLipids = []
        clust2TotalLipids = []
        outlier2TotalLipids = []
        meanCorePerCluster = []
        stdCorePerCluster = []
        meanLipidsPerCluster = []
        stdLipidsPerCluster = []
        silhouette_Coefficent = []

        # Extracting lipids to calculate centroids from the container dict
        for value in lipidContainer.values():

            # Collecting radius cutoff from rFile
            rCut = float(rAvgLipids[C])
            min_samples = int(minSample[C])
            keyCoreLipids = []
            keyClusterLipids = []
            num = len(value)

            Up, Lo = lf.leafletLipidSeparator(value)
            nClustUp, nCoreUp, nBoundUp, nNoiseUp, silhoUp = lf.lsDBSCAN(Up,
                                                                        rCut,
                                                                        min_samples,
                                                                        box,
                                                                        True)
            keyCoreLipids.extend(nCoreUp)
            keyClusterLipids.extend(np.add(nCoreUp, nBoundUp))

            nClustLo, nCoreLo, nBoundLo, nNoiseLo, silhoLo = lf.lsDBSCAN(Lo,
                                                                        rCut,
                                                                        min_samples,
                                                                        box,
                                                                        True)
            keyCoreLipids.extend(nCoreLo)
            keyClusterLipids.extend(np.add(nCoreLo, nBoundLo))

            numClusters.append(nClustUp + nClustLo)

            # Worst Silhouette Coefficent of both
            silhouette_Coefficent.append(min(silhoUp, silhoLo))

            core2TotalLipids.append((np.sum(keyCoreLipids))/num)
            clust2TotalLipids.append((np.sum(keyClusterLipids))/num)
            outlier2TotalLipids.append((nNoiseUp + nNoiseLo)/num)

            meanCorePerCluster.append(np.mean(keyCoreLipids))
            stdCorePerCluster.append(np.std(keyCoreLipids))
            meanLipidsPerCluster.append(np.mean(keyClusterLipids))
            stdLipidsPerCluster.append(np.std(keyClusterLipids))

            # Updating key Counter
            C += 1

        if __name__ == "__main__":
            print("\t".join(map(str, numClusters)),
                "\t".join(map(str, core2TotalLipids)),
                "\t".join(map(str, clust2TotalLipids)),
                "\t".join(map(str, outlier2TotalLipids)),
                "\t".join(map(str, meanCorePerCluster)),
                "\t".join(map(str, stdCorePerCluster)),
                "\t".join(map(str, meanLipidsPerCluster)),
                "\t".join(map(str, stdLipidsPerCluster)),
                "\t".join(map(str, silhouette_Coefficent)))
        else:
            numClustersDict[frameCounter] = numClusters
            core2TotalLipidsDict[frameCounter] = core2TotalLipids
            clust2TotalLipidsDict[frameCounter] = clust2TotalLipids
            outlier2TotalLipidsDict[frameCounter] = outlier2TotalLipids
            meanCorePerClusterDict[frameCounter] = meanCorePerCluster
            stdCorePerClusterDict[frameCounter] = stdCorePerCluster
            meanLipidsPerClusterDict[frameCounter] = meanLipidsPerCluster
            stdLipidsPerClusterDict[frameCounter] = stdLipidsPerCluster
            silhouette_CoefficentDict[frameCounter] = silhouette_Coefficent
            frameCounter += 1

    if __name__ == "__main__":
        pass
    else:
        return(numClustersDict,
            core2TotalLipidsDict,
            clust2TotalLipidsDict,
            outlier2TotalLipidsDict,
            meanCorePerClusterDict,
            stdCorePerClusterDict,
            meanLipidsPerClusterDict,
            stdLipidsPerClusterDict,
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
    header2 = "# Individual Species Contribution :\t " + "\t".join(headerList)
    header3 = "# Cluster-count\tCore to Total Lipids\tCluster lipids to\
            Total Lipids\tOutliers To Total Lipids\tMean Core lipids per cluster\
            \tSTD Core lipids per cluster\t Mean lipids per cluster\t STD lipids \
            per cluster\t Silhouette Coefficent"
    print(header, flush=True)
    print(header2, flush=True)
    print(header3, flush=True)

    dbscanAnalysisSpecies(fmodel=args.model,
                         ftrajectory=args.trajectory,
                         fparam=args.parameter)