from functools import cmp_to_key
from queue import PriorityQueue
import math

"""
    this class is used to be like a BRIDGE between the pathetic priority queue of python
    to work like p.queue of java with COMPERATOR function
    in place to set the lambda cmp func directly to the p.queue, 
    there is a class that "steal" the lower than and equal of comparing methods and force the priority queue to compare in the way we decided here
    this way - we can decide to compare two nodes via its dist_map value f3.. 
"""


class Bridge_class:
    def __init__(self, node_id: int, comperator_func):
        self.node_id = node_id
        self.cmp_func = comperator_func

    def __lt__(self, other):
        return self.cmp_func(self.node_id) < other.cmp_func(other.node_id)

    def __eq__(self, other):
        return self.cmp_func(self.node_id) == other.cmp_func(other.node_id)


"""
    this class inherit from priority queue BUT:
    use Bridge_class to "push" another mechanic of comparing between nodes in the way we decide
    huge credit to comment 2 in this link: https://stackoverflow.com/questions/57487170/is-it-possible-to-pass-a-comparator-to-a-priorityqueue-in-python
"""


class ExtendedPriorityQueue(PriorityQueue):
    def __init__(self, key):
        self.key = key
        super().__init__()

    def _get(self):
        bridge = super()._get()
        return bridge.node_id

    def _put(self, item):
        super()._put(Bridge_class(item, self.key))


def key_transform(node_id: int):
    """
    :param node_id: index of relevant node in the graph
    :return: node_id modulo 1000
    """
    return node_id % 1000


def init_maps(curr_graph, p_map: dict, d_map: dict, v_map: dict):
    """
    initialize maps for Dijkstra algorithm
    :param curr_graph:
    :param p_map: prev map init to -1 (no prev node)
    :param d_map: distance map init to infinity (no path from src to curr node)
    :param v_map: visited map init to False (not visited yet)
    :return:
    """
    for i in range(1000):
        p_map[i] = {}
        d_map[i] = {}
        v_map[i] = {}
    temp_dict = curr_graph.get_all_v()
    for node in temp_dict.keys():
        k_node = key_transform(node)
        p_map.get(k_node)[node] = -1
        d_map.get(k_node)[node] = math.inf
        v_map.get(k_node)[node] = False


def Dijkstra(src_node: int, curr_graph):
    """
     * dijkstra algo via: https://www.youtube.com/watch?v=pSqmAO-m7Lk
                    || https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
     * using regular priority queue(binomal min heap)
     * running time O(|E|log|V| + |V|log|V|)
    :param src_node: which node we start algo from
    :param curr_graph: relevant graph
    :return: nothing yet.
    """
    """
    map mechanics:
        1st key->key_transform(curr_node_id), value->inner dict 
        2nd key->curr_node_id, value->via type of map 
    """
    prev_map = {}  # value->father of the curr node
    dist_map = {}  # value->distance from src_node to curr_node
    visit_map = {}  # value->visited in curr_node while the algo running
    init_maps(curr_graph, prev_map, dist_map, visit_map)  # init before start
    # ensure valid input
    if src_node not in visit_map.get(key_transform(src_node)):
        return dist_map, prev_map, visit_map

    # create min_heap via our crafted heap (that can get a lambada function)
    min_heap = ExtendedPriorityQueue(key=cmp_to_key(lambda node1, node2: -1
    if dist_map.get(key_transform(node1))[node1] < dist_map.get(key_transform(node2))[node2]
    else (0 if dist_map.get(key_transform(node1))[node1] == dist_map.get(key_transform(node2))[node2]
          else 1)))

    # init src node and vars
    dist_map.get(key_transform(src_node))[src_node] = 0.0
    min_heap.put(src_node)
    new_dist: float
    curr_node: int
    dest_node: int
    out_edges: dict

    while not min_heap.empty():
        # pop first node
        curr_node = min_heap.get()
        # mark him as visited
        visit_map.get(key_transform(curr_node))[curr_node] = True
        # get all his edges
        out_edges = curr_graph.all_out_edges_of_node(curr_node)
        # loop over all his OUT edges
        if out_edges is not None:

            for edge in out_edges.values():
                dest_node = edge[0]  # save as var the destination node of the edge
                if visit_map.get(key_transform(dest_node))[dest_node]:
                    continue  # pass if visited

                new_dist = dist_map.get(key_transform(curr_node))[curr_node] + edge[1]  # cal new distance
                if new_dist < dist_map.get(key_transform(dest_node))[dest_node]:
                    # edit only if there is shorter distance
                    dist_map.get(key_transform(dest_node))[dest_node] = new_dist  # distance
                    prev_map.get(key_transform(dest_node))[dest_node] = curr_node  # curr_node is the father
                    min_heap.put(dest_node)  # put in heap

    return dist_map, prev_map, visit_map


