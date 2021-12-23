from functools import cmp_to_key

from src import DiGraph
from queue import PriorityQueue
import math


class _Wrapper:
    def __init__(self, item, key):
        self.item = item
        self.key = key

    def __lt__(self, other):
        return self.key(self.item) < other.key(other.item)

    def __eq__(self, other):
        return self.key(self.item) == other.key(other.item)


class KeyPriorityQueue(PriorityQueue):
    def __init__(self, key):
        self.key = key
        super().__init__()

    def _get(self):
        wrapper = super()._get()
        return wrapper.item

    def _put(self, item):
        super()._put(_Wrapper(item, self.key))


def key_transform(node_id: int):
    """
    :param node_id:
    :return: key modolu 1000 (first dict key)
    """
    return node_id % 1000


def init_maps(curr_graph: DiGraph.DiGraph, p_map: dict, d_map: dict, v_map: dict):
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


def Dijkstra(src_node: int, curr_graph: DiGraph.DiGraph):
    """
     * dijkstra algo via: https://www.youtube.com/watch?v=pSqmAO-m7Lk
                    || https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
     * using regular priority queue(binomal min heap)
     * running time O(|E|log|V| + |V|log|V|)
    :param src_node: which node we start algo from
    :param curr_graph: relevant graph
    :return: tuple of (dist_map, prev_map, visit_map)
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
    min_heap = KeyPriorityQueue(key=cmp_to_key(lambda node1, node2: -1
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

            for edge in out_edges.items():
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
