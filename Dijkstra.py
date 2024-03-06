import heapq


class Dijkstra:
    def __init__(self, graph: dict[int, dict[int, int]]):
        """
        Initilize the Dijkstra Class and set variables.
        Input:
            Graph ({int : {(int, int)}}) : A graph dictionary with node as key and a dictionary as value with
            nieghbors and weight.
        Return:
            None
        """
        self.graph = graph
        self.distances = {}
        self.predecessors = {}

    def compute_shortest_paths(self, start_node: int):
        """
        Calculates the shortest path to all possible nodes from a start node and store in predecessor.
        Input:
            start_node (int) : Integer representing start node.
        Return:
            None
        """
        self.distances = {node: float("infinity") for node in self.graph.graph}
        self.distances[start_node] = 0
        self.predecessors = {node: None for node in self.graph.graph}

        # Initialize the min heap
        priority_queue = [(0, start_node)]
        while priority_queue:
            """
            Citation: https://www.geeksforgeeks.org/dijkstras-shortest-path-algorithm-using-priority_queue-stl/
            Inspiration for using a min-heap with with Dijkstra algorithm.

            Citation: https://docs.python.org/3/library/heapq.html
            Heap Queue alogirthm sets up a binary tree with parents less than or equal to children
            """
            current_distance, current_node = heapq.heappop(priority_queue)
            # If shorter path already found -> continue
            if current_distance > self.distances[current_node]:
                continue
            for neighbor, weight in self.graph.get_neighbors(current_node).items():
                distance = current_distance + weight
                if distance < self.distances[neighbor]:
                    self.distances[neighbor] = distance
                    self.predecessors[neighbor] = current_node
                    heapq.heappush(priority_queue, (distance, neighbor))

    def get_shortest_path(self, end_node: int) -> list[int]:
        """
        Returns the shortests path from end node to the start node.
        Input:
            end_node (int) : Integer representing end node.
        Return:
            path [(int)] : List of shortest path from start node to end node.
        """
        path = []
        current = end_node
        while current is not None:
            path.append(current)
            current = self.predecessors[current]
        return path[::-1]
