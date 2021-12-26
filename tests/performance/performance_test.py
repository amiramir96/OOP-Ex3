from tests.performance.compare_test import compare_test
from tests.performance.regular_test import regular_test


def main():
    # get input of nodes
    nodes = 0
    nodes = input(
        'hi dear user, if u would like to run the COMPARASION test:\n -> testing in compare to the java project, press 0\nfor regular perforamnce test:\n please input NATURAL amount of node - BE AWARE, for every node there is gonna be 20 '
        'out edges.\n')
    if int(nodes) == 0:
        print("100 nodes graph in python results:\n")
        compare_test(100)
        print()
        print("1K nodes graph in python results:\n")
        compare_test(1000)
        print()
        print("10K nodes graph in python results:\n")
        compare_test(10000)
        print()
        print("100K nodes graph in python results:\n")
        print()
        compare_test(100000)
        print("1M nodes graph in python results:\n")
        regular_test(1000000)
    else:
        regular_test(int(nodes))


if __name__ == '__main__':
    main()
