import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from statistics import mean

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
    "Shenyang": {
        "Dijkstra": 13.571,
        "CH": 0.785,
        "A*": 8.139,
        "AF": 3.366,
        "Custom": 1.542,
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
    "Shenyang": {"Nodes": 13000, "Edges": 19000},
    "Dhaka": {"Nodes": 15300, "Edges": 20000},
    "Baghdad": {"Nodes": 60000, "Edges": 89000},
    "Beijing": {"Nodes": 84000, "Edges": 110000},
    "Sao Paolo": {"Nodes": 214000, "Edges": 310000},
    "Los Angeles": {"Nodes": 405000, "Edges": 551000},
    "New York": {"Nodes": 449000, "Edges": 622000},
    "Paris": {"Nodes": 474000, "Edges": 643000},
    "Washington DC": {"Nodes": 513000, "Edges": 659000},
}

# secondary_algos = ["AF", "Custom"]
# # Generate plots for each algorithm
algorithms = ["Dijkstra", "CH", "AF"]
# for algorithm in algorithms:
#     nodes = []
#     edges = []
#     runtimes = []

#     for city, props in city_properties.items():
#         if (
#             algorithm in runtime_data[city]
#         ):  # Check if algorithm data exists for the city
#             nodes.append(props["Nodes"])
#             edges.append(props["Edges"])
#             runtimes.append(runtime_data[city][algorithm])

#     # Plot runtime vs nodes
#     plt.figure(figsize=(10, 5))
#     plt.plot(nodes, runtimes, "o-", label=f"{algorithm} vs Nodes")
#     plt.title(f"{algorithm} Algorithm Runtime vs Nodes")
#     plt.xlabel("Number of Nodes")
#     plt.ylabel("Runtime (ms)")
#     plt.grid(True)
#     plt.legend()
#     plt.savefig(f"Images/{algorithm}_runtime_vs_nodes.png")
#     plt.close()

#     # Plot runtime vs edges
#     plt.figure(figsize=(10, 5))
#     plt.plot(edges, runtimes, "o-", label=f"{algorithm} vs Edges")
#     plt.title(f"{algorithm} Algorithm Runtime vs Edges")
#     plt.xlabel("Number of Edges")
#     plt.ylabel("Runtime (ms)")
#     plt.grid(True)
#     plt.legend()
#     plt.savefig(f"Images/{algorithm}_runtime_vs_edges.png")
#     plt.close()


# # Setup plot for nodes
# plt.figure(figsize=(14, 7))
# for algorithm in algorithms:
#     nodes = []
#     runtimes = []
#     for city, props in city_properties.items():
#         if algorithm in runtime_data[city]:
#             nodes.append(props["Nodes"])
#             runtimes.append(runtime_data[city][algorithm])
#     if nodes:  # Check if there is data to plot
#         plt.plot(nodes, runtimes, "-o", label=f"{algorithm}")

# plt.title("Algorithm Runtime vs Nodes")
# plt.xlabel("Number of Nodes")
# plt.ylabel("Runtime (ms)")
# plt.legend()
# plt.grid(True)
# plt.savefig("Images/runtime_vs_nodes_BABY_algorithms.png")
# # plt.show()


for algorithm in algorithms:
    plt.figure(figsize=(14, 7))
    edges = []
    runtimes = []
    theo = []
    factor = []
    for city, props in city_properties.items():
        if algorithm in runtime_data[city]:
            edges.append(props["Edges"])
            runtimes.append(runtime_data[city][algorithm])
            theoretical = props["Edges"] * np.log(props["Edges"])
            theo.append(theoretical)
            factor.append(theoretical / runtime_data[city][algorithm])
    if edges:  # Check if there is data to plot
        print(factor)
        runtimes = [runtimes[i] * mean(factor) for i in range(len(runtimes))]
        plt.plot(edges, runtimes, "-o", label=f"{algorithm}")
        plt.plot(edges, theo, "-x", label="Theoretical Runtime")

    plt.title("Algorithm Runtime vs Edges")
    plt.xlabel("Number of Edges")
    plt.ylabel("Runtime Scaled")
    plt.legend()
    plt.grid(True)
    plt.savefig(f"Images/runtime_vs_edges_{algorithm}ONLY_algorithms.png")
