"""
    File:        transportation_network.py
    Author:      Alex Axton, Nathanial Field, Michael Scoleri
    Course:      CS 330 - Algorithms
    Semester:    Spring 2024
    Assignment:  Term Project: Transportation networks
    Description: Utilizes helper classes to execute Dijkstra Algorithm.
"""

from src.graph import Graph
from Algorithms.Dijkstra import Dijkstra


def main():
    graph_file = "road-chesapeake.mtx"
    start_node = 8
    end_node = 25

    graph = Graph()
    graph.read_from_mtx_file(graph_file)
    graph.visualize_graph()

    dijkstra = Dijkstra(graph)
    shortest_path = dijkstra.find_shortest_path(start_node, end_node)
    print(f"Shortest path from {start_node} to {end_node}: {shortest_path}")


if __name__ == "__main__":
    main()
