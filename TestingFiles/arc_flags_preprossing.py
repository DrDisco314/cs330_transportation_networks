import heapq
import sys
import random
import pickle  # Updated import for Python 3

sys.path.append("../cs330_transportation_networks")
from src.graph import Graph, Node
from Algorithms.Dijkstra import Dijkstra
from Algorithms.Arc_Flags import ArcFlags

cities = [
    "Baghdad",
    "Beijing",
    "LosAngeles",
    "NewYork",
    "Paris",
    "SaoPaolo",
    "Surat",
    "WashingtonDC",
]


def save_to_pickle(name, instance):
    with open(f"ArcFlagInstances/{name}_object.pkl", "wb") as filehandler:
        pickle.dump(instance, filehandler)


def preprocess(name):
    graph_file = f"Data/{name}_Edgelist.csv"
    graph = Graph()
    graph.num_partitions_axis = 6
    graph.read_from_csv_file_node(graph_file)

    arc_flags = ArcFlags(graph)
    arc_flags.preprocess_graph()
    print("preprocessing done...")
    save_to_pickle(name, arc_flags)


def main():
    for item in cities:
        preprocess(item)


if __name__ == "__main__":
    main()
