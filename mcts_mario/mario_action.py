from mcts.mcts import BaseAction
from .mario_status import StatusProvider
from .mario_status import ACTION
import numpy


ground_action_set = (ACTION.LEFT, ACTION.RIGHT, ACTION.JUMP,
                     ACTION.JUMP_LEFT, ACTION.JUMP_RIGHT)

air_action_set = (ACTION.LEFT, ACTION.RIGHT)


class MarioAction(BaseAction):

    __action = ACTION.NONE
    __can_jump = False

    def __init__(self, action):
        super().__init__()
        self.__action = action._action
        self.__can_jump = StatusProvider.mario_status().jump_chance() != 0

    def dimension(self):
        if self.__can_jump:
            return len(ground_action_set)
        return len(air_action_set)

    def action_set(self):
        if self.__can_jump:
            return ground_action_set
        return air_action_set

    def __eq__(self, ins):
        return self.__action == ins.__action and self.__can_jump == ins.__can_jump

    def encode(self):
        command = numpy.zeros(5, int)
        for i in range(5):
            if self.__action & 1 << i:
                command[i] = 1
        return command

    def decode(self, tele_action):
        if len(tele_action) < 5:
            raise 'protocal error'
        for i in range(5):
            if tele_action[i] == 1:
                self.__action += 1 << i
