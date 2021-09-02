__author__="Sergey Karakovskiy, sergey at idsia fullstop ch"
__date__ ="$May 13, 2009 1:05:14 AM$"

class Experiment(object):

    def __init__(self, env, agent):
        self.env = env
        self.agent = agent
        self.stepid = 0

    def _oneInteraction(self):
        self.stepid += 1
        self.agent.integrateObservation(self.env.getObservation())
#        print "experiment.py self.agent.getAction(): ", self.agent.getAction(), "\n"
        self.env.performAction(self.agent.getAction())
        reward = self.env.getReward()
        self.agent.giveReward(reward)
        return reward
