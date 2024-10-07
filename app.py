import random
import math

labyrinth_space = []

# Start and Exit Randomly defined with distance constraint
def generating_labyrinth(labyrinth_space, n_rows, n_cols, wall_ratio, min_distance):

    labyrinth = labyrinth_space

    # initializing lab matrix
    for n in range(n_rows):
        labyrinth.append([])

    num_squares = n_rows * n_cols
    exp_walls = int(num_squares * wall_ratio)
    walls_counter = 0
    start_defined = False
    exit_defined = False

    start_pos = (None, None)
    exit_pos = (None, None)

    counter = 0

    # Building the labyrinth
    for i in range(n_rows):
        for j in range(n_cols):
            counter += 1
            obj = {
                "id": None,
                "start": False,
                "wall": False,
                "exit": False,
                "distance_from_start": None,
                "distance_to_exit": None,
                "connections": {
                    "up": None,
                    "diag_up_right": None,
                    "right": None,
                    "diag_down_right": None,
                    "down": None,
                    "diag_down_left": None,
                    "left": None,
                    "diag_up_left": None
                }
            }
            obj["id"] = str(counter)

            if walls_counter <= exp_walls:
                obj["wall"] = random.random() < 0.3
                if obj["wall"]:
                    walls_counter += 1

            labyrinth[i].append(obj)

    # Assign start and exit positions with minimum distance constraint
    while True:
        start_pos = (random.randint(0, n_rows - 1), random.randint(0, n_cols - 1))
        if not labyrinth[start_pos[0]][start_pos[1]]["wall"]:
            labyrinth[start_pos[0]][start_pos[1]]["start"] = True
            break

    while True:
        exit_pos = (random.randint(0, n_rows - 1), random.randint(0, n_cols - 1))
        if not labyrinth[exit_pos[0]][exit_pos[1]]["wall"] and start_pos != exit_pos:
            distance = math.sqrt((start_pos[0] - exit_pos[0]) ** 2 + (start_pos[1] - exit_pos[1]) ** 2)
            if distance >= min_distance:  # Ensure minimum distance
                labyrinth[exit_pos[0]][exit_pos[1]]["exit"] = True
                break

    # Painting Heuristic
    for i in range(n_rows):
        for j in range(n_cols):
            labyrinth[i][j]["distance_from_start"] = round(
                math.sqrt((start_pos[0] - i) ** 2 + (start_pos[1] - j) ** 2), 1)
            labyrinth[i][j]["distance_to_exit"] = round(
                math.sqrt((exit_pos[0] - i) ** 2 + (exit_pos[1] - j) ** 2), 1)

            # Connections (optional)
            try:
                if not labyrinth[i][j + 1]["wall"]:
                    labyrinth[i][j]["connections"]["up"] = labyrinth[i][j + 1]["id"]
            except:
                labyrinth[i][j]["connections"]["up"] = None

            try:
                if not labyrinth[i + 1][j + 1]["wall"]:
                    labyrinth[i][j]["connections"]["diag_up_right"] = labyrinth[i + 1][j + 1]["id"]
            except:
                labyrinth[i][j]["connections"]["diag_up_right"] = None

            try:
                if not labyrinth[i + 1][j]["wall"]:
                    labyrinth[i][j]["connections"]["right"] = labyrinth[i + 1][j]["id"]
            except:
                labyrinth[i][j]["connections"]["right"] = None

            try:
                if not labyrinth[i + 1][j - 1]["wall"]:
                    labyrinth[i][j]["connections"]["diag_down_right"] = labyrinth[i + 1][j - 1]["id"]
            except:
                labyrinth[i][j]["connections"]["diag_down_right"] = None

            try:
                if not labyrinth[i][j - 1]["wall"]:
                    labyrinth[i][j]["connections"]["down"] = labyrinth[i][j - 1]["id"]
            except:
                labyrinth[i][j]["connections"]["down"] = None

            try:
                if not labyrinth[i - 1][j - 1]["wall"]:
                    labyrinth[i][j]["connections"]["diag_down_left"] = labyrinth[i - 1][j - 1]["id"]
            except:
                labyrinth[i][j]["connections"]["diag_down_left"] = None

            try:
                if not labyrinth[i - 1][j]["wall"]:
                    labyrinth[i][j]["connections"]["left"] = labyrinth[i - 1][j]["id"]
            except:
                labyrinth[i][j]["connections"]["left"] = None

            try:
                if not labyrinth[i - 1][j + 1]["wall"]:
                    labyrinth[i][j]["connections"]["diag_up_left"] = labyrinth[i - 1][j + 1]["id"]
            except:
                labyrinth[i][j]["connections"]["diag_up_left"] = None

    return labyrinth, start_pos, exit_pos

