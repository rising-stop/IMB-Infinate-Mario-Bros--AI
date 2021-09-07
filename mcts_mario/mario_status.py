from .grid_service import GridService
from .grid_service import EnemyType
from .grid_service import SceneType

class GameStatus(object):
    def update(self, incomming):
        raise 'Not implement'

class MarioStatus(GameStatus):

    _may_jump = False
    _on_ground = False
    _abs_position = [0.0, 0.0]

    def may_jump(self):
        return self._may_jump

    def on_ground(self):
        return self._on_ground

    def update(self, incomming):
        pass


class EnemyStatus(GameStatus):

    def __init__(self, grid):
        self._grid_service = grid

    # single_enemy = {'type': EnemyType(),
    #                 'x': float(),
    #                 'y': float(),
    #                 'grid_x': int(),
    #                 'grid_y': int()
    #                 'dir_distance': float(),
    #                 }

    _enemy_list = []

    def _single_cmp(self, lhs, rhs):
        if lhs['dir_distance'] < rhs['dir_distance']:
            return 1
        elif lhs['dir_distance'] > rhs['dir_distance']:
            return -1
        return 0

    def update(self, incomming):
        self._enemy_list.clear()
        for enemyfloat in incomming:
            grid = self._grid_service.grid_match(enemyfloat)
            self._enemy_list.append({
                'type': EnemyType(enemyfloat[0]),
                'x': float(enemyfloat[1]),
                'y': float(enemyfloat[2]),
                'grid_x': grid[0],
                'grid_y': grid[1],
                'dir_distance': self._grid_service.dir_distance(grid)
            })
        sorted(self._enemy_list, self._single_cmp)


class StatusProvider(GameStatus):

    def update(self, incomming):
        pass
