import multiprocessing
import sys
from typing import List
import json
from src import GraphAlgoInterface, GraphInterface, DiGraph
from src.BFS import iterative_BFS
from src.BFS import iterative_transpose_BFS
from src.Dijkstra import Dijkstra, longest_road, multi_process_beat_thread

"""
:param node_id: index of relevant node in the graph
:return: node_id modulo 1000
"""


def key_transform(node_id):
    return node_id % 1000


def parents_list_helper(id1: int, id2: int, dist_map: dict, parents_map: dict):
    """
    use prev_map form dijkstra to return list of nodes that represents the shortes path from id1 to id2
    :param id1: src_node
    :param id2: dest_node
    :param parents_map: output from dijkstra (prev_map) - ea node_id key is point to its father in the shortest path
    :return: parents list from id1 to id2 if exist, [] blank list if not exist
    """
    # ensure valid input
    if id2 not in parents_map.get(key_transform(id2)):
        return float('inf'), []
    # init vars
    parents_list = []
    curr_node = id2
    while curr_node != -1 and curr_node != id1:
        # loop over anccesor parents of id2 till stands on id1 or -1 (represent dead end)
        parents_list.insert(0, curr_node)
        curr_node = parents_map.get(curr_node % 1000)[curr_node]

    if curr_node == id1:
        # last parent is id1, found path
        parents_list.insert(0, curr_node)
        return dist_map.get(key_transform(id2))[id2], parents_list
    else:
        # no existing path
        return float('inf'), []


class GraphAlgo(GraphAlgoInterface.GraphAlgoInterface):

    def __init__(self, *args):
        # empty initialization
        if len(args) == 0:
            self.graph = None
        # received graph
        elif len(args) > 0 and type(args[0]) == GraphInterface:
            self.graph = args[0]
        # received string (file path)
        elif len(args) > 0 and type(args[0]) == str:
            self.load_from_json(args[0])
        self.is_connected = -1

    def get_graph(self) -> GraphInterface.GraphInterface:
        """
        :return: the directed graph on which the algorithm works on.
        """
        return self.graph

    def is_connected_graph(self, src_node: int):
        """
        use BFS algorithm to check if graph is strongly connected
        given a curr_node in the graph - this happens if graph stands within the 2 next terms:
            1 - there is a path from that curr_node to any other node in the graph
            2 - there is a path from any node in the graph to that curr_node
        Running Time: O(|E| + Log|V|)
        :param src_node: node to start from the BFS
        :return: boolean
        """
        # ez cases - graph already have been checked:
        if self.is_connected == 0:
            return False
        if self.is_connected == 1:
            return True
        # have to calculate
        if self.is_connected == -1:
            if not iterative_BFS(self.get_graph(), src_node) or not iterative_transpose_BFS(self.get_graph(), src_node):
                self.is_connected = 0
                return False
            else:
                self.is_connected = 1
                return True

    def load_from_json(self, file_name: str) -> bool:
        """
        Loads a graph from a json file.
        @param file_name: The path to the json file
        @returns True if the loading was successful, False o.w.
        """
        self.graph = DiGraph.DiGraph()
        success = True
        # load file for reading
        curr_path = sys.path[0]  # current path from which the script is running
        # make sure the script isn't run from 'src' or 'tests' directory,
        # so we will get the path we want
        if curr_path[-3:] == 'src':
            # replace last occurrence of src
            # see: https://stackoverflow.com/questions/2556108/rreplace-how-to-replace-the-last-occurrence-of-an-expression-in-a-string
            curr_path = curr_path.rsplit('src', 1)[0]
        if curr_path[-5:] == 'tests':
            # replace last occurrence of tests
            curr_path = curr_path.rsplit('tests', 1)[0]
        if curr_path[-1:] != '\\':
            curr_path += '\\'
        path = curr_path + file_name
        with open(path, 'r') as file:
            data = json.load(file)

        # add nodes
        for node in data['Nodes']:
            pos = tuple(map(float, node['pos'].split(',')))
            curr_sec = self.graph.add_node(node['id'], pos)
            if not curr_sec:
                success = False

        # add edges
        for edge in data['Edges']:
            curr_sec = self.get_graph().add_edge(edge['src'], edge['dest'], edge['w'])
            if not curr_sec:
                success = False
        self.is_connected = -1  # zero is_connected flag
        return success

    def save_to_json(self, file_name: str) -> bool:
        """
        Saves the graph in JSON format to a file
        @param file_name: The path to the out file
        @return: True if the save was successful, False o.w.
        """
        curr_path = sys.path[0]  # current path from which the script is running
        # make sure the script isn't run from 'src' or 'tests' directory,
        # so we will get the path we want
        if curr_path[-3:] == 'src':
            # replace last occurrence of src
            # see: https://stackoverflow.com/questions/2556108/rreplace-how-to-replace-the-last-occurrence-of-an-expression-in-a-string
            curr_path = curr_path.rsplit('src', 1)[0]
        if curr_path[-5:] == 'tests':
            # replace last occurrence of tests
            curr_path = curr_path.rsplit('tests', 1)[0]
        if curr_path[-1:] != '\\':
            curr_path += '\\'
        path = curr_path + file_name

        # create dictionary to write
        g = {'Edges': [],
             'Nodes': []}
        # add nodes and edges
        total_v = self.graph.v_size()  # total number of nodes/ edges
        total_e = self.graph.e_size()
        nodes_added = 0
        edges_added = 0
        # for each node, add it and all the edges coming out of him
        for node in self.graph.get_all_v().values():
            node_dict = {'id': node[0],
                         'pos': str(node[1][0]) + ',' + str(node[1][1]) + ',' + str(node[1][2])}
            g['Nodes'].append(node_dict)
            nodes_added += 1
            for edge in self.get_graph().all_out_edges_of_node(node[0]).values():
                edge_dict = {'src': node[0],
                             'w': edge[1],
                             'dest': edge[0]}
                g['Edges'].append(edge_dict)
                edges_added += 1

        # make sure all the graph is in the dict
        if total_v != nodes_added or total_e != edges_added:
            return False
        # write as pretty print to the file
        with open(path, 'w') as file:
            file.write(json.dumps(g, sort_keys=True, indent=4))
            print(json.dumps(g, sort_keys=True, indent=4))  # TODO delete
            return True

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        """
        Returns the shortest path from node id1 to node id2 using Dijkstra's Algorithm
        @param id1: The start node id
        @param id2: The end node id
        @return: The distance of the path, a list of the nodes ids that the path goes through
        Notes:
        If there is no path between id1 and id2, or one of them dose not exist the function returns (float('inf'),[])
        More info:
        https://en.wikipedia.org/wiki/Dijkstra's_algorithm
        Running Time: O(|E|*Log(|V|))
        """
        # reminder: dij[0]=dict_map, dij[1]=prev_map, dij[2]=visit_map
        ans_tuple = Dijkstra(id1, self.graph)
        ans = parents_list_helper(id1, id2, ans_tuple[0], ans_tuple[1])  # tuple of (weight, list)
        return ans

    def TSP(self, node_lst: List[int]) -> (List[int], float):
        """
        Finds the shortest path that visits all the nodes in the list
        :param node_lst: A list of nodes id's
        :return: A list of the nodes id's in the path, and the overall distance
        """

    def centerPoint(self) -> (int, float):
        """
        1. can be center if and only if there the graph is connected
        2. loop over ea node and use dijkstra on
        3. take the longest weighted path of ea node from bullet 2
        4. the minimal node with the longest weighted path is the center!
        Running Time: O(|V|*|E|Log(|V|))
        :return:
        """
        # hold one node from the graph
        nodes_map = self.get_graph().get_all_v()
        for node in nodes_map.keys():
            if node is None:
                return None, float('inf')
            else:
                first_n = node
            break
        # ensure that the graph is connected
        if self.is_connected_graph(first_n):
            # inits
            longest_bet_shortest = float('inf')
            ans_node = -1

            if self.get_graph().e_size() + self.get_graph().v_size() > 20000 and multiprocessing.cpu_count() > 2:
                # gonna use multi peocessing, split nodes between
                core_allocate = multiprocessing.cpu_count() - 1  # keep one core outside the game - ensure pc wont die
                list_list_nodes = []  # gonna work 2D

                for i in range(core_allocate):
                    # create amount of inner list as amount of cores to allocate to multi processing
                    list_list_nodes.append([])

                for node in nodes_map.keys():
                    # split nodes equally as possible between all the inner lists
                    x = node % core_allocate
                    list_list_nodes[x].append(node)

                # create core_allocate-1 diff processes for ea list
                my_first_multi_processing = []
                for listt in list_list_nodes:
                    my_first_multi_processing.append(\
                        multiprocessing.Process(target=multi_process_beat_thread, args=[listt]))

                for p in my_first_multi_processing:
                    p.start()

                for pi in my_first_multi_processing:
                    pi.join()

                for tup in list_list_nodes:
                    if tup[1] < longest_bet_shortest:
                        longest_bet_shortest = tup[1]
                        ans_node = tup[0]

                return ans_node, longest_bet_shortest  # ans :-)

            else:  # small amount of objects, multi processing shall delay our running time
                # loop over all nodes
                for node in nodes_map.keys():
                    # use dijkstra
                    dist_map = Dijkstra(node, self.get_graph())[0]
                    # take longest val and compare it to others
                    longest_temp = longest_road(dist_map)
                    if longest_temp < longest_bet_shortest:
                        # save only if its the smallest value till now
                        longest_bet_shortest = longest_temp
                        ans_node = node
                return ans_node, longest_bet_shortest  # ans :-)
        else:  # else there is no center
            return None, float('inf')

    def plot_graph(self) -> None:
        """
        Plots the graph.
        If the nodes have a position, the nodes will be placed there.
        Otherwise, they will be placed in a random but elegant manner.
        @return: None
        """
        raise NotImplementedError
