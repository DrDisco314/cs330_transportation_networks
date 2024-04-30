import sys
import time

sys.path.append("../cs330_transportation_networks")

from Algorithms.CH import CH
import dijkstar as dij


def convert_pandana_to_dijkstar(pandana_network):
    graph = dij.Graph()
    for node_id in pandana_network.nodes_df.index:
        connections = pandana_network.edges_df[
            pandana_network.edges_df["from"] == node_id
        ]
        for _, edge in connections.iterrows():
            graph.add_edge(edge["from"], edge["to"], {"cost": edge["weight"]})
            edges += 1
    return graph


def euclidean_heuristic(u, v, nodes_df):
    u_x, u_y = nodes_df.loc[u, "x"], nodes_df.loc[u, "y"]
    v_x, v_y = nodes_df.loc[v, "x"], nodes_df.loc[v, "y"]
    return ((v_x - u_x) ** 2 + (v_y - u_y) ** 2) ** 0.5


def main():
    contracted_network = CH("Data/Baghdad_Edgelist.csv")
    dijkstar_graph = convert_pandana_to_dijkstar(contracted_network.graph_network)

    start_node, end_node = 11, 60  # Example nodes
    cost_func = lambda u, v, edge, prev_edge: edge["cost"]
    heuristic_func = lambda u, v: euclidean_heuristic(u, v, contracted_network.nodes)

    path_info = dij.find_path(
        dijkstar_graph,
        start_node,
        end_node,
        cost_func=cost_func,
        heuristic_func=heuristic_func,
    )
    print(path_info.nodes)  # Output the path


if __name__ == "__main__":
    main()
