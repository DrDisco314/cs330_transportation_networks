import matplotlib.pyplot as plt

# Runtime and city data
runtime_data = {
    "Surat": {
        "Dijkstra": 2.454,
        "CH": 0.571,
        "A*": 0.437,
        "AF": 0.846,
        "Custom": 0.411,
    },
    "Quanzhou": {
        "Dijkstra": 4.177,
        "CH": 0.622,
        "A*": 0.565,
        "AF": 3.668,
        "Custom": 0.924,
    },
    "Dongguan": {
        "Dijkstra": 4.408,
        "CH": 0.69,
        "A*": 1.095,
        "AF": 2.134,
        "Custom": 0.328,
    },
    "Zhengzhou": {
        "Dijkstra": 6.209,
        "CH": 0.552,
        "A*": 1.009,
        "AF": 2.053,
        "Custom": 0.149,
    },
    "Dhaka": {
        "Dijkstra": 10.036,
        "CH": 0.68,
        "A*": 1.337,
        "AF": 3.170,
        "Custom": 0.844,
    },
    "Baghdad": {
        "Dijkstra": 78.178,
        "CH": 2.069,
        "A*": 1.642,
    },
    "Beijing": {
        "Dijkstra": 88.141,
        "CH": 3.031,
        "A*": 0.36,
    },
    "Sao Paolo": {
        "Dijkstra": 248.22,
        "CH": 6.504,
        "A*": 0.791,
    },
    "Los Angeles": {
        "Dijkstra": 155.514,
        "CH": 9.641,
        "A*": 0.940,
    },
    "New York": {
        "Dijkstra": 448.363,
        "CH": 12.226,
        "A*": 0.481,
    },
    "Paris": {
        "Dijkstra": 689.68,
        "CH": 8.98,
        "A*": 1.108,
    },
    "Washington DC": {
        "Dijkstra": 763.671,
        "CH": 12.333,
        "A*": 0.271,
    },
}


city_properties = {
    "Surat": {"Nodes": 2600, "Edges": 3700},
    "Quanzhou": {"Nodes": 5600, "Edges": 7600},
    "Dongguan": {"Nodes": 8300, "Edges": 11150},
    "Zhengzhou": {"Nodes": 9100, "Edges": 12800},
    "Dhaka": {"Nodes": 15300, "Edges": 20000},
    "Baghdad": {"Nodes": 60000, "Edges": 89000},
    "Beijing": {"Nodes": 84000, "Edges": 110000},
    "Sao Paolo": {"Nodes": 214000, "Edges": 310000},
    "Los Angeles": {"Nodes": 405000, "Edges": 551000},
    "New York": {"Nodes": 449000, "Edges": 622000},
    "Paris": {"Nodes": 474000, "Edges": 643000},
    "Washington DC": {"Nodes": 513000, "Edges": 659000},
}

secondary_algos = ["AF", "Custom"]
# Generate plots for each algorithm
algorithms = ["Dijkstra", "CH", "A*"]
for algorithm in algorithms:
    nodes = []
    edges = []
    runtimes = []

    for city, props in city_properties.items():
        if (
            algorithm in runtime_data[city]
        ):  # Check if algorithm data exists for the city
            nodes.append(props["Nodes"])
            edges.append(props["Edges"])
            runtimes.append(runtime_data[city][algorithm])

    # Plot runtime vs nodes
    plt.figure(figsize=(10, 5))
    plt.plot(nodes, runtimes, "o-", label=f"{algorithm} vs Nodes")
    plt.title(f"{algorithm} Algorithm Runtime vs Nodes")
    plt.xlabel("Number of Nodes")
    plt.ylabel("Runtime (ms)")
    plt.grid(True)
    plt.legend()
    plt.savefig(f"Images/{algorithm}_runtime_vs_nodes.png")
    plt.close()

    # Plot runtime vs edges
    plt.figure(figsize=(10, 5))
    plt.plot(edges, runtimes, "o-", label=f"{algorithm} vs Edges")
    plt.title(f"{algorithm} Algorithm Runtime vs Edges")
    plt.xlabel("Number of Edges")
    plt.ylabel("Runtime (ms)")
    plt.grid(True)
    plt.legend()
    plt.savefig(f"Images/{algorithm}_runtime_vs_edges.png")
    plt.close()


# Setup plot for nodes
plt.figure(figsize=(14, 7))
for algorithm in algorithms:
    nodes = []
    runtimes = []
    for city, props in city_properties.items():
        if algorithm in runtime_data[city]:
            nodes.append(props["Nodes"])
            runtimes.append(runtime_data[city][algorithm])
    if nodes:  # Check if there is data to plot
        plt.plot(nodes, runtimes, "-o", label=f"{algorithm}")

plt.title("Algorithm Runtime vs Nodes")
plt.xlabel("Number of Nodes")
plt.ylabel("Runtime (ms)")
plt.legend()
plt.grid(True)
plt.savefig("Images/runtime_vs_nodes_main_algorithms.png")
# plt.show()

plt.figure(figsize=(14, 7))
for algorithm in algorithms:
    edges = []
    runtimes = []
    for city, props in city_properties.items():
        if algorithm in runtime_data[city]:
            edges.append(props["Edges"])
            runtimes.append(runtime_data[city][algorithm])
    if edges:  # Check if there is data to plot
        plt.plot(edges, runtimes, "-o", label=f"{algorithm}")

plt.title("Algorithm Runtime vs Edges")
plt.xlabel("Number of Edges")
plt.ylabel("Runtime (ms)")
plt.legend()
plt.grid(True)
plt.savefig("Images/runtime_vs_edges_main_algorithms.png")
# plt.show()

# Setup plot for edges
plt.figure(figsize=(14, 7))
for algorithm in secondary_algos:
    edges = []
    runtimes = []
    for city, props in city_properties.items():
        if algorithm in runtime_data[city]:
            edges.append(props["Nodes"])
            runtimes.append(runtime_data[city][algorithm])
    if edges:  # Check if there is data to plot
        plt.plot(edges, runtimes, "-o", label=f"{algorithm}")

plt.title("Algorithm Runtime vs Nodes")
plt.xlabel("Number of Nodes")
plt.ylabel("Runtime (ms)")
plt.legend()
plt.grid(True)
plt.savefig("Images/runtime_vs_nodes_AF_algorithms.png")
plt.show()

plt.figure(figsize=(14, 7))
for algorithm in secondary_algos:
    edges = []
    runtimes = []
    for city, props in city_properties.items():
        if algorithm in runtime_data[city]:
            edges.append(props["Edges"])
            runtimes.append(runtime_data[city][algorithm])
    if edges:  # Check if there is data to plot
        plt.plot(edges, runtimes, "-o", label=f"{algorithm}")

plt.title("Algorithm Runtime vs Edges")
plt.xlabel("Number of Edges")
plt.ylabel("Runtime (ms)")
plt.legend()
plt.grid(True)
plt.savefig("Images/runtime_vs_edges_AF_algorithms.png")
