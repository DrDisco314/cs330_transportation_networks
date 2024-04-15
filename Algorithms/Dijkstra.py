"""
    File:        Dijkstra.py
    Author:      Alex Axton, Nathanial Field, Michael Scoleri
    Course:      CS 330 - Algorithms
    Semester:    Spring 2024
    Assignment:  Term Project: Transportation networks
    Description: Implements a brute force solution to the
      transportation network routing problem using Dijkstra's algorithm.
"""

import heapq
import time


class Dijkstra:
    def __init__(self, graph: dict[int, dict[int, int]]):
        """
        Initilize the Dijkstra Class and set variables.
        Input:
            Graph ({int : {(int, int)}}) : A graph dictionary with node as key and a dictionary as value with
            nieghbors and weight.
        Return:
            None
        """
        self.graph = graph
        self.distances = {}
        self.predecessors = {}

    def compute_shortest_paths(self, start_node: int):
        """
        Calculates the shortest path to all possible nodes from a start node and store in predecessor.
        Input:
            start_node (int) : Integer representing start node.
        Return:
            None
        """

        # Initialize parameters
        self.distances = {node: float("infinity") for node in self.graph.graph}
        self.distances[start_node] = 0
        self.predecessors = {node: None for node in self.graph.graph}

        # Initialize the min heap
        priority_queue = [(0, start_node)]
        while priority_queue:
            """
            Citation: https://www.geeksforgeeks.org/dijkstras-shortest-path-algorithm-using-priority_queue-stl/
            Inspiration for using a priority queue with with Dijkstra algorithm.

            Citation: https://docs.python.org/3/library/heapq.html
            Heap Queue keeps track of most recently visted nodes on top of stack.
            """
            current_distance, current_node = heapq.heappop(priority_queue)
            # If shorter path already found, continue
            if current_distance > self.distances[current_node]:
                continue
            for neighbor, weight in self.graph.get_neighbors(current_node).items():
                distance = current_distance + weight
                if distance < self.distances[neighbor]:
                    self.distances[neighbor] = distance
                    self.predecessors[neighbor] = current_node
                    heapq.heappush(priority_queue, (distance, neighbor))

    def get_shortest_path(self, end_node: int) -> list[int]:
        """
        Returns the shortests path from end node to the start node.
        Input:
            end_node (int) : Integer representing end node.
        Return:
            path [(int)] : List of shortest path from start node to end node.
        """
        path = []
        current = end_node
        while current is not None:
            path.append(current)
            current = self.predecessors[current]
        if len(path) == 1:
            return None
        return path[::-1]

    def find_shortest_path(self, start_node: int, end_node: int) -> list[int]:
        """
        Function that uses helper functions compute_shortest_paths and get_shortest_path to
        find the shortest path between start node and end node.
        Input:
            start_node (int) : Integer representing the starting node.
            end_node (int) : Integer representing the starting node.
        Return:
             List of shortest path from start node to end node.
        """
        self.compute_shortest_paths(start_node)
        return self.get_shortest_path(end_node)