# Function to print the labyrinth
def print_labyrinth(labyrinth):
    for row in labyrinth:
        row_str = ""
        for cell in row:
            if cell["start"]:
                row_str += "S "  # Start position
            elif cell["exit"]:
                row_str += "E "  # Exit position
            elif cell["wall"]:
                row_str += "█ "  # Wall
            else:
                row_str += ". "  # Open space
        print(row_str)

# Parameters
nrows = 5
ncols = 5
min_distance = 3  # Minimum distance between start and exit

# Generating and printing the labyrinth
labyrinth_space, start_pos, exit_pos = generating_labyrinth(labyrinth_space=labyrinth_space, n_rows=nrows, n_cols=ncols, wall_ratio=0.2, min_distance=min_distance)
print_labyrinth(labyrinth_space)


import heapq

# A* Algorithm utilizing labyrinth structure
def a_star_search(labyrinth, start_pos, exit_pos):
    # Extract the distance from the labyrinth directly
    def get_heuristic(pos):
        return labyrinth[pos[0]][pos[1]]["distance_to_exit"]

    n_rows, n_cols = len(labyrinth), len(labyrinth[0])
    
    # Priority queue: (f, g, (x, y), path)
    open_list = []
    heapq.heappush(open_list, (0, 0, start_pos, []))
    
    # Costs and visited sets
    g_costs = {start_pos: 0}
    visited = set()
    
    while open_list:
        f, g, current, path = heapq.heappop(open_list)

        if current in visited:
            continue
        visited.add(current)

        # Append current position to the path
        new_path = path + [current]

        # If we reach the exit, return the path
        if current == exit_pos:
            return new_path

        # Explore neighbors, including diagonals
        connections = labyrinth[current[0]][current[1]]["connections"]
        neighbors = [
            (current[0] - 1, current[1]),  # Up
            (current[0] + 1, current[1]),  # Down
            (current[0], current[1] - 1),  # Left
            (current[0], current[1] + 1),  # Right
            (current[0] - 1, current[1] + 1),  # Diagonal up-right
            (current[0] + 1, current[1] + 1),  # Diagonal down-right
            (current[0] + 1, current[1] - 1),  # Diagonal down-left
            (current[0] - 1, current[1] - 1),  # Diagonal up-left
        ]
        
        for direction, conn in connections.items():
            if conn:  # Check if a connection exists
                neighbor = neighbors[["up", "diag_up_right", "right", "diag_down_right", 
                                      "down", "diag_down_left", "left", "diag_up_left"].index(direction)]
                x, y = neighbor

                if 0 <= x < n_rows and 0 <= y < n_cols and not labyrinth[x][y]["wall"]:
                    new_g = g + 1  # Assuming uniform cost for moving
                    if neighbor not in g_costs or new_g < g_costs[neighbor]:
                        g_costs[neighbor] = new_g
                        h = get_heuristic(neighbor)
                        f = new_g + h
                        heapq.heappush(open_list, (f, new_g, neighbor, new_path))

    return None  # No path found

# Function to visualize the path in the labyrinth
def print_labyrinth_with_path(labyrinth, path):
    for i, row in enumerate(labyrinth):
        row_str = ""
        for j, cell in enumerate(row):
            if (i, j) in path:
                row_str += "P "  # Path
            elif cell["start"]:
                row_str += "S "  # Start position
            elif cell["exit"]:
                row_str += "E "  # Exit position
            elif cell["wall"]:
                row_str += "█ "  # Wall
            else:
                row_str += ". "  # Open space
        print(row_str)

# Run A* on the generated labyrinth
path = a_star_search(labyrinth_space, start_pos, exit_pos)
if path:
    print("Path found!")
    print_labyrinth_with_path(labyrinth_space, path)
else:
    print("No path found.")
