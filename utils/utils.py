import time
from mario_game.mario_game import StatusProvider
import networkx as nx
import matplotlib.pyplot as plt
import random

class RandomTime:
    previous_random_time = 0
    duplicate_times = 0

    def random_time_ns():
        rand_time = int(time.time() * 1e6)
        if rand_time == RandomTime.previous_random_time:
            RandomTime.duplicate_times += 1
        else:
            RandomTime.duplicate_times = 0
        RandomTime.previous_random_time = rand_time
        return rand_time


class GlobalCounter:
    __count_num = 0

    def count():
        GlobalCounter.__count_num += 1
        return GlobalCounter.__count_num

def random_ID():
    return '%05d' % GlobalCounter.count()

def no_duplicate_ID():
    return str(RandomTime.random_time_ns()) + '%04d' % RandomTime.duplicate_times