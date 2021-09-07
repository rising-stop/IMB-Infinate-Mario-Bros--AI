
class MarioAgent:
#    class MarioAgent(Agent):
    """ An agent is an entity capable of producing actions, based on previous observations.
        Generally it will also learn from experience. It can interact directly with a Task.
    """

    def __init__(self, agentname='MarioAgent'):
        self._name = agentname

    def integrateObservation(self, obs):
        raise "Not implemented"

    def getAction(self):
        raise "Not implemented"

    def giveReward(self, reward):
        pass
    def getName(self):
        if self._name is None:
            self._name = self.__class__.__name__
        return self._name

    def setName(self, newname):
        """Change name to newname. Uniqueness is not guaranteed anymore."""
        self._name = newname

    _name = None

    def __repr__(self):
        """ The default representation of a named object is its name. """
        return "<%s '%s'>" % (self.__class__.__name__, self.name)
    def newEpisode(self):
        pass


