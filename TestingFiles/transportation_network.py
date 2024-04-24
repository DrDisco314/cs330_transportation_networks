"""
    File:        transportation_network.py
    Author:      Alex Axton, Nathanial Field, Michael Scoleri
    Course:      CS 330 - Algorithms
    Semester:    Spring 2024
    Assignment:  Term Project: Transportation networks
    Description: Utilizes helper classes to execute Dijkstra Algorithm.
"""
import sys
sys.path.append("../cs330_transportation_networks")
from src.graph import Graph
from Algorithms.Dijkstra import Dijkstra


def main():
    # graph_file = "Data/road-chesapeake.mtx"
    # start_node = 8
    # end_node = 25

    graph_file = "Data/NewYork_Edgelist.csv"
    start_node = 269071
    end_node = 809837

    graph = Graph()
    graph.read_from_csv_file(graph_file)
    # graph.read_from_mtx_file(graph_file)
    # graph.visualize_graph()

    dijkstra = Dijkstra(graph)
    shortest_path = dijkstra.find_shortest_path(start_node, end_node)
    print(f"Shortest path from {start_node} to {end_node}: {shortest_path}")


if __name__ == "__main__":
    main()
