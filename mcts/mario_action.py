from mario_game.world_engine import WorldEngine
from mario_game.mario_game import *
from mario_game.grid_service import GridService
import numpy


ground_action_set = (ACTION.LEFT, ACTION.RIGHT, ACTION.JUMP,
                     ACTION.JUMP_LEFT, ACTION.JUMP_RIGHT)

air_action_set = (ACTION.LEFT, ACTION.RIGHT)

class MarioAction:

    __action = ACTION.NONE
    __can_jump = False

    def __init__(self, action, jump_chance=0):
        super().__init__()
        self.__action = action._action
        self.__can_jump = jump_chance != 0

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


class MarioState:

    __engine = WorldEngine()

    def __init__(self, status=MarioStatus()):
        super().__init__()
        self.__mario_status = status

    def status(self):
        return self.__mario_status

    def set_status(self, status):
        self.__mario_status = status

    def is_terminal(self):
        if GridService.is_falling_dead(self.__mario_status) or \
                self.__mario_status.grid_position()[0] == 21:
            return False
        return True

    def reward(self):
        if self.__mario_status.grid_position()[0] == 21:
            return 1.0
        return float(self.__mario_status.grid_position()[0]) / 22.0

    def reset_map(self, scene):
        MarioState.__engine.world_set(scene)

    def step(self, mario_action):
        MarioState.__engine.mario_step(self.__mario_status, mario_action)

    def action_set(self):
        if self.__mario_status.jump_chance() != 0:
            return ground_action_set
        return air_action_set

    def __repr__(self) -> str:
        return self.__mario_status.__repr__()
