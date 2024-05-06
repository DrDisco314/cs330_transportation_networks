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


def save_to_pickle(name, instance1, num):
    if instance1 is None:
        print("Instance is none")
        return
    with open(f"ArcFlagInstances/{name}_{num}_object.pkl", "wb") as filehandler:
        pickle.dump(instance1, filehandler)


def preprocess(name, num):
    graph_file = f"Data/{name}_Edgelist.csv"
    graph = Graph()
    graph.num_partitions_axis = num
    graph.read_from_csv_file_node(graph_file)

    arc_flags = ArcFlags(graph)
    arc_flags.preprocess_graph()
    print("preprocessing done...")
    # for key, value in arc_flags.graph.items():
    #     print(key, value)
    save_to_pickle(name, arc_flags.graph, num)


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


def test_instance_pickle(name, num):
    source_id = 1
    target_id = 25
    source_node = None
    target_node = None

    with open(f"ArcFlagInstances/{name}_{num}_object.pkl", "rb") as filehandler:
        arc_flag_graph = pickle.load(filehandler)

    arc_flag = ArcFlags(arc_flag_graph)

    source_node = arc_flag.graph.return_node(source_id)
    target_node = arc_flag_graph.return_node(target_id)
    shortest_path = arc_flag.arc_flags_dijkstra(source_node, target_node)
    print(f"Shortest path: {shortest_path}")


def main():
    item = "Surat"
    num = 4
    # for item in cities:
    #     preprocess(item)
    # test_instance_pickle(item, num)
    preprocess(item, num)


if __name__ == "__main__":
    main()
