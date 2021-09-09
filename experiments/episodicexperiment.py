from pynput.keyboard import Key, Listener
import time
from .experiment import Experiment

class EpisodicExperiment(Experiment):
    """ The extension of Experiment to handle episodic tasks. """

    _paused = False

    def __init__(self, env, agent):
        super().__init__(env, agent)
        self._key_listener = Listener(on_press = self._key_pause)
        self._key_listener.start()

    def __del__(self):
        self._key_listener.stop()

    def doEpisodes(self, number=1):
        """ returns the rewards of each step as a list """
        all_rewards = []
        for dummy in range(number):
            rewards = []
            # the agent is informed of the start of the episode
            self.agent.newEpisode()
            self.env.reset()
            while not self.env.isFinished():
                if self._paused:
                    time.sleep(0.1)
                else:
                    r = self._oneInteraction()
                    rewards.append(r)
            all_rewards.append(rewards)
        return all_rewards

    def _key_pause(self, key):
        if key == Key.space:
            self._paused = ~self._paused
        # if self._paused:
        #     self.env.pause_game()
        # else:
        #     self.env.resume_game()

# class EpisodicExperiment(Experiment):
#    """
#    Documentation
#    """
#
#    statusStr = ("Loss...", "Win!")
#    agent = None
#    task = None
#
#    def __init__(self, agent, task):
#        """Documentation"""
#        self.agent = agent
#        self.task = task
#
#    def doEpisodes(self, amount):
#        for i in range(amount):
#            self.agent.newEpisode()
#            self.task.startNew()
#            while not self.task.isFinished():
#                obs = self.task.getObservation()
#                if len(obs) == 3:
#                    self.agent.integrateObservation(obs)
#                    self.task.performAction(self.agent.produceAction())
#
#            r = self.task.getReward()
#            s = self.task.getStatus()
#            print "Episode #%d finished with status %s, fitness %f..." % (i, self.statusStr[s], r)
#            self.agent.giveReward(r)
