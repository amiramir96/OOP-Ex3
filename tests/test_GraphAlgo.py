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
        print(algo.get_graph().v_size())

    def test_save_to_json(self):
        algo = GraphAlgo()
        algo.load_from_json(r'data\A4.json')
        print(algo.get_graph().v_size())
        algo.save_to_json('data\\saved_graph.json')

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
        self.fail()

    def test_center_point(self):
        """
        cases:
        less than 20k total obj (nodes+edges) - without multi processing
            1- connected graph, check currect answer (node_id, float_weight)
            2- not connected graph. for currect answer (None, float('inf'))
        more than 20k total ovj (nodes+edges) - use multi processing
        :return:
        """
        algo = GraphAlgo()
        algo.load_from_json(r'data\A5.json')
        ans = algo.centerPoint()
        self.assertEqual(ans[0], 40)
        self.assertEqual(ans[1], 9.291743173960954)
        algo.get_graph().remove_node(40)
        ans = algo.centerPoint()
        self.assertEqual(ans[0], None)
        self.assertEqual(ans[1], float('inf'))

    def test_plot_graph(self):
        self.fail()
