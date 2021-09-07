import numpy
from .marioagent import MarioAgent


class MCTSAgent(MarioAgent):
    def __init__(self, agentname):
        super().__init__(agentname=agentname)

    def integrateObservation(self, local_view):
        raise "Not implemented"

    def getAction(self):
        raise "Not implemented"

    def giveReward(self, reward):
        pass

    def __repr__(self):
        """ The default representation of a named object is its name. """
        return "<%s '%s'>" % (self.__class__.__name__, self.name)

    def newEpisode(self):
        pass
