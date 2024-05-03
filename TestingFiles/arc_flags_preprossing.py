import heapq
import sys
import random
import pickle

sys.path.append("../cs330_transportation_networks")
from src.graph import Graph, Node
from Algorithms.Dijkstra import Dijkstra
from Algorithms.Arc_Flags import ArcFlags

cities = [
    "Surat",
    "Baghdad",
    "Beijing",
    "LosAngeles",
    "NewYork",
    "Paris",
    "SaoPaolo",
    "WashingtonDC",
]


def save_to_pickle(name, instance1):
    with open(f"ArcFlagInstances/{name}_object.pkl", "wb") as filehandler:
        pickle.dump(instance1, filehandler)


def preprocess(name):
    graph_file = f"Data/{name}_Edgelist.csv"
    graph = Graph()
    graph.num_partitions_axis = 2
    graph.read_from_csv_file_node(graph_file)

    arc_flags = ArcFlags(graph)
    arc_flags.preprocess_graph()
    print("preprocessing done...")
    save_to_pickle(name, arc_flags.graph)


def straight_up():
    graph_file = "Data/Surat_Edgelist.csv"
    graph = Graph()
    graph.num_partitions_axis = 2
    graph.read_from_csv_file_node(graph_file)

    ### Testing arc-flags dijkstra
    nodes = list(graph.graph.keys())
    source = 1
    target = 10
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


def test_instance_pickle(name):
    source_id = 1
    target_id = 15
    source_node = None
    target_node = None

    with open(f"ArcFlagInstances/{name}_object.pkl", "rb") as filehandler:
        arc_flag_graph = pickle.load(filehandler)

    for node in arc_flag_graph.graph.keys():
        if node.value == source_id:
            source_node = node
        if node.value == target_id:
            target_node = node

    arc_flag = ArcFlags(arc_flag_graph)
    shortest_path = arc_flag.arc_flags_dijkstra(source_node, target_node)
    print(f"Shortest path: {shortest_path}")


def main():
    item = "Surat"
    # for item in cities:
    #     preprocess(item)
    test_instance_pickle(item)
    # preprocess("Surat")


if __name__ == "__main__":
    main()