# plt.show()

# # Setup plot for edges
# plt.figure(figsize=(14, 7))
# for algorithm in secondary_algos:
#     edges = []
#     runtimes = []
#     for city, props in city_properties.items():
#         if algorithm in runtime_data[city]:
#             edges.append(props["Nodes"])
#             runtimes.append(runtime_data[city][algorithm])
#     if edges:  # Check if there is data to plot
#         plt.plot(edges, runtimes, "-o", label=f"{algorithm}")

# plt.title("Algorithm Runtime vs Nodes")
# plt.xlabel("Number of Nodes")
# plt.ylabel("Runtime (ms)")
# plt.legend()
# plt.grid(True)
# plt.savefig("Images/runtime_vs_nodes_AF_algorithms.png")
# plt.show()

# plt.figure(figsize=(14, 7))
# for algorithm in secondary_algos:
#     edges = []
#     runtimes = []
#     for city, props in city_properties.items():
#         if algorithm in runtime_data[city]:
#             edges.append(props["Edges"])
#             runtimes.append(runtime_data[city][algorithm])
#     if edges:  # Check if there is data to plot
#         plt.plot(edges, runtimes, "-o", label=f"{algorithm}")


# plt.title("Algorithm Runtime vs Edges")
# plt.xlabel("Number of Edges")
# plt.ylabel("Runtime (ms)")
# plt.legend()
# plt.grid(True)
# plt.savefig("Images/runtime_vs_edges_AF_algorithms.png")


# def model_and_plot(algorithm):
#     # Extract data for the algorithm
#     nodes = []
#     edges = []
#     runtimes = []

#     for city, data in runtime_data.items():
#         if algorithm in data:
#             nodes.append(city_properties[city]["Nodes"])
#             edges.append(city_properties[city]["Edges"])
#             runtimes.append(data[algorithm])

#     # Convert to numpy arrays for regression
#     X = np.column_stack((nodes, edges))
#     y = np.array(runtimes)

#     # Create and fit the model
#     model = LinearRegression().fit(
#         X, np.log(y)
#     )  # Using log(y) if relationship is exponential

#     # Predict for plotting
#     predicted = np.exp(model.predict(X))  # Inverse of log is exp

#     # Plotting
#     plt.figure(figsize=(10, 5))
#     plt.scatter(nodes, runtimes, color="blue", label="Actual Data")
#     plt.scatter(nodes, predicted, color="red", label="Predicted Data", alpha=0.6)
#     plt.title(f"{algorithm} Algorithm: Runtime vs Nodes and Edges")
#     plt.xlabel("Number of Nodes")
#     plt.ylabel("Runtime (ms)")
#     plt.legend()
#     plt.grid(True)
#     plt.show()

#     # Print model coefficients
#     print(
#         f"Model for {algorithm}: Coefficient for Nodes = {model.coef_[0]}, Edges = {model.coef_[1]}"
#     )

#     # Plotting with Nodes and Edges together might be more informative if visualized in 3D
#     from mpl_toolkits.mplot3d import Axes3D

#     fig = plt.figure()
#     ax = fig.add_subplot(111, projection="3d")
#     ax.scatter(nodes, edges, runtimes, color="blue", label="Actual Data")
#     ax.scatter(nodes, edges, predicted, color="red", label="Predicted Data", alpha=0.6)
#     ax.set_xlabel("Number of Nodes")
#     ax.set_ylabel("Number of Edges")
#     ax.set_zlabel("Runtime (ms)")
#     plt.title(f"{algorithm} Runtime Model")
#     plt.legend()
#     plt.show()


# def main():
#     # Loop through each algorithm to model and plot
#     for algorithm in runtime_data[
#         "Surat"
#     ].keys():  # Assuming each city has the same set of algorithms
#         print(algorithm)
#         model_and_plot(algorithm)


# if __name__ == "__main__":
#     main()
