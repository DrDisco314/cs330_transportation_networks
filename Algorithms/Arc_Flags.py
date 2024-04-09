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
sys.path.append('C:/comp_sci/cs330/cs330_transportation_networks/src')
from graph import Graph, Node

graph_file = "Data/NewYork_Edgelist.csv"
graph = Graph()
graph.read_from_csv_file_node(graph_file)

# Sets the number of partitions to take along a given axis.
NUM_PARTITIONS_AXIS = 10

def rectangular_partition(graph: Graph) -> tuple[list[float],list[float]]:
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

	# print(f"width: {width}")
	print(f"height: {height}")

	print(f"minimum x coord: {graph.smallest_x_node.xcoord}")
	print(f"minimum y coord: {graph.smallest_y_node.ycoord}")
	print(f"maximum x coord: {graph.largest_x_node.xcoord}")
	print(f"maximum y coord: {graph.largest_y_node.ycoord}")

	print(f"w_partition_size: {w_partition_size}")
	print(f"h_partition_size: {h_partition_size}")
	print(f"width partitions: {width_partitions}")
	print(f"height partitions: {height_partitions}")

	return (width_partitions, height_partitions)


def get_node_region(node: Node, paritions: tuple[list[float],list[float]]
	) -> tuple[int, int]:
	
	width_partitions = partitions[0]
	node_x_region = None
	for idx, partition in enumerate(width_partitions):
		if node.xcoord <= partition:
			node_x_region = idx

	height_partitions = partitions[1]
	node_y_region = None
	for idx, partition in enumerate(height_partitions):
		if node.ycoord <= partition:
			node_y_region = idx

	return (node_x_region, node_y_region)


def preprocess_graph(graph):
	partitions = rectangular_partition(graph) 


partitions = rectangular_partition(graph)
test_node = Node(1)
test_node.xcoord = 509471
test_node.ycoord = 4435791

node_region = get_node_region(test_node, partitions)
print(f"node region: {node_region}")


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