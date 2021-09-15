import random
from .mario_action import *
from mario_game.world_engine import *


class Node:

    __childs = []

    def __init__(self, state, action, parent=None):
        self.__visits = 1
        self.__reward = 0.0
        self.__action = action
        self.__parent = parent
        self.__state = state

    def parent(self):
        return self.__parent

    def update(self, reward):
        self.__reward += reward
        self.__visits += 1

    def is_expand(self):
        return len(self.__childs) != 0

    def expand(self):
        if self.is_expand():
            raise 'expand: node is full'

        for action in self.__action().action_set():
            self.__childs.append(
                Node(SimulationProvider.step(self.__state, action), action, self))

    def reward(self):
        return self.__state.reward()

    def evalue(self):
        raise 'Not implement'


class MCTS:

    __max_move = 1000
    __max_search_time = 10

    def __init__(self, root, max_move=1000, max_time=10):
        self.__root = root
        self.__max_move = max_move
        self.__max_search_time = max_time

    def search(self):
        for itr in range(int(self.__max_move)):
            trial_node = self.__tree_policy(self.__root)
            local_reward = self.__default_policy(trial_node.state)
            self.__backup(trial_node, local_reward)
        return self.__best_child()

    def __tree_policy(self, node):
        while node.state.terminal() == False:
            if node.is_fully_expand():
                node.expand()
                node = self.__best_child(node)
                break
            else:
                node = self.__best_child(node)
        return node

    def __default_policy(self, state):
        raise 'Not implement'

    def __backup(self, node, reward):
        while node != None:
            node.update(reward)

    def __best_child(self, node):
        bestscore = 0.0
        bestchildren = []
        for c in node.children:
            score = node.evalue()
            if score == bestscore:
                bestchildren.append(c)
            if score > bestscore:
                bestchildren = [c]
                bestscore = score
        return random.choice(bestchildren)
