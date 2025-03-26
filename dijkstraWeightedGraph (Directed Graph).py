class Graph:
    def __init__(self, size):
        self.adj_matrix = [[0] * size for _ in range(size)]
        self.size = size
        self.vertex_data = [''] * size

    def add_edge(self, u, v, weight):
        if 0 <= u < self.size and 0 <= v < self.size:
            self.adj_matrix[u][v] = weight
            self.adj_matrix[v][u] = weight  # For directed graph

    def add_vertex_data(self, vertex, data):
        if 0 <= vertex < self.size:
            self.vertex_data[vertex] = data

    def dijkstra(self, start_vertex_data): # Find the index of the start vertex based on its data label
        start_vertex = self.vertex_data.index(start_vertex_data) # Initialize an array to store the shortest distances from start_vertex to each vertex
        distances = [float('inf')] * self.size # Set all distances to infinity initially
        distances[start_vertex] = 0 # Distance to the start vertex is 0
        visited = [False] * self.size # Initially, all vertices are unvisited
        # Loop through all vertices to find the shortest paths
        for _ in range(self.size): # Find the vertex with the smallest distance that has not been visited
           min_distance = float('inf')  # Set initial minimum distance to infinity
        u = None  # Variable to store the vertex with the smallest distance

        # Iterate through all vertices to find the closest unvisited vertex
        for i in range(self.size):
            if not visited[i] and distances[i] < min_distance:
                min_distance = distances[i]  # Update the minimum distance
                u = i  # Update the closest vertex

        # If no vertex was found (all remaining vertices are unreachable), stop the algorithm
        if u is None:
            break

        # Mark the selected vertex as visited
        visited[u] = True

        # Update the distances of neighboring vertices
        for v in range(self.size):
            # Check if there is an edge between u and v, and if v has not been visited
            if self.adj_matrix[u][v] != 0 and not visited[v]:
                # Calculate the alternative distance through u
                alt = distances[u] + self.adj_matrix[u][v]

                # If the alternative distance is shorter, update the shortest known distance to v
                if alt < distances[v]:
                    distances[v] = alt
       # Return the computed shortest distances from the start vertex to all other vertices
        return distances

g = Graph(7)

g.add_vertex_data(0, 'A')
g.add_vertex_data(1, 'B')
g.add_vertex_data(2, 'C')
g.add_vertex_data(3, 'D')
g.add_vertex_data(4, 'E')
g.add_vertex_data(5, 'F')
g.add_vertex_data(6, 'G')

g.add_edge(3, 0, 4)  # D - A, weight 4
g.add_edge(3, 4, 2)  # D - E, weight 2
g.add_edge(0, 2, 3)  # A - C, weight 3
g.add_edge(0, 4, 4)  # A - E, weight 4
g.add_edge(2, 4, 4)  # C - E, weight 4
g.add_edge(4, 6, 5)  # E - G, weight 5
g.add_edge(2, 5, 5)  # C - F, weight 5
g.add_edge(2, 1, 2)  # C - B, weight 2
g.add_edge(1, 5, 2)  # B - F, weight 2
g.add_edge(6, 5, 5)  # G - F, weight 5

# Dijkstra's algorithm from D to all vertices
print("Dijkstra's Algorithm starting from vertex D:\n")
distances = g.dijkstra('D')
for i, d in enumerate(distances):
    print(f"Shortest distance from D to {g.vertex_data[i]}: {d}")
