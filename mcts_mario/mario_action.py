from mcts.mcts import BaseAction
from .mario_status import StatusProvider
from .mario_status import ACTION
import numpy


ground_action_set = (ACTION.LEFT, ACTION.RIGHT, ACTION.JUMP,
                     ACTION.JUMP_LEFT, ACTION.JUMP_RIGHT)

air_action_set = (ACTION.LEFT, ACTION.RIGHT,
                  ACTION.JUMP_LEFT, ACTION.JUMP_RIGHT)


class MarioAction(BaseAction):

    _action = 0
    _on_ground = False

    def __init__(self, action):
        super().__init__()
        self._action = action._action
        self._on_ground = StatusProvider.mario_status().on_ground()

    def dimension(self):
        if self._on_ground:
            return len(ground_action_set)
        return len(air_action_set)

    def action_set(self):
        if self._on_ground:
            return ground_action_set
        return air_action_set

    def __eq__(self, ins):
        return self._action == ins._action and self._on_ground == ins._on_ground

    def encode(self):
        command = numpy.zeros(5, int)
        for i in range(5):
            if self._action & 1 << i:
                command[i] = 1
        return command

    def decode(self, tele_action):
        if len(tele_action) < 5:
            raise 'protocal error'
        for i in range(5):
            if tele_action[i] == 1:
                self._action += 1 << i
