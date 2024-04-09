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
from dijkstar import Graph as DijkstarGraph, find_path, NoPathError
from src.graph import Graph as myGraph
from Algorithms.Dijkstra import Dijkstra
from Algorithms.CH import CH
import time


class TestGraphAndDijkstra(unittest.TestCase):
    def setUp(self):
        """
        Initialize the testing suite.
        Input:
            None
        Return:
            None
        """
        graph_file = "Data/NewYork_Edgelist.csv"
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
                    ch_path_info = self.myCH.find_shortest_path(start_node, end_node)
                    self.assertIsNotNone(dijkstrar_path_info.nodes)
                    self.assertEqual(
                        self.myDijkstra.find_shortest_path(start_node, end_node),
                        dijkstrar_path_info.nodes,
                        ch_path_info,
                    )
                except NoPathError:
                    self.assertIsNone(
                        self.myDijkstra.find_shortest_path(start_node, end_node)
                    )
                    self.assertIsNot(True, ch_path_info)

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
