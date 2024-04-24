import matplotlib.pyplot as plt

# Runtime and city data
runtime_data = {
    "Surat": {
        "Nodes": [2, 4, 8, 16, 32, 64],
        "Dijkstra": [2.5, 2.4, 2.4, 2.4, 2.4, 2.4],
        "CH": [0.6, 0.6, 0.6, 0.4, 0.5, 0.4],
    },
    "Baghdad": {
        "Nodes": [2, 4, 8, 16, 32, 64, 128],
        "Dijkstra": [82.1, 77.5, 75.2, 79.4, 75.4, 75.4, 75.2],
        "CH": [2.4, 2.2, 2.2, 2.0, 2.2, 2.1, 2.24],
    },
    "Sao Paolo": {
        "Nodes": [2, 4, 8, 16, 32, 64, 128],
        "Dijkstra": [33.8, 33.5, 333.6, 333.1, 336.4, 339.3, 346.3],
        "CH": [6.6, 6.0, 6.8, 6.7, 6.5, 6.5, 7.3],
    },
    "New York": {
        "Nodes": [2, 4, 8, 16, 32, 64, 128],
        "Dijkstra": [505.2, 75.7, 512.6, 526.1, 514.8, 522.9, 513.7],
        "CH": [12.2, 13.1, 12.8, 13.2, 12.0, 13.0, 12.0],
    },
    "Washington D.C.": {
        "Nodes": [2, 4, 8, 16, 32, 64, 128],
        "Dijkstra": [786.8, 785.0, 747.1, 771.5, 764.5, 760.0, 742.4],
        "CH": [14.2, 14.6, 14.3, 14.5, 14.5, 14.0, 14.7],
    },
}

city_properties = {
    "Surat": {"Nodes": 2600, "Edges": 3700},
    "Baghdad": {"Nodes": 60000, "Edges": 89000},
    "Sao Paolo": {"Nodes": 214000, "Edges": 310000},
    "New York": {"Nodes": 449000, "Edges": 622000},
    "Washington D.C.": {"Nodes": 513000, "Edges": 659000},
}

# Plotting runtimes vs nodes for each city
for city, data in runtime_data.items():
    plt.figure()
    plt.plot(data["Nodes"], data["Dijkstra"], marker="o", label="Dijkstra")
    plt.plot(data["Nodes"], data["CH"], marker="x", label="Contraction Hierarchies")
    plt.title(f"{city} Graph Runtimes")
    plt.xlabel("Nodes")
    plt.ylabel("Runtime (ms)")
    plt.legend()
    plt.grid(True)
    plt.savefig(f"Images/{city}_runtimes.png")
    plt.close()

# Nodes and edges vs Dijkstra runtime for n=64
edges = []
nodes = []
dijkstra_runtimes_64 = []
ch_runtime_64 = []

for city, props in city_properties.items():
    if 64 in runtime_data[city]["Nodes"]:
        index = runtime_data[city]["Nodes"].index(64)
        nodes.append(props["Nodes"])
        edges.append(props["Edges"])
        dijkstra_runtimes_64.append(runtime_data[city]["Dijkstra"][index])
        ch_runtime_64.append(runtime_data[city]["CH"][index])


plt.figure()
plt.plot(nodes, dijkstra_runtimes_64, "o-", label="Dijkstra Runtime at n=64")
plt.plot(nodes, ch_runtime_64, marker="x", label="CH Runtime at n=64")
plt.title("Dijkstra Runtime at n=64 vs Number of Nodes")
plt.xlabel("Number of Nodes")
plt.ylabel("Runtime (ms)")
plt.legend()
plt.grid(True)
plt.savefig("Images/runtime_vs_nodes.png")
plt.close()

plt.figure()
plt.plot(edges, dijkstra_runtimes_64, "o-", label="Dijkstra Runtime at n=64")
plt.plot(edges, ch_runtime_64, marker="x", label="CH Runtime at n=64")
plt.title("Dijkstra Runtime at n=64 vs Number of Edges")
plt.xlabel("Number of Edges")
plt.ylabel("Runtime (ms)")
plt.legend()
plt.grid(True)
plt.savefig("Images/runtime_vs_edges.png")
plt.close()
