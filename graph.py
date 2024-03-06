"""
    File:        graph.py
    Author:      Alex Axton, Nathanial Field, Michael Scoleri
    Course:      CS 330 - Algorithms
    Semester:    Spring 2024
    Assignment:  Term Project: Transportation networks
    Description: Implements the Graph class to create a data structure from a file. The data structure
                can be used with any shortest path algorithm.
"""

import networkx as nx
import matplotlib.pyplot as plt


class Graph:
    def __init__(self):
        """
        Initialize the Graph Class.
        Input:
            None
        Return:
            None
        """
        self.graph = {}

    def add_edge(self, node1: int, node2: int, weight: int):
        """
        Adds the edge from one node to another.
        Input:
            Node1 (int) : Integer representing first node.
            Node2 (int) : Intger representing second node
            weight (int) : Integer representing weight of edge from 2 nodes.
        Return:
            None
        """
        if node1 not in self.graph:
            self.graph[node1] = {}
        if node2 not in self.graph:
            self.graph[node2] = {}
        self.graph[node1][node2] = weight
        self.graph[node2][node1] = weight

    def read_from_mtx_file(self, filename: str):
        """
        Reads in a file in the form of matrix where nodes are in the same line. Weight is the abs(node1-node2)
        Input:
            filename (str) : Filename as a string
        Return:
            None
        """
        try:
            with open(filename, "r") as file:
                for line in file:
                    if line.startswith("%"):
                        continue
                    parts = line.split()

                    if len(parts) == 2 or len(parts) == 3:
                        node1, node2 = int(parts[0]), int(parts[1])
                        weight = abs(node1 - node2)
                        self.add_edge(node1, node2, weight)
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def get_neighbors(self, node: int) -> dict:
        """
        Returns the neighbors of a given node. Will return an empty dictionary if no neioghbors exists.
        Input:
            node (int) : Integer representing node to find neighbors for.
        Return:
            Dictionary with all neighbors as key and weights as value
        """
        return self.graph.get(node, {})

    def visualize_graph(self):
        """
        Visualize the current graph using the NetworkX package.
        Input:
            None
        Return:
            None
        """

        """Citation: https://networkx.org/
        Package for visualizing a weighted graph
        """
        G = nx.Graph()
        for node, neighbors in self.graph.items():
            for neighbor, weight in neighbors.items():
                G.add_edge(node, neighbor, weight=weight)

        pos = nx.spring_layout(G)
        nx.draw_networkx_nodes(G, pos, node_size=700)
        nx.draw_networkx_edges(G, pos, width=2)
        nx.draw_networkx_labels(G, pos, font_size=10, font_family="sans-serif")

        edge_labels = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

        plt.axis("off")
        plt.show()
