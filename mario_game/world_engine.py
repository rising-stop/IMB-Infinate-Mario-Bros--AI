from os import stat
from .mario_game import MarioStatus, StatusProvider
from .mario_game import ACTION
from .grid_service import GridService
import copy

from mario_game import mario_game


class WorldEngine:

    __grid_service = GridService()

    def world_set(self, mario_scene):
        self.__grid_service.update_grid(mario_scene)

    def simulate(self, mario_status, action):
        mario_status = self.mario_step(
            mario_status, ACTION.parse_action(action))
        print('simuation1: ', mario_status)
        mario_status = self.mario_step(
            mario_status, ACTION.parse_action(action))
        print('simuation2: ', mario_status)

    def mario_step(self, mario_status, action):
        # x-axis step
        if action == ACTION.LEFT or action == ACTION.JUMP_LEFT:
            if self.__grid_service.is_blocked(mario_status, [1, 0]):
                mario_status.grid_position()[0] += 1
        if action == ACTION.RIGHT or action == ACTION.JUMP_RIGHT:
            if not self.__grid_service.is_blocked(mario_status, [-1, 0]):
                mario_status.grid_position()[0] -= 1

        # y-axis step
        if mario_status.on_ground():
            # on ground jump case
            mario_status = self.__try_jump(mario_status, action)
        elif mario_status.jump_chance() != 0:
            # case 1: rising phase
            mario_status = self.__try_jump(mario_status, action)
        elif mario_status.jump_chance() == 0:
            # case 2: falling phase
            if not self.__grid_service.is_blocked(mario_status, [0, 1]):
                mario_status.grid_position()[1] += 1

        # status update
        if self.__grid_service.is_blocked(mario_status, [0, 1]):
            mario_status.status()['may_jump'] = True
            mario_status.status()['on_ground'] = True
            mario_status.status()[
                'jump_chance'] = StatusProvider.mario_status().JUMP_HEIGHT
        else:
            mario_status.status()['may_jump'] = False
            mario_status.status()['on_ground'] = False
        return mario_status

    def __try_jump(self, mario_status, action):
        if action == ACTION.JUMP:
            if not self.__grid_service.is_blocked(mario_status, [0, -1]):
                mario_status.grid_position()[1] -= 1
                mario_status.status()['jump_chance'] -= 1
        elif action == ACTION.JUMP_LEFT:
            if not self.__grid_service.is_blocked(mario_status, [1, -1]):
                mario_status.grid_position()[1] -= 1
                mario_status.status()['jump_chance'] -= 1
        elif action == ACTION.JUMP_RIGHT:
            if not self.__grid_service.is_blocked(mario_status, [-1, -1]):
                mario_status.grid_position()[1] -= 1
                mario_status.status()['jump_chance'] -= 1
        else:
            mario_status.status()['jump_chance'] = 0
        return mario_status

    def __enemy_step(action):
        pass


class SimulationProvider:

    __engine = WorldEngine()

    def set_world(mario_scene):
        SimulationProvider.__engine.world_set(mario_scene)

    def step(mario_status, action):
        return SimulationProvider.__engine.mario_step(mario_status, action)
