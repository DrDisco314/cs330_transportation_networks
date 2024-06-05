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
import math


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

    # Cite: https://stackoverflow.com/questions/53554199/heapq-push-typeerror-not-supported-between-instances
    # Description: An evil error was occuring when pushing tuples of (distance, Node) onto the priority
    #              queue for dijkstra's algorithm due to multiple entries having the same distance. To resolve
    #              this, Nodes need the < comparison operator implemented to determine order of priority queue.
    def __lt__(self, other):
        return self.value < other.value


class Edge:
    def __init__(self, weight: float, num_flags: int):
        """
        Initialize the Edge Class.
        Input:
            weight (float) : weight of an edge
            num_flags (int) : Number of arc flag entries to store
        Return:
            None
        """
        self.weight = weight
        self.arc_flags = [False for _ in range(num_flags)]

    def __str__(self):
        return f"{self.weight}"

    def __repr__(self):
        return f"{self.weight}"


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
        self.num_partitions_axis = None
        self.smallest_x_node = None
        self.smallest_y_node = None
        self.largest_x_node = None
        self.largest_y_node = None

    def euclidean_distance(self, u: Node, v: Node):
        """
        Calculates the Euclidean distance between 2 nodes.
        Inputs:
            u (Node) : Source Node.
            v (Node) : Neighbor Node.
            e (any) : Current Edge.
            prev_e (any) : previous edge.
        Output:
            (Float) : Euclidean distance between U and V.
        """
        x1, y1 = u.xcoord, u.ycoord
        x2, y2 = v.xcoord, v.ycoord
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def add_edge(self, node1: int, node2: int, weight: float):
        """
        Adds the edge from one node to another.
        Input:
            Node1 (int) : Integer representing first node.
            Node2 (int) : Intger representing second node
            weight (float) : float representing weight of edge from 2 nodes.
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
        Adds the Edge from one node to another.
        Input:
            Node1 (Node) : Node representing source of Edge.
            Node2 (Node) : Node representing destination of Edge.
            weight (float) : float representing weight of Edge from 2 nodes.
        Return:
            None
        """
        if node1 not in self.graph:
            self.graph[node1] = {}
        if node2 not in self.graph:
            self.graph[node2] = {}

        # Symetric Implementation. Number of partitions true for rectangular partition.
        # Add edge with memory for arc flags determined by number of regions in partition
        self.graph[node1][node2] = Edge(self.euclidean_distance(node1, node2), self.num_partitions_axis**2)
        self.graph[node2][node1] = Edge(self.euclidean_distance(node1, node2), self.num_partitions_axis**2)

    def rectangular_partition(self) -> tuple[list[float], list[float]]:
        """
        Creates partitions in coordinate space to break a graph into rectangular region
        Input:
            None.
        Return:
            tuple[list[float], list[float]] : Defines a first and second list to mark points along
                the x and y axes respectively as partition lines
        """
        # Width and height of farthest nodes in graph
        width = self.largest_x_node.xcoord - self.smallest_x_node.xcoord
        height = self.largest_y_node.ycoord - self.smallest_y_node.ycoord

        partitions = []

        # Get partition popints along x axis
        width_partitions = []
        w_partition_size = width / self.num_partitions_axis
        current_parition = self.smallest_x_node.xcoord
        for width_partition in range(self.num_partitions_axis):
            current_parition += w_partition_size
            width_partitions.append(current_parition)

        # Get partition popints along y axis
        height_partitions = []
        h_partition_size = height / self.num_partitions_axis
        current_parition = self.smallest_y_node.ycoord
        for height_partition in range(self.num_partitions_axis):
            current_parition += h_partition_size
            height_partitions.append(current_parition)

        return (width_partitions, height_partitions)

    def get_node_region(
        self, partitions: tuple[list[float], list[float]], node: Node) -> tuple[int, int]:
        """
        Returns the region that a node belongs to
        Input:
            node (Node) : Node to get region of
            paritions (tuple[list[float], list[float]]) : The rectangular parition points along the graph to
                be compared with node's coordinates
        Return:
            tuple[int, int] : The region that the node belongs to stored as (x Region, y region) where
            (0, 0) is the first rectangular region
        """
        # Get x-axis partition poiints and determine partition size
        width_partitions = partitions[0]
        w_partition_size = width_partitions[1] - width_partitions[0]

        node_x_region = None
        # check node coordinate with x partition points till node is within parition region
        for idx, partition in enumerate(width_partitions):
            if (
                node.xcoord <= partition
                and node.xcoord >= (partition - w_partition_size)
                or node.xcoord == partition
            ):
                node_x_region = idx

            # Precision in coordinates makes for rounding issues in some coordinates. If coordinates
            # is past last partition line place in the final partition region to maintain desired number
            # of partition regions.
            if node_x_region == None:
                node_x_region = len(width_partitions) - 1

        height_partitions = partitions[1]
        h_partition_size = height_partitions[1] - height_partitions[0]

        node_y_region = None
        for idx, partition in enumerate(height_partitions):
            if (
                node.ycoord <= partition
                and node.ycoord >= (partition - h_partition_size)
                or node.ycoord == partition
            ):
                node_y_region = idx

            if node_y_region == None:
                node_y_region = len(height_partitions) - 1

        return (node_x_region, node_y_region)

    def process_nodes(self, filename: str) -> list[Node]:
        """
        Processes the nodes in filename as Node objects
        input:
            filanme (str): String of file to process nodes from
        Return:
            nodes (list[Node]): List of processed nodes
        """
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

    def partition_nodes(self, nodes: list[Node]) -> list[Node]:
        """
        Uses a rectangular partition to assign each node in nodes to a region.
        input:
            nodes list[Node] : List of nodes to be assigned region by partition function
        Returns:
            nodes list[Node] : List node nodes with assigned region
        """

        partitions = self.rectangular_partition()
        for node in nodes.values():
            node.region = self.get_node_region(partitions, node)

        return nodes

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

    def read_from_csv_file_node(self, filename: str):
        """
        Reads in a file in the form of csv where nodes are in the same line.
        Input:
            filename (str) : Filename as a string
        Return:
            None
        """
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

        # Set the region of each node using a partition function
        partioned_nodes = self.partition_nodes(processed_nodes)

        try:
            with open(filename, newline="") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    start_node = partioned_nodes[int(row["START_NODE"])]
                    end_node = partioned_nodes[int(row["END_NODE"])]
                    self.add_edge_node(
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

    def return_node(self, value: int) -> Node | None:
        """
        Returns the node with a given value.
        Input:
            Value (int) : ID of desired node.
        Output:
            (Node) : desired node if exists.
        """
        for key in self.graph:
            if key.value == value:
                return key
        return None
