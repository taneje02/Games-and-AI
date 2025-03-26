import pygame
import math
from queue import PriorityQueue

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")

# Define colors for visualization
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255 , 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUISE = (64, 224, 208)

class Vertex:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUISE

    def reset(self):
        self.color = WHITE

    def make_closed(self):
        self.color = RED

    def make_start(self):
        self.color = ORANGE

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUISE

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other): # For PriorityQueue, not used in this specific implementation
        return False


def h(p1, p2):
    """
    Heuristic function (Manhattan distance) to estimate the distance between two points.
    """
    x1, y1 = p1
    x2, y2 = p2
    #return 0 # Dijkstra (if you want to see Dijkstra's behavior)
    return abs(x2 - x1) + abs(y2 - y1) # Manhattan distance


def reconstruct_path(came_from, current, draw):
    """
    Reconstructs the path from the end node back to the start node.
    """
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw() # Redraw the screen to show the path being constructed


def astar(draw, grid, start, end):
    """
    Implements the A* pathfinding algorithm.

    Args:
        draw: A function to redraw the grid on the screen.
        grid: The 2D list representing the grid of Vertex objects.
        start: The starting Vertex object.
        end: The ending Vertex object.

    Returns:
        True if a path is found, False otherwise.
    """
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start)) # (f_score, count, node) - f_score is priority
    came_from = {} # Dictionary to store the previous node for each node in the path
    g_score = {vertex: float("inf") for row in grid for vertex in row} # Cost from start to node
    g_score[start] = 0
    f_score = {vertex: float("inf") for row in grid for vertex in row} # Estimated total cost from start to end through node
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start} # To keep track of items in the priority queue for efficient checking

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2] # Get the node with the lowest f_score
        open_set_hash.remove(current)

        if current == end: # If the current node is the end node, we found a path
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True # Path found

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1 # Cost to reach neighbor from current node (assuming cost of 1 to move to adjacent cell)

            if temp_g_score < g_score[neighbor]: # If a shorter path to the neighbor is found
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos()) # Calculate the new f_score
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open() # Mark the neighbor as being in the open set

        draw() # Redraw the screen to show the progress

        if current != start:
            current.make_closed() # Mark the current node as explored

    return False # No path found


def make_grid(rows, width):
    """
    Creates a grid of Vertex objects.
    """
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            vertex = Vertex(i, j, gap, rows)
            grid[i].append(vertex)
    return grid


def draw_grid(win, rows, width):
    """
    Draws the grid lines on the Pygame window.
    """
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
    for j in range(rows):
        pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
    """
    Clears the screen and draws the grid and all the Vertex objects.
    """
    win.fill(WHITE)

    for row in grid:
        for vertex in row:
            vertex.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()


def get_clicked_pos(pos, rows, width):
    """
    Gets the row and column index of the grid cell that was clicked.
    """
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col


def main(win, width):
    """
    The main function that runs the Pygame window and handles user interaction.
    """
    ROWS = 50 # Number of rows and columns in the grid
    grid = make_grid(ROWS, width)

    start = None
    end = None

    run = True
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]: # LEFT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                vertex = grid[row][col]
                if not start and vertex != end:
                    start = vertex
                    start.make_start()

                elif not end and vertex != start:
                    end = vertex
                    end.make_end()

                elif vertex != end and vertex != start:
                    vertex.make_barrier()

            elif pygame.mouse.get_pressed()[2]: # RIGHT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                vertex = grid[row][col]
                vertex.reset()
                if vertex == start:
                    start = None
                elif vertex == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for vertex in row:
                            vertex.update_neighbors(grid)

                    astar(lambda: draw(win, grid, ROWS, width), grid, start, end)
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)
        pygame.quit()

main(WIN, WIDTH)