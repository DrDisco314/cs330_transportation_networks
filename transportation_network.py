"""
    File:        transportation_network.py
    Author:      Alex Axton, Nathanial Field, Michael Scoleri
    Course:      CS 330 - Algorithms
    Semester:    Spring 2024
    Assignment:  Term Project: Transportation networks
    Description: Implements a brute force solution to the
      transportation network routing problem using Dijkstra's algorithm.
"""

### Dykstra pesudocode

# function Dijkstra(Graph, source):
#  2      
#  3      for each vertex v in Graph.Vertices:
#  4          dist[v] ← INFINITY
#  5          prev[v] ← UNDEFINED
#  6          add v to Q
#  7      dist[source] ← 0
#  8      
#  9      while Q is not empty:
# 10          u ← vertex in Q with min dist[u]
# 11          remove u from Q
# 12          
# 13          for each neighbor v of u still in Q:
# 14              alt ← dist[u] + Graph.Edges(u, v)
# 15              if alt < dist[v]:
# 16                  dist[v] ← alt
# 17                  prev[v] ← u
# 18
# 19      return dist[], prev[]


def read_file(filename):
    i = 0
    try:
        with open(filename, 'r') as file:
            # Read lines one by one
            for line in file:
                # Process each line as needed
                print(line.strip())  # Example: Print each line without trailing newline characters
                i += 1
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    print(f"i: {i}")


if __name__ == "__main__":
    filename = "road-chesapeake.mtx"
    read_file(filename)