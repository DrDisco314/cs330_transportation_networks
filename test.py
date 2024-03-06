import unittest
from dijkstar import Graph as DijkstarGraph, find_path
from graph import Graph as myGraph
from Dijkstra import Dijkstra


class TestGraphAndDijkstra(unittest.TestCase):
    def setUp(self):
        graph_file = "road-chesapeake.mtx"
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
        # Test basic graph structure assertions
        self.assertIn(32, self.graph.graph)
        self.assertIn(12, self.graph.graph[1])
        self.assertEqual(self.graph.graph[1][23], 22)

    def test_shortest_path(self):
        # Test to make sure existing Dijkstra is finding the same path for 110 different paths.
        start_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        end_list = [25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]
        for start_node in start_list:
            for end_node in end_list:
                self.myDijkstra.compute_shortest_paths(start_node)
                path_info = find_path(self.dijkstar_graph, start_node, end_node)
                self.assertIsNotNone(path_info.nodes)
                self.assertEqual(
                    self.myDijkstra.get_shortest_path(end_node), path_info.nodes
                )


if __name__ == "__main__":
    unittest.main()
