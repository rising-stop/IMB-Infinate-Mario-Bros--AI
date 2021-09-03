import random


class BaseAction:
    def __init__(self):
        pass

    def dimension(self):
        raise 'Not implement'

    def next_action(self, actions):
        raise self._random_action(actions)

    def _random_action(self, actions):
        unused_action = []
        for action in self._action_set():
            if action in actions:
                continue
            unused_action.append(action)
        return random.choice(unused_action)

    def _action_set(self):
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
        new_action = self._action.next_action(
            [c._action for c in self._childs])
        self._childs.append(Node(new_action, self))


class MCTS:

    _max_move = 1000
    _max_search_time = 10

    def __init__(self, root, max_move=1000, max_time=10):
        self._root = root
        self._max_move = max_move
        self._max_search_time = max_time

    def search(self):
        for itr in range(int(self._max_move)):
            trial_node = self._tree_policy(self._root)
            local_reward = self._default_policy(trial_node.state)
            self._backup(trial_node, local_reward)
        return self._best_child()

    def _tree_policy(self, node):
        while node.state.terminal() == False:
            if len(node.children) == 0:
                return node.expand()
            elif random.uniform(0, 1) < .5:
                node = self._best_child(node)
            else:
                if node.is_fully_expand() == False:
                    return node.expand()
                else:
                    node = self._best_child(node)
        return node

    def _default_policy(self, state):
        while state.is_terminal() == False:
            state = state.random_next_state()
        return state.reward()

    def _backup(self, node, reward):
        while node != None:
            node.update(reward)

    def _expand(self, node):
        raise 'Not implement'

    def _best_child(self, node):
        bestscore = 0.0
        bestchildren = []
        for c in node.children:
            score = self._node_score(c)
            if score == bestscore:
                bestchildren.append(c)
            if score > bestscore:
                bestchildren = [c]
                bestscore = score
        return random.choice(bestchildren)

    def _node_score(self):
        raise 'Not implement'
