import matplotlib.pyplot as plt

# Runtime and city data
runtime_data = {
    "Surat": {
        "Nodes": [2, 4, 8, 16, 32, 64],
        "Dijkstra": [1.932, 1.990, 1.926, 1.939, 1.949, 1.961],
        "CH": [0.469, 0.515, 0.350, 0.426, 0.382, 0.451],
        "A*": [0.008, 0.011, 0.017, 0.128, 0.180, 1.686],
        "Arc Flags": [0.571, 0.572, 0.566, 0.584, 0.591, 0.980],
        "Custom": [0.007, 0.012, 0.022, 0.200, 0.279, 2.577],
    },
    "Quanzhou": {
        "Nodes": [2, 4, 8, 16, 32, 64, 128],
        "Dijkstra": [3.980, 3.854, 0.625, 3.845, 3.873, 3.961, 3.966],
        "CH": [0.606, 0.532, 0.401, 0.477, 0.501, 0.522, 0.560],
        "A*": [0.009, 0.014, 0.031, 0.169, 0.685, 1.818, 14.028],
        "Arc Flags": [3.696, 3.523, 0.795, 3.552, 2.438, 3.857, 0.929],
        "Custom": [0.012, 0.018, 0.041, 0.272, 1.103, 2.852, 6.943],
    },
    "Baghdad": {
        "Nodes": [2, 4, 8, 16, 32, 64, 128],
        "Dijkstra": [66.052, 64.321, 62.935, 62.746, 64.238, 64.774, 66.810],
        "CH": [1.904, 1.697, 1.650, 1.503, 1.675, 1.866, 1.867],
        "A*": [0.017, 0.025, 0.037, 0.211, 1.947, 5.907, 67.751],
        "Arc Flags": ["N/A"] * 7,
        "Custom": ["N/A"] * 7,
    },
    "Beijing": {
        "Nodes": [2, 4, 8, 16, 32, 64, 128],
        "Dijkstra": [9.816, 76.705, 77.186, 78.196, 78.631, 78.573, 84.653],
        "CH": [2.358, 2.067, 2.314, 2.147, 2.221, 2.314, 2.564],
        "A*": [0.013, 0.016, 0.107, 0.175, 0.240, 1.267, 103.603],
        "Arc Flags": ["N/A"] * 7,
        "Custom": ["N/A"] * 7,
    },
    "Sao Paolo": {
        "Nodes": [2, 4, 8, 16, 32, 64, 128],
        "Dijkstra": [28.817, 29.199, 323.994, 315.699, 324.746, 317.260, 308.416],
        "CH": [5.460, 5.673, 5.827, 5.745, 6.155, 5.920, 5.537],
        "A*": [0.013, 0.017, 0.172, 0.123, 2.300, 1.587, 261.309],
        "Arc Flags": ["N/A"] * 7,
        "Custom": ["N/A"] * 7,
    },
}


city_properties = {
    "Surat": {"Nodes": 2600, "Edges": 3700},
    "Quanzhou": {"Nodes": 5600, "Edges": 7600},
    "Baghdad": {"Nodes": 60000, "Edges": 89000},
    "Beijing": {"Nodes": 84000, "Edges": 110000},
    "Sao Paolo": {"Nodes": 214000, "Edges": 310000},
    "Los Angeles": {"Nodes": 405000, "Edges": 551000},
    "New York": {"Nodes": 449000, "Edges": 622000},
    "Paris": {"Nodes": 474000, "Edges": 643000},
    "Washington D.C.": {"Nodes": 513000, "Edges": 659000},
}


# Plotting runtimes vs nodes for each city
for city, data in runtime_data.items():
    plt.figure(figsize=(10, 5))
    plt.plot(data["Nodes"], data["Dijkstra"], marker="o", label="Dijkstra")
    plt.plot(data["Nodes"], data["CH"], marker="x", label="CH")
    plt.plot(data["Nodes"], data["A*"], marker="^", label="A*")
    plt.plot(data["Nodes"], data["Arc Flags"], marker="s", label="Arc Flags")
    plt.plot(data["Nodes"], data["Custom"], marker="d", label="Custom")
    plt.title(f"{city} Graph Runtimes")
    plt.xlabel("Path Length")
    plt.ylabel("Runtime (ms)")
    plt.legend()
    plt.grid(True)
    plt.savefig(f"Images/{city}_runtimes.png")
    plt.show()

# Nodes and edges vs runtime at path length of 64
nodes = []
edges = []
runtime_64 = []

for city, props in city_properties.items():
    if 64 in runtime_data[city]["Nodes"]:
        index = runtime_data[city]["Nodes"].index(64)
        nodes.append(props["Nodes"])
        edges.append(props["Edges"])
        runtime_64.append(runtime_data[city]["Dijkstra"][index])

plt.figure()
plt.plot(nodes, runtime_64, "o-", label="Runtime at n=64")
plt.title("Runtime vs Number of Nodes at Path Length of 64")
plt.xlabel("Number of Nodes")
plt.ylabel("Runtime (ms)")
plt.legend()
plt.grid(True)
plt.savefig("Images/runtime_vs_nodes.png")
plt.show()

plt.figure()
plt.plot(edges, runtime_64, "o-", label="Runtime at n=64")
plt.title("Runtime vs Number of Edges at Path Length of 64")
plt.xlabel("Number of Edges")
plt.ylabel("Runtime (ms)")
plt.legend()
plt.grid(True)
plt.savefig("Images/runtime_vs_edges.png")
plt.show()
