from random import randint
from unittest import TestCase

from src.DiGraph import DiGraph
from src.GraphAlgo import GraphAlgo


class TestGraphAlgo(TestCase):
    def test_get_graph(self):
        """
        cases:
            1- empty graph algo = None
            2- load from data a graph
            3- set input of existing graph
        :return:
        """
        # case 1
        algo = GraphAlgo()
        self.assertEqual(algo.get_graph(), None)

        # case 2
        algo.load_from_json(r'data\A4.json')
        self.assertEqual(algo.get_graph().v_size(), 40)
        self.assertEqual(algo.get_graph().e_size(), 102)
        algo = GraphAlgo(r'data\A4.json')
        self.assertEqual(algo.get_graph().v_size(), 40)
        self.assertEqual(algo.get_graph().e_size(), 102)

        # case 3
        g = DiGraph()
        g.add_node(1, (0, 0))
        g.add_node(2, (3, 2))
        g.add_node(3, (8, 2))
        g.add_edge(1, 2, 18)
        algo = GraphAlgo(g)
        self.assertEqual(algo.get_graph().v_size(), 3)
        self.assertEqual(algo.get_graph().e_size(), 1)

    def test_load_from_json(self):
        algo = GraphAlgo()
        algo.load_from_json(r'data\A4.json')
        self.assertEqual(40, algo.get_graph().v_size())

    def test_save_to_json(self):
        algo = GraphAlgo()
        algo.load_from_json(r'data\A4.json')
        algo.save_to_json('saved_graph.json')
        algo.load_from_json('saved_graph.json')
        self.assertEqual(40, algo.get_graph().v_size())

    def test_shortest_path(self):
        """
            1,2 - ordinary, shortest path in graph
            3 - ask for shortest path (use dijkstra) while one of the nodes isnt exists in the graph
            4 - both of nodes is not exists in the graph
        """
        algo = GraphAlgo()
        # case 1:
        algo.load_from_json(r'data\A0.json')
        ans = algo.shortest_path(8, 3)
        w_ans = 7.282598961846713
        self.assertEqual(ans[0], w_ans)
        # case 2:
        algo.load_from_json(r'data\A4.json')
        ans = algo.shortest_path(0, 5)
        w_ans = 6.834625309281369
        self.assertEqual(ans[0], w_ans)
        # case 3:
        algo.get_graph().remove_node(0)
        ans = algo.shortest_path(5, 0)
        w_ans = float('inf')
        self.assertEqual(ans[0], w_ans)
        ans = algo.shortest_path(123812, 3)
        self.assertEqual(ans[0], w_ans)
        # case 4:
        ans = algo.shortest_path(12031, 12391)
        self.assertEqual(ans[0], w_ans)

    def test_tsp(self):
        """
        cases:
            1,2- ordinary, strongly connected graph
            3- 2 strongly connected component, connected with one direction of edges (other wise they will be strongly
                    connected component)
            4- 3 strongly connected components, there is no cycle in 3 of them but there is path along the thre
            5- 4 strongly connected components - there is no valid path for ans (path is none)
            6- graph has 2 disjoint componnents, there is no path between them (no valid path, path is none)
        """
        algo = GraphAlgo()
        # case 1
        algo.load_from_json(r'data\A0.json')
        ans = algo.TSP([0, 9, 3])
        self.assertEqual([9, 10, 0, 1, 2, 3], ans[0])
        # case 2
        algo.load_from_json(r'data\A5.json')
        ans = algo.TSP([0, 11, 41, 23, 32, 12, 7, 3, 35, 39])
        self.assertEqual([0, 8, 7, 11, 12, 3, 13, 14, 15, 39, 40, 41, 40, 39, 38, 37, 36, 35, 36, 31, 23, 31, 32] , ans[0])
        # case 3
        algo.get_graph().remove_edge(39, 40)
        ans = algo.TSP([15, 41, 23])
        self.assertEqual(9.19429557236042, ans[1])
        # case 4
        algo.get_graph().remove_edge(13, 14)
        ans = algo.TSP([34, 47, 8])
        self.assertEqual(29.322570741971425, ans[1])
        # case 5
        algo.get_graph().add_node(555, (11, 11))
        algo.get_graph().add_edge(555, 0, 2.5)
        ans = algo.TSP([555, 34, 47, 8])
        # case 6
        self.assertEqual(None, ans[0])
        algo.get_graph().remove_node(40)
        ans = algo.TSP([40, 5])
        self.assertEqual(None, ans[0])

    def test_center_point(self):
        """
        cases:
            1. less than 20k total obj (nodes+edges) - without multi processing
                1- connected graph, check currect answer (node_id, float_weight)
                2- not connected graph. for currect answer (None, float('inf'))
            2. more than 20k total ovj (nodes+edges) - use multi processing
                2.1- connected graph, check currect answer (node_id, float_weight)
                2.2- not connected graph. for currect answer (None, float('inf'))
        """
        algo = GraphAlgo()
        # case 1.1
        algo.load_from_json(r'data/A5.json')
        ans = algo.centerPoint()
        self.assertEqual(ans[0], 40)
        self.assertEqual(ans[1], 9.291743173960954)

        # case 1.2
        algo.get_graph().remove_node(40)
        ans = algo.centerPoint()
        self.assertEqual(ans[0], None)
        self.assertEqual(ans[1], float('inf'))

        # case 2.1
        for i in range(1000):
            algo.get_graph().add_node(i)
        all_nodes = algo.get_graph().get_all_v()
        for node in all_nodes.keys():
            for i in range(20):
                algo.get_graph().add_edge(node, randint(0, 1000), randint(1, 12))
        algo.centerPoint()
        self.assertEqual(algo.get_graph().v_size(), 1000)

        # case 2.2
        algo.get_graph().remove_node(40)
        algo.get_graph().add_node(40, (1, 1))
        ans = algo.centerPoint()
        self.assertEqual(ans[0], None)

    def test_plot_graph(self):
        g = GraphAlgo('data/A0.json')
        g.plot_graph()

