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
from dijkstar import Graph as DijkstarGraph, find_path
from src.graph import Graph as myGraph
from Algorithms.Dijkstra import Dijkstra
import time


class TestGraphAndDijkstra(unittest.TestCase):
    def setUp(self):
        """
        Initialize the testing class.
        Input:
            None
        Return:
            None
        """
        graph_file = "Data/road-chesapeake.mtx"
        self.graph = myGraph()
        self.graph.read_from_mtx_file(graph_file)
        self.myDijkstra = Dijkstra(self.graph)

        # Convert to Dijkstar graph
        """
        Citation: https://pypi.org/project/Dijkstar/
        Pre-existing Dijksta Algorithm to make sure our implentation is working the same.
        """
        self.dijkstar_graph = DijkstarGraph()
        for node, neighbors in self.graph.graph.items():
            for neighbor, weight in neighbors.items():
                self.dijkstar_graph.add_edge(node, neighbor, weight)

    def test_graph_structure(self):
        """
        Test the graph class to ensure functioning as expected.
        Input:
            None
        Output:
            None
        """
        self.assertIn(32, self.graph.graph)
        self.assertIn(12, self.graph.graph[1])
        self.assertEqual(self.graph.graph[1][23], 22)

    def test_shortest_path(self):
        """
        Test to make sure existing Dijkstra is finding the same path for 150 different paths using Dijkstrar package.
        Input:
            None
        Output:
            None
        """
        start_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        end_list = [25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39]
        for start_node in start_list:
            for end_node in end_list:
                path_info = find_path(self.dijkstar_graph, start_node, end_node)
                self.assertIsNotNone(path_info.nodes)
                self.assertEqual(
                    self.myDijkstra.find_shortest_path(start_node, end_node),
                    path_info.nodes,
                )

    def test_dijkstra_time(self):
        """
        Tests and prints the performance of our Dijkstra algorithm in milliseconds.
        Input:
            None
        Output:
            None.
        """
        nodes_to_test = [2, 4, 8, 16, 32]
        start_node = 1
        print("{:<15} {:<15} {:<10}".format("Nodes", "Nodes Visited", "Time (ms)"))

        ### Redo with better graphs


if __name__ == "__main__":
    unittest.main()
