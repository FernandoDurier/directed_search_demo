# Import necessary libraries
import pygame  # Library for creating games and multimedia applications
import heapq  # Implements a priority queue algorithm
from collections import deque  # Implements a double-ended queue

# Pygame initialization
pygame.init()  # Initialize all imported Pygame modules

# Constants
# Define colors using RGB format
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600  # Screen dimensions
BACKGROUND_COLOR = (255, 255, 255)  # White background
NODE_COLOR = (0, 0, 255)  # Blue for nodes
EDGE_COLOR = (0, 0, 0)  # Black for edges
VISITED_COLOR = (255, 0, 0)  # Red for visited nodes
PATH_COLOR = (0, 255, 0)  # Green for the final path
FONT_COLOR = (0, 0, 0)  # Black for text
NODE_RADIUS = 20  # Radius of nodes for drawing
DELAY_MS = 1000  # Delay in milliseconds for animation

# Graph representing Romania's map with distances between cities
romania_map = {
    'A':{"B":3,"H":4},
    'B':{"A":3,"C":4,"H":5},
    'C':{"B":4,"D":8,"G":3},
    'D':{"C":8,"E":2,"F":3,"G":8},
    'E':{"D":2},
    'F':{"D":3,"G":4},
    'G':{"C":3,"D":8,"F":4,"H":2},
    'H':{"A":4,"B":5,"G":2}
}

# Straight-line distances (heuristic) to Bucharest for A* and GBFS algorithms
distances_to_bucharest = {
    "A":15,
    "B":14,
    "C":10,
    "D":2,
    "E":0,
    "F":5,
    "G":9,
    "H":11
}

# Node positions for visualization purposes
city_positions = {
    'A': (50, 50), 'B': (200, 50), 'C': (300, 50),
    'D': (400, 50), 'E': (500, 50), 'F': (400, 200),
    'G': (300, 200), 'H': (200, 200)
}

# Set up the Pygame screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Create the display window
pygame.display.set_caption("Pathfinding from Arad to Bucharest")  # Set the window title
font = pygame.font.SysFont(None, 24)  # Load a default font for rendering text

# Drawing utility function to render the graph on the screen
def draw_graph(graph, visited, path):
    screen.fill(BACKGROUND_COLOR)  # Clear the screen with the background color
    
    # Draw edges between nodes and display costs
    for city in graph:
        for neighbor, cost in graph[city].items():
            pygame.draw.line(screen, EDGE_COLOR, city_positions[city], city_positions[neighbor], 2)  # Draw edge
            # Calculate the midpoint for displaying the cost
            midpoint = (
                (city_positions[city][0] + city_positions[neighbor][0]) // 2,
                (city_positions[city][1] + city_positions[neighbor][1]) // 2
            )
            # Render the cost label at the midpoint
            cost_label = font.render(str(cost), True, FONT_COLOR)
            screen.blit(cost_label, midpoint)  # Blit cost label to the screen

    # Draw nodes (cities) with their corresponding distances to Bucharest
    for city, pos in city_positions.items():
        color = NODE_COLOR  # Default color for nodes
        if city in visited:
            color = VISITED_COLOR  # Change color if the city has been visited
        if city in path:
            color = PATH_COLOR  # Change color if the city is part of the path
        pygame.draw.circle(screen, color, pos, NODE_RADIUS)  # Draw the city as a circle
        
        # Render the city's name and its distance to Bucharest
        label = font.render(f"{city} ({distances_to_bucharest[city]})", True, FONT_COLOR)
        screen.blit(label, (pos[0] - 30, pos[1] - 40))  # Position the label above the node
    
    pygame.display.flip()  # Update the display to show the drawn elements
    pygame.time.delay(DELAY_MS)  # Pause to create an animation effect

# Function to calculate the total cost of the path
def calculate_path_cost(graph, path):
    total_cost = 0  # Initialize total cost to zero
    for i in range(len(path) - 1):
        total_cost += graph[path[i]][path[i + 1]]  # Sum the costs of edges in the path
    return total_cost  # Return the total cost

# BFS Algorithm implementation
def bfs(graph, start, goal):
    queue = deque([(start, [start])])  # Initialize the queue with the starting city and the path
    visited = set()  # Set to keep track of visited cities
    visited_count = 0  # Count of visited nodes
    expanded_count = 0  # Count of expanded nodes
    
    while queue:  # Continue until the queue is empty
        current_city, path = queue.popleft()  # Dequeue the next city and its path
        expanded_count += 1  # Increment the count of expanded nodes
        
        if current_city == goal:  # Check if we reached the goal
            total_cost = calculate_path_cost(graph, path)  # Calculate the cost of the found path
            print(f"BFS: Visited {visited_count} nodes, Expanded {expanded_count} nodes.")  # Print stats
            return path, total_cost  # Return the path and its cost

        if current_city not in visited:  # If the city has not been visited
            visited.add(current_city)  # Mark it as visited
            visited_count += 1  # Increment the count of visited nodes

        for neighbor in graph[current_city]:  # Iterate over neighbors
            if neighbor not in visited and neighbor not in [city for city, _ in queue]:
                queue.append((neighbor, path + [neighbor]))  # Add the neighbor and the updated path to the queue
        
        draw_graph(graph, visited, path)  # Draw the current state of the graph

    print("BFS: No path found.")  # If the queue is empty and goal not reached
    return None, float('inf')  # Return None and infinite cost

# DFS Algorithm implementation
def dfs(graph, start, goal):
    stack = [(start, [start])]  # Initialize the stack with the starting city and the path
    visited = set()  # Set to keep track of visited cities
    visited_count = 0  # Count of visited nodes
    expanded_count = 0  # Count of expanded nodes

    while stack:  # Continue until the stack is empty
        current_city, path = stack.pop()  # Pop the next city and its path
        expanded_count += 1  # Increment the count of expanded nodes

        if current_city == goal:  # Check if we reached the goal
            total_cost = calculate_path_cost(graph, path)  # Calculate the cost of the found path
            print(f"DFS: Visited {visited_count} nodes, Expanded {expanded_count} nodes.")  # Print stats
            return path, total_cost  # Return the path and its cost

        if current_city not in visited:  # If the city has not been visited
            visited.add(current_city)  # Mark it as visited
            visited_count += 1  # Increment the count of visited nodes

            for neighbor in reversed(graph[current_city]):  # Iterate over neighbors in reverse order
                if neighbor not in visited:
                    stack.append((neighbor, path + [neighbor]))  # Add neighbor and the updated path to the stack
        
        draw_graph(graph, visited, path)  # Draw the current state of the graph

    print("DFS: No path found.")  # If the stack is empty and goal not reached
    return None, float('inf')  # Return None and infinite cost

# UCS Algorithm implementation
def ucs(graph, start, goal):
    queue = [(0, start, [start])]  # Initialize the priority queue with cost, city, and path
    visited = set()  # Set to keep track of visited cities
    visited_count = 0  # Count of visited nodes
    expanded_count = 0  # Count of expanded nodes

    while queue:  # Continue until the queue is empty
        cost, current_city, path = heapq.heappop(queue)  # Dequeue the city with the lowest cost
        expanded_count += 1  # Increment the count of expanded nodes

        if current_city == goal:  # Check if we reached the goal
            print(f"UCS: Visited {visited_count} nodes, Expanded {expanded_count} nodes.")  # Print stats
            return path, cost  # Return the path and its cost

        if current_city not in visited:  # If the city has not been visited
            visited.add(current_city)  # Mark it as visited
            visited_count += 1  # Increment the count of visited nodes

            for neighbor in graph[current_city]:  # Iterate over neighbors
                if neighbor not in visited:
                    new_cost = cost + graph[current_city][neighbor]  # Calculate the new cost
                    heapq.heappush(queue, (new_cost, neighbor, path + [neighbor]))  # Add to the queue with the new cost
        
        draw_graph(graph, visited, path)  # Draw the current state of the graph

    print("UCS: No path found.")  # If the queue is empty and goal not reached
    return None, float('inf')  # Return None and infinite cost

# Dijkstra's Algorithm implementation
def dijkstra(graph, start, goal):
    queue = [(0, start, [start])]  # Initialize the priority queue with cost, city, and path
    visited = set()  # Set to keep track of visited cities
    visited_count = 0  # Count of visited nodes
    expanded_count = 0  # Count of expanded nodes

    while queue:  # Continue until the queue is empty
        cost, current_city, path = heapq.heappop(queue)  # Dequeue the city with the lowest cost
        expanded_count += 1  # Increment the count of expanded nodes

        if current_city == goal:  # Check if we reached the goal
            print(f"Dijkstra: Visited {visited_count} nodes, Expanded {expanded_count} nodes.")  # Print stats
            return path, cost  # Return the path and its cost

        if current_city not in visited:  # If the city has not been visited
            visited.add(current_city)  # Mark it as visited
            visited_count += 1  # Increment the count of visited nodes

            for neighbor in graph[current_city]:  # Iterate over neighbors
                if neighbor not in visited:
                    new_cost = cost + graph[current_city][neighbor]  # Calculate the new cost
                    heapq.heappush(queue, (new_cost, neighbor, path + [neighbor]))  # Add to the queue with the new cost
        
        draw_graph(graph, visited, path)  # Draw the current state of the graph

    print("Dijkstra: No path found.")  # If the queue is empty and goal not reached
    return None, float('inf')  # Return None and infinite cost

# Greedy Best-First Search Algorithm
def gbfs(graph, start, goal):
    open_set = [(distances_to_bucharest[start], start, [start])]
    visited = set()
    visited_count = 0  # Count of visited nodes
    expanded_count = 0  # Count of expanded nodes
    
    while open_set:
        _, current_city, path = heapq.heappop(open_set)
        expanded_count += 1  # We are expanding this node
        
        if current_city == goal:
            print(f"GBFS: Visited {visited_count} nodes, Expanded {expanded_count} nodes.")
            return path, calculate_path_cost(graph, path)

        if current_city not in visited:
            visited.add(current_city)
            visited_count += 1

        for neighbor in graph[current_city]:
            if neighbor not in visited and neighbor not in [city for _, city, _ in open_set]:
                heapq.heappush(open_set, (distances_to_bucharest[neighbor], neighbor, path + [neighbor]))
        
        draw_graph(graph, visited, path)  # Draw progress
    return None, 0

# A* Algorithm implementation
def a_star(graph, start, goal):
    queue = [(0 + distances_to_bucharest[start], start, [start])]  # Initialize the priority queue with cost + heuristic
    visited = set()  # Set to keep track of visited cities
    visited_count = 0  # Count of visited nodes
    expanded_count = 0  # Count of expanded nodes

    while queue:  # Continue until the queue is empty
        cost, current_city, path = heapq.heappop(queue)  # Dequeue the city with the lowest total cost
        expanded_count += 1  # Increment the count of expanded nodes

        if current_city == goal:  # Check if we reached the goal
            print(f"A*: Visited {visited_count} nodes, Expanded {expanded_count} nodes.")  # Print stats
            return path, cost  # Return the path and its cost

        if current_city not in visited:  # If the city has not been visited
            visited.add(current_city)  # Mark it as visited
            visited_count += 1  # Increment the count of visited nodes

            for neighbor in graph[current_city]:  # Iterate over neighbors
                if neighbor not in visited:
                    new_cost = cost - distances_to_bucharest[current_city] + graph[current_city][neighbor] + distances_to_bucharest[neighbor]  # Update total cost with heuristic
                    heapq.heappush(queue, (new_cost, neighbor, path + [neighbor]))  # Add to the queue with the new total cost
        
        draw_graph(graph, visited, path)  # Draw the current state of the graph

    print("A*: No path found.")  # If the queue is empty and goal not reached
    return None, float('inf')  # Return None and infinite cost

# Main function to run the pathfinding algorithms
def main():
    # Execute all pathfinding algorithms and visualize the results
    algorithms = [bfs, dfs, ucs, dijkstra, gbfs, a_star]  # List of algorithms to run
    start_city = 'A'  # Starting city
    goal_city = 'E'  # Goal city

    for algorithm in algorithms:  # Iterate through each algorithm
        print(f"Running {algorithm.__name__}...")  # Print the name of the algorithm
        path, cost = algorithm(romania_map, start_city, goal_city)  # Execute the algorithm
        if path:
            print(f"Path: {' -> '.join(path)}, Cost: {cost}")  # Print the path and its cost
        else:
            print("No path found.")  # If no path is found
    
    pygame.quit()  # Quit Pygame when done

# Run the main function if this script is executed
if __name__ == "__main__":
    main()  # Call the main function to start the program
