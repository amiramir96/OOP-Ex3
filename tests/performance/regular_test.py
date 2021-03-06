import time
from random import randint

from src.DiGraph import DiGraph
from src.GraphAlgo import GraphAlgo


def regular_test(nodes: int):
    nodes = nodes
    # build graph
    start = time.time()
    curr_graph = DiGraph()
    for i in range(nodes):
        curr_graph.add_node(i)
    all_nodes = curr_graph.get_all_v()
    for node in all_nodes:
        for i in range(20):
            curr_graph.add_edge(node, randint(0, nodes), randint(1, 12))
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
    algo.shortest_path(randint(0, nodes-1), randint(0, nodes-1))
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
        print("TSP time:", shortest_path_time * 21)  # (tsp_list input+1) * dijkstra times
    else:
        tsp_list = []
        i = 0
        while i < 20 and curr_graph.v_size() > 20:
            x = randint(0, nodes-1)
            if x not in tsp_list:
                i = i+1
                tsp_list.append(x)
        start = time.time()
        print("tsp list of nodes:", tsp_list)
        ans_tsp = algo.TSP(tsp_list)
        print("the ans of TSP is:", ans_tsp)
        end = time.time()
        print("TSP time:", end - start, "seconds")

    # save_graph
    start = time.time()
    algo.save_to_json(r'saved_graph.json')
    end = time.time()
    print("save_graph time:", end - start, "seconds")

    # load_graph
    start = time.time()
    algo.load_from_json(r'saved_graph.json')
    end = time.time()
    print("load_graph time:", end - start, "seconds")
