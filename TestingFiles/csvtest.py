import sys
import time

sys.path.append("../cs330_transportation_networks")

from src.graph import Graph
from Algorithms.Dijkstra import Dijkstra


def main():
    start_node = 247191
    end_node = 184
    mygraph = Graph()

    mygraph.read_from_csv_file("Data/NewYork_Edgelist.csv")
    # dictgraph = mygraph.return_graph()
    # for key, value in dictgraph.items():
    #     print(key, value)
    #     input("yo")
    dijkstra = Dijkstra(mygraph)
    start = time.time()
    shortest_path = dijkstra.find_shortest_path(start_node, end_node)
    end = time.time()
    print(f"Time taken: {(end-start)*1000} (ms)")
    (
        print(f"Shortest path from {start_node} to {end_node}: {shortest_path}")
        if shortest_path is not None
        else print("No path found.")
    )


if __name__ == "__main__":
    main()