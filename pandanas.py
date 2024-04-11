import pandas as pd
import pandana as pdna
from graph import Graph

mygraph = Graph()
mygraph.read_from_mtx_file("road-chesapeake.mtx")
edges = []
for node_from, connections in mygraph.graph.items():
    for node_to, weight in connections.items():
        edges.append((node_from, node_to, weight))

edges_df = pd.DataFrame(edges, columns=["node_from", "node_to", "weight"])
print(edges_df.head())
network = pdna.Network(
    edges_df["node_from"], edges_df["node_to"], edges_df["weight"], edges_df["weight"]
)