def Dijkstra_transpose(src_node: int, curr_graph):
    """
        --------- same as above, twist - run over the in_edges of the graph nodes -> look on the "transposed graph" ------
     * using regular priority queue(binomal min heap)
     * running time O(|E|log|V| + |V|log|V|)
    :param src_node: which node we start algo from
    :param curr_graph: relevant graph
    :return: nothing yet.
    """
    """
    map mechanics:
        1st key->key_transform(curr_node_id), value->inner dict 
        2nd key->curr_node_id, value->via type of map 
    """
    prev_map = {}  # value->father of the curr node
    dist_map = {}  # value->distance from src_node to curr_node
    visit_map = {}  # value->visited in curr_node while the algo running
    init_maps(curr_graph, prev_map, dist_map, visit_map)  # init before start
    # ensure valid input
    if src_node not in visit_map.get(key_transform(src_node)):
        return dist_map, prev_map, visit_map

    # create min_heap via our crafted heap (that can get a lambada function)
    min_heap = ExtendedPriorityQueue(key=cmp_to_key(lambda node1, node2: -1
    if dist_map.get(key_transform(node1))[node1] < dist_map.get(key_transform(node2))[node2]
    else (0 if dist_map.get(key_transform(node1))[node1] == dist_map.get(key_transform(node2))[node2]
          else 1)))

    # init src node and vars
    dist_map.get(key_transform(src_node))[src_node] = 0.0
    min_heap.put(src_node)
    new_dist: float
    curr_node: int
    dest_node: int
    in_edges: dict

    while not min_heap.empty():
        # pop first node
        curr_node = min_heap.get()
        # mark him as visited
        visit_map.get(key_transform(curr_node))[curr_node] = True
        # get all his edges
        in_edges = curr_graph.all_in_edges_of_node(curr_node)
        # loop over all his IN edges - its TRANSPOSED GRAPH!!!
        if in_edges is not None:

            for edge in in_edges.values():
                dest_node = edge[0]  # save as var the destination node of the edge
                if visit_map.get(key_transform(dest_node))[dest_node]:
                    continue  # pass if visited

                new_dist = dist_map.get(key_transform(curr_node))[curr_node] + edge[1]  # cal new distance
                if new_dist < dist_map.get(key_transform(dest_node))[dest_node]:
                    # edit only if there is shorter distance
                    dist_map.get(key_transform(dest_node))[dest_node] = new_dist  # distance
                    prev_map.get(key_transform(dest_node))[dest_node] = curr_node  # curr_node is the father
                    min_heap.put(dest_node)  # put in heap

    return dist_map, prev_map, visit_map


def longest_road(dist_map):
    """
    :param dist_map: of dijkstra output
    :return: max distance value in the dist_map
    """
    max_dist = 0.0  # minimal
    for inner_dictt in dist_map.values():
        for dist in inner_dictt.values():
            max_dist = max(dist, max_dist)  # switch for higher
    return max_dist


def multi_process_beat_thread(node_list: list, curr_graph):
    """
    meanwhile center function from graphAlgo
    for graph with alot of objects, we would like to split between all the pc cores the dijkstra cals
    with using this method, running time of center shall be reduce approximately of 33~50% time in graphs of more than 20k objects
    :param node_list: list of nodes to run dijkstra on
    :param curr_graph: graph we work on
    :return: node_id, shortest_bet_longests
    represents: from all the node_list, node_id is the one with the smallest longest shortest path
    """
    # def defualt
    shortest_bet_longests = float('inf')
    node_id = -1
    for node in node_list:  # loop over all nodes
        node_longest_path = longest_road(Dijkstra(node, curr_graph)[0])  # dijkstra + get longest
        if node_longest_path < shortest_bet_longests:
            # edit our best node if and only if his longest path is shorter than the curr_node
            node_id = node
            shortest_bet_longests = node_longest_path
    return node_id, shortest_bet_longests
