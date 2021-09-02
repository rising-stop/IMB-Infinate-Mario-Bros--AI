__author__ = "Sergey Karakovskiy, sergey at idsia fullstop ch"
__date__ = "$May 13, 2009 1:29:41 AM$"

from .tcpenvironment import TCPEnvironment
from utils.dataadaptor import extractObservation


class MarioEnvironment(TCPEnvironment):
    """ An Environment class, wrapping access to the MarioServer, 
    and allowing interactions to a level. """

    # tracking cumulative reward
    _cumReward = 0
    # tracking the number of samples
    _samples = 0
    # reward
    _finished = False
    _reward = 0
    _status = 0

    def getObservation(self):
        obs = extractObservation(TCPEnvironment.getObservation(self))
        if len(obs) == TCPEnvironment._numberOfFitnessValues:
            self._reward = obs[1]
            self._status = obs[0]
            self._finished = True
        return obs

    def performAction(self, action):
        if not self.isFinished():
            TCPEnvironment.performAction(self, action)
            self._addReward()
            self._samples += 1

    def isFinished(self):
        return self._finished

    def reset(self):
        """ reinitialize the environment """
        # Note: if a task needs to be reset at the start, the subclass constructor
        # should take care of that.
        TCPEnvironment.reset(self)
        self._cumReward = 0
        self._samples = 0

    def getTotalReward(self):
        """ the accumulated reward since the start of the episode """
        return self._cumReward

    def getReward(self):
        """ Fitness gained on the level """
        return self._reward

    def getWinStatus(self):
        return self._status

    def _addReward(self):
        """ a filtered mapping towards performAction of the underlying environment. """
        # by default, the cumulative reward is just the sum over the episode
        self._cumReward += self.getReward()
