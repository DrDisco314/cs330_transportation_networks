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
from statistics import mean
from dijkstar import Graph as DijkstarGraph, find_path, NoPathError
from src.graph import Graph as myGraph
from Algorithms.Dijkstra import Dijkstra
from Algorithms.CH import CH
from Algorithms.Arc_Flags import ArcFlags
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
        name = "Baghdad"
        graph_file = f"Data/{name}_Edgelist.csv"
        self.graph = myGraph()
        self.graph.read_from_csv_file(graph_file)
        self.myDijkstra = Dijkstra(self.graph)
        self.myCH = CH(graph_file)

        # Convert to Dijkstar graph
        """
        Citation: https://pypi.org/project/Dijkstar/
        Pre-existing Dijksta Algorithm to make sure our implentation is working the same.
        """
        self.dijkstar_graph = DijkstarGraph()
        for node, neighbors in self.graph.graph.items():
            for neighbor, weight in neighbors.items():
                self.dijkstar_graph.add_edge(node, neighbor, weight)

    def euclidean_distance(self, cur_node, end_node):
        x1, y1 = cur_node[0], cur_node[1]
        x2, y2 = end_node[0], end_node[1]
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    def a_star_cost_function(self, u, v, edge, prev_edge):
        if isinstance(edge, tuple):
            length, name = edge
        else:
            length = edge  # Only length is provided, no name
            name = None  # Default or dummy name

        if prev_edge and isinstance(prev_edge, tuple):
            prev_length, prev_name = prev_edge
        else:
            prev_name = None

        cost = length
        if name != prev_name:
            cost += 10  # Additional cost for changing routes or similar logic
        return cost

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
        start_list = [247191, 247202, 247132, 247072, 697284, 898404, 1057992]
        end_list = [298519, 298528, 45266, 12, 6, 8, 16, 18, 1, 2, 4]
        for start_node in start_list:
            for end_node in end_list:
                try:
                    dijkstrar_path_info = find_path(
                        self.dijkstar_graph, start_node, end_node
                    )
                    astar_path_info = find_path(
                        self.dijkstar_graph,
                        start_node,
                        end_node,
                        cost_func=self.a_star_cost_function,
                        heuristic_func=self.euclidean_distance
                    )
                    ch_path_info = self.myCH.find_shortest_path(
                        start_node, end_node)
                    self.assertIsNotNone(dijkstrar_path_info.nodes)
                    self.assertEqual(
                        self.myDijkstra.find_shortest_path(
                            start_node, end_node),
                        dijkstrar_path_info.nodes,
                        ch_path_info,
                    )
                    self.assertEqual(astar_path_info, dijkstrar_path_info)
                except NoPathError:
                    self.assertIsNone(
                        self.myDijkstra.find_shortest_path(
                            start_node, end_node)
                    )
                    self.assertIsNot(True, ch_path_info)

    def test_Algorithm_time(self):
        """
        Tests and prints the performance of our algorithms in milliseconds.
        Input:
            None
        Output:
            None.
        """

        print(
            "{:<15} {:<10} {:<10} {:<10}".format(
                "Path Length",
                "Dijkstar Time (ms)",
                "Contraction Heirachies (ms)",
                "A* (MS)",
            )
        )

        for i in range(1, 15):
            path_length = 0
            starting_node = 1
            ending_node = 1
            while path_length != 2**i:
                try:
                    ending_node += 1
                    # ch_start_time = time.time()
                    path_info = self.myCH.find_shortest_path(
                        starting_node, ending_node)
                    # ch_end_time = time.time()
                    path_length = len(path_info)

                except Exception as e:
                    starting_node += 1
                    # ending_node = starting_node + 1
                    continue
            dij_time_list = []
            ch_time_list = []
            astar_time_list = []
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

                astar_start_time = time.time()
                find_path(
                    self.dijkstar_graph,
                    starting_node,
                    ending_node,
                    cost_func=self.a_star_cost_function,
                )
                astar_end_time = time.time()
                astar_time = (astar_end_time - astar_start_time) * 1000
                astar_time_list.append(astar_time)

            print(
                "{:<15} {:<10.3f} {:<10.3f} {:<10.3f}".format(
                    path_length,
                    mean(dij_time_list),
                    mean(ch_time_list),
                    mean(astar_time_list),
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
