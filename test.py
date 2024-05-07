"""
    File:        test.py
    Author:      Alex Axton, Nathanial Field, Michael Scoleri
    Course:      CS 330 - Algorithms
    Semester:    Spring 2024
    Assignment:  Term Project: Transportation networks
    Description: Implements the unittest and dijkstrar package to run unit tests on the graph
                and dijkstra implementation. 
"""

import unittest
import pickle
from statistics import mean
from dijkstar import Graph as DijkstarGraph, find_path, NoPathError
from src.graph import Graph as myGraph
from src.graph import Node
from Algorithms.Dijkstra import Dijkstra
from Algorithms.CH import CH
from Algorithms.Arc_Flags import *
from Algorithms.CustomAlgo import CustomAlgo
import time
import math


class TestGraphAndDijkstra(unittest.TestCase):
    def setUp(self):
        """
        Initialize the testing suite and all 5 algorithms.
        Input:
            None
        Return:
            None
        """
        self.name = "Surat"
        num = "3"
        graph_file = f"Data/{self.name}_Edgelist.csv"
        self.graph = myGraph()
        self.graph.read_from_csv_file(graph_file)
        self.myDijkstra = Dijkstra(self.graph)
        self.myCH = CH(graph_file)

        arc_flag_file = f"ArcFlagInstances/{self.name}_{num}_object.pkl"
        with open(arc_flag_file, "rb") as file:
            arc_flag_graph = pickle.load(file)
        self.arc_flags = ArcFlags(arc_flag_graph)

        # Convert to Dijkstar graph
        """
        Citation: https://pypi.org/project/Dijkstar/
        Pre-existing Dijksta Algorithm to make sure our implentation is working the same.
        """
        self.node_graph = myGraph()
        self.node_graph.num_partitions_axis = 3
        self.node_graph.read_from_csv_file_node(graph_file)

        self.dijkstar_graph = DijkstarGraph()
        for node, neighbors in self.node_graph.graph.items():
            for neighbor, weight in neighbors.items():
                self.dijkstar_graph.add_edge(node, neighbor, weight.weight)

        self.custom_algo = CustomAlgo(arc_flag_file)

    def euclidean_distance(self, u: Node, v: Node, e, prev_e):
        """
        Calculates the Euclidean distance between 2 nodes.
        Inputs:
            u (Node) : Source Node.
            v (Node) : Neighbor Node.
            e (any) : Current Edge.
            prev_e (any) : previous edge.
        Output:
            (Float) : Euclidean distance between U and V.
        """
        x1, y1 = u.xcoord, u.ycoord
        x2, y2 = v.xcoord, v.ycoord
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def a_star_cost_function(self, u, v, edge, prev_edge):
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
        return edge

    def test_graph_structure(self):
        """
        Test the graph class to ensure functioning as expected (ONLY FOR NEW YORK).
        Input:
            None
        Output:
            None
        """
        if self.name == "NewYork":
            self.assertIn(805200, self.graph.graph)
            self.assertIn(2, self.graph.graph[1])
            self.assertEqual(self.graph.graph[1][2], 14.570863)
        else:
            self.assertIsNone(None)

    def test_shortest_path(self):
        """
        Test to make sure existing Dijkstra is finding the same path for 96 different paths using Dijkstrar package
        on the Surat Graph. Uses assert functions to confirm correctness.
        Input:
            None
        Output:
            None
        """
        if self.name != "Surat":
            self.assertIsNone(None)
            return
        start_list = [1, 2, 4, 5, 10, 11, 12, 13, 15, 16, 20, 21]
        end_list = [122, 134, 131, 135, 208, 213, 216, 268]
        no_path = 0
        for start_node in start_list:
            for end_node in end_list:
                try:
                    # Find path using our version of Dijkstra
                    mydijkstra = self.myDijkstra.find_shortest_path(
                        start_node, end_node
                    )

                    # Find path using Dijkstar Dikjstra
                    node1 = self.node_graph.return_node(start_node)
                    node2 = self.node_graph.return_node(end_node)
                    dijkstrar_path_info = find_path(self.dijkstar_graph, node1, node2)
                    dijkstrar_path_info = [
                        item.value for item in dijkstrar_path_info[0]
                    ]

                    # Find path using A*
                    astar_path_info = find_path(
                        self.dijkstar_graph,
                        node1,
                        node2,
                        cost_func=self.a_star_cost_function,
                        heuristic_func=self.euclidean_distance,
                    )
                    astar_path_info = [item.value for item in astar_path_info[0]]

                    # Find Path using Contraction Hierarchies
                    ch_path_info = self.myCH.find_shortest_path(start_node, end_node)

                    # Find path using arc flags
                    node1 = self.arc_flags.graph.return_node(start_node)
                    node2 = self.arc_flags.graph.return_node(end_node)
                    arc_flag_path = self.arc_flags.arc_flags_dijkstra(node1, node2)
                    arc_flag_path = [item.value for item in arc_flag_path]

                    # Find path using custom algorithm.
                    node1 = self.custom_algo.arc_flags_graph.return_node(start_node)
                    node2 = self.custom_algo.arc_flags_graph.return_node(end_node)
                    custom_algo_path = self.custom_algo.find_shortest_path(node1, node2)
                    custom_algo_path = [item.value for item in custom_algo_path[0]]

                    # Confirm a path exists.
                    self.assertIsNotNone(dijkstrar_path_info)

                    # Use multiple asserts to confirm that each path found is indentical.
                    self.assertTrue(
                        all(a == b for a, b in zip(mydijkstra, dijkstrar_path_info)),
                        "Dijkstra Failed",
                    )
                    self.assertTrue(
                        all(a == b for a, b in zip(ch_path_info, dijkstrar_path_info)),
                        "CH Failed",
                    )
                    self.assertTrue(
                        all(a == b for a, b in zip(arc_flag_path, dijkstrar_path_info)),
                        "Arc Flags Failed",
                    )
                    self.assertTrue(
                        all(
                            a == b for a, b in zip(astar_path_info, dijkstrar_path_info)
                        ),
                        "A star Failed",
                    )
                    self.assertTrue(
                        all(
                            a == b
                            for a, b in zip(custom_algo_path, dijkstrar_path_info)
                        ),
                        "Custom Algo Failed",
                    )

                except NoPathError:
                    no_path += 1
                    self.assertIsNone(
                        self.myDijkstra.find_shortest_path(start_node, end_node)
                    )
                    self.assertIsNot(True, ch_path_info)

        print("\n")
        print(
            f"Out of {len(start_list) * len(end_list)} possible routes, {no_path} had no path."
        )

    def test_Algorithm_time(self):
        """
        Tests and prints the performance of our algorithms in milliseconds.
        Input:
            None
        Output:
            None.
        """

        headers = [
            "Path Length",
            "Dijkstar Time (ms)",
            "Contraction Hierarchies (ms)",
            "A* (ms)",
            "Arc Flags (ms)",
            "Custom Algo (ms)",
        ]
        header_format = "{:<15} {:<20} {:<25} {:<10} {:<15} {:<15}"
        print("\n")
        print(header_format.format(*headers))
        dij_time_list = []
        ch_time_list = []
        astar_time_list = []
        arc_flags_time_list = [0]
        Custom_algo_time_list = [0]

        # Find a path up to size 64.
        for i in range(1, 7):
            path_length = 0
            starting_node = 1
            ending_node = 1

            # Use contraction heirarchies to find a path of desired length.
            while path_length != 2**i:
                try:
                    ending_node += 1
                    path_info = self.myCH.find_shortest_path(starting_node, ending_node)
                    path_length = len(path_info)

                except Exception as e:
                    starting_node += 1
                    continue

            # Find the same path 5 times.
            for j in range(5):
                # Test Dijkstra
                dij_start_time = time.time()
                self.myDijkstra.find_shortest_path(starting_node, ending_node)
                dij_end_time = time.time()
                dij_time = (dij_end_time - dij_start_time) * 1000
                dij_time_list.append(dij_time)

                # Test Contraction Heirachy
                ch_start_time = time.time()
                self.myCH.find_shortest_path(starting_node, ending_node)
                ch_end_time = time.time()
                ch_time = (ch_end_time - ch_start_time) * 1000
                ch_time_list.append(ch_time)

                # Test A*
                node1 = self.node_graph.return_node(starting_node)
                node2 = self.node_graph.return_node(ending_node)
                astar_start_time = time.time()
                find_path(
                    self.dijkstar_graph,
                    node1,
                    node2,
                    cost_func=self.a_star_cost_function,
                )
                astar_end_time = time.time()
                astar_time = (astar_end_time - astar_start_time) * 1000
                astar_time_list.append(astar_time)

                # Test Arc Flags
                node1 = self.arc_flags.graph.return_node(starting_node)
                node2 = self.arc_flags.graph.return_node(ending_node)
                arc_flags_start_time = time.time()
                self.arc_flags.arc_flags_dijkstra(node1, node2)
                arc_flags_end_time = time.time()
                arc_flags_time = (arc_flags_end_time - arc_flags_start_time) * 1000
                arc_flags_time_list.append(arc_flags_time)

                # Test custom algorithm
                node1 = self.custom_algo.arc_flags_graph.return_node(starting_node)
                node2 = self.custom_algo.arc_flags_graph.return_node(ending_node)
                custom_algo_start_time = time.time()
                self.custom_algo.find_shortest_path(node1, node2)
                custom_algo_end_time = time.time()
                custom_algo_time = (
                    custom_algo_end_time - custom_algo_start_time
                ) * 1000
                Custom_algo_time_list.append(custom_algo_time)

            data = [
                path_length,
                mean(dij_time_list),
                mean(ch_time_list),
                mean(astar_time_list),
                mean(arc_flags_time_list),
                mean(Custom_algo_time_list),
            ]
        print(
            header_format.format(
                path_length,
                f"{mean(dij_time_list):.3f}",
                f"{mean(ch_time_list):.3f}",
                f"{mean(astar_time_list):.3f}",
                f"{mean(arc_flags_time_list):.3f}",
                f"{mean(Custom_algo_time_list):.3f}",
            )
        )


if __name__ == "__main__":
    # All tests:
    # unittest.main()

    # Specfic Tests:
    suite = unittest.TestSuite()
    suite.addTest(TestGraphAndDijkstra("test_Algorithm_time"))
    runner = unittest.TextTestRunner()
    runner.run(suite)

    suite = unittest.TestSuite()
    suite.addTest(TestGraphAndDijkstra("test_shortest_path"))
    runner = unittest.TextTestRunner()
    runner.run(suite)
