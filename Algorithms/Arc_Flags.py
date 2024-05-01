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
        self.graph = {}
        self.distances = {}

def bidirectional_dijkstra(graph: Graph, start_node: Node, end_node: Node):
    """
    Runs a bidirectional Dijkstra's algorithm between start_node and end_node
    Input:
        graph Graph : A graph object with node keys and a dictionary as value storing other
            Node neighbors and weight.
        start_node Node : A starting node storing a label, coordinates, and weights to other Node objects.
        end_node Node : An ending node storing a label, coordinates, and weights to other Node objects.
    Output:
        (set_f, set_b) : A tuple containing the forward and backward search shortest path trees.
    """

    # Citation: https://www.homepages.ucl.ac.uk/~ucahmto/math/2020/05/30/bidirectional-dijkstra.html
    # Pseudocode algorithm and website's description were very helpful for implementing a bidirectional
    #   dijkstra's algorithm.

    # Define values for the forward search
    distances_f = {node: float("inf") for node in graph.graph}
    distances_f[start_node] = 0
    priority_queue_f = [(0, start_node)]
    set_f = set()
    predecessors_f = {node: None for node in graph.graph}

    # Define values for the backward search
    distances_b = {node: float("inf") for node in graph.graph}
    distances_b[end_node] = 0
    priority_queue_b = [(0, end_node)]
    set_b = set()
    predecessors_b = {node: None for node in graph.graph}

    # Initialize distance from source to target to infinite till better seen
    mu = float("inf")

    transition_vertex = None

    while priority_queue_f and priority_queue_b:
        current_distance_f, current_node_f = heapq.heappop(priority_queue_f)
        current_distance_b, current_node_b = heapq.heappop(priority_queue_b)

        set_f.add(current_node_f)
        set_b.add(current_node_b)

        # Check the neighbors of current stack node on the forward search
        for neighbor_f, edge_f in graph.get_neighbors(current_node_f).items():

            distance = current_distance_f + edge_f.weight
            if (neighbor_f not in set_f) and (distances_f[neighbor_f] > distance):
                distances_f[neighbor_f] = distance
                predecessors_f[neighbor_f] = current_node_f
                heapq.heappush(priority_queue_f, (distances_f[neighbor_f], neighbor_f))

            if (neighbor_f in set_b) and (distance + distances_b[neighbor_f] < mu):
                mu = distance + distances_b[neighbor_f]
                transition_vertex = neighbor_f

        # Check the neighbors of current stack node on the backward search
        for neighbor_b, edge_b in graph.get_neighbors(current_node_b).items():

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
            return(predecessors_f, predecessors_b, transition_vertex)

def reconstruct_shortest_path(predecessors_f, predecessors_b, meeting_node):
    """
    Takes in the predecessors of some meeting node and using them reconstructs the
    shortest path from some source to target node.
    Input:
        graph Graph : A graph object with node keys and a dictionary as value storing other
            Node neighbors and weight.
        start_node Node : A starting node storing a label, coordinates, and weights to other Node objects.
        end_node Node : An ending node storing a label, coordinates, and weights to other Node objects.
    Output:
        (set_f, set_b) : A tuple containing the forward and backward search shortest path trees.
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

def print_progress(current_index, total_entries):
    percent_finished = (current_index + 1) / total_entries * 100
    print()
    print(f"Preprocessing: {percent_finished:.0f}% done.")
    print()


def preprocess_graph(graph: Graph) -> Graph:
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
    nodes = list(graph.graph.keys())
    # print(f"nodes: {nodes}")

    # Identify edge nodes in the collection of nodes
    edge_nodes = []
    for key, value in graph.graph.items():
        start_node_region = key.region
        for node in value.keys():
            if node.region != start_node_region:
                edge_nodes.append(key)

    # Do a shortest path search between an edge node and all other nodes to set arc-flag vectors
    for index, edge_node in enumerate(edge_nodes):
        print_progress(index, len(edge_nodes))
        for node in nodes:
            node_region = node.region
            arc_flag_index = node_region[0] + (node_region[1] * graph.num_partitions_axis)
            node_neighbors = graph.graph[node]

            # Every edge from a node by definition has the node's region arc flag set
            for neighbor in node_neighbors:
                graph.graph[node][neighbor].arc_flags[arc_flag_index] = True
            
            # Try doing a bidirectional dijkstra between every node and edge node to set arc flags
            try:
                predecessors_f, predecessors_b, transition_vertex = bidirectional_dijkstra(graph, node, edge_node)
            except: 
                pass
            else:
                shortest_path = reconstruct_shortest_path(predecessors_f, predecessors_b, transition_vertex)
                edge_node_region = edge_node.region

                # set the arc-flags along the shortest path corresponding to the edge node's reigon
                for i in range(len(shortest_path) - 1):
                    # Take (x, y) region and get index by taking nth region
                    arc_flag_index = edge_node_region[0] + (edge_node_region[1] * graph.num_partitions_axis)
                    graph.graph[shortest_path[i]][shortest_path[i+1]].arc_flags[arc_flag_index] = True

    return graph
    ### Verify an edge case isn't being missed for shortest path between edge nodes and when edge_node == node

    
def get_shortest_path(end_node, predecessors):
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


def arc_flags_dijkstra(graph, source, target):
    
    # Initialize parameters
    distances = {node: float("infinity") for node in graph.graph}
    distances[source] = 0
    predecessors = {node: None for node in graph.graph}
    target_region = target.region
    arc_flag_index = target_region[0] + (target_region[1] * graph.num_partitions_axis)

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
        for neighbor, edge in graph.get_neighbors(current_node).items():
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