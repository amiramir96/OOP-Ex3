import multiprocessing
import queue
import time

from src import *
from src.DiGraph import DiGraph
from src.GraphAlgo import GraphAlgo


def check():
    """
    Graph: |V|=4 , |E|=5
    {0: 0: |edges out| 1 |edges in| 1, 1: 1: |edges out| 3 |edges in| 1, 2: 2: |edges out| 1 |edges in| 1, 3: 3: |edges out| 0 |edges in| 2}
    {0: 1}
    {0: 1.1, 2: 1.3, 3: 10}
    (3.4, [0, 1, 2, 3])
    (2.8, [0, 1, 3])
    (inf, [])
    2.062180280059253 [1, 10, 7]
    17.693921758901507 [47, 46, 44, 43, 42, 41, 40, 39, 15, 16, 17, 18, 19]
    11.51061380461898 [20, 21, 32, 31, 30, 29, 14, 13, 3, 2]
    inf []
    (7, 6.806805834715163)
    ([1,3,4,2],3.5)
    """
    check0()
    check1()
    check2()
    check3()


def check0():
    """
    This function tests the naming (main methods of the DiGraph class, as defined in GraphInterface.
    :return:
    """
    print('check 0:')
    g = DiGraph()  # creates an empty directed graph
    for n in range(4):
        g.add_node(n)
    g.add_edge(0, 1, 1)
    g.add_edge(1, 0, 1.1)
    g.add_edge(1, 2, 1.3)
    g.add_edge(2, 3, 1.1)
    g.add_edge(1, 3, 1.9)
    g.remove_edge(1, 3)
    g.add_edge(1, 3, 10)
    print(g)  # prints the __repr__ (func output)
    print(g.get_all_v())  # prints a dict with all the graph's vertices.
    print(g.all_in_edges_of_node(1))
    print(g.all_out_edges_of_node(1))
    g_algo = GraphAlgo(g)
    print(g_algo.shortest_path(0, 3))
    g_algo.plot_graph()


def check1():
    """
       This function tests the naming (main methods of the GraphAlgo class, as defined in GraphAlgoInterface.
    :return:
    """
    print('check 1:')
    g_algo = GraphAlgo()  # init an empty graph - for the GraphAlgo
    file = "../data/T0.json"
    g_algo.load_from_json(file)  # init a GraphAlgo from a json file
    print(g_algo.shortest_path(0, 3))
    print(g_algo.shortest_path(3, 1))
    print(g_algo.centerPoint())
    g_algo.save_to_json(file + '_saved')
    g_algo.plot_graph()


def check2():
    """ This function tests the naming, basic testing over A5 json file.
      :return:
      """
    print('check 2:')
    g_algo = GraphAlgo()
    file = '../tests/correctness/A5.json'
    g_algo.load_from_json(file)
    g_algo.get_graph().remove_edge(13, 14)
    g_algo.save_to_json(file + "_edited")
    dist, path = g_algo.shortest_path(1, 7)
    print(dist, path)
    dist, path = g_algo.shortest_path(47, 19)
    print(dist, path)
    dist, path = g_algo.shortest_path(20, 2)
    print(dist, path)
    dist, path = g_algo.shortest_path(2, 20)
    print(dist, path)
    print(g_algo.TSP([1, 2, 3]))
    g_algo.plot_graph()


def check3():
    """ This function tests the naming, basic testing over A5 json file.
      :return:
      """
    print('check 3:')
    g = DiGraph()  # creates an empty directed graph
    for n in range(5):
        g.add_node(n)
    g.add_edge(0, 1, 1)
    g.add_edge(0, 4, 5)
    g.add_edge(1, 0, 1.1)
    g.add_edge(1, 2, 1.3)
    g.add_edge(1, 3, 1.9)
    g.add_edge(2, 3, 1.1)
    g.add_edge(3, 4, 2.1)
    g.add_edge(4, 2, .5)
    g_algo = GraphAlgo(g)
    print(g_algo.centerPoint())
    print(g_algo.TSP([1, 2, 4]))
    g_algo.plot_graph()

def printq(qlist):
    for x in qlist:
        print(str(x) + " im from list: "+ str(x%2))

def do_some():
    print('sleeping 1 seconds..')
    time.sleep(1)
    print('done sleeping..')

if __name__ == '__main__':
    check()
    # list_of_lists = []
    # core_allocate = int((multiprocessing.cpu_count())-1)
    # for i in range(core_allocate):
    #     list_of_lists.append([])
    #
    # for i in range(100000):
    #     x = i % core_allocate
    #     list_of_lists[x].append(i)
    #
    # proccess = []
    # for x in list_of_lists:
    #         p = multiprocessing.Process(target=printq, args=[x])
    #         proccess.append(p)
    #
    # for x in proccess:
    #     x.start()
    #
    # for x in proccess:
    #     x.join()
    # print("amount of core to use: ", core_allocate)
    # print("done")