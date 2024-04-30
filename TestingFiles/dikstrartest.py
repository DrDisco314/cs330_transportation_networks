import sys
import time

sys.path.append("../cs330_transportation_networks")

from dijkstar import Graph as DijkstarGraph, find_path, NoPathError
from src.graph import Graph as myGraph

graph_file = "Data/Baghdad_Edgelist.csv"
graph = myGraph()
graph.read_from_csv_file(graph_file)
dijkstar_graph = DijkstarGraph()
for node, neighbors in graph.graph.items():
    for neighbor, weight in neighbors.items():
        dijkstar_graph.add_edge(node, neighbor, weight)

start_node = 11
end_node = 60
info = find_path(dijkstar_graph, start_node, end_node)
print(info.nodes)
