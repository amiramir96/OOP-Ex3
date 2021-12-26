import random
from src import GraphInterface


def key_transform(node_id: int):
    """
    :param node_id: index of relevant node in the graph
    :return: node_id modulo 1000
    """
    return node_id % 1000


class DiGraph(GraphInterface.GraphInterface):
    """
        fields:
        node_map - dict of dicts of nodes (look for logic block to understand mechanic)
        edge_out_map - dict of dicts of dicts of the out edges of the curr node
        edge_in_map - dict of dicts of dicts of the in edges of the curr node
        mc - mode counter, count the changes over the graph
        node/edge _size - total amount of nodes/edges in the graph

        logic implementation:
        this class reprsenets directed weighted graph
        the inner struct of the class hold few Dimensions of data:
            1- 1st dim: dict of dicts, numbered within 0 to 999 keys, represent ea node_id modolu 1000 (src node_id for edges struct)
            2- 2nd dim: represent ea node_id which is unique
            3- 3rd dim(for edge structs): holds for ea node_id -> dict of all relevant edge
        this way of stocking data let us to SUPPORT millions of objects with far less heap capacity suppliy
        for example: graph with 20m edges (demands 2 dicts of 20m in 1 dimension) will cost 1.5gb~2.2gb approximate ram
                        BUT, with our struct strategy the cost of the same graph will drop to around 250mb ram (approximat)
            why is this gap? read more about hashtable and its demands to support an O(1) add,remove,contains funcs.
    """

    def __init__(self):
        self.node_map = {}
        self.edge_out_map = {}
        self.edge_in_map = {}
        for i in range(1000):
            self.node_map[i] = {}
            self.edge_out_map[i] = {}
            self.edge_in_map[i] = {}
        self.mc = 0
        self.node_size = 0
        self.edge_size = 0

    def v_size(self) -> int:
        """
        Returns the number of vertices in this graph
        @return: The number of vertices in this graph
        """
        return self.node_size

    def e_size(self) -> int:
        """
        Returns the number of edges in this graph
        @return: The number of edges in this graph
        """
        return self.edge_size

    def get_all_v(self) -> dict:
        """
        return a dictionary of all the nodes in the Graph, each node is represented using a pair
        (node_id, node_data)
        """
        all_node_dict = {}
        for dict_of_nodes in self.node_map.values():
            # all_node_dict = {**all_node_dict, **dict_of_nodes}
            for node in dict_of_nodes.items():
                all_node_dict[node[0]] = node
        return all_node_dict

    def all_in_edges_of_node(self, id1: int) -> dict:
        """return a dictionary of all the nodes connected to (into) node_id ,
        each node is represented using a pair (other_node_id, weight)
         """
        in_edges_dict = {}
        if id1 in self.edge_in_map.get(key_transform(id1)):
            for edge in self.edge_in_map.get(key_transform(id1)).get(id1).items():
                in_edges_dict[edge[0]] = edge[1]
        return in_edges_dict

    def all_out_edges_of_node(self, id1: int) -> dict:
        """return a dictionary of all the nodes connected from node_id , each node is represented using a pair
        (other_node_id, weight)
        """
        out_edges_dict = {}
        if id1 in self.edge_out_map.get(key_transform(id1)):
            for edge in self.edge_out_map.get(key_transform(id1)).get(id1).items():
                out_edges_dict[edge[0]] = edge[1]
        return out_edges_dict

    def get_mc(self) -> int:
        """
        Returns the current version of this graph,
        on every change in the graph state - the MC should be increased
        @return: The current version of this graph.
        """
        return self.mc

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        """
        Adds an edge to the graph.
        @param id1: The start node of the edge
        @param id2: The end node of the edge
        @param weight: The weight of the edge
        @return: True if the edge was added successfully, False o.w.
        Note: If the edge already exists or one of the nodes dose not exists the functions will do nothing
        """
        # check if there is no way that edge is existing between the two nodes
        if id1 not in self.node_map.get(key_transform(id1)) or id2 not in self.node_map.get(key_transform(id2)):
            return False
        if id1 in self.edge_out_map.get(key_transform(id1)):
            if id2 in self.edge_out_map.get(key_transform(id1)).get(id1):
                # last nested if is to check if there is already edge between the two nodes
                # no need to check opposite case since both of maps is simetric
                return False

        # create new dict if there was not edge out for the relevant node
        if id1 not in self.edge_out_map.get(key_transform(id1)):
            self.edge_out_map.get(key_transform(id1))[id1] = {}
        # create new dict if there was not edge in for the relevant node
        if id2 not in self.edge_in_map.get(key_transform(id2)):
            self.edge_in_map.get(key_transform(id2))[id2] = {}

        # add correctly
        self.edge_out_map.get(key_transform(id1)).get(id1)[id2] = weight
        self.edge_in_map.get(key_transform(id2)).get(id2)[id1] = weight
        # edit inner vars
        self.mc = self.mc + 1
        self.edge_size = self.edge_size + 1
        return True

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        """
        Adds a node to the graph.
        @param node_id: The node ID
        @param pos: The position of the node
        @return: True if the node was added successfully, False o.w.
        Note: if the node id already exists the node will not be added
        """
        if pos is None:
            # if no pos input, lets rand it! <3
            pos = (round(random.uniform(0, 50), 4), round(random.uniform(0, 50), 4), 0.0)
        if node_id in self.node_map.get(key_transform(node_id)):  # always point first to the inner relevant dict
            return False
        self.node_map.get(key_transform(node_id))[node_id] = pos  # add currectly
        # edit inner vars
        self.mc = self.mc + 1
        self.node_size = self.node_size + 1
        return True

    def remove_node(self, node_id: int) -> bool:
        """
        Removes a node from the graph.
        @param node_id: The node ID
        @return: True if the node was removed successfully, False o.w.
        Note: if the node id does not exists the function will do nothing
        """
        """
            3 phases:
            1- loop over all the out_edges of the curr nodes and remove them from the in_edges struct
            2- loop over all the in_edges of the curr nodes and remove them from the out_edges struct
            3- edit inner vars
        """
        if node_id not in self.node_map.get(key_transform(node_id)):
            # node is not exisiting in the graph
            return False
        # phase 1
        i = 0
        # add to list all the relevant edge that shall be removed
        # this way - avoid from RuntimeError: dictionary changed size during iteration
        removal_list = []
        if self.edge_out_map.get(key_transform(node_id)).get(node_id) is not None:
            for out_edge_dest in self.edge_out_map.get(key_transform(node_id)).get(node_id).keys():
                removal_list.append(out_edge_dest)
                i = i+1
            for dest_edge in removal_list:
                self.remove_edge(node_id, dest_edge)
        # phase 2
        j = 0
        removal_list = []
        if self.edge_in_map.get(key_transform(node_id)).get(node_id) is not None:
            for in_edge_src in self.edge_in_map.get(key_transform(node_id)).get(node_id).keys():
                removal_list.append(in_edge_src)
                j = j+1
            for in_edge in removal_list:
                self.remove_edge(in_edge, node_id)
        # phase 3
        del self.node_map.get(key_transform(node_id))[node_id]
        self.mc = self.mc + 1
        self.node_size = self.node_size - 1
        return True

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        """
        Removes an edge from the graph.
        @param node_id1: The start node of the edge
        @param node_id2: The end node of the edge
        @return: True if the edge was removed successfully, False o.w.
        Note: If such an edge does not exists the function will do nothing
        """
        # one of the nodes is not exists in the graph, just return false
        if node_id1 not in self.node_map.get(key_transform(node_id1)) or node_id2 not in self.node_map.get(
                key_transform(node_id2)):
            return False

        # both of the nodes exists but one of the dont even have edges!
        if node_id1 not in self.edge_out_map.get(key_transform(node_id1)) or node_id2 not in self.edge_in_map.get(key_transform(node_id2)):
            return False

        # there is no edge existing between both of the nodes
        # check only one of the maps is fine since we work symmetry
        if node_id2 not in self.edge_out_map.get(key_transform(node_id1)).get(node_id1):
            return False

        # otherwise, remove the relevant edge
        # if its the last edge of the currect node, remove also its dict
        if len(self.edge_out_map.get(key_transform(node_id1)).get(node_id1)) == 1:
            # last edge
            del self.edge_out_map.get(key_transform(node_id1))[node_id1]
        else:
            # is not the last
            del self.edge_out_map.get(key_transform(node_id1)).get(node_id1)[node_id2]

        if len(self.edge_in_map.get(key_transform(node_id2)).get(node_id2).items()) == 1:
            # last edge
            del self.edge_in_map.get(key_transform(node_id2))[node_id2]
        else:
            # is not the last
            del self.edge_in_map.get(key_transform(node_id2)).get(node_id2)[node_id1]
        # edit inner vars
        self.mc = self.mc + 1
        self.edge_size = self.edge_size - 1
        return True

    def __repr__(self):
        print_dict = {}
        all_nodes = self.get_all_v()
        for node in all_nodes.keys():
            x = {node: (self.all_out_edges_of_node(node), len(self.all_out_edges_of_node(node).keys()),
                        self.all_in_edges_of_node(node), len(self.all_in_edges_of_node(node)))}
            print_dict[node] = x
        return str(print_dict)

# def run():
#     g = DiGraph()
#     print(g.mc)
#
# if __name__ == '__main__':
#     DiGraph()

