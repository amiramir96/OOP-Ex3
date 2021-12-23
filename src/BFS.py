from src.DiGraph import DiGraph

"""
    fk u python
    what a horrible stack.. seriously whats ur problem to implement basic data structre?
    i dont want to use list like a stack, i want a stack, with smaller variet of methods!
"""


class myStack:
    # based on list
    def __init__(self):
        self.stack = []

    def pop(self):
        # -1 for empty, item for exist
        if len(self.stack) == 0:
            return -1
        else:
            self.stack.pop(0)

    # add first in the list
    def push(self, node_id: int):
        self.stack.append(node_id)

    # True for empty
    def isEmpty(self):
        return len(self.stack) == 0

    def size(self):
        return len(self.stack)


"""
:param node_id: index of relevant node in the graph
:return: node_id modulo 1000
"""


def key_transform(node_id: int):
    return node_id % 1000


"""
implementation of BFS - Breadth First Search
can be used for to check if graph "is connected" (strongly since its directed graph)
for more details on the algorithm: https://www.youtube.com/watch?v=oDqjPvD54Ss
using stack to hold nodes that we shall loop over all their edges
using dict to hold boolean for ea node, if visited
:param: src_node: which node to start BFS from
:return: boolean - True if all nodes is accessible from src_node, otherwise false
"""


def check_visited(visited_map: dict):
    for inner_dict_of_nodes in visited_map:
        for bool in inner_dict_of_nodes.values():
            if not bool:
                return False
    return True


def iterative_BFS(curr_graph: DiGraph, src_node: int):
    # visit dict
    visited_map = {}
    for i in range(1000):  # for more data on this strategy, look at DiGraph
        visited_map[i] = {}
    temp_dict = curr_graph.get_all_v()
    for node in temp_dict.keys():  # edit all nodes bool value to false (not visited yet)
        visited_map.get(key_transform(node))[node] = False
    # init stack
    stack = myStack()
    stack.push(src_node)
    # init vars
    temp_node: int
    dest_node: int
    edge_out_dict: dict

    while not stack.isEmpty():
        # loop over all the graph nodes
        # new iterate, pop for node and iterate over its out_edges
        temp_node = stack.pop()
        edge_out_dict = curr_graph.all_out_edges_of_node(temp_node)

        for dest_node in edge_out_dict.keys():
            if visited_map.get(key_transform(dest_node))[dest_node] is False:
                # for every node connected to curr_node that un visited, push to stack and  mark as visited
                stack.push(dest_node)
                visited_map.get(key_transform(dest_node))[dest_node] = True

    return check_visited(visited_map)  # boolean


"""for more details on BFS algorithm, look upstairs this function run on the TRANSPOSE edges of the graph, 
which means on the "in_edges" of ea node will be helpful to check if graph is connected (there is path from given 
node to any other nodes, and from any other node to this node)
"""


def iterative_transpose_BFS(curr_graph: DiGraph, src_node: int):
    # visit dict
    visited_map = {}
    for i in range(1000):  # for more data on this strategy, look at DiGraph
        visited_map[i] = {}
    temp_dict = curr_graph.get_all_v()
    for node in temp_dict.keys():  # edit all nodes bool value to false (not visited yet)
        visited_map.get(key_transform(node))[node] = False
    # init stack
    stack = myStack()
    stack.push(src_node)
    # init vars
    temp_node: int
    dest_node: int
    edge_in_dict: dict

    while not stack.isEmpty():
        # loop over all the graph nodes
        # new iterate, pop for node and iterate over its in_edges
        temp_node = stack.pop()
        edge_in_dict = curr_graph.all_in_edges_of_node(temp_node)

        for dest_node in edge_in_dict.keys():
            if visited_map.get(key_transform(dest_node))[dest_node] is False:
                # for every node connected to curr_node that un visited, push to stack and  mark as visited
                stack.push(dest_node)
                visited_map.get(key_transform(dest_node))[dest_node] = True

    return check_visited(visited_map)  # boolean