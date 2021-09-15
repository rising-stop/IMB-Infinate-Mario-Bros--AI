from numpy.core.getlimits import iinfo
from .grid_service import GridService
from .grid_service import EnemyType
from .grid_service import MarioScene
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

    __status = {
        'may_jump': True,
        'on_ground': True,
        'jump_chance': JUMP_HEIGHT,
        'pos': [0.0, 0.0],
        'speed': [0.0, 0.0],
        'grid': [0, 0]
    }

    def update(self, incomming, jump_chance):
        self.__status = {
            'may_jump': incomming[0],
            'on_ground': incomming[1],
            'jump_chance': jump_chance,
            'grid': [GridService.MARIO_X_POSITION,
                     GridService.MARIO_Y_POSITION]
        }

    def status(self):
        return self.__status

    def may_jump(self):
        return self.__status['may_jump']

    def on_ground(self):
        return self.__status['on_ground']

    def grid_position(self):
        return self.__status['grid']

    def jump_chance(self):
        return self.__status['jump_chance']

    def __repr__(self):
        return self.__status.__repr__()

    def debug_info(self):
        print('\n####### Mario Status #######')
        print('status ', self.__status)


class EnemyStatus(GameStatus):

    # single_enemy = {'type': EnemyType(),
    #                 'x': float(),
    #                 'y': float(),
    #                 'grid_x': int(),
    #                 'grid_y': int()
    #                 }

    _enemy_list = []

    def update(self, incomming, grid_service):
        self._enemy_list.clear()
        enemy_data_len = len(incomming[1])
        if enemy_data_len % 3 != 0:
            raise 'enemy data error'
        for index in range(0, enemy_data_len, 3):
            grid = grid_service.grid_match(
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

    __mario_scene = MarioScene()
    __grid_service = GridService()
    __mario_status = MarioStatus()
    __enemy_status = EnemyStatus()

    def update(incomming):
        StatusProvider.__mario_scene.parse_grid_map(incomming[4])
        StatusProvider.__grid_service.update_grid(StatusProvider.__mario_scene)
        StatusProvider.__mario_status.update(
            [incomming[0], incomming[1]], StatusProvider.provide_mario_jump_chance(incomming))
        StatusProvider.__enemy_status.update(
            [incomming[2], incomming[3]], StatusProvider.__grid_service)

    def mario_status():
        return StatusProvider.__mario_status

    def enemy_status():
        return StatusProvider.__enemy_status

    def mario_scene():
        return StatusProvider.__mario_scene

    def grid_service():
        return StatusProvider.__grid_service

    def debug_info():
        StatusProvider.__grid_service.show_grid()
        StatusProvider.__mario_status.debug_info()
        StatusProvider.__enemy_status.debug_info()

    __previous_action = ACTION.NONE

    def update_command(action):
        StatusProvider.__previous_action = action

    def provide_mario_jump_chance(incomming):
        jump_chance = 0
        if incomming[0] and incomming[1]:
            jump_chance = MarioStatus.JUMP_HEIGHT
        elif StatusProvider.__previous_action.value & KEY_JUMP:
            jump_chance = max(
                0, StatusProvider.__mario_status.__status['jump_chance'] - 1)

        return jump_chance
