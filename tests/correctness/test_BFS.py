from unittest import TestCase

from src.DiGraph import DiGraph
from src.BFS import iterative_BFS
from src.BFS import iterative_transpose_BFS


class Test(TestCase):

    def test_BFS(self):
        """
        test iterative and iterative_transpose methods
        cases:
            1,2 - ordinary for False
            3,4 - ordinary for True
            5,6,7 - added node isolated from the graph and added only one edge to him
                    if we start from that node with BFS the returns is True
                    if we start from another node / via transpose func, returns False



        """
        g = DiGraph()
        g.add_node(0, (0, 0))
        g.add_node(1, (1, 1))
        g.add_node(2, (2, 0))
        g.add_edge(1, 2, 3.1)
        g.add_edge(0, 1, 3.1)
        # case 1:
        bol = iterative_BFS(g, 1)
        self.assertEqual(bol, False)
        # case 2:
        bol = iterative_transpose_BFS(g, 0)
        self.assertEqual(bol, False)
        g.add_edge(2, 0, 3.1)
        # case 3:
        bol = iterative_BFS(g, 0)
        self.assertEqual(bol, True)
        bol = iterative_transpose_BFS(g, 0)
        # case 4:
        self.assertEqual(bol, True)
        g.add_node(5, (8, 3))
        g.add_edge(5, 0, 11)
        # case 5:
        bol = iterative_BFS(g, 5)
        self.assertEqual(bol, True)
        # case 6:
        bol = iterative_BFS(g, 1)
        self.assertEqual(bol, False)
        # case 7:
        bol = iterative_transpose_BFS(g, 5)
        self.assertEqual(bol, False)
