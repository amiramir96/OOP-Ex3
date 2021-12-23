import sys
from typing import List
import json
from src import GraphAlgoInterface, GraphInterface, DiGraph


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

    def get_graph(self) -> GraphInterface.GraphInterface:
        """
        :return: the directed graph on which the algorithm works on.
        """
        return self.graph

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
                         'pos': str(node[1][0])+','+str(node[1][1])+','+str(node[1][2])}
            g['Nodes'].append(node_dict)
            nodes_added += 1
            for edge in self.graph.all_in_edges_of_node(node[0]).values:
                edge_dict = {'src': node[0],
                             'w': edge[1],
                             'dest': edge[0]}
                g['Edges'].append(edge_dict)
                edges_added += 1

        # make sure all the graph is in the dict
        if total_e != nodes_added or total_e != edges_added:
            return False
        # write as pretty print to the file
        with open(path, 'w') as file:
            file.write(json.dumps(g, sort_keys=True, indent=4))
            print(json.dumps(g, sort_keys=True, indent=4))#TODO delete
            return True

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        """
        Returns the shortest path from node id1 to node id2 using Dijkstra's Algorithm
        @param id1: The start node id
        @param id2: The end node id
        @return: The distance of the path, a list of the nodes ids that the path goes through
        Example:
#      >>> from GraphAlgo import GraphAlgo
#       >>> g_algo = GraphAlgo()
#        >>> g_algo.addNode(0)
#        >>> g_algo.addNode(1)
#        >>> g_algo.addNode(2)
#        >>> g_algo.addEdge(0,1,1)
#        >>> g_algo.addEdge(1,2,4)
#        >>> g_algo.shortestPath(0,1)
#        (1, [0, 1])
#        >>> g_algo.shortestPath(0,2)
#        (5, [0, 1, 2])
        Notes:
        If there is no path between id1 and id2, or one of them dose not exist the function returns (float('inf'),[])
        More info:
        https://en.wikipedia.org/wiki/Dijkstra's_algorithm
        """
        raise NotImplementedError

    def TSP(self, node_lst: List[int]) -> (List[int], float):
        """
        Finds the shortest path that visits all the nodes in the list
        :param node_lst: A list of nodes id's
        :return: A list of the nodes id's in the path, and the overall distance
        """

    def centerPoint(self) -> (int, float):
        """
        Finds the node that has the shortest distance to it's farthest node.
        :return: The nodes id, min-maximum distance
        """

    def plot_graph(self) -> None:
        """
        Plots the graph.
        If the nodes have a position, the nodes will be placed there.
        Otherwise, they will be placed in a random but elegant manner.
        @return: None
        """
        raise NotImplementedError
