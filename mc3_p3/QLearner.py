"""
Template for implementing QLearner  (c) 2015 Tucker Balch
"""

import numpy as np
import random as rand

class QLearner(object):

    def __init__(self, \
        num_states=100, \
        num_actions = 4, \
        alpha = 0.2, \
        gamma = 0.9, \
        rar = 0.5, \
        radr = 0.99, \
        dyna = 0, \
        verbose = False):

        self.verbose = verbose
        self.num_actions = num_actions
        self.s = 0
        self.alpha=alpha
        self.a = 0
        self.rar=rar
        self.gamma = gamma
        self.radr = radr
        self.num_states = num_states
        self.Q = np.random.uniform(low=-1.0,high=1.0,size=(num_actions,num_states))
        # elf.Q = np.random.random([self.num_actions,self.num_states])

    def querysetstate(self, s):
        """
        @summary: Update the state without updating the Q-table
        @param s: The new state
        @returns: The selected action
        """



        if np.random.uniform(0,1) < self.rar:
            action = rand.randint(0, self.num_actions-1)
        else:
            action = self.Q[:, s].argmax()

        self.s = s

        if self.verbose: print "s =", s,"a =",action




        return action

    def query(self,s_prime,r):
        """
        @summary: Update the Q table and return an action
        @param s_prime: The new state
        @param r: The ne state
        @returns: The selected action
        """

        # action = self.querysetstate(s_prime)


        # if np.random.uniform(0,1) < self.rar:
        #     action = rand.randint(0, self.num_actions-1)
        # else:
        #     action = self.Q[:, self.s].argmax()


        if self.verbose: print "s =", s_prime,"a =",action,"r =",r

        # tmp = []
        # for i in range(0,self.num_actions):
        #     tmp.append(self.Q[i,s_prime])
        #
        # max_action = tmp.index(max(tmp))

        # print "LOOK ",  self.Q[max_action, s_prime]

        action = self.Q[:, s_prime].argmax()

        self.Q[self.a,self.s] = (1-self.alpha)*self.Q[self.a,self.s]  \
                + self.alpha * (r + self.gamma*self.Q[action,s_prime])


        self.rar = self.radr*self.rar
        self.a = action
        self.s = s_prime

        return action

if __name__=="__main__":
    print "Remember Q from Star Trek? Well, this isn't him"
