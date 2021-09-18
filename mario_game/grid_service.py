from enum import Enum
from utils.tree_drawer import TreeDrawer

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
    __path = []

    def __getitem__(self, index):
        return self.__local_scene[index]

    def __setitem__(self, index, value):
        self.__local_scene[index] = value

    def clear_path(self):
        self.__path.clear()

    def add_path_point(self, point):
        self.__path.append((point[0], point[1]))

    def path(self):
        return self.__path

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

    __grid = MarioScene()
    __saver_level = []

    MARIO_X_POSITION = 10
    MARIO_Y_POSITION = 10
    GRID_SIZE = 16

    def update_grid(grid):
        GridService.__grid = grid
        GridService.cal_saver_level()

    def cal_saver_level():
        for x in range(SCENE_SIZE):
            is_meet_ground = False
            for reverse_y in range(SCENE_SIZE):
                y = SCENE_SIZE - reverse_y - 1
                if (not is_meet_ground) and \
                        GridService.__grid[x][y] == SceneType.KIND_UNPASSABLE:
                    is_meet_ground = True
                if is_meet_ground and \
                        GridService.__grid[x][y] != SceneType.KIND_UNPASSABLE:
                    GridService.__saver_level.append(y + 1)
                    break
            if len(GridService.__saver_level) != x + 1:
                GridService.__saver_level.append(SCENE_SIZE - 1)

    def grid_match(mariofloats, enemyfloats):
        return [GridService.MARIO_X_POSITION + round((enemyfloats[0] - mariofloats[0])/GridService.GRID_SIZE),
                GridService.MARIO_Y_POSITION + round((enemyfloats[1] - mariofloats[1])/GridService.GRID_SIZE)]

    def is_blocked(status, grid_action):
        if (status.grid_position()[0] + grid_action[0]) >= SCENE_SIZE or \
            (status.grid_position()[0] + grid_action[0]) < 0 or \
            (status.grid_position()[1] + grid_action[1]) >= SCENE_SIZE or \
                (status.grid_position()[1] + grid_action[1]) < 0:
            return True
        return GridService.__grid[status.grid_position()[0] +
                                  grid_action[0]][status.grid_position()[1] +
                                                  grid_action[1]] != SceneType.KIND_NONE

    def is_falling_dead(status):
        if status.on_ground() or status.jump_chance() != 0:
            return False
        pos = status.grid_position()
        for future_x in range(pos[0], SCENE_SIZE):
            if pos[1] >= GridService.__saver_level[pos[0]]:
                return True
            pos[0] = future_x
            pos[1] += 1
            if pos[1] >= SCENE_SIZE:
                break
        return False

    def show_grid():
        ret = ""
        for y in range(SCENE_SIZE):
            tmpData = ""
            for x in range(SCENE_SIZE):
                if x == GridService.MARIO_X_POSITION and y == GridService.MARIO_Y_POSITION:
                    tmpData += GridService.__mapElToStr(1)
                elif (x, y) in GridService.__grid.path():
                    tmpData += GridService.__mapElToStr('****')
                else:
                    tmpData += GridService.__mapElToStr(
                        GridService.__grid[x][y].value)
            ret += "\n%s" % tmpData
        print(ret)

    def __mapElToStr(el):
        """maps element of levelScene to str representation"""
        s = ""
        if (el == 0):
            s = "##"
        s += "#MM#" if (el == 95) else str(el)
        while (len(s) < 4):
            s += "#"
        return s + " "

    def dump_to_array():
        out_array = []
        for x in range(SCENE_SIZE):
            for y in range(SCENE_SIZE):
                out_array.append(GridService.__grid[x][y].value)
        return out_array

    def load_from_array(in_array):
        index = 0
        for x in range(SCENE_SIZE):
            for y in range(SCENE_SIZE):
                GridService.__grid[x][y] = SceneType(int(in_array[index]))
                index += 1
