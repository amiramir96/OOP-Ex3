from src import GraphAlgo
import sys


def main(path):
    g = GraphAlgo.GraphAlgo(path)
    g.plot_graph()


if __name__ == '__main__':
    if len(sys.argv) == 1:
        main('data\\A1.json')
    else:
        main(sys.argv[1])
