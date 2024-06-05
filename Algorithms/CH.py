"""
Authors: Michael Scoleri, Alex Axton, Nathanial Field
Date: 04/04/2024
File: CH.py
Implementation of the Contractional Hierachy algorithm using the Pandana Package.
Citation:
    Author: Fletcher Foti
    Link: https://udst.github.io/pandana/index.html
"""

import pandana as pdna
import pandas as pd


class CH:
    def __init__(self, filename: str):
        """
        Initialzie the CH class.
        Input:
            filename (str) : path to graph csv.
        Return:
            None
        """
        self.filename = filename
        self.create_network()

    def create_network(self):
        """
        Helper function for creating network.
        Input:
            None
        Output:
            None
        """
        self.create_dataframes()
        self.create_pandana_network()

    def create_dataframes(self):
        """
        Create dataframes in the format expected by the pandana package.
        Input:
            None
        Output:
            None
        """
        self.dataframe = pd.read_csv(self.filename)
        self.edges = self.dataframe[["START_NODE", "END_NODE", "LENGTH"]]
        self.edges.columns = ["from", "to", "weight"]

        self.nodes = (
            self.dataframe[["START_NODE", "XCoord", "YCoord"]]
            .drop_duplicates("START_NODE")
            .set_index("START_NODE")
        )
        self.nodes.index.name = "node_id"
        self.nodes.columns = ["x", "y"]

    def create_pandana_network(self):
        """
        Use the pandana package to create the graph network. Will autonatically contract the edges.
        Input:
            None
        Output:
            None
        """
        self.graph_network = pdna.Network(
            self.nodes["x"],
            self.nodes["y"],
            self.edges["from"],
            self.edges["to"],
            self.edges[["weight"]],
        )
        self.graph_network.precompute(3000)

    def find_shortest_path(self, start_node: int, end_node: int) -> list[int]:
        """
        Use the pandana package to find the shortest path between 2 nodes.
        Input:
            start_node (int) : node_id of source
            end_node (int) : node id of destination
        Return:
            Shortest path [int] : List of integers representing shortest path.
        """
        return self.graph_network.shortest_path(start_node, end_node)
