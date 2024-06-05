import sys
import time

sys.path.append("../cs330_transportation_networks")

from dijkstar import Graph as DijkstarGraph, find_path, NoPathError
from Algorithms.Dijkstra import Dijkstra
from src.graph import Graph as myGraph

graph_file = "Data/Baghdad_Edgelist.csv"
graph = myGraph()
graph.read_from_csv_file(graph_file)
dijkstar_graph = DijkstarGraph()
for node, neighbors in graph.graph.items():
    for neighbor, weight in neighbors.items():
        dijkstar_graph.add_edge(node, neighbor, weight)
        
dijkstra = Dijkstra(graph)

start_list = [1, 2, 4, 5, 10, 11, 12, 13, 15, 16, 20, 21, 26, 27, 28, 37, 38, 49,
              56, 57, 60, 62, 69, 71, 82, 86, 94, 95, 103, 107, 109, 113]
end_list = [122, 134, 131, 135, 208, 213, 216, 268, 309, 313, 316, 318, 319, 321,
            325, 326, 352, 398, 401, 408, 412, 417, 422, 424, 426]
count = 0

start_node = None
end_node = None

for node in start_list:
    start_node = node
    for node in end_list:
        # print("--------------------------------------------------------------")
        end_node = node

        try:
            info = find_path(dijkstar_graph, start_node, end_node)
            # print(f"Shortest path from {start_node} to {end_node}: {info.nodes}")
        except:
            info = None
            # print(f"No a* shortest path could be found from {start_node} to {end_node}")
        try:
            dijkstra_shortest_path = dijkstra.find_shortest_path(start_node, end_node)
            # print(f"Shortest path from {start_node} to {end_node}: {dijkstra_shortest_path}")
        except:
            dijkstra_shortest_path = None
            # print(f"No dijkstra shortest path could be found from {start_node} to {end_node}")
        
        if info:
            if info.nodes == dijkstra_shortest_path:
                count += 1
            # print(f"dijkstra == a*: {info.nodes == dijkstra_shortest_path}")
            # print(info.nodes)
            # print(dijkstra_shortest_path)
        else:
            if info == dijkstra_shortest_path:
                count += 1
            # print(f"dijkstra == a*: {info == dijkstra_shortest_path}")
            # print(info)
            # print(dijkstra_shortest_path)
        # print()


print("SUMMARY")
print(f"Out of {len(start_list)*len(end_list)} cases, {count} are correct.")
    
