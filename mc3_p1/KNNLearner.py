"""
KNN Learner class
Where "k" is the number of nearest neighbors to find.
Xtrain and Xtest should be ndarrays (numpy objects) where each
row represents an X1, X2, X3... XN set of feature values.
The columns are the features and the rows are the individual
example instances. Y and Ytrain are single dimension ndarrays
that indicate the value we are attempting to predict with X.

Use Euclidean distance. Take the mean of the closest k points'
Y values to make your prediction. If there are multiple
equidistant points on the boundary of being selected
or not selected, you may use whatever method you like
to choose among them.
"""

import numpy as np

class KNNLearner(object):

    def __init__(self,k):
        self.k = k

    def addEvidence(self,Xtrain,Ytrain):
        """
        @summary: Add training data to learner
        @param Xtrain: X values of training data to add
        @param Ytrain: the Y training values
        """
        self.Xtrain = Xtrain
        self.Ytrain = Ytrain

        
    def query(self,Xtest):
        """
        @summary: Estimate a set of test points given the model we built.
        @param points: should be a numpy array with each row corresponding to a specific query.
        @returns the estimated values according to the saved model.
        """
        # Calculate distance between each point in X test vs each point in x train, then
        # take the average of those training values


        # You only need to go through the data once. Start with an empty array of 'k' values
        # and store the first 'k' distances in it. Now, go through your remaining distances.
        # If you find a distance smaller than stored in your array, replace the biggest value in the
        # array with the smaller distance.
        Ytest = np.zeros(len(Xtest))
        for i in range(0,len(Xtest)):
            k_dist = np.zeros(self.k)
            y_vals  = np.zeros (self.k)
            for neighbor_idx in range(0,self.k):
                k_dist[neighbor_idx] =  np.linalg.norm(self.Xtrain[neighbor_idx]-Xtest[i])
                y_vals[neighbor_idx] = self.Ytrain[neighbor_idx]

            # print "K DIST ", k_dist
            for j in range(self.k,len(self.Xtrain)):

                # Begin storing the remaining distances, replacing the biggest current value
                # with the smaller distance
                dist = np.linalg.norm(self.Xtrain[j]-Xtest[i])

                # print "curr k dist is " , zip(k_dist,y_vals)
                # If distance smaller than largest current value, replace
                if dist < np.amax(k_dist):
                    # print " max dist is " ,np.amax(k_dist), " thus replacing with " , dist
                    tmp_max = np.argmax(k_dist)
                    k_dist[tmp_max] = dist
                    y_vals[tmp_max] = self.Ytrain[j]
                    # print "adding y train ", self.Ytrain[j]

                    # print "updated max dist is now ",np.amax(k_dist)
            # Now for this test point we have the k closest training points
            # Next we need to take the average of those points' Y values
            # print "k nearest x val distances are " , k_dist
            # print "associated k y vals are " , y_vals
            Ytest[i] = np.mean(y_vals)
            # print "Adding prediction of ", np.mean(y_vals)
        return Ytest


if __name__=="__main__":
    print "the secret clue is 'zzyzx'"