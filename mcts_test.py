#!/usr/bin/python

from mario_game.mario_game import StatusProvider
from mcts.mario_action import MarioState
from mario_game.grid_service import GridService
import random
import copy

def main():
    StatusProvider.load_from_json()
    StatusProvider.debug_info()

    mario_scene = copy.deepcopy(StatusProvider.mario_scene())

    state = MarioState(StatusProvider.mario_status())
    while state.is_terminal():
        state.step(random.choice(state.action_set()))
        mario_scene.add_path_point(state.status().grid_position())

    GridService.update_grid(mario_scene)
    GridService.show_grid()

if __name__ == "__main__":
    main()
else:
    print("This is module to be run rather than imported.")
