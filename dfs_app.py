import pygame
import random
import math
import datetime  # Import datetime for timestamp

# Initialize pygame
pygame.init()

# Constants
CELL_SIZE = 100  # Increased square size
GRID_COLOR = (200, 200, 200)
WALL_COLOR = (0, 0, 0)
START_COLOR = (128, 0, 128)  # Purple for start
EXIT_COLOR = (255, 255, 0)  # Yellow for exit
PATH_COLOR = (0, 255, 0)  # Green for final path
EXPLORED_COLOR = (0, 0, 255)  # Blue for explored cells
DELAY_MS = 100  # Delay in milliseconds

# Initialize screen
def init_screen(n_rows, n_cols):
    screen = pygame.display.set_mode((n_cols * CELL_SIZE, n_rows * CELL_SIZE))
    pygame.display.set_caption("Labyrinth DFS Pathfinding")
    return screen

# Start and Exit Randomly defined with distance constraint
def generating_labyrinth(labyrinth_space, n_rows, n_cols, wall_ratio, min_distance):
    labyrinth = labyrinth_space

    # Initializing lab matrix
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
                "id": counter,  # Directly use the counter for ID
                "start": False,
                "wall": False,
                "exit": False,
                "distance_from_start": float('inf'),  # Initialize to infinity
                "connections": {
                    "up": None,
                    "right": None,
                    "down": None,
                    "left": None
                }
            }

            if walls_counter < exp_walls:
                obj["wall"] = random.random() < 0.3
                if obj["wall"]:
                    walls_counter += 1

            labyrinth[i].append(obj)

    # Assign start and exit positions with minimum distance constraint
    while True:
        start_pos = (random.randint(0, n_rows - 1), random.randint(0, n_cols - 1))
        if not labyrinth[start_pos[0]][start_pos[1]]["wall"]:
            labyrinth[start_pos[0]][start_pos[1]]["start"] = True
            labyrinth[start_pos[0]][start_pos[1]]["distance_from_start"] = 0  # Distance to start is 0
            break

    while True:
        exit_pos = (random.randint(0, n_rows - 1), random.randint(0, n_cols - 1))
        if not labyrinth[exit_pos[0]][exit_pos[1]]["wall"] and start_pos != exit_pos:
            distance = math.sqrt((start_pos[0] - exit_pos[0]) ** 2 + (start_pos[1] - exit_pos[1]) ** 2)
            if distance >= min_distance:  # Ensure minimum distance
                labyrinth[exit_pos[0]][exit_pos[1]]["exit"] = True
                break

    # Connections (including borders as walls)
    for i in range(n_rows):
        for j in range(n_cols):
            if i > 0 and not labyrinth[i - 1][j]["wall"]:  # Up
                labyrinth[i][j]["connections"]["up"] = (i - 1, j)
            if i < n_rows - 1 and not labyrinth[i + 1][j]["wall"]:  # Down
                labyrinth[i][j]["connections"]["down"] = (i + 1, j)
            if j > 0 and not labyrinth[i][j - 1]["wall"]:  # Left
                labyrinth[i][j]["connections"]["left"] = (i, j - 1)
            if j < n_cols - 1 and not labyrinth[i][j + 1]["wall"]:  # Right
                labyrinth[i][j]["connections"]["right"] = (i, j + 1)

    return labyrinth, start_pos, exit_pos

# Draw the labyrinth on the screen
def draw_labyrinth(screen, labyrinth, path, visited, start_pos, exit_pos):
    screen.fill(GRID_COLOR)

    for i, row in enumerate(labyrinth):
        for j, cell in enumerate(row):
            x, y = j * CELL_SIZE, i * CELL_SIZE

            # Colors based on the current status of the cell
            if cell["wall"]:
                color = WALL_COLOR
            elif (i, j) == start_pos:
                color = START_COLOR
            elif (i, j) == exit_pos:
                color = EXIT_COLOR
            elif (i, j) in path:
                color = PATH_COLOR  # Final path color (green)
            elif (i, j) in visited:
                color = EXPLORED_COLOR  # Explored cells color (blue)
            else:
                color = GRID_COLOR

            # Draw cell background
            pygame.draw.rect(screen, color, pygame.Rect(x, y, CELL_SIZE, CELL_SIZE))

            # Draw borders
            pygame.draw.rect(screen, WALL_COLOR, pygame.Rect(x, y, CELL_SIZE, CELL_SIZE), 2)  # Thicker border

            # Display text: ID in the center
            font = pygame.font.SysFont(None, 24)
            id_text = font.render(str(cell["id"]), True, (0, 0, 0))
            screen.blit(id_text, (x + CELL_SIZE // 2 - 10, y + CELL_SIZE // 2 - 10))

    pygame.display.flip()

# Depth-First Search algorithm with visual feedback
def dfs_search_with_ui(labyrinth, start_pos, exit_pos, screen):
    stack = [start_pos]
    visited = set()
    path = []
    found = False

    while stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None

        current = stack.pop()
        visited.add(current)

        # Print the current cell being explored
        print(f"Exploring: {current}")

        if current == exit_pos:
            found = True
            break

        connections = labyrinth[current[0]][current[1]]["connections"]
        for direction, neighbor in connections.items():
            if neighbor is not None:
                neighbor_row, neighbor_col = neighbor

                if not labyrinth[neighbor_row][neighbor_col]["wall"] and neighbor not in visited:
                    # Calculate distance from the start node
                    labyrinth[neighbor_row][neighbor_col]["distance_from_start"] = labyrinth[current[0]][current[1]]["distance_from_start"] + 1
                    stack.append(neighbor)

        draw_labyrinth(screen, labyrinth, [], visited, start_pos, exit_pos)
        pygame.time.delay(DELAY_MS)  # Delay for visualization

    if found:
        # Backtrack to create the path
        path = []
        current = exit_pos
        while current is not None and current in visited:
            path.append(current)
            # Find the previous cell based on distance from start
            for direction, neighbor in labyrinth[current[0]][current[1]]["connections"].items():
                if neighbor is not None:
                    neighbor_row, neighbor_col = neighbor
                    if labyrinth[neighbor_row][neighbor_col]["distance_from_start"] == labyrinth[current[0]][current[1]]["distance_from_start"] - 1:
                        current = (neighbor_row, neighbor_col)
                        break
            else:
                current = None
        return path[::-1]  # Return the path from start to exit

    return None  # No path found

# Save final screen as JPG with timestamp
def save_screen_as_jpg(screen):
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    filename = f"dfs_labyrinth_{timestamp}.jpg"
    pygame.image.save(screen, filename)
    print(f"Screen saved as {filename}")

# Main function
def main():
    n_rows, n_cols = 8, 8
    wall_ratio = 0.4
    min_distance = 5

    screen = init_screen(n_rows, n_cols)

    labyrinth = []
    labyrinth, start_pos, exit_pos = generating_labyrinth(labyrinth, n_rows, n_cols, wall_ratio, min_distance)

    # Run DFS pathfinding
    path = dfs_search_with_ui(labyrinth, start_pos, exit_pos, screen)
    if path is not None:
        print(f"Path found: {path}")
        draw_labyrinth(screen, labyrinth, path, [], start_pos, exit_pos)  # Draw final path
        pygame.time.delay(2000)  # Wait before saving
        save_screen_as_jpg(screen)  # Save the screen as a JPG
    else:
        print("No path found!")

    pygame.quit()

if __name__ == "__main__":
    main()
