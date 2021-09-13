import random


class BaseAction:
    def __init__(self):
        pass

    def dimension(self):
        raise 'Not implement'

    def action_set(self):
        raise 'Not implement'


class BaseState:
    def is_terminal(self):
        raise 'Not implement'

    def reward(self):
        raise 'Not implement'

    def next_state(self, action):
        raise 'Not implement'


class Node:

    _childs = []

    def __init__(self, state, action, parent=None):
        self._visits = 1
        self._reward = 0.0
        self._action = action
        self._parent = parent
        self._state = state.next_state(action)

    def parent(self):
        return self._parent

    def update(self, reward):
        self._reward += reward
        self._visits += 1

    def is_fully_expand(self):
        return len(self._childs == self._action.dimension())

    def expand(self):
        if self.is_fully_expand():
            raise 'expand: node is full'

        for action in self._action().action_set():
            self._childs.append(Node(action, self))

    def reward(self):
        return self._state.reward

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
            if len(node.children) == 0:
                node.expand()
                node = self.__best_child(node)
                break
            else:
                node = self.__best_child(node)
        return node

    def __default_policy(self, state):
        while state.is_terminal() == False:
            state = state.random_next_state()
        return state.reward()

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

