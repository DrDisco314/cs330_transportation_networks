"""
    File:        Dijkstra.py
    Author:      Alex Axton, Nathanial Field, Michael Scoleri
    Course:      CS 330 - Algorithms
    Semester:    Spring 2024
    Assignment:  Term Project: Transportation networks
    Description: Implements an improved brute force solution using arc-flags to drastically
    	improve the running time of Dijkstra's algorithm.
"""

import heapq
import sys

sys.path.append("C:/comp_sci/cs330/cs330_transportation_networks/src")
from graph import Graph, Node

graph_file = "Data/NewYork_Edgelist.csv"
graph = Graph()
graph.read_from_csv_file_node(graph_file)

# Sets the number of partitions to take along a given axis.
NUM_PARTITIONS_AXIS = 10


def bidirectional_dijkstra(graph: Graph, start_node: Node, end_node: Node):
    distances_f = {node: float("inf") for node in self.graph.graph}
    distances_f[start_node] = 0
    priority_queue_f = [(0, start_node)]
    set_f = {node: None for node in self.graph.graph}

    distances_b = {node: float("inf") for node in self.graph.graph}
    distances_b[end_node] = 0
    priority_queue_b = [(0, end_node)]
    set_b = {node: None for node in self.graph.graph}

	### the conditional here may need to be an or statement - check this.
	while priority_queue_forward and priority_queue_backward:
		current_distance_f, current_node_f = heapq.heappop(priority_queue_f)
		current_distance_b, current_node_b = heapq.heappop(priority_queue_b)

    	mu = float("inf")

        set_f[current_node_f] = current_node_f
        set_b[current_node_b] = current_node_b

        for neighbor_f, weight_f in self.graph.get_neighbors(current_node_f).items():

            distance = current_distance_f + weight_f
            if (neighbor_f not in set_f) and distances_f[neighbor_f] > distance:
                distances_f[neighbor_f] = distance
                heapq.heappush(priority_queue, (distance, neighbor_f))

            if (neighbor_f in set_b) and distance + distances_b[neighbor_f] < mu:
                mu = distance + distances_b[neighbor_f]

        for neighbor_b, weight_b in self.graph.get_neighbors(current_node_b).items():

            distance = current_distance_b + weight_b
            if (neighbor_b not in set_b) and distances_b[neighbor_b] > distance:
                distances_b[neighbor_b] = distance
                heapq.heappush(priority_queue, (distance, neighbor_b))

            if (neighbor_b in set_f) and distance + distances_f[neighbor_b] < mu:
                mu = distance + distances_f[neighbor_b]

        # mu is distance from s-t
        	# Verify that this is the termination condition
        if distances_f[current_node_f] + distances_b[current_node_b] >= mu:
            return (set_f, set_b)


###pseudocode implementation
def psuedocode_bi_dijk(G):
	while Qf is not empty and Qb is not empty:
	    u = extract_min(Qf); v = extract_min(Qb)
	    Sf.add(u); Sb.add(v)
	    for x in adj(u):
	        relax(u, x)
	        if x in Sb and df[u] + w(u, x) + db[x] < mu:
	            mu = df[u] + w(u, x) + db[x]
	    for x in adj(v):
	        relax(v, x)
	        if x in Sf and db[v] + w(v, x) + df[x] < mu:
	            mu = db[v] + w(v, x) + df[x]
	    if df[u] + db[v] >= mu:
	        break # mu is the true distance s-t

## pseudocode bidirectional relax
def relax(u,x):
	if (x is not in Sf) and df[x] > df[u] + weight(u, x):
	    df[x] = df[u] + weight(u, x)
	    Qf.add(x, priority=df[x])


def rectangular_partition(graph: Graph) -> tuple[list[float], list[float]]:
    width = graph.largest_x_node.xcoord - graph.smallest_x_node.xcoord
    height = graph.largest_y_node.ycoord - graph.smallest_y_node.ycoord

    partitions = []

    width_partitions = []
    w_partition_size = width / NUM_PARTITIONS_AXIS
    current_parition = graph.smallest_x_node.xcoord
    for width_partition in range(NUM_PARTITIONS_AXIS):
        current_parition += w_partition_size
        width_partitions.append(current_parition)

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

    width_partitions = partitions[0]
    w_partition_size = width_partitions[1] - width_partitions[0]
    node_x_region = None
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


def preprocess_graph(graph):
    partitions = rectangular_partition(graph)

    ### Debugging, print the first 10 dictionary entries
    # count = 0
    # for key, value in graph.graph.items():
    #     if count < 10:
    #         print(f"{key}: {value}")
    #         for k in value.keys():
    #         	print("keys in value")
    #         	print(f"{k}")
    #         count += 1
    #     else:
    #     	break

    ### Identify edge nodes in the collection of nodes
    edge_nodes = []
    for key, value in graph.graph.items():
        start_node_region = get_node_region(key, partitions)
        key.region = start_node_region
        for node in value.keys():
            if get_node_region(node, partitions) != start_node_region:
                edge_nodes.append(key)

    # Do a shortest path search between an edge node and all nodes in its region
    for edge_node in edge_nodes:
        pass


preprocess_graph(graph)


# We can now exploit this property: for a specified region r
# 0 ∈ R and a boundary node b of r
# 0 we
# calculate the set Tb of arcs a ∈ A with fa(r
# 0
# ) = true and where a is on a shortest path via b to
# any node in r
# 0
# . The reversed arcs corresponding to arcs in the set Tb form in fact a shortest path tree
# in the reverse graph Grev. A shortest path tree can be computed in time O(n log n) on sparse graphs.
# Therefore, we can compute the flag entries fa(r
# 0
# ) for region r
# 0
# for all nodes a ∈ A at once, if we
# compute a shortest path tree for each boundary node of r
# 0
# . This can be done in time O(kn log n) with
# k = |Br
# 0|, where Br
# 0 is the boundary node set of r
# 0
# : Br
# 0 = {v ∈ r
# 0
# | ∃(u, v) ∈ A such that ru 6= rv =
# r
# 0}.
