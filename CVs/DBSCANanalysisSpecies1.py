#!/usr/bin/env python3
'''
Example:
    python3 DBSCANanalysis.py --model 1DIPC.psf
                              --traj fixed_1DIPC_100.dcd
                              --lipid_list lipidListNoCHOL.dat
                              --r rFileNoChol.dat > test4
'''

# Importing functional modules
import loos
import loos.pyloos
import sys
import argparse
import numpy as np
import miscFuncs.loosFuncs as lf


def dbscanAnalysisSpecies(fmodel, ftrajectory, flipidsList, fradius, min_samples=7):

    # Parsing the arguments into variables
    model = loos.createSystem(fmodel)
    trajectory = loos.pyloos.Trajectory(ftrajectory, model)

    # Reading rFile
    rFileLipids, rAvgLipids, rVarLipids = lf.rFileReader(fradius)

    # Converting model into dictionary
    lipidContainer, system, lipidList = lf.segs2pyDicts(model,
                                                        flipidsList)
    # Sanity Check
    if lipidList != rFileLipids:
        sys.exit("Lipids listed in --lipid_list and --r arguments are different.\n\
                The order in which lipids listed in both files must be same too!")

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
        for key, value in lipidContainer.items():

            # Collecting radius cutoff from rFile
            rCut = float(rAvgLipids[C])
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
    parser.add_argument("--lipid_list",
                        dest="lipidsList",
                        help="List of lipids in the system")
    parser.add_argument("--r_file",
                        dest="radius",
                        help="File consisitng of radius of local region")
    args = parser.parse_args()

    # Printing out header for output file
    headerList = lf.seg2pyList(args.lipidsList)
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
                         flipidsList=args.lipidsList,
                         fradius=args.radius)