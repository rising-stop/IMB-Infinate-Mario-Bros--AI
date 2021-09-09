from numpy.core.getlimits import iinfo
from .grid_service import GridService
from .grid_service import EnemyType
from .grid_service import SceneType
import math
from enum import Enum


KEY_LEFT = 1 << 0
KEY_RIGHT = 1 << 1
KEY_DOWN = 1 << 2
KEY_JUMP = 1 << 3
KEY_SPEED = 1 << 4


class ACTION(Enum):
    NONE = 0
    LEFT = KEY_LEFT
    RIGHT = KEY_RIGHT
    JUMP = KEY_JUMP
    JUMP_LEFT = KEY_JUMP + KEY_LEFT
    JUMP_RIGHT = KEY_JUMP + KEY_RIGHT

    def parse_action(action):
        sum = 0
        for i in range(5):
            if action[i] == 1:
                sum += 1 << i
        return ACTION(sum)

class GameStatus(object):
    def update(self, incomming):
        raise 'Not implement'


class MarioStatus(GameStatus):

    JUMP_HEIGHT = 3

    _status = {
        'may_jump': True,
        'on_ground': True,
        'jump_chance': JUMP_HEIGHT,
        'pos': [0.0, 0.0],
        'speed': [0.0, 0.0],
        'grid': [0, 0]
    }

    def __init__(self, grid):
        self._grid_service = grid

    def update(self, incomming):
        jump_chance = self._status['jump_chance']
        if incomming[0] and incomming[1]:
            jump_chance = self.JUMP_HEIGHT

        self._status = {
            'may_jump': incomming[0],
            'on_ground': incomming[1],
            'jump_chance': jump_chance,
            'grid': [self._grid_service.MARIO_X_POSITION,
                     self._grid_service.MARIO_Y_POSITION]
        }

    def mutable_status(self):
        return self._status

    def may_jump(self):
        return self._status['may_jump']

    def on_ground(self):
        return self._status['on_ground']

    def grid_position(self):
        return self._status['grid']

    def jump_chance(self):
        return self._status['jump_chance']

    def __repr__(self):
        return self._status.__repr__()

    def debug_info(self):
        print('\n####### Mario Status #######')
        print('status ', self._status)

class EnemyStatus(GameStatus):

    def __init__(self, grid):
        self._grid_service = grid

    # single_enemy = {'type': EnemyType(),
    #                 'x': float(),
    #                 'y': float(),
    #                 'grid_x': int(),
    #                 'grid_y': int()
    #                 }

    _enemy_list = []

    def update(self, incomming):
        self._enemy_list.clear()
        enemy_data_len = len(incomming[1])
        if enemy_data_len % 3 != 0:
            raise 'enemy data error'
        for index in range(0, enemy_data_len, 3):
            grid = self._grid_service.grid_match(
                incomming[0], [incomming[1][index + 1], incomming[1][index + 2]])
            self._enemy_list.append({
                'type': EnemyType(incomming[1][index]),
                'floats': [float(incomming[1][index + 1]),
                           float(incomming[1][index + 2])],
                'grid': grid
            })

    def debug_info(self):
        print('\n####### Enemy Status #######')
        print('enemy info', self._enemy_list)


grid_service = GridService()
mario_status = MarioStatus(grid_service)
enemy_status = EnemyStatus(grid_service)


class StatusProvider(GameStatus):

    def update(incomming):
        grid_service.update(incomming[4])
        mario_status.update([incomming[0], incomming[1], incomming[2]])
        enemy_status.update([incomming[2], incomming[3]])

    def mario_status():
        return mario_status

    def enemy_status():
        return enemy_status

    def grid_service():
        return grid_service

    def debug_info():
        mario_status.debug_info()
        enemy_status.debug_info()
