import csv
import math

def read_csv(filename):
    with open(filename, mode='r') as file:
        csv_reader = csv.DictReader(file)
        data = [row for row in csv_reader]
    return data

def calculate_euclidean_distance(x1, y1, x2, y2):
    print(f"x1, x2: {x1, x2}")
    print(f"y1, y2: {y1, y2}")
    print(f"euclidean distance: {math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)}")
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def update_lengths_with_euclidean(data):
    nodes = {}
    updated_data = []

    for entry in data:
        start_node = int(entry["START_NODE"])
        end_node = int(entry["END_NODE"])
        x_coord = float(entry["XCoord"])
        y_coord = float(entry["YCoord"])

        if start_node not in nodes:
            nodes[start_node] = (x_coord, y_coord)

    for entry in data:
        start_node = int(entry["START_NODE"])
        end_node = int(entry["END_NODE"])
        x1, y1 = nodes[start_node]
        x2, y2 = nodes[end_node]

        # Calculate Euclidean distance
        distance = calculate_euclidean_distance(x1, y1, x2, y2)

        # Update LENGTH with the calculated Euclidean distance
        entry["LENGTH"] = distance
        updated_data.append(entry)
        print(f"entry: {entry}")

    return updated_data

def write_csv(filename, data):
    fieldnames = data[0].keys()
    with open(filename, mode='w', newline='') as file:
        csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
        csv_writer.writeheader()
        csv_writer.writerows(data)

# Example usage
input_filename = 'Data/Surat_Edgelist.csv'
output_filename = 'Data/Surat_Edgelist_euclidean.csv'

data = read_csv(input_filename)
updated_data = update_lengths_with_euclidean(data)
write_csv(output_filename, updated_data)

print(f"Updated data has been saved to {output_filename}")