from enum import Enum

SCENE_SIZE = 22


class SceneType(Enum):
    KIND_NONE = 0
    KIND_BRICK = 16
    KIND_QUESTION_BRICK = 21
    KIND_UNPASSABLE = -99


class EnemyType(Enum):
    KIND_GOOMBA = 2
    KIND_GOOMBA_WINGED = 3
    KIND_RED_KOOPA = 4
    KIND_RED_KOOPA_WINGED = 5
    KIND_GREEN_KOOPA = 6
    KIND_GREEN_KOOPA_WINGED = 7
    KIND_BULLET_BILL = 8
    KIND_SPIKY = 9
    KIND_SPIKY_WINGED = 10
    KIND_ENEMY_FLOWER = 12
    KIND_SHELL = 13
    KIND_MUSHROOM = 14
    KIND_FIRE_FLOWER = 15
    KIND_PARTICLE = 21
    KIND_SPARCLE = 22
    KIND_COIN_ANIM = 20
    KIND_FIREBALL = 25


class GridService():

    MARIO_X_POSITION = 11
    MARIO_Y_POSITION = 11
    GRID_SIZE = 16

    _local_scene = [[SceneType.KIND_NONE for _ in range(
        SCENE_SIZE)] for _ in range(SCENE_SIZE)]

    def update(self, incomming):
        for row in range(SCENE_SIZE):
            for col in range(SCENE_SIZE):
                if incomming[row][col] in SceneType._value2member_map_:
                    self._local_scene[row][col] = SceneType(
                        incomming[row][col])
                elif incomming[row][col] < 0:
                    self._local_scene[row][col] = SceneType.KIND_UNPASSABLE

    def grid_match(self, mariofloats, enemyfloats):
        return [self.MARIO_X_POSITION + round((enemyfloats[0] - mariofloats[0])/self.GRID_SIZE),
                self.MARIO_Y_POSITION + round((enemyfloats[1] - mariofloats[1])/self.GRID_SIZE)]

    def is_blocked(self, status, grid_action):
        return self._local_scene[status.grid_position()[0] +
                                 grid_action[0]][status.grid_position()[1] +
                                                 grid_action[1]] != SceneType.KIND_NONE
