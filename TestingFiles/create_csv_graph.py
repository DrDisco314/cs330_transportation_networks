def parse_graph_file(graph_filename):
    edges = {}
    with open(graph_filename, "r") as file:
        for line in file:
            if line.startswith("a"):
                parts = line.split()
                start_node, end_node, length = (
                    int(parts[1]),
                    int(parts[2]),
                    float(parts[3]),
                )
                if start_node not in edges:
                    edges[start_node] = {}
                edges[start_node][end_node] = length
    return edges


def parse_coords_file(coords_filename):
    coords = {}
    with open(coords_filename, "r") as file:
        for line in file:
            if line.startswith("v"):
                parts = line.split()
                node_id = int(parts[1])
                x_coord = float(parts[2])
                y_coord = float(parts[3])
                coords[node_id] = (x_coord, y_coord)
    return coords


def create_csv_file(edges, coords, output_filename):
    with open(output_filename, "w") as file:
        file.write("XCoord,YCoord,START_NODE,END_NODE,EDGE,LENGTH\n")
        edge_id = 1
        for start_node, connections in edges.items():
            if start_node in coords:
                x_coord, y_coord = coords[start_node]
                for end_node, length in connections.items():
                    if end_node in coords:
                        file.write(
                            f"{x_coord},{y_coord},{start_node},{end_node},{edge_id},{length}\n"
                        )
                        edge_id += 1


edges = parse_graph_file(
    "/Users/michaelscoleri/Desktop/Coding/School/Algos/cs330_transportation_networks/Data/USA-road-d.NY.gr"
)
coords = parse_coords_file("/Users/michaelscoleri/Downloads/USA-road-d.NY.co")
create_csv_file(edges, coords, "DIMCAS_New_York_graph.csv")
