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
from src.graph import Node

sys.path.append("../cs330_transportation_networks")


def euclidean_distance(x1: float, y1: float, x2: float, y2: float):
    """
    Calculate the Euclidean distance between 2 points.
    Input:
        x1 (float) : x coordinate of point 1.
        y1 (float) : y coordinate of point 1.
        x2 (float) : x coordinate of point 2.
        y2 (float) : y coordinate of point 2.
    Output:
        (float) : Euclidean Distance
    """
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


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

    def find_shortest_path(self, start_node: Node, end_node: Node):
        """
        Find and return the shortest path between 2 nodes.
        Input:
            Start_node (Node) : Starting node.
            end_node (Node) : Destination node.
        Output:
            (PathInfo) : Dijkstar Type containing shortest path, or None.
        """

        def heuristic_func(u, v, edge, prev_edge):
            return euclidean_distance(u.xcoord, u.ycoord, v.xcoord, v.ycoord)

        try:
            cost_func = lambda u, v, edge, prev_edge: edge["cost"]
            return find_path(
                self.dijkstar_graph,
                start_node,
                end_node,
                cost_func=cost_func,
                heuristic_func=heuristic_func,
            )
        except NoPathError:
            return None


# def main():
#     custom_algo = CustomAlgo("ArcFlagInstances/Surat_object.pkl")
#     start_node_id = 1
#     end_node_id = 25
#     path_info = custom_algo.find_shortest_path(start_node_id, end_node_id)
#     for node in path_info[0]:
#         print(node.value)
#     print("Path info:", path_info)


# if __name__ == "__main__":
#     main()
