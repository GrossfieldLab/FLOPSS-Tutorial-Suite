#!/usr/bin/env python3
'''
Example:
    python3 DBSCANanalysis.py --model 1DIPC.psf
                              --traj fixed_1DIPC_100.dcd
                              --lipid_list lipidListNoCHOL.dat
'''

# Importing functional modules
import loos
import loos.pyloos
import sys
import argparse
import math
import numpy as np
import miscFuncs.loosFuncs as lf
from hmmlearn import hmm
'''
pip install --user git+https://github.com/hmmlearn/hmmlearn
'''

def findBestNstateModel(obs, maxN, random_states=10):
    '''
    Gives the best N state model that can fit input data(obs). The function only
    checks upto maxN(int) states. The fucntion also returns a bool to denote the 
    convergence of the model
    '''

    scores = []
    models = []
    for n_components in range(1, (maxN+1)):
        for idx in range(random_states):  # N different random starting states
            # define our hidden Markov model
            model = hmm.GaussianHMM(n_components=n_components, random_state=idx)
            model.fit(obs)
            models.append(model)
            scores.append(model.score(obs))

    # get the best model
    model = models[np.argmax(scores)]

    # Return the best N states and bool for model convergence
    # Example : If hmm shows 3 component model is best and if the model converged
    # the function returns (3, True)
    return (model.n_components, model.monitor_.converged)

def hmmNstateFit(obs, n_component):
    '''
    Returns hidden state series for the given data(obs) based on n_component model
    '''

    # Define the HMM model with n states
    model = hmm.GaussianHMM(n_components=n_component)

    # Train the model
    model.fit(obs)

    # Predict the most likely sequence of hidden states
    hidden_states = model.predict(obs)

    # Most likely sequence of hidden states
    return (hidden_states)

def diffBtwNstates(obs, n_component):
    '''
    Returns the difference between extreme hidden states
    in the input data by fitting the data into a 
    n_component hmm model

    '''
    states = hmmNstateFit(obs, n_component)
    stateMeanValue = np.zeros((n_component))
    for component in range(n_component):
        stateArray = np.argwhere(states==component)
        stateMeanValue[component] = np.mean(obs[stateArray])

    maxStateValue = np.amax(stateMeanValue)
    minStateValue = np.amin(stateMeanValue)
    diffStates = np.abs(maxStateValue - minStateValue)
    return (diffStates)


