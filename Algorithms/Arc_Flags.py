"""
    File:        Arc_Flags.py
    Author:      Alex Axton, Nathanial Field, Michael Scoleri
    Course:      CS 330 - Algorithms
    Semester:    Spring 2024
    Assignment:  Term Project: Transportation networks
    Description: Implements an improved brute force solution using arc-flags to
    	improve the running time of Dijkstra's algorithm.
"""

import heapq
import sys
import random

sys.path.append("../cs330_transportation_networks")
from src.graph import Graph, Node, Edge
from Algorithms.Bidirectional_Dijkstra import BidirectionalDijkstra

class ArcFlags:
    def __init__(self, graph: dict[Node, dict[Node, Edge]]):
        """
        Initilize the ArcFlags Class and set variables.
        Input:
            Graph ({Node : {(Node, Edge)}}) : A graph dictionary with node as key and a dictionary as value with
            neighbors and edges.
        Return:
            None
        """
        self.graph = graph


    def print_progress(self, current_index, total_entries):
        percent_finished = (current_index + 1) / total_entries * 100
        print()
        print(f"Preprocessing: {percent_finished:.0f}% done.")
        print()


    def preprocess_graph(self):
        """
            Preprocesses a graph with arc-flags such that each edge has the appropriate arc-flags
                vector set. The arc-flags vector has n-regions and for each element n_i if it is true
                and edge is the shortest path to the region R_i, else false. The graph is preprocesseed
                using the shortest path tree between border nodes and all other nodes in a region.
        Input:
            graph Graph : The Graph object to be preprocessed
        Output:
            Graph : Resultant graph object has been processed such that each edge has its arc-flags vector set
                using a rectangual partition.
        """
        # Use rectangular partition function
        # partitions = rectangular_partition(graph, graph.num_partitions_axis)
        nodes = list(self.graph.graph.keys())

        bi_dijkstra = BidirectionalDijkstra(self.graph)
        # Identify edge nodes in the collection of nodes
        edge_nodes = []
        for key, value in self.graph.graph.items():
            start_node_region = key.region
            for node in value.keys():
                if node.region != start_node_region:
                    edge_nodes.append(key)

        # Do a shortest path search between an edge node and all other nodes to set arc-flag vectors
        for index, edge_node in enumerate(edge_nodes):
            self.print_progress(index, len(edge_nodes))
            for node in nodes:
                node_region = node.region
                arc_flag_index = node_region[0] + (node_region[1] * self.graph.num_partitions_axis)
                node_neighbors = self.graph.graph[node]

                # Every edge from a node by definition has the node's region arc flag set
                for neighbor in node_neighbors:
                    self.graph.graph[node][neighbor].arc_flags[arc_flag_index] = True
                
                # Try doing a bidirectional dijkstra between every node and edge node to set arc flags
                try:
                    shortest_path = bi_dijkstra.bidirectional_dijkstra(node, edge_node)
                    edge_node_region = edge_node.region

                    # set the arc-flags along the shortest path corresponding to the edge node's reigon
                    for i in range(len(shortest_path) - 1):
                        # Take (x, y) region and get index by taking nth region
                        arc_flag_index = edge_node_region[0] + (edge_node_region[1] * self.graph.num_partitions_axis)
                        self.graph.graph[shortest_path[i]][shortest_path[i+1]].arc_flags[arc_flag_index] = True
                
                # No shortest path could be found, no arc flags to update
                except:
                    pass                
    
    def get_shortest_path(self, end_node, predecessors):
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
            current = predecessors[current]
        if len(path) == 1:
            return None
        return path[::-1]


    def arc_flags_dijkstra(self, source, target):
        
        # Initialize parameters
        distances = {node: float("infinity") for node in self.graph.graph}
        distances[source] = 0
        predecessors = {node: None for node in self.graph.graph}
        target_region = target.region
        arc_flag_index = target_region[0] + (target_region[1] * self.graph.num_partitions_axis)

        print(f"Source node: {source}")
        print(f"Source node region: {source.region}")
        print(f"Target node: {target}")
        print(f"Target node region: {target.region}")
        print(f"Desired arc flag index: {arc_flag_index}")

        # Initialize the min heap
        priority_queue = [(0, source)]
        while priority_queue:
            """
            Citation: https://www.geeksforgeeks.org/dijkstras-shortest-path-algorithm-using-priority_queue-stl/
            Inspiration for using a priority queue with with Dijkstra algorithm.

            Citation: https://docs.python.org/3/library/heapq.html
            Heap Queue keeps track of most recently visted nodes on top of stack.
            """
            current_distance, current_node = heapq.heappop(priority_queue)
            # If shorter path already found, continue
            if current_distance > distances[current_node]:
                continue
            for neighbor, edge in self.graph.get_neighbors(current_node).items():
                # Check that the neigbor node is on a shortest path to border node in target region
                if edge.arc_flags[arc_flag_index] == False:
                    continue
                else:
                    distance = current_distance + edge.weight
                    if distance < distances[neighbor]:
                        distances[neighbor] = distance
                        predecessors[neighbor] = current_node
                        heapq.heappush(priority_queue, (distance, neighbor))

        return get_shortest_path(target, predecessors)