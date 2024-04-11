import sys
import time

sys.path.append("../cs330_transportation_networks")
from Algorithms.Arc_Flags import bidirectional_dijkstra
from src.graph import Graph, Node

myGraph = Graph()
myGraph.read_from_csv_file_node("Data/NewYork_Edgelist.csv")

start_node = 37
end_node = 67
print(bidirectional_dijkstra(myGraph, start_node, end_node))
# print(a)
# print()
# print(b)
