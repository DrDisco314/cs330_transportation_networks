import heapq
import sys
import random

sys.path.append("../cs330_transportation_networks")
from src.graph import Graph, Node
from Algorithms.Dijkstra import Dijkstra
from Algorithms.Arc_Flags import *


### Debugging: Testing on a sample graph
graph_file = "Data/Surat_Edgelist.csv"
graph = Graph()
graph.num_partitions_axis = 10
graph.read_from_csv_file_node(graph_file)

### Testing arc-flags dijkstra
nodes = list(graph.graph.keys())
source = 761
target = 6819
for node in nodes:
    if node.value == source:
        source = node
    if node.value == target:
        target = node

arc_flags = ArcFlags(graph)
arc_flags.preprocess_graph()
print("preprocessing done...")


shortest_path = arc_flags.arc_flags_dijkstra(source, target)
print(f"shortest_path: {shortest_path}")


### Testing bidirectional dijkstra's path
# print("testing...")

# nodes = list(graph.graph.keys())

# # print(nodes[0])
# start_node = random.choice(nodes)
# end_node = random.choice(nodes)
# print(f"Random node 1: {start_node}")
# print(f"Random node 2: {end_node}")


# predecessors_f, predecessors_b, transition_vertex = bidirectional_dijkstra(graph, start_node, end_node)
# # path_f = []
# # path_b = []

# print(f"transition_vertex: {transition_vertex}")

# path = reconstruct_shortest_path(predecessors_f, predecessors_b, transition_vertex)
# print("path")
# print(path)



### Find a path with dijkstra's algorithm for comparing to bidirectional output
# graph_file = "Data/NewYork_Edgelist.csv"
# start_node = start_node.value
# end_node = end_node.value

# graph = Graph()
# graph.read_from_csv_file(graph_file)
# # graph.read_from_mtx_file(graph_file)
# # graph.visualize_graph()

# dijkstra = Dijkstra(graph)
# shortest_path = dijkstra.find_shortest_path(start_node, end_node)
# print(f"Shortest path from {start_node} to {end_node}: {shortest_path}")

# print(f"Bidirectional dijkstra path == dijkstra's path: {path == shortest_path}")
