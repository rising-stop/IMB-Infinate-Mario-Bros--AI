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

previous_action = ACTION.NONE

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
        
        if incomming[0] and incomming[1]:
            jump_chance = self.JUMP_HEIGHT
        elif previous_action.value & KEY_JUMP:
            jump_chance = max(0, self._status['jump_chance'] - 1)
        else:
            jump_chance = 0

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


class StatusProvider(GameStatus):

    __grid_service = GridService()
    __mario_status = MarioStatus(__grid_service)
    __enemy_status = EnemyStatus(__grid_service)

    def update(incomming):
        StatusProvider.grid_service().update(incomming[4])
        StatusProvider.mario_status().update([incomming[0], incomming[1], incomming[2]])
        StatusProvider.enemy_status().update([incomming[2], incomming[3]])

    def mario_status():
        return StatusProvider.__mario_status

    def enemy_status():
        return StatusProvider.__enemy_status

    def grid_service():
        return StatusProvider.__grid_service

    def set_previous_action(action):
        global previous_action
        previous_action = action

    def previous_action():
        global previous_action
        return previous_action

    def debug_info():
        StatusProvider.__grid_service.debug_info()
        StatusProvider.__mario_status.debug_info()
        StatusProvider.__enemy_status.debug_info()
