import networkx as nx
import matplotlib.pyplot as plt


class Graph:
    def __init__(self):
        self.graph = {}

    def add_edge(self, node1, node2, weight):
        if node1 not in self.graph:
            self.graph[node1] = {}
        if node2 not in self.graph:
            self.graph[node2] = {}
        self.graph[node1][node2] = weight
        self.graph[node2][node1] = weight

    def read_from_mtx_file(self, filename):
        try:
            with open(filename, "r") as file:
                for line in file:
                    if line.startswith("%"):
                        continue
                    parts = line.split()

                    if len(parts) == 2 or len(parts) == 3:
                        node1, node2 = int(parts[0]), int(parts[1])
                        weight = abs(node1 - node2)
                        self.add_edge(node1, node2, weight)
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def get_neighbors(self, node):
        return self.graph.get(node, {})

    def visualize_graph(self):
        """Citation: https://networkx.org/
        Package for visualizing a weighted graph
        """
        G = nx.Graph()
        for node, neighbors in self.graph.items():
            for neighbor, weight in neighbors.items():
                G.add_edge(node, neighbor, weight=weight)

        pos = nx.spring_layout(G)
        nx.draw_networkx_nodes(G, pos, node_size=700)
        nx.draw_networkx_edges(G, pos, width=2)
        nx.draw_networkx_labels(G, pos, font_size=10, font_family="sans-serif")

        edge_labels = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

        plt.axis("off")
        plt.show()
