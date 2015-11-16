__author__ = 'jfalkson'

import LinRegLearner as lrl
import KNNLearner as knn
import random

# import BagLearner as bl
# learner = bl.BagLearner(learner = knn.KNNLearner, kwargs = {"k":3}, bags = 20, boost = False)
# learner.addEvidence(Xtrain, Ytrain)
# Y = learner.query(Xtest)

# learners = []
# kwargs = {"k":10}
# for i in range(0,bags):
#     learners.append(learner(**kwargs))

"""
A simple wrapper for linear regression.  (c) 2015 Tucker Balch
"""

import numpy as np

class BagLearner(object):

    def __init__(self, learner, kwargs, bags, boost = False):
        self.learner = learner
        self.kwargs  = kwargs
        self.nbags    = bags
        self.boost   = boost

    def addEvidence(self,Xtrain,Ytrain):

        # Need to randomly select the size of the training set
        # of data

        self.Xtrain = Xtrain
        self.Ytrain = Ytrain
        M = self.Xtrain.shape[0]
        # print "x train shape ", self.Xtrain.shape
        # print "y train shape " , self.Ytrain.shape
        # List of arrays of random indices (with replacement)
        idxs = [np.random.random_integers(0, M - 1, size=M) for i in range(self.nbags)]
        #print "idx is " , idxs
        # Lists of arrays of random x and y values
        self.xbags = [self.Xtrain[idxs[k]] for k in range(self.nbags)]

        # print self.xbags

        self.ybags = [self.Ytrain[idxs[j]] for j in range(self.nbags)]

        #print " self.bags shape is " , self.bags.shape



    def query(self,points):
        """
        @summary: Estimate a set of test points given the model we built.
        @param points: should be a numpy array with each row corresponding to a specific query.
        @returns the estimated values according to the saved model.
        """
        learners = []
        bag_res = np.zeros((len(self.xbags),len(points),))
        # print len(self.xbags), " bags and " , len(points) , " points "
        self.points = points
        #get a separate learner for each bag
        for i in range(0,self.nbags):
            learners.append(self.learner(**self.kwargs))


        # print np.asarray(self.xbags[1])
        for j in range(0,len(learners)):
            # For each learner we add x and y training data



            learners[j].addEvidence(self.xbags[j],self.ybags[j])

            # We populate the bagging results with the jth learning querying points
            # print bag_res.shape
            # print bag_res[0]
            # print bag_res[599]
            # print bag_res[j]
            # print learners[j].query(points)

            bag_res[j] = learners[j].query(self.points)

            # print "bag res is " , bag_res[j]

        # print np.mean(bag_res, axis = 0)

        return np.mean(bag_res, axis=0)
        # return (self.model_coefs[:-1] * points).sum(axis = 1) + self.model_coefs[-1]

if __name__=="__main__":
    print "the secret clue is 'zzyzx'"