def dbscanAnalysisSpeciesRscan(fmodel, ftrajectory, flipidsList):

    '''
    Returns 2 dictionaries corresponding to (1) difference between
    extreame hidden states for each lipid species (2) Number of states
    fit by HMM model for each lipid species
    '''

    # Parsing the arguments into variables
    model = loos.createSystem(fmodel)
    trajectory = loos.pyloos.Trajectory(ftrajectory, model)

    # Converting model into dictionary
    lipidContainer, system, lipidList = lf.segs2pyDicts(model,
                                                        flipidsList)
    
    # Printing out header for output file
    headerList = []
    for segID in lipidList:
        headerList.append(str(segID))

    hmmStateDiffDict = {}
    statesInModelDict = {}
    totalFrames = len(trajectory)
    totalSpecies = len(lipidList)

    firstFrame = trajectory[0]
    firstBox = firstFrame.periodicBox()
    planeDiagonal = math.sqrt(firstBox[0]**2 + firstBox[1]**2)
    rMax = round(planeDiagonal/2)
    rRange = np.arange(10, rMax, 0.5)

    # TODO: This iteration process is really inefficent. Since we are also
    # looking at parameter pairs that makes no sense - like looking for 60
    # neighbors in 10 A range, etc. Need to benchmark to see, if further
    # code optimization is really necessary since this would be a one-time
    # task. 
    # 
    # One thing we can do is to use lf.areaPerLipid function to
    # find avg area per lipid to see, how many lipids will be there in our
    # search plane and decide on the min_sample based on that. Good first
    # pass would be to use an upper/lower-bound on min_samples. But the problem
    # with this approach is that it will be only applicable to lipids
    #
    # The other way would be to keep a zero counter when DBSCAN hits zero
    # and break if zerocounter hit N number of times. I have implemente a 
    # crude version with the zeroCounter variable. It can also be improved
    # if wanted

    for r in rRange:
        zeroCounter = 0
        for min_samples in range(5, 61, 1):
            if zeroCounter < 5 :

                hmmStatesDiff = np.zeros((totalSpecies))
                statesInModel = np.zeros((totalSpecies))
                clusterLipids2Total= np.zeros((totalFrames, totalSpecies))

                frameCounter = 0

                for frame in trajectory:

                    box = frame.periodicBox()

                    # Initializing key Counter
                    C = 0

                    # Extracting lipids to calculate centroids from the container dict
                    for key, value in lipidContainer.items():

                        # Collecting radius cutoff from rFile
                        keyClusterLipids = []
                        num = len(value)

                        Up, Lo = lf.leafletLipidSeparator(value)

                        # DBSCAN
                        nClustUp, nCoreUp, nBoundUp, nNoiseUp, silhoUp = lf.lsDBSCAN(Up,
                                                                                    r,
                                                                                    min_samples,
                                                                                    box,
                                                                                    True)

                        keyClusterLipids.extend(np.add(nCoreUp, nBoundUp))
                        

                        nClustLo, nCoreLo, nBoundLo, nNoiseLo, silhoLo = lf.lsDBSCAN(Lo,
                                                                                    r,
                                                                                    min_samples,
                                                                                    box,
                                                                                    True)

                        keyClusterLipids.extend(np.add(nCoreLo, nBoundLo))

                        clusterLipids2Total[frameCounter, C] = (np.sum(keyClusterLipids))/num

                        # Updating key Counter
                        C += 1
                    frameCounter += 1


                # HMM
                for C in range(totalSpecies):
                    data = clusterLipids2Total[:, C]
                    bestNstate, convergenceBool = findBestNstateModel(data[:, None], maxN=5)
                    if convergenceBool:
                        hmmStatesDiff[C] = diffBtwNstates(data[:, None], n_component=bestNstate)
                        statesInModel[C] = bestNstate
                    else:
                        hmmStatesDiff[C] = -1
                        statesInModel[C] = np.nan 
                    
                # ZERO COUNTER
                # Feeding zeroCounter when hmmStates fit single state model with 0 differences
                # Right now, the zeroCounter stops min_samples loop as it hit 5 times and go to
                # next r value. This won't fully make this loop efficent but for that we need
                # to take care of each lipid species separately but this is something!
                if not np.any(hmmStatesDiff):
                    zeroCounter += 1  
                # Else zeroCount resets
                else:
                    zeroCounter = 0

                # OUTPUT WRITING
                dictKey = tuple([r, min_samples])
                hmmStateDiffDict[dictKey] = hmmStatesDiff 
                statesInModelDict[dictKey] = statesInModel

                # Waiting for the loop to be over, to write the whole dict
                # would be risky if we are scanning a wide range
                if __name__ == "__main__":
                    print ("\t".join(map(str, dictKey)),
                       "\t".join(map(str, hmmStatesDiff)),
                       "\t".join(map(str, statesInModel)), flush=True)

            else:
                break

    return(hmmStateDiffDict, statesInModelDict)

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
    args = parser.parse_args()

    # Printing out header for output file
    headerList = lf.seg2pyList(args.lipidsList)
    header = "# " + " ".join(sys.argv)
    header2 = "# System consisting of species :\t " + "\t".join(headerList)
    header3 = "# radius cutoff (epsilon)\t\
        min_samples\t\
        state differences for lipid species"
    print(header, flush=True)
    print(header2, flush=True)
    print(header3, flush=True)

    dbscanAnalysisSpeciesRscan(fmodel=args.model,
                               ftrajectory=args.trajectory,
                               flipidsList=args.lipidsList)