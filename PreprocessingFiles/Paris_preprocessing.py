import heapq
import sys
import random
import pickle
import time

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


def save_to_pickle(name, instance1, num_paritions):
    with open(
        f"ArcFlagInstances/{name}_{num_paritions}_object.pkl", "wb"
    ) as filehandler:
        pickle.dump(instance1, filehandler)


def preprocess(name):
    graph_file = f"Data/{name}_Edgelist.csv"
    graph = Graph()

    num_paritions = 2
    graph.num_partitions_axis = num_paritions
    string_name_paritions = str(num_paritions)

    graph.read_from_csv_file_node(graph_file)

    arc_flags = ArcFlags(graph)
    arc_flags.preprocess_graph()
    print("preprocessing done...")
    save_to_pickle(name, arc_flags.graph, string_name_paritions)


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


def test_instance_pickle():
    name = "Surat"
    # with open(f"GraphInstances/{name}_object.pkl", "rb") as filehandler:
    #     graph = pickle.load(filehandler)
    graph = Graph()
    graph.num_partitions_axis = 2
    graph.read_from_csv_file_node(f"Data/{name}_Edgelist.csv")

    # Set initial source and target IDs
    source_id = 1
    target_id = 15

    # Initialize source and target node variables
    source_node = None
    target_node = None

    # Attempt to find the actual node objects in the graph
    # print("Checking node types and values...")
    # # for node in graph.graph.keys():
    # #     if node.value < 100:
    # #         print(f"Node ID: {node.value}, Type: {type(node)}")

    for node in graph.graph.keys():
        if node.value == source_id:
            source_node = node
        if node.value == target_id:
            target_node = node

    # Check if nodes were found
    if not source_node or not target_node:
        print(f"Could not find nodes for IDs {source_id} and {target_id} in the graph.")
        return  # Exit if nodes are not found

    print("Nodes found. Loading ArcFlags instance...")
    with open(f"ArcFlagInstances/{name}_object.pkl", "rb") as filehandler:
        arc_flag_graph = pickle.load(filehandler)
    arc_flag = ArcFlags(arc_flag_graph)

    # print(vars(arc_flag))
    # arc_flag.test()
    # print(vars(graph))
    # Assuming arc_flag is not None and has the method arc_flags_dijkstra implemented
    shortest_path = arc_flag.arc_flags_dijkstra(source_node, target_node)
    print(f"Shortest path: {shortest_path}")


def main():
    item = "Paris"
    start = time.time()
    preprocess(item)
    end = time.time()
    elapsed_time = end - start
    with open(f"PreprocessingFiles/Times/{item}_time.txt", "w") as file:
        file.write(f"{elapsed_time:.2f}")


if __name__ == "__main__":
    main()
