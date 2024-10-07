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
DELAY_MS = 500  # Delay in milliseconds for animation

# Graph representing Romania's map with distances between cities
romania_map = {
    'Arad': {'Zerind': 75, 'Sibiu': 140, 'Timisoara': 118},
    'Zerind': {'Arad': 75, 'Oradea': 71},
    'Oradea': {'Zerind': 71, 'Sibiu': 151},
    'Sibiu': {'Arad': 140, 'Oradea': 151, 'Fagaras': 99, 'Rimnicu Vilcea': 80},
    'Fagaras': {'Sibiu': 99, 'Bucharest': 211},
    'Rimnicu Vilcea': {'Sibiu': 80, 'Craiova': 146, 'Pitesti': 97},
    'Timisoara': {'Arad': 118, 'Lugoj': 111},
    'Lugoj': {'Timisoara': 111, 'Mehadia': 70},
    'Mehadia': {'Lugoj': 70, 'Drobeta': 75},
    'Drobeta': {'Mehadia': 75, 'Craiova': 120},
    'Craiova': {'Drobeta': 120, 'Rimnicu Vilcea': 146, 'Pitesti': 138},
    'Pitesti': {'Rimnicu Vilcea': 97, 'Craiova': 138, 'Bucharest': 101},
    'Bucharest': {'Fagaras': 211, 'Pitesti': 101, 'Giurgiu': 90, 'Urziceni': 85},
    'Giurgiu': {'Bucharest': 90},
    'Urziceni': {'Hirsova': 98, 'Vaslui': 142},
    'Hirsova': {'Eforie': 86, 'Urziceni': 98},
    'Eforie': {'Hirsova': 86},
    'Vaslui': {'Hirsova': 142, 'Iasi': 92},
    'Iasi': {'Vaslui': 92, 'Neant': 87},
    'Neant': {'Iasi': 87},
}

# Straight-line distances (heuristic) to Bucharest for A* and GBFS algorithms
distances_to_bucharest = {
    'Arad': 366, 'Zerind': 374, 'Oradea': 380, 'Sibiu': 253, 'Fagaras': 176,
    'Rimnicu Vilcea': 193, 'Craiova': 160, 'Pitesti': 100, 'Timisoara': 329,
    'Lugoj': 244, 'Mehadia': 241, 'Drobeta': 242, 'Bucharest': 0,
    'Giurgiu': 77, 'Urziceni': 80, 'Hirsova': 151, 'Eforie': 161,
    'Vaslui': 199, 'Iasi': 226, 'Neant': 234
}

# Node positions for visualization purposes
city_positions = {
    'Arad': (50, 50), 'Zerind': (100, 100), 'Oradea': (150, 50),
    'Sibiu': (200, 150), 'Fagaras': (300, 100), 'Rimnicu Vilcea': (250, 250),
    'Craiova': (350, 350), 'Pitesti': (450, 250), 'Bucharest': (500, 350),
    'Timisoara': (50, 150), 'Lugoj': (100, 250), 'Mehadia': (150, 350),
    'Drobeta': (200, 450), 'Giurgiu': (500, 450), 'Urziceni': (400, 350),
    'Hirsova': (350, 200), 'Eforie': (250, 300), 'Vaslui': (300, 400),
    'Iasi': (350, 500), 'Neant': (380, 550)
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
    algorithms = [bfs, dfs, ucs, dijkstra, a_star]  # List of algorithms to run
    start_city = 'Arad'  # Starting city
    goal_city = 'Bucharest'  # Goal city

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
