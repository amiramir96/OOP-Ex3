from unittest import TestCase

from src.Dijkstra import Dijkstra, multi_process_beat_thread
from src.GraphAlgo import GraphAlgo


class Test(TestCase):
    def test_dijkstra(self):
        """
        cases:
            1,2 - ordinary, shortest path in graph
            3 - ask for shortest path (use dijkstra) while one of the nodes isnt exists in the graph
            4 - both of nodes is not exists in the graph
            5 - check multi processing on dijkstra!
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
        algo.load_from_json(r'data\A4.json')
        # case 5:
        listn = [1, 2, 3, 4, 8, 56456]  # check multi process and in same time
        # ensure that if one of the list nodes is not exist nothing will get bomb
        ans = multi_process_beat_thread(listn, algo.get_graph())
        # (8, 10.660789474757282)
        self.assertEqual(ans[0], 8)
        self.assertEqual(ans[1], 10.660789474757282)