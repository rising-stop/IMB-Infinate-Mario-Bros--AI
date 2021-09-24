from os import stat
from .mario_game import StatusProvider
from .mario_game import ACTION
from .grid_service import GridService

from mario_game import mario_game


class WorldEngine:

    def world_set(self, mario_scene):
        GridService.update_grid(mario_scene)

    def mario_step(self, mario_status, action):
        # case 1: on ground:
        if mario_status.on_ground():
            # x-axis step
            mario_status = self.__try_move(mario_status, action)
            # y-axis step
            mario_status = self.__try_jump(mario_status, action)
            if not GridService.is_blocked(mario_status, [0, 1]):
                mario_status.status()['jump_chance'] = 0
        # case 2: not on ground:
        else:
            # x-axis step
            mario_status = self.__try_move(mario_status, action)
            # y-axis step
            if mario_status.jump_chance() != 0:
                # case 1: rising phase
                mario_status = self.__try_jump(mario_status, action)
            elif mario_status.jump_chance() == 0:
                # case 2: falling phase
                if not GridService.is_blocked(mario_status, [0, 1]):
                    mario_status.grid_position()[1] += 1

        # status update
        if GridService.is_blocked(mario_status, [0, 1]):
            mario_status.status()['may_jump'] = True
            mario_status.status()['on_ground'] = True
            mario_status.status()[
                'jump_chance'] = StatusProvider.mario_status().JUMP_HEIGHT
        else:
            mario_status.status()['may_jump'] = False
            mario_status.status()['on_ground'] = False
        return mario_status

    def __try_move(self, mario_status, action):
        if action in (ACTION.LEFT, ACTION.RIGHT, ACTION.JUMP_LEFT, ACTION.JUMP_RIGHT):
            if action == ACTION.LEFT or action == ACTION.JUMP_LEFT:
                if not GridService.is_blocked(mario_status, [1, 0]):
                    mario_status.grid_position()[0] += 1
            if action == ACTION.RIGHT or action == ACTION.JUMP_RIGHT:
                if not GridService.is_blocked(mario_status, [-1, 0]):
                    mario_status.grid_position()[0] -= 1
        return mario_status

    def __try_jump(self, mario_status, action):
        if action in (ACTION.JUMP, ACTION.JUMP_LEFT, ACTION.JUMP_RIGHT):
            if action == ACTION.JUMP:
                if not GridService.is_blocked(mario_status, [0, -1]):
                    mario_status.grid_position()[1] -= 1
            elif action == ACTION.JUMP_LEFT:
                if not GridService.is_blocked(mario_status, [1, -1]):
                    mario_status.grid_position()[1] -= 1
            elif action == ACTION.JUMP_RIGHT:
                if not GridService.is_blocked(mario_status, [-1, -1]):
                    mario_status.grid_position()[1] -= 1
            else:
                pass
            if GridService.is_blocked(mario_status, [-1, 0]):
                mario_status.status()['jump_chance'] = 0
            else:
                mario_status.status()['jump_chance'] = max(
                    mario_status.status()['jump_chance'] - 1, 0)
        return mario_status

    def __enemy_step(action):
        pass


class SimulationProvider:

    __engine = WorldEngine()

    def set_world(mario_scene):
        SimulationProvider.__engine.world_set(mario_scene)

    def step(mario_status, action):
        return SimulationProvider.__engine.mario_step(mario_status, action)
