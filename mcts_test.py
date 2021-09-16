#!/usr/bin/python

from mario_game.mario_game import StatusProvider
import networkx as nx
import matplotlib.pyplot as plt
import random


class tree_node:
    node_size = 1
    default_interval = 1

    def __init__(self, id):
        self.id = id
        self.child = []
        self.node_interval = []
        self.total_width = tree_node.node_size

    def dump(self, indent=0):
        info = '    ' * indent + ' |- ' if indent > 0 else '    '
        print('%s%s' % (info, self.id))
        for node in self.child:
            node.dump(indent + 1)


def generate_tree():
    id = 0
    root = tree_node(id)
    for _ in range(3):
        id += 1
        root.child.append(tree_node(id))
    node1 = root.child[0]
    for _ in range(2):
        id += 1
        node1.child.append(tree_node(id))
    id += 1
    root.child[1].child.append(tree_node(id))
    node2 = root.child[2]
    for _ in range(4):
        id += 1
        node2.child.append(tree_node(id))
    node3 = node2.child[1]
    for _ in range(2):
        id += 1
        node3.child.append(tree_node(id))
    return root


def cal_node_interval(node=tree_node(0)):
    # return condition
    child_size = len(node.child)
    if child_size == 0:
        return
    # loop for every interval
    for index in range(child_size):
        cal_node_interval(node.child[index])
        if index == 0:
            continue
        node.node_interval.append(
            int(node.child[index].total_width / 2) +
            int(node.child[index - 1].total_width / 2) + 1)
    node.total_width = child_size * \
        tree_node.node_size + sum(node.node_interval)


scale = 0.1


def draw_child_node(graph, node, pos):
    if len(node.child) == 0:
        return
    global scale
    child_pos_x = 0.
    for index in range(len(node.child)):
        if index == 0:
            child_pos_x = pos[0] - node.total_width * scale / 2. + \
                tree_node.node_size * scale / 2.
            graph.add_node(node.child[index].id, pos=(
                child_pos_x, pos[1] - 0.1))
        else:
            child_pos_x += node.node_interval[index - 1] * scale + \
                tree_node.node_size * scale
            graph.add_node(node.child[index].id, pos=(
                child_pos_x, pos[1] - 0.1))
        graph.add_edge(node.child[index].id, node.id)
        draw_child_node(graph, node.child[index], pos=(
            child_pos_x, pos[1] - 0.1))


def node_visualize():
    root = generate_tree()
    cal_node_interval(root)
    node_graph = nx.Graph()
    node_graph.add_node(root.id, pos=(0., 0.))
    draw_child_node(node_graph, root, (0., 0.))
    nx.draw(node_graph, nx.get_node_attributes(node_graph, 'pos'),
            node_color=[random.random() for i in range(len(node_graph.nodes))],
            with_labels=True,
            node_size=200,
            edge_color='gray',
            width=3,
            cmap=plt.cm.Dark2,
            edge_cmap=plt.cm.Blues
            )
    plt.show()


def main():
    node_visualize()
    # StatusProvider.load_from_json()
    # StatusProvider.debug_info()


if __name__ == "__main__":
    main()
else:
    print("This is module to be run rather than imported.")
