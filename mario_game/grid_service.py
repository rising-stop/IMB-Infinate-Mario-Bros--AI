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


class MarioScene():

    __local_scene = [[SceneType.KIND_NONE for _ in range(
        SCENE_SIZE)] for _ in range(SCENE_SIZE)]

    def __getitem__(self, index):
        return self.__local_scene[index]

    def __setitem__(self, index, value):
        self.__local_scene[index] = value

    def parse_grid_map(self, incomming):
        close_row = 0
        is_empty_col = True
        for row in range(SCENE_SIZE):
            for col in range(SCENE_SIZE):
                if incomming[col][row] in SceneType._value2member_map_:
                    self.__local_scene[row][col] = SceneType(
                        incomming[col][row])
                elif incomming[col][row] < 0:
                    is_empty_col = False
                    self.__local_scene[row][col] = SceneType.KIND_UNPASSABLE
            if is_empty_col:
                close_row += 1
        self.__shrink_active_area(close_row)

    def __shrink_active_area(self, close_row):
        for row in range(close_row):
            for col in range(SCENE_SIZE):
                self.__local_scene[row][col] = SceneType.KIND_UNPASSABLE


class GridService():

    def __init__(self, grid = None):
        self.__grid = grid

    MARIO_X_POSITION = 10
    MARIO_Y_POSITION = 10
    GRID_SIZE = 16

    def update_grid(self, grid):
        self.__grid = grid

    def grid_match(self, mariofloats, enemyfloats):
        return [self.MARIO_X_POSITION + round((enemyfloats[0] - mariofloats[0])/self.GRID_SIZE),
                self.MARIO_Y_POSITION + round((enemyfloats[1] - mariofloats[1])/self.GRID_SIZE)]

    def is_blocked(self, status, grid_action):
        return self.__grid[status.grid_position()[0] +
                           grid_action[0]][status.grid_position()[1] +
                                           grid_action[1]] != SceneType.KIND_NONE

    def is_falling_dead(self, status):
        pass

    def show_grid(self):
        ret = ""
        for y in range(22):
            tmpData = ""
            for x in range(22):
                if x == self.MARIO_X_POSITION and y == self.MARIO_Y_POSITION:
                    tmpData += self.__mapElToStr(1)
                else:
                    tmpData += self.__mapElToStr(self.__grid[x][y].value)
            ret += "\n%s" % tmpData
        print(ret)

    def __mapElToStr(self, el):
        """maps element of levelScene to str representation"""
        s = ""
        if (el == 0):
            s = "##"
        s += "#MM#" if (el == 95) else str(el)
        while (len(s) < 4):
            s += "#"
        return s + " "
