"""
    File:        Bidirectional_Dijkstra.py
    Author:      Alex Axton, Nathanial Field, Michael Scoleri
    Course:      CS 330 - Algorithms
    Semester:    Spring 2024
    Assignment:  Term Project: Transportation networks
    Description: Implements an improvement on dijkstra's algorithm through a bidirectional search
        for the transportation network routing problem
"""

import heapq
import sys

sys.path.append("../cs330_transportation_networks")
from src.graph import Graph, Node, Edge


class BidirectionalDijkstra:
    def __init__(self, graph: dict[Node, dict[Node, Edge]]):
        """
        Initilize the BidirectionalDijkstra Class and set variables.
        Input:
            Graph ({Node : {(Node, Edge)}}) : A graph dictionary with node as key and a dictionary as value with
            neighbors and Edges to perform bidirectional search on.
        Return:
            None
        """
        self.graph = graph

    def reconstruct_shortest_path(self, predecessors_f: dict[Node, Node], predecessors_b: dict[Node, Node],
        meeting_node: Node) -> list[Node]:
        """
        Takes in the predecessors of some meeting node and using them reconstructs the
        shortest path from some source to target node.
        Input:
            predecessors_f (dict[Node, Node]) : Dictionary of predecessors from the forward search
            predecessors_b (dict[Node, Node]) : Dictionary of predecessors from the backward search
            meeting_node (Node) : Meeting node of forward and backward search
        Output:
            path (list[Node]) : List of nodes on shortest path from a source to target node
        """
        path = []
        
        # Reconstruct path from start node to meeting node using predecessors from forward search
        current_node = meeting_node
        while (current_node in predecessors_f):
            path.append(current_node)
            current_node = predecessors_f[current_node]

        # Reverse the path since it was constructed in reverse order
        path.reverse()

        # Reconstruct path from end node to meeting node using predecessors from backward search
        current_node = meeting_node
        while (current_node in predecessors_b):
            current_node = predecessors_b[current_node]
            if current_node:
                path.append(current_node)

        return path

    def bidirectional_dijkstra(self, start_node: Node, end_node: Node) -> list[Node]:
        """
        Runs a bidirectional Dijkstra's algorithm between start_node and end_node
        Input:
            start_node (Node) : A starting node storing a label, coordinates, and weights to other Node objects.
            end_node (Node) : An ending node storing a label, coordinates, and weights to other Node objects.
        Output:
            shortest_path (list[Node]) : List of nodes forming the shortest path from start to end node
        """

        # Citation: https://www.homepages.ucl.ac.uk/~ucahmto/math/2020/05/30/bidirectional-dijkstra.html
        # Pseudocode algorithm and website's description were very helpful for implementing a bidirectional
        #   dijkstra's algorithm.

        # Define values for the forward search
        distances_f = {node: float("inf") for node in self.graph.graph}
        distances_f[start_node] = 0
        priority_queue_f = [(0, start_node)]
        set_f = set()
        predecessors_f = {node: None for node in self.graph.graph}

        # Define values for the backward search
        distances_b = {node: float("inf") for node in self.graph.graph}
        distances_b[end_node] = 0
        priority_queue_b = [(0, end_node)]
        set_b = set()
        predecessors_b = {node: None for node in self.graph.graph}

        # Initialize distance from source to target to infinite till better seen
        mu = float("inf")

        transition_vertex = None

        while priority_queue_f and priority_queue_b:
            current_distance_f, current_node_f = heapq.heappop(priority_queue_f)
            current_distance_b, current_node_b = heapq.heappop(priority_queue_b)

            set_f.add(current_node_f)
            set_b.add(current_node_b)

            # Check the neighbors of current stack node on the forward search
            for neighbor_f, edge_f in self.graph.get_neighbors(current_node_f).items():

                distance = current_distance_f + edge_f.weight
                if (neighbor_f not in set_f) and (distances_f[neighbor_f] > distance):
                    distances_f[neighbor_f] = distance
                    predecessors_f[neighbor_f] = current_node_f
                    heapq.heappush(priority_queue_f, (distances_f[neighbor_f], neighbor_f))

                if (neighbor_f in set_b) and (distance + distances_b[neighbor_f] < mu):
                    mu = distance + distances_b[neighbor_f]
                    transition_vertex = neighbor_f

            # Check the neighbors of current stack node on the backward search
            for neighbor_b, edge_b in self.graph.get_neighbors(current_node_b).items():

                distance = current_distance_b + edge_b.weight
                if (neighbor_b not in set_b) and (distances_b[neighbor_b] > distance):
                    distances_b[neighbor_b] = distance
                    predecessors_b[neighbor_b] = current_node_b
                    heapq.heappush(priority_queue_b, (distances_b[neighbor_b], neighbor_b))

                if (neighbor_b in set_f) and (distance + distances_f[neighbor_b] < mu):
                    mu = distance + distances_f[neighbor_b]
                    transition_vertex = neighbor_b

            # mu is distance from s-t
            if (distances_f[current_node_f] + distances_b[current_node_b]) >= mu:
                
                shortest_path = self.reconstruct_shortest_path(predecessors_f, predecessors_b, transition_vertex)
                return shortest_path

        return Exception(f"No Shortest path could be found from {start_node.value} to {end_node.value}.")