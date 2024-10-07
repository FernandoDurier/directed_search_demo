import pygame
import random
import math
import heapq
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
    pygame.display.set_caption("Labyrinth A* Pathfinding")
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
                math.sqrt((start_pos[0] - i) ** 2 + (start_pos[1] - j) ** 2), 1
            )
            labyrinth[i][j]["distance_to_exit"] = round(
                math.sqrt((exit_pos[0] - i) ** 2 + (exit_pos[1] - j) ** 2), 1
            )

            # Connections (including borders as walls)
            if i > 0 and not labyrinth[i - 1][j]["wall"]:  # Up
                labyrinth[i][j]["connections"]["up"] = labyrinth[i - 1][j]["id"]
            if i < n_rows - 1 and not labyrinth[i + 1][j]["wall"]:  # Down
                labyrinth[i][j]["connections"]["down"] = labyrinth[i + 1][j]["id"]
            if j > 0 and not labyrinth[i][j - 1]["wall"]:  # Left
                labyrinth[i][j]["connections"]["left"] = labyrinth[i][j - 1]["id"]
            if j < n_cols - 1 and not labyrinth[i][j + 1]["wall"]:  # Right
                labyrinth[i][j]["connections"]["right"] = labyrinth[i][j + 1]["id"]
            if i > 0 and j < n_cols - 1 and not labyrinth[i - 1][j + 1]["wall"]:  # Diagonal up right
                labyrinth[i][j]["connections"]["diag_up_right"] = labyrinth[i - 1][j + 1]["id"]
            if i < n_rows - 1 and j < n_cols - 1 and not labyrinth[i + 1][j + 1]["wall"]:  # Diagonal down right
                labyrinth[i][j]["connections"]["diag_down_right"] = labyrinth[i + 1][j + 1]["id"]
            if i < n_rows - 1 and j > 0 and not labyrinth[i + 1][j - 1]["wall"]:  # Diagonal down left
                labyrinth[i][j]["connections"]["diag_down_left"] = labyrinth[i + 1][j - 1]["id"]
            if i > 0 and j > 0 and not labyrinth[i - 1][j - 1]["wall"]:  # Diagonal up left
                labyrinth[i][j]["connections"]["diag_up_left"] = labyrinth[i - 1][j - 1]["id"]

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

            # Display text: ID in the center, distances on corners
            font = pygame.font.SysFont(None, 24)
            id_text = font.render(str(cell["id"]), True, (0, 0, 0))
            start_dist_text = font.render(f"S: {cell['distance_from_start']}", True, (0, 0, 0))
            exit_dist_text = font.render(f"E: {cell['distance_to_exit']}", True, (0, 0, 0))

            # Place text in the cell
            screen.blit(id_text, (x + CELL_SIZE // 2 - 10, y + CELL_SIZE // 2 - 10))
            screen.blit(start_dist_text, (x + 5, y + 5))
            screen.blit(exit_dist_text, (x + CELL_SIZE - 40, y + 5))

    pygame.display.flip()

# A* algorithm with visual feedback
def a_star_search_with_ui(labyrinth, start_pos, exit_pos, screen):
    def get_heuristic(pos):
        return labyrinth[pos[0]][pos[1]]["distance_to_exit"]

    n_rows, n_cols = len(labyrinth), len(labyrinth[0])
    open_list = []
    heapq.heappush(open_list, (0, 0, start_pos, []))

    g_costs = {start_pos: 0}
    visited = set()

    while open_list:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None

        f, g, current, path = heapq.heappop(open_list)
        if current in visited:
            continue
        visited.add(current)

        new_path = path + [current]

        # Print the current cell being explored
        print(f"Exploring: {current}")

        if current == exit_pos:
            return new_path

        connections = labyrinth[current[0]][current[1]]["connections"]
        for direction, neighbor_id in connections.items():
            if neighbor_id is not None:
                neighbor_row, neighbor_col = (int(neighbor_id) - 1) // n_cols, (int(neighbor_id) - 1) % n_cols
                if (neighbor_row, neighbor_col) not in visited and not labyrinth[neighbor_row][neighbor_col]["wall"]:
                    g_cost = g + 1  # Assuming uniform cost for movement
                    f_cost = g_cost + get_heuristic((neighbor_row, neighbor_col))

                    if (neighbor_row, neighbor_col) not in g_costs or g_cost < g_costs[(neighbor_row, neighbor_col)]:
                        g_costs[(neighbor_row, neighbor_col)] = g_cost
                        heapq.heappush(open_list, (f_cost, g_cost, (neighbor_row, neighbor_col), new_path))

        draw_labyrinth(screen, labyrinth, new_path, visited, start_pos, exit_pos)
        pygame.time.delay(DELAY_MS)  # Delay for visualization

    return None  # No path found

# Save final screen as JPG with timestamp
def save_screen_as_jpg(screen):
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    filename = f"a_star_labyrinth_{timestamp}.jpg"
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

    # Run A* pathfinding
    path = a_star_search_with_ui(labyrinth, start_pos, exit_pos, screen)
    if path is not None:
        print(f"Path found: {path}")
        draw_labyrinth(screen, labyrinth, path, [], start_pos, exit_pos)  # Draw final path
        pygame.time.delay(2000)  # Wait before saving
        save_screen_as_jpg(screen)  # Save the screen as JPG

    pygame.quit()

if __name__ == "__main__":
    main()
