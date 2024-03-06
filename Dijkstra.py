import heapq


class Dijkstra:
    def __init__(self, graph):
        self.graph = graph
        self.distances = {}
        self.predecessors = {}

    def compute_shortest_paths(self, start_node):
        self.distances = {node: float("infinity") for node in self.graph.graph}
        self.distances[start_node] = 0
        self.predecessors = {node: None for node in self.graph.graph}

        priority_queue = [(0, start_node)]
        while priority_queue:
            """
            Citation: https://docs.python.org/3/library/heapq.html
            Heap Queue alogirthm sets up a binary tree with parents less than or equal to children
            """
            current_distance, current_node = heapq.heappop(priority_queue)
            if current_distance > self.distances[current_node]:
                continue
            for neighbor, weight in self.graph.get_neighbors(current_node).items():
                distance = current_distance + weight
                if distance < self.distances[neighbor]:
                    self.distances[neighbor] = distance
                    self.predecessors[neighbor] = current_node
                    heapq.heappush(priority_queue, (distance, neighbor))

    def get_shortest_path(self, end_node):
        path = []
        current = end_node
        while current is not None:
            path.append(current)
            current = self.predecessors[current]
        return path[::-1]
