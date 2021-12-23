from unittest import TestCase

from src.GraphAlgo import GraphAlgo


class TestAlgo(TestCase):


    def test_load(self):
        algo = GraphAlgo()
        algo.load_from_json(r'data\A4.json')

