#!/usr/bin/python

import sys

from experiments.episodicexperiment import EpisodicExperiment
from client.marioenvironment import MarioEnvironment
from agents.forwardagent import ForwardAgent
from agents.forwardrandomagent import ForwardRandomAgent


# from pybrain.... episodic import EpisodicExperiment
# TODO: reset sends: vis, diff=, lt=, ll=, rs=, mariomode, time limit, pw,
# with creatures, without creatures HIGH.
# send creatures.

def main():
    agent = ForwardAgent()
    env = MarioEnvironment(is_debug=False, agentname=agent.getName())
    exp = EpisodicExperiment(env, agent)
    print('Env Ready')
    exp.doEpisodes(1)
    print('mm 2: %d' % env.getReward())

    env.setDifficulty(0)
    exp.doEpisodes(1)
    print('mm 0: %d' % env.getReward())

    env.setDifficulty(4)
    exp.doEpisodes(1)
    print('mm 0: %d' % env.getReward())

    env.setDifficulty(5)
    exp.doEpisodes(1)
    print('mm 0, ld 5: %d' % env.getReward())

    env.setDifficulty(6)
    exp.doEpisodes(1)
    print('mm 1, ld 5: %d' % env.getReward())

    env.setDifficulty(10)
    exp.doEpisodes(1)
    print('mm 2, ld 5: %f' % env.getReward())

    print("finished")

#    clo = CmdLineOptions(sys.argv)
#    task = MarioTask(MarioEnvironment(clo.getHost(), clo.getPort(), clo.getAgent().name))
#    exp = EpisodicExperiment(clo.getAgent(), task)
#    exp.doEpisodes(3)


if __name__ == "__main__":
    main()
else:
    print("This is module to be run rather than imported.")
