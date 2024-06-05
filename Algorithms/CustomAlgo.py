"""
    File:        Arc_Flags.py
    Author:      Michael Scoleri, Alex Axton, Nathanial Field
    Course:      CS 330 - Algorithms
    Semester:    Spring 2024
    Assignment:  Term Project: Transportation networks
    Description: Implements A star search on an Arc Flag, preprocessed graph.
"""

import math
import sys
import pickle
from dijkstar import Graph as astar_graph, find_path, NoPathError

sys.path.append("../cs330_transportation_networks")
from src.graph import Graph, Node, Edge

EMPIRICAL_HEURISTIC_CONSTANT = 1e10


def arc_flag_euclidean_distance(
    u: Node, v: Node, graph: Graph, target_index: int) -> float:
    """
    Calculate a heuristic cost of travelling from a current node, u, to a neighbor node, v,
    by making use of Euclidean distance and whether or not the arc flag from u to v is set.
    Input:
        u (Node) : Current node object being explored
        v (Node) : Neighbor node object being explored
        graph (Graph) : Arc flags graph object with preprocessed edges
        target_index (int) : Desired arc flag index to check if edge is on a shortest path
            to the region where the target node of the search lies
    Output:
        (float) : Euclidean Distance
    """
    # Get the edge object connecting u and v
    node_neighbors = graph.graph[u]
    desired_neighbor_edge = node_neighbors[v]

    # Decentivize A* picking edges where the arc flag leading to target region is false
    # by adding a large, empirically determined constant, when arc_flag[target_index] is false
    arc_flag_heuristic = (
        EMPIRICAL_HEURISTIC_CONSTANT
        if not desired_neighbor_edge.arc_flags[target_index]
        else 0
    )
    return (
        math.sqrt((v.xcoord - u.xcoord) ** 2 + (v.ycoord - u.ycoord) ** 2)
        + arc_flag_heuristic
    )


class CustomAlgo:
    def __init__(self, arc_flags_filename: str):
        """ "
        Initialize the CustomAlgo Class.
        Input:
            arc_flags_filename (str) : The path to the arc flags graph instance.
        Output:
            None.
        """
        self.arc_flags_filename = arc_flags_filename
        self.arc_flags_graph = self.load_arc_flags()
        self.dijkstar_graph = self.build_dijkstar_graph()

    def load_arc_flags(self):
        """
        Load the arc flags graph instance.
        Input:
            None.
        Output:
            None.
        """
        with open(self.arc_flags_filename, "rb") as file:
            return pickle.load(file)

    def build_dijkstar_graph(self):
        """
        Constructs the Dijkstar graph, only using arc flag edges.
        Input:
            None.
        Output:
            None.
        """
        dijkstar_graph = astar_graph()
        num_partitions = self.arc_flags_graph.num_partitions_axis

        for node in self.arc_flags_graph.graph:
            for neighbor, edge in self.arc_flags_graph.get_neighbors(node).items():
                neighbor_region_index = neighbor.region[0] + (
                    neighbor.region[1] * num_partitions
                )
                if edge.arc_flags[neighbor_region_index]:
                    dijkstar_graph.add_edge(node, neighbor, {"cost": edge.weight})

        return dijkstar_graph
    
    def cost_function(self, u, v, edge, prev_edge):
        """
        Return the cost of the edge.
        Inputs:
            u (Node) : Source Node.
            v (Node) : Neighbor Node.
            e (any) : Current Edge.
            prev_e (any) : previous edge.
        Output:
            (Float) : cost of edge between U and V.
        """
        # print(f"edge: {edge}")
        # print(f"{self.euclidean_distance(u, v, None, None)}")
        return math.sqrt((v.xcoord - u.xcoord) ** 2 + (v.ycoord - u.ycoord) ** 2)

    def find_shortest_path(self, start_node: Node, end_node: Node):
        """
        Find and return the shortest path between 2 nodes.
        Input:
            Start_node (Node) : Starting node.
            end_node (Node) : Destination node.
        Output:
            (PathInfo) : Dijkstar Type containing shortest path, or None.
        """
        # Get number of partitions in graph and use to determine the arc flag index of target node
        num_partitions = self.arc_flags_graph.num_partitions_axis
        target_node_region_index = end_node.region[0] + (
            end_node.region[1] * num_partitions
        )

        def heuristic_func(u, v, edge, prev_edge):
            return arc_flag_euclidean_distance(
                u, v, self.arc_flags_graph, target_node_region_index
            )

        # Run dijkstra with a cost and heuristic function - making this A*
        try:
            return find_path(
                self.dijkstar_graph,
                start_node,
                end_node,
                cost_func=self.cost_function,
                heuristic_func=heuristic_func,
            )
        except NoPathError:
            return None
