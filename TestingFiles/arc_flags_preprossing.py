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


def save_to_pickle(name, instance):
    with open(f"ArcFlagInstances/{name}_object.pkl", "wb") as filehandler:
        pickle.dump(instance, filehandler)


def preprocess(name):
    graph_file = f"Data/{name}_Edgelist.csv"
    graph = Graph()
    graph.num_partitions_axis = 2
    graph.read_from_csv_file_node(graph_file)

    arc_flags = ArcFlags(graph)
    arc_flags.preprocess_graph()
    print("preprocessing done...")
    save_to_pickle(name, arc_flags)


def test_instance_pickle():

    graph_file = "Data/Surat_Edgelist.csv"
    graph = Graph()
    graph.read_from_csv_file_node(graph_file)
    source = 1
    target = 5
    for node in nodes:
        if node.value == source:
            source = node
        if node.value == target:
            target = node
    print("Loading Pickle...")
    arc_flag = pickle.load("ArcFlagInstances/Surat_object.pkl")
    if arc_flag == None:
        print("Uh oh")
    print("Instance Loaded...")
    shortest_path = arc_flags.arc_flags_dijkstra(source, target)
    print(f"shortest_path: {shortest_path}")


def main():
    # for item in cities:
    #     preprocess(item)
    test_instance_pickle()


if __name__ == "__main__":
    main()
