from os import stat
from .mario_status import StatusProvider
from .mario_status import ACTION
import copy


class WorldEngine:

    def simulate(action):
        mario_status = copy.deepcopy(StatusProvider.mario_status())
        print('simuation1: ', WorldEngine._mario_step(
            mario_status, ACTION.parse_action(action)))
        print('simuation2: ', WorldEngine._mario_step(
            mario_status, ACTION.parse_action(action)))

    def _mario_step(status, action):
        # x-axis step
        if action == ACTION.LEFT or action == ACTION.JUMP_LEFT:
            if not StatusProvider.grid_service().is_blocked(status, [1, 0]):
                status.grid_position()[0] += 1
        if action == ACTION.RIGHT or action == ACTION.JUMP_RIGHT:
            if not StatusProvider.grid_service().is_blocked(status, [-1, 0]):
                status.grid_position()[0] -= 1

        # y-axis step
        if status.on_ground():
            # on ground jump case
            WorldEngine._try_jump(status, action)
        elif status.jump_chance() != 0:
            # case 1: rising phase
            WorldEngine._try_jump(status, action)
        elif status.jump_chance() == 0:
            # case 2: falling phase
            if not StatusProvider.grid_service().is_blocked(status, [0, 1]):
                status.grid_position()[1] += 1

        # status update
        if StatusProvider.grid_service().is_blocked(status, [0, 1]):
            status.mutable_status()['may_jump'] = True
            status.mutable_status()['on_ground'] = True
            status.mutable_status()[
                'jump_chance'] = StatusProvider.mario_status().JUMP_HEIGHT
        else:
            status.mutable_status()['may_jump'] = False
            status.mutable_status()['on_ground'] = False

        return status

    def _try_jump(status, action):
        if action == ACTION.JUMP:
            if not StatusProvider.grid_service().is_blocked(status, [0, -1]):
                status.grid_position()[1] -= 1
                status.mutable_status()['jump_chance'] -= 1
        elif action == ACTION.JUMP_LEFT:
            if not StatusProvider.grid_service().is_blocked(status, [1, -1]):
                status.grid_position()[1] -= 1
                status.mutable_status()['jump_chance'] -= 1
        elif action == ACTION.JUMP_RIGHT:
            if not StatusProvider.grid_service().is_blocked(status, [-1, -1]):
                status.grid_position()[1] -= 1
                status.mutable_status()['jump_chance'] -= 1
        else:
            status.mutable_status()['jump_chance'] = 0

    def _enemy_step(action):
        pass
