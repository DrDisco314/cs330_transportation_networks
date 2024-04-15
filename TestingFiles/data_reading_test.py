import csv
import sys

sys.path.append("../cs330_transportation_networks")


def count_nodes_and_edges(filename):
    nodes = set()
    edges = set()
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            start_node = row['START_NODE']
            end_node = row['END_NODE']
            nodes.add(start_node)
            nodes.add(end_node)
            edge = row['EDGE']
            edges.add(edge)
    
    num_nodes = len(nodes)
    num_edges = len(edges)
    
    print(f"Filename: {filename}")
    print(f"Number of nodes: {num_nodes}")
    print(f"Number of edges: {num_edges}")
    print()

files = ["Data/Baghdad_Edgelist.csv",
"Data/Beijing_Edgelist.csv",
"Data/LosAngeles_Edgelist.csv",
"Data/Paris_Edgelist.csv",
"Data/SaoPaolo_Edgelist.csv",
"Data/Surat_Edgelist.csv",
"Data/WashingtonDC_Edgelist.csv",
"Data/NewYork_Edgelist.csv"]

for file in files:
    count_nodes_and_edges(file)