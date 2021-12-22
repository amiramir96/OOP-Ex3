from unittest import TestCase

from src import DiGraph


class TestDiGraph(TestCase):

    def test_v_size(self):
        """
        check regular cases of oridnary addid node
        special case - add node with existing id -> ensure that its wont be added
        """
        g = DiGraph.DiGraph()
        g.add_node(0, (0, 0))
        self.assertEqual(g.v_size(), 1)
        g.add_node(1, (1, 1))
        g.add_node(2, (2, 0))
        g.add_edge(0, 1, 2)
        g.add_edge(1, 2, 3)
        self.assertEqual(g.v_size(), 3)

        # special case
        g.add_node(0, (1, 1.1))
        self.assertEqual(g.v_size(), 3)

        g.add_node(8, (-1, 2))
        self.assertEqual(g.v_size(), 4)

    def test_e_size(self):
        """
        check regular cases of oridnary add edge
        special case 1 - add edge between two nodes that there is edge between them already
        special case 2 - add edge that one of the nodes is not exists in the graph
        """
        g = DiGraph.DiGraph()
        g.add_node(0, (0, 0))
        g.add_node(1, (1, 1))
        g.add_node(2, (2, 0))
        g.add_edge(0, 1, 2)
        g.add_edge(1, 2, 3)
        self.assertEqual(g.e_size(), 2)

        # special case 1
        g.add_edge(0, 1, 3.5)
        self.assertEqual(g.e_size(), 2)

        # special case 2
        g.add_edge(0, 11, 2.2)
        self.assertEqual(g.e_size(), 2)

    def test_get_all_v(self):
        """
        cases: 1- get dict of all nodes after created graph
               2- after removed node still works
        """
        g = DiGraph.DiGraph()
        g.add_node(0, (0, 0))
        g.add_node(1, (1, 1))
        g.add_node(2, (2, 0))
        # case 1
        dictt = g.get_all_v()
        i = 0
        for node in dictt.keys():
            self.assertEqual(node, i)
            i = i+1
        # case 2
        g.remove_node(2)
        dictt = g.get_all_v()
        i = 0
        for node in dictt.keys():
            self.assertEqual(node, i)
            i = i + 1

    def test_all_in_edges_of_node(self):
        """
        cases: 1- get dict of all in_edges of node after created graph
               2- after removed edge still works
        """
        g = DiGraph.DiGraph()
        g.add_node(0, (0, 0))
        g.add_node(1, (1, 1))
        g.add_node(2, (2, 0))
        g.add_edge(1, 2, 3.1)
        g.add_edge(0, 2, 1.1)
        # case 1
        dictt = g.all_in_edges_of_node(2)
        i = 3.1
        for edge_in in dictt.values():
            self.assertEqual(edge_in, i)
            i = i-2
        # case 2
        g.remove_edge(1, 2)
        dictt = g.all_in_edges_of_node(2)
        i = 1.1
        for edge_in in dictt.values():
            self.assertEqual(edge_in, i)
            i = i-2

    def test_all_out_edges_of_node(self):
        """
        cases: 1- get dict of all out_edges of node after created graph
               2- after removed edge still works
        """
        g = DiGraph.DiGraph()
        g.add_node(0, (0, 0))
        g.add_node(1, (1, 1))
        g.add_node(2, (2, 0))
        g.add_edge(1, 2, 3)
        g.add_edge(0, 2, 1.1)
        g.add_edge(1, 0, 15)
        # case 1
        dictt = g.all_out_edges_of_node(1)
        i = 3
        for edge_in in dictt.values():
            self.assertEqual(edge_in, i)
            i = i + 12
        # case 2
        g.remove_edge(1, 2)
        dictt = g.all_out_edges_of_node(1)
        i = 15
        for edge_in in dictt.values():
            self.assertEqual(edge_in, i)
            i = i + 1


    def test_get_mc(self):
        """
        cases: 1- add node / edges -> +1 to mc
               2- remove edge -> +1 to mc
               3- remove object that not exist in the graph -> mc no change
               4- add object that wont be able to be added -> mc no change
               5- remove node -> +1 + k to mc while k = amount of out+in edges of that node
        """
        g = DiGraph.DiGraph()
        # case 1
        g.add_node(0, (0, 0))
        g.add_node(1, (1, 1))
        g.add_node(2, (2, 0))
        g.add_edge(0, 1, 2.9)
        g.add_edge(1, 2, 3.1)
        self.assertEqual(g.get_mc(), 5)

        # case 2
        g.remove_edge(1, 2)
        self.assertEqual(g.get_mc(), 6)

        # case 3
        g.remove_edge(1, 0)
        self.assertEqual(g.get_mc(), 6)

        # case 4
        g.add_node(0, (1, 1.1))
        self.assertEqual(g.get_mc(), 6)

        # case 5
        g.remove_node(1)
        self.assertEqual(g.get_mc(), 8)


    def test_add_edge(self):
        """
        check regular cases of oridnary add edge
        special case 1 - add edge between two nodes that there is edge between them already
        special case 2 - add edge that one of the nodes is not exists in the graph
        """
        g = DiGraph.DiGraph()
        g.add_node(0, (0, 0))
        g.add_node(1, (1, 1))
        g.add_node(2, (2, 0))
        g.add_edge(0, 1, 2)
        g.add_edge(1, 2, 3)
        self.assertEqual(g.e_size(), 2)

        # special case 1
        g.add_edge(0, 1, 3.5)
        self.assertEqual(g.e_size(), 2)

        # special case 2
        g.add_edge(0, 11, 2.2)
        self.assertEqual(g.e_size(), 2)

    def test_add_node(self):
        """
        check regular cases of oridnary addid node
        special case - add node with existing id -> ensure that its wont be added
        """
        g = DiGraph.DiGraph()
        g.add_node(0, (0, 0))
        self.assertEqual(g.v_size(), 1)
        g.add_node(1, (1, 1))
        g.add_node(2, (2, 0))
        g.add_edge(0, 1, 2)
        g.add_edge(1, 2, 3)
        self.assertEqual(g.v_size(), 3)

        # special case
        g.add_node(0, (1, 1.1))
        self.assertEqual(g.v_size(), 3)

        g.add_node(8, (-1, 2))
        self.assertEqual(g.v_size(), 4)

    def test_remove_node(self):
        """
        check regular cases of oridnary remove node with edges -> check sizes and edges removed
                remove node_id that not exist -> avoidance from exception
        """
        g = DiGraph.DiGraph()
        g.add_node(0, (0, 0))
        g.add_node(1, (1, 1))
        g.add_node(2, (2, 0))
        g.add_edge(0, 1, 2.9)
        g.add_edge(1, 2, 3.1)
        self.assertEqual(g.v_size(), 3)
        # first case
        g.remove_node(1)
        self.assertEqual(g.v_size(), 2)
        self.assertEqual(g.e_size(), 0)

        # second case
        g.remove_node(18)
        self.assertEqual(g.v_size(), 2)
        self.assertEqual(g.e_size(), 0)

    def test_remove_edge(self):
        """
        check 1- regular cases of oridnary remove edge -> check sizes decrease
              2-  remove edge that not exists between existing node
              3-  remove edge that not exists while one or both of the nodes isnt exists
        """
        g = DiGraph.DiGraph()
        g.add_node(0, (0, 0))
        g.add_node(1, (1, 1))
        g.add_node(2, (2, 0))
        g.add_edge(0, 1, 2.9)
        g.add_edge(1, 2, 3.1)
        self.assertEqual(g.v_size(), 3)
        # first case
        g.remove_edge(1, 2)
        self.assertEqual(g.v_size(), 3)
        self.assertEqual(g.e_size(), 1)

        # second case
        g.remove_edge(1, 0)
        g.remove_edge(0, 2)
        self.assertEqual(g.v_size(), 3)
        self.assertEqual(g.e_size(), 1)

        # third case
        g.remove_edge(18, 1)
        g.remove_edge(1, 119)
        g.remove_edge(18, 112)
        self.assertEqual(g.v_size(), 3)
        self.assertEqual(g.e_size(), 1)
