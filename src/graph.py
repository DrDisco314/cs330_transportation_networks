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
import csv


class Node:
    def __init__(self, value: int):
        """
        Initialize the Node Class.
        Input:
            Value of node
        Return:
            None
        """
        self.value = value
        self.xcoord = None
        self.ycoord = None
        self.region = None

    def __str__(self):
        return f"Node {self.value} ({self.xcoord}, {self.ycoord})"

    def __repr__(self):
        return f"Node {self.value} ({self.xcoord}, {self.ycoord})"


class Edge:
    def __init__(self, weight: float, num_flags: int):
        """
        Initialize the Edge Class.
        Input:
            Weight of edge
        Return:
            None
        """
        self.weight = weight
        self.arc_flags = [False for _ in range(num_flags)]


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
        self.smallest_x_node = None
        self.smallest_y_node = None
        self.largest_x_node = None
        self.largest_y_node = None

    def add_edge(self, node1: int, node2: int, weight: float):
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

        # Symetric Implementation
        self.graph[node1][node2] = weight
        self.graph[node2][node1] = weight

    def add_edge_node(self, node1: Node, node2: Node, weight: float):
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

        # Symetric Implementation
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

    def read_from_csv_file(self, filename: str):
        """
        Reads in a file in the form of csv where nodes are in the same line.
        Input:
            filename (str) : Filename as a string
        Return:
            None
        """

        try:
            with open(filename, newline="") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.add_edge(
                        int(row["START_NODE"]),
                        int(row["END_NODE"]),
                        float(row["LENGTH"]),
                    )
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def process_nodes(self, filename: str):
        nodes = {}
        try:
            with open(filename, newline="") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    node = Node(int(row["START_NODE"]))
                    node.xcoord = float(row["XCoord"])
                    node.ycoord = float(row["YCoord"])

                    if node not in nodes:
                        nodes[int(row["START_NODE"])] = node
                    else:
                        continue

            return nodes

        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def read_from_csv_file_node(self, filename: str):
        """
        Reads in a file in the form of csv where nodes are in the same line.
        Input:
            filename (str) : Filename as a string
        Return:
            None
        """
        ##XCoord,YCoord,START_NODE,END_NODE,EDGE,LENGTH
        processed_nodes = self.process_nodes(filename)

        self.smallest_x_node = min(
            processed_nodes.values(), key=lambda node: node.xcoord
        )
        self.largest_x_node = max(
            processed_nodes.values(), key=lambda node: node.xcoord
        )
        self.smallest_y_node = min(
            processed_nodes.values(), key=lambda node: node.ycoord
        )
        self.largest_y_node = max(
            processed_nodes.values(), key=lambda node: node.ycoord
        )

        try:
            with open(filename, newline="") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    start_node = processed_nodes[int(row["START_NODE"])]
                    end_node = processed_nodes[int(row["END_NODE"])]
                    self.add_edge(
                        start_node,
                        end_node,
                        float(row["LENGTH"]),
                    )
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def read_from_csv_file(self, filename: str):
        """
        Reads in a file in the form of csv where nodes are in the same line.
        Input:
            filename (str) : Filename as a string
        Return:
            None
        """
        ##XCoord,YCoord,START_NODE,END_NODE,EDGE,LENGTH
        try:
            with open(filename, newline="") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.add_edge(
                        int(row["START_NODE"]),
                        int(row["END_NODE"]),
                        float(row["LENGTH"]),
                    )
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

    def return_graph(self) -> dict:
        """
        Return the graph.
        Input:
            None
        Return:
            Dictionary of graph
        """
        return self.graph
