"""
    File:        transportation_network.py
    Author:      Alex Axton, Nathanial Field, Michael Scoleri
    Course:      CS 330 - Algorithms
    Semester:    Spring 2024
    Assignment:  Term Project: Transportation networks
    Description: Implements a brute force solution to the
      transportation network routing problem using Dijkstra's algorithm.
"""

from graph import Graph
from Dijkstra import Dijkstra


def main():
    graph_file = "road-chesapeake.mtx"
    start_node = 1
    end_node = 32

    graph = Graph()
    graph.read_from_mtx_file(graph_file)
    graph.visualize_graph()

    dijkstra = Dijkstra(graph)
    dijkstra.compute_shortest_paths(start_node)

    shortest_path = dijkstra.get_shortest_path(end_node)
    print(f"Shortest path from {start_node} to {end_node}: {shortest_path}")


if __name__ == "__main__":
    main()
