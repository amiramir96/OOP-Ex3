from unittest import TestCase

from src.GraphAlgo import GraphAlgo


class TestAlgo(TestCase):

    def test_load(self):
        algo = GraphAlgo()
        algo.load_from_json(r'data\A4.json')
<<<<<<< Updated upstream
        print(algo.get_graph().v_size())

    def test_save(self):
        algo = GraphAlgo()
        algo.load_from_json(r'data\A4.json')
        print(algo.get_graph().v_size())
        algo.save_to_json('data\\saved_graph.json')
=======
>>>>>>> Stashed changes
