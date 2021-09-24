from utils.utils import random_ID
import networkx as nx
import matplotlib.pyplot as plt
import random


class tree_node:
    node_size = 1
    default_interval = 1
    scale = 0.1

    def __init__(self, id):
        self.id = id
        self.child = []
        self.node_interval = []
        self.total_width = tree_node.node_size
        self.label = ''

    def dump(self, indent=0):
        info = '    ' * indent + ' |- ' if indent > 0 else '    '
        print('%s%s' % (info, self.id))
        for node in self.child:
            node.dump(indent + 1)

class TreeDrawer:

    __label_dict = {}

    def generate_tree(node):
        new_key = random_ID()
        root = tree_node(new_key)
        TreeDrawer.__label_dict[new_key] = node.label()
        TreeDrawer.copy_child(root, node)
        return root

    def copy_child(ori_node, node):
        for child in node.childs():
            new_key = random_ID()
            new_tree = tree_node(new_key)
            ori_node.child.append(new_tree)
            TreeDrawer.__label_dict[new_key] = node.label()
            TreeDrawer.copy_child(new_tree, child)

    def cal_node_interval(node):
        # return condition
        child_size = len(node.child)
        if child_size == 0:
            return
        # loop for every interval
        for index in range(child_size):
            TreeDrawer.cal_node_interval(node.child[index])
            if index == 0:
                continue
            node.node_interval.append(
                int(node.child[index].total_width / 2) +
                int(node.child[index - 1].total_width / 2) + 1)
        node.total_width = child_size * \
            tree_node.node_size + sum(node.node_interval)

    def draw_child_node(graph, node, pos):
        if len(node.child) == 0:
            return
        child_pos_x = 0.
        for index in range(len(node.child)):
            if index == 0:
                child_pos_x = pos[0] - node.total_width * tree_node.scale / 2. + \
                    tree_node.node_size * tree_node.scale / 2.
                graph.add_node(node.child[index].id, pos=(
                    child_pos_x, pos[1] - 0.1))
            else:
                child_pos_x += node.node_interval[index - 1] * tree_node.scale + \
                    tree_node.node_size * tree_node.scale
                graph.add_node(node.child[index].id, pos=(
                    child_pos_x, pos[1] - 0.1))
            graph.add_edge(node.child[index].id, node.id)
            TreeDrawer.draw_child_node(graph, node.child[index], pos=(
                child_pos_x, pos[1] - 0.1))

    def node_visualize(node):
        root = TreeDrawer.generate_tree(node)
        TreeDrawer.cal_node_interval(root)
        node_graph = nx.Graph()
        node_graph.add_node(root.id, pos=(0., 0.))
        TreeDrawer.draw_child_node(
            node_graph, root, (0., 0.))
        nx.draw(node_graph, nx.get_node_attributes(node_graph, 'pos'),
                node_color=[random.random()
                            for i in range(len(node_graph.nodes))],
                labels=TreeDrawer.__label_dict,
                with_labels=True,
                # node_size=200,
                edge_color='gray',
                width=3,
                cmap=plt.cm.Dark2,
                edge_cmap=plt.cm.Blues
                )
        plt.show()
