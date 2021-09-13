
from os import stat
from .tcpenvironment import TCPEnvironment
from utils.dataadaptor import extractObservation
from mcts_mario.mario_status import ACTION, StatusProvider
from mcts_mario.world_engine import WorldEngine

class MarioEnvironment(TCPEnvironment):
    """ An Environment class, wrapping access to the MarioServer, 
    and allowing interactions to a level. """

    _is_debug = False

    # tracking cumulative reward
    _cumReward = 0
    # tracking the number of samples
    _samples = 0
    # reward
    _finished = False
    _reward = 0
    _status = 0

    def __init__(self, is_debug=False, agentname='UnnamedClient', **otherargs):
        super(MarioEnvironment, self).__init__(agentname)
        self._is_debug = is_debug

    def getObservation(self):
        ob = extractObservation(TCPEnvironment.getObservation(self))
        if ob is None:
            return None
        if len(ob) == TCPEnvironment._numberOfFitnessValues:
            self._reward = ob[1]
            self._status = ob[0]
            self._finished = True
        if  len(ob) == TCPEnvironment._numberOfObeservationValues:
            StatusProvider.update(ob)
            if self._is_debug:
                StatusProvider.debug_info()
        return ob

    def performAction(self, action):
        if not self.isFinished():
            StatusProvider.set_previous_action(ACTION.parse_action(action))
            TCPEnvironment.performAction(self, action)
            if self._is_debug:
                print('action: ', action)
                WorldEngine.simulate(action)
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
        self._finished = False
        self._reward = 0
        self._status = 0

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