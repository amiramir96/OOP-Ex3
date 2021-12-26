import time
from random import randint

from src.DiGraph import DiGraph
from src.GraphAlgo import GraphAlgo


def compare_test(nodes: int):
    algo = GraphAlgo()
    start = time.time()
    if nodes == 100:
        algo.load_from_json(r'tests\performance\100performance.json')
    elif nodes == 1000:
        algo.load_from_json(r'tests\performance\1Kperformance.json')
    elif nodes == 10000:
        algo.load_from_json(r'tests\performance\10Kperformance.json')
    elif nodes == 100000:
        algo.load_from_json(r'tests\performance\100Kperformance.json')
    else:
        return -1
    curr_graph = algo.get_graph()
    end = time.time()
    print("Create graph time:", end - start, "seconds", "\nnumber of nodes:", curr_graph.v_size(),
          "\nnumber of edges: ", curr_graph.e_size())
    algo = GraphAlgo(curr_graph)

    # isConnected
    start = time.time()
    algo.is_connected_graph(0)
    end = time.time()
    print("isConnected time:", end - start, "seconds")

    # center
    start = time.time()
    algo.shortest_path(randint(0, nodes), randint(0, nodes))
    end = time.time()
    shortest_path_time = end - start
    if curr_graph.e_size() + curr_graph.v_size() > 250000:
        print("center approximate time is: ", shortest_path_time * nodes, "seconds")  # dijkstra * |V|
    else:
        start = time.time()
        algo.centerPoint()
        end = time.time()
        print("center time:", end - start, "seconds")

    # shortest_path
    print("shortest_path time:", shortest_path_time, "seconds")

    # TSP
    if curr_graph.e_size() + curr_graph.v_size() > 250000:
        print("TSP time:", shortest_path_time * 20 * 2)  # tsp_list input * 2 * dijkstra times
    else:
        tsp_list = []
        for i in range(21):
            x = randint(0, nodes-1)
            if x not in tsp_list:
                tsp_list.append(x)
        print(nodes)
        algo.TSP(tsp_list)
        end = time.time()
        print("TSP time:", end - start, "seconds")

    # save_graph
    start = time.time()
    algo.save_to_json('saved_graph.json')
    end = time.time()
    print("save_graph time:", end - start, "seconds")

    # load_graph
    start = time.time()
    algo.load_from_json('saved_graph.json')
    end = time.time()
    print("load_graph time:", end - start, "seconds")
