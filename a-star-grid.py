class Node: 
    def __init__(self, row, col): 
        self.row = row 
        self.col = col 
        self.neighbors = [] 
     
    def get_pos(self): 
        return (self.row, self.col) 
 
    def add_neighbors(self, grid): 
        rows, cols = len(grid), len(grid[0]) 
        if self.row > 0 and grid[self.row - 1][self.col] != "#":  # Up 
            self.neighbors.append(grid[self.row - 1][self.col]) 
        if self.row < rows - 1 and grid[self.row + 1][self.col] != "#":  # 
Down 
            self.neighbors.append(grid[self.row + 1][self.col]) 
        if self.col > 0 and grid[self.row][self.col - 1] != "#":  # Left 
            self.neighbors.append(grid[self.row][self.col - 1]) 
        if self.col < cols - 1 and grid[self.row][self.col + 1] != "#":  # 
Right 
            self.neighbors.append(grid[self.row][self.col + 1]) 
 
def draw(): 
    pass  # Placeholder function, can be used to visualize the grid 
 
# Create grid and convert characters to Node objects 
grid_layout = [ 
    ["S", ".", ".", ".", "."], 
    ["#", "#", ".", "#", "."], 
    [".", ".", ".", "#", "."], 
    [".", "#", "#", "#", "."], 
    [".", ".", ".", ".", "E"], 
] 
 
grid = [[Node(r, c) if cell != "#" else "#" for c, cell in enumerate(row)] 
for r, row in enumerate(grid_layout)] 
 
# Add neighbors for each node 
for row in grid: 
    for node in row: 
        if node != "#": 
            node.add_neighbors(grid) 
 
start = grid[0][0]  # Start node (S) 
end = grid[4][4]  # End node (E) 
 
# Run A* algorithm 
if astar(draw, grid, start, end): 
print("Path found!") 
else: 
print("No path available.") 