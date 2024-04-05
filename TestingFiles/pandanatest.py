import pandana as pdna
import pandas as pd
from pandas import DataFrame
import csv
from pandana import Network
import time


def load_csv(filename: str) -> DataFrame:
    df = pd.read_csv(filename)
    return df


def create_pandanas_network(df: DataFrame) -> Network:
    """Create 2 dataframes following format
    https://udst.github.io/pandana/index.html
    """

    nodes = (
        df[["START_NODE", "XCoord", "YCoord"]]
        .drop_duplicates("START_NODE")
        .set_index("START_NODE")
    )
    nodes.index.name = "node_id"
    nodes.columns = ["x", "y"]

    edges = df[["START_NODE", "END_NODE", "LENGTH"]]
    edges.columns = ["from", "to", "weight"]

    graph_network = pdna.Network(
        nodes["x"], nodes["y"], edges["from"], edges["to"], edges[["weight"]]
    )
    return graph_network


def find_shortest_path(net: Network):
    start_node = 247191
    end_node = 184
    start = time.time()
    shortest_distance = net.shortest_path(start_node, end_node)
    end = time.time()
    print(f"Time taken: {(end-start)*1000} (ms)")
    print(shortest_distance)


def main():
    graphdf = load_csv("Data/NewYork_Edgelist.csv")
    graph_network = create_pandanas_network(graphdf)
    find_shortest_path(graph_network)


if __name__ == "__main__":
    main()
