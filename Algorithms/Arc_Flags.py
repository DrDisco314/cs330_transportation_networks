"""
    File:        Arc_Flags.py
    Author:      Alex Axton, Nathanial Field, Michael Scoleri
    Course:      CS 330 - Algorithms
    Semester:    Spring 2024
    Assignment:  Term Project: Transportation networks
    Description: Implements an improved brute force solution using arc-flags to drastically
    	improve the running time of Dijkstra's algorithm.
"""

import heapq
import sys
import random

sys.path.append("../cs330_transportation_networks/src")
from src.graph import Graph, Node


### Debugging: Testing on a sample graph
graph_file = "Data/NewYork_Edgelist.csv"
graph = Graph()
graph.read_from_csv_file_node(graph_file)

# Sets the number of partitions to take along a given axis.
NUM_PARTITIONS_AXIS = 10


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
        for neighbor_f, weight_f in graph.get_neighbors(current_node_f).items():

            distance = current_distance_f + weight_f
            if (neighbor_f not in set_f) and (distances_f[neighbor_f] > distance):
                distances_f[neighbor_f] = distance
                predecessors_f[neighbor_f] = current_node_f
                heapq.heappush(priority_queue_f, (distances_f[neighbor_f], neighbor_f))

            if (neighbor_f in set_b) and (distance + distances_b[neighbor_f] < mu):
                mu = distance + distances_b[neighbor_f]
                transition_vertex = neighbor_f

        # Check the neighbors of current stack node on the backward search
        for neighbor_b, weight_b in graph.get_neighbors(current_node_b).items():

            distance = current_distance_b + weight_b
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
    
    print("Something wrong happened")


def reconstruct_shortest_path(predecessors_f, predecessors_b, meeting_node):
    path = []
    
    # Reconstruct path from start node to meeting node using predecessors from forward search
    current_node = meeting_node
    while current_node in predecessors_f:
        path.append(current_node)
        current_node = predecessors_f[current_node]
    # Add the start node
    path.append(current_node)

    # Reverse the path since it was constructed in reverse order
    path.reverse()

    # Reconstruct path from end node to meeting node using predecessors from backward search
    current_node = meeting_node
    while current_node in predecessors_b:
        current_node = predecessors_b[current_node]
        path.append(current_node)

    return path


def rectangular_partition(graph: Graph) -> tuple[list[float], list[float]]:
    """
        Creates partitions in coordinate space to break a graph into rectangular region
    Input:
        graph Graph : A graph object with node keys and a dictionary as value storing other
            Node neighbors and weight
    Output:
        tuple[list[float], list[float]] : Defines a first and second list to mark points along
            the x and y axes respectively as partition lines
    """
    # Width and height of farthest nodes in graph
    width = graph.largest_x_node.xcoord - graph.smallest_x_node.xcoord
    height = graph.largest_y_node.ycoord - graph.smallest_y_node.ycoord

    partitions = []

    # Get partition popints along x axis
    width_partitions = []
    w_partition_size = width / NUM_PARTITIONS_AXIS
    current_parition = graph.smallest_x_node.xcoord
    for width_partition in range(NUM_PARTITIONS_AXIS):
        current_parition += w_partition_size
        width_partitions.append(current_parition)

    # Get partition popints along y axis
    height_partitions = []
    h_partition_size = height / NUM_PARTITIONS_AXIS
    current_parition = graph.smallest_y_node.ycoord
    for height_partition in range(NUM_PARTITIONS_AXIS):
        current_parition += h_partition_size
        height_partitions.append(current_parition)

    return (width_partitions, height_partitions)


def get_node_region(
    node: Node, partitions: tuple[list[float], list[float]]
) -> tuple[int, int]:
    """
        Returns the region that a node belongs to
    Input:
        node Node : Node to get region of
        paritions tuple[list[float], list[float]] : The rectangular parition points along the graph to
            be compared with node's coordinates
    Output:
        tuple[int, int] : The region that the node belongs to stored as (x Region, y region) where
        (0, 0) is the first rectangular region
    """
    # Get x-axis partition poiints and determine partition size
    width_partitions = partitions[0]
    w_partition_size = width_partitions[1] - width_partitions[0]

    node_x_region = None
    # check node coordinate with x partition points till node is within parition region
    for idx, partition in enumerate(width_partitions):
        if node.xcoord <= partition and node.xcoord >= (partition - w_partition_size):
            node_x_region = idx

    height_partitions = partitions[1]
    h_partition_size = height_partitions[1] - height_partitions[0]
    node_y_region = None
    for idx, partition in enumerate(height_partitions):
        if node.ycoord <= partition and node.ycoord >= (partition - h_partition_size):
            node_y_region = idx

    return (node_x_region, node_y_region)


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
    partitions = rectangular_partition(graph)

    # Identify edge nodes in the collection of nodes
    edge_nodes = []
    for key, value in graph.graph.items():
        start_node_region = get_node_region(key, partitions)
        key.region = start_node_region
        for node in value.keys():
            if get_node_region(node, partitions) != start_node_region:
                edge_nodes.append(key)

    # Do a shortest path search between an edge node and all nodes in its region to set arc-flag vectors
    for edge_node in edge_nodes:
        # bidirectional_dijkstra
        pass


print("testing...")

nodes = list(graph.graph.keys())

# print(nodes[0])
start_node = random.choice(nodes)
end_node = random.choice(nodes)
print(f"Random node 1: {start_node}")
print(f"Random node 2: {end_node}")


predecessors_f, predecessors_b, transition_vertex = bidirectional_dijkstra(graph, start_node, end_node)
# path_f = []
# path_b = []

print(f"transition_vertex: {transition_vertex}")

path = reconstruct_shortest_path(predecessors_f, predecessors_b, transition_vertex)
print("path")
print(path)
