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
        Initialize the testing suite.
        Input:
            None
        Return:
            None
        """
        name = "Surat"
        graph_file = f"Data/{name}_Edgelist.csv"
        self.graph = myGraph()
        self.graph.read_from_csv_file(graph_file)
        self.myDijkstra = Dijkstra(self.graph)
        self.myCH = CH(graph_file)

        arc_flag_file = f"ArcFlagInstances/{name}_object.pkl"
        with open(arc_flag_file, "rb") as file:
            arc_flag_graph = pickle.load(file)
        self.arc_flags = ArcFlags(arc_flag_graph)

        # Convert to Dijkstar graph
        """
        Citation: https://pypi.org/project/Dijkstar/
        Pre-existing Dijksta Algorithm to make sure our implentation is working the same.
        """
        self.node_graph = myGraph()
        self.node_graph.num_partitions_axis = 2
        self.node_graph.read_from_csv_file_node(graph_file)

        self.dijkstar_graph = DijkstarGraph()
        for node, neighbors in self.node_graph.graph.items():
            for neighbor, weight in neighbors.items():
                self.dijkstar_graph.add_edge(node, neighbor, weight.weight)

        self.custom_algo = CustomAlgo(arc_flag_file)

    def euclidean_distance(self, u: Node, v: Node, e, prev_e):
        x1, y1 = u.xcoord, u.ycoord
        x2, y2 = v.xcoord, v.ycoord
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def a_star_cost_function(self, u, v, edge, prev_edge):
        return edge

    def test_graph_structure(self):
        """
        Test the graph class to ensure functioning as expected.
        Input:
            None
        Output:
            None
        """
        self.assertIn(805200, self.graph.graph)
        self.assertIn(2, self.graph.graph[1])
        self.assertEqual(self.graph.graph[1][2], 14.570863)

    def test_shortest_path(self):
        """
        Test to make sure existing Dijkstra is finding the same path for 150 different paths using Dijkstrar package.
        Input:
            None
        Output:
            None
        """
        start_list = [1, 2, 4, 5, 10, 11, 12, 13, 15, 16, 20, 21]
        end_list = [122, 134, 131, 135, 208, 213, 216, 268]
        no_path = 0
        for start_node in start_list:
            for end_node in end_list:
                try:
                    mydijkstra = self.myDijkstra.find_shortest_path(
                        start_node, end_node
                    )

                    node1 = self.node_graph.return_node(start_node)
                    node2 = self.node_graph.return_node(end_node)
                    dijkstrar_path_info = find_path(self.dijkstar_graph, node1, node2)
                    dijkstrar_path_info = [
                        item.value for item in dijkstrar_path_info[0]
                    ]

                    astar_path_info = find_path(
                        self.dijkstar_graph,
                        node1,
                        node2,
                        cost_func=self.a_star_cost_function,
                        heuristic_func=self.euclidean_distance,
                    )
                    astar_path_info = [item.value for item in astar_path_info[0]]

                    ch_path_info = self.myCH.find_shortest_path(start_node, end_node)

                    node1 = self.arc_flags.graph.return_node(start_node)
                    node2 = self.arc_flags.graph.return_node(end_node)
                    arc_flag_path = self.arc_flags.arc_flags_dijkstra(node1, node2)
                    arc_flag_path = [item.value for item in arc_flag_path]

                    custom_algo_path = self.custom_algo.find_shortest_path(
                        start_node, end_node
                    )
                    custom_algo_path = [item.value for item in custom_algo_path[0]]

                    self.assertIsNotNone(dijkstrar_path_info)

                    self.assertTrue(
                        all(a == b for a, b in zip(mydijkstra, dijkstrar_path_info))
                    )
                    self.assertTrue(
                        all(a == b for a, b in zip(ch_path_info, dijkstrar_path_info))
                    )
                    self.assertTrue(
                        all(a == b for a, b in zip(arc_flag_path, dijkstrar_path_info))
                    )
                    self.assertTrue(
                        all(
                            a == b for a, b in zip(astar_path_info, dijkstrar_path_info)
                        )
                    )
                    self.assertTrue(
                        all(
                            a == b
                            for a, b in zip(custom_algo_path, dijkstrar_path_info)
                        )
                    )

                except NoPathError:
                    no_path += 1
                    self.assertIsNone(
                        self.myDijkstra.find_shortest_path(start_node, end_node)
                    )
                    self.assertIsNot(True, ch_path_info)

        print(
            f"Out of {len(start_list) * len(end_list)}, possible routes, {no_path} had no path."
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
        ]
        header_format = "{:<15} {:<20} {:<25} {:<10} {:<15}"
        print(header_format.format(*headers))

        for i in range(1, 15):
            path_length = 0
            starting_node = 1
            ending_node = 1
            while path_length != 2**i:
                try:
                    ending_node += 1
                    path_info = self.myCH.find_shortest_path(starting_node, ending_node)
                    path_length = len(path_info)

                except Exception as e:
                    starting_node += 1
                    continue
            dij_time_list = []
            ch_time_list = []
            astar_time_list = []
            arc_flags_time_list = []
            for j in range(5):
                dij_start_time = time.time()
                self.myDijkstra.find_shortest_path(starting_node, ending_node)
                dij_end_time = time.time()
                dij_time = (dij_end_time - dij_start_time) * 1000
                dij_time_list.append(dij_time)

                ch_start_time = time.time()
                self.myCH.find_shortest_path(starting_node, ending_node)
                ch_end_time = time.time()
                ch_time = (ch_end_time - ch_start_time) * 1000
                ch_time_list.append(ch_time)

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

                node1 = self.arc_flags.graph.return_node(starting_node)
                node2 = self.arc_flags.graph.return_node(ending_node)
                arc_flags_start_time = time.time()
                self.arc_flags.arc_flags_dijkstra(node1, node2)
                arc_flags_end_time = time.time()
                arc_flags_time = (arc_flags_end_time - arc_flags_start_time) * 1000
                arc_flags_time_list.append(arc_flags_time)

            data = [
                path_length,
                mean(dij_time_list),
                mean(ch_time_list),
                mean(astar_time_list),
                mean(arc_flags_time_list),
            ]
            print(
                header_format.format(
                    path_length,
                    f"{mean(dij_time_list):.3f}",
                    f"{mean(ch_time_list):.3f}",
                    f"{mean(astar_time_list):.3f}",
                    f"{mean(arc_flags_time_list):.3f}",
                )
            )


if __name__ == "__main__":
    # All tests:
    # unittest.main()

    # Specfic Tests:
    # suite = unittest.TestSuite()
    # suite.addTest(TestGraphAndDijkstra("test_Algorithm_time"))
    # runner = unittest.TextTestRunner()
    # runner.run(suite)

    suite = unittest.TestSuite()
    suite.addTest(TestGraphAndDijkstra("test_shortest_path"))
    runner = unittest.TextTestRunner()
    runner.run(suite)
