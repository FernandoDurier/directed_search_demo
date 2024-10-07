import pygame
import heapq
from collections import deque

# Pygame initialization
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BACKGROUND_COLOR = (255, 255, 255)
NODE_COLOR = (0, 0, 255)
EDGE_COLOR = (0, 0, 0)
VISITED_COLOR = (255, 0, 0)
PATH_COLOR = (0, 255, 0)
FONT_COLOR = (0, 0, 0)
NODE_RADIUS = 20
DELAY_MS = 500

# Graph for Romania map with distances
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

# Straight-line distances (heuristic) to Bucharest
distances_to_bucharest = {
    'Arad': 366, 'Zerind': 374, 'Oradea': 380, 'Sibiu': 253, 'Fagaras': 176,
    'Rimnicu Vilcea': 193, 'Craiova': 160, 'Pitesti': 100, 'Timisoara': 329,
    'Lugoj': 244, 'Mehadia': 241, 'Drobeta': 242, 'Bucharest': 0,
    'Giurgiu': 77, 'Urziceni': 80, 'Hirsova': 151, 'Eforie': 161,
    'Vaslui': 199, 'Iasi': 226, 'Neant': 234
}

# Node positions for visualization (simplified layout)
city_positions = {
    'Arad': (50, 50), 'Zerind': (100, 100), 'Oradea': (150, 50),
    'Sibiu': (200, 150), 'Fagaras': (300, 100), 'Rimnicu Vilcea': (250, 250),
    'Craiova': (350, 350), 'Pitesti': (450, 250), 'Bucharest': (500, 350),
    'Timisoara': (50, 150), 'Lugoj': (100, 250), 'Mehadia': (150, 350),
    'Drobeta': (200, 450), 'Giurgiu': (500, 450), 'Urziceni': (400, 350),
    'Hirsova': (350, 200), 'Eforie': (250, 300), 'Vaslui': (300, 400),
    'Iasi': (350, 500), 'Neant': (380, 550)
}


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pathfinding from Arad to Bucharest")
font = pygame.font.SysFont(None, 24)


# Drawing utilities
def draw_graph(graph, visited, path):
    screen.fill(BACKGROUND_COLOR)
    
    # Draw edges with costs
    for city in graph:
        for neighbor, cost in graph[city].items():
            pygame.draw.line(screen, EDGE_COLOR, city_positions[city], city_positions[neighbor], 2)
            # Display edge costs
            midpoint = (
                (city_positions[city][0] + city_positions[neighbor][0]) // 2,
                (city_positions[city][1] + city_positions[neighbor][1]) // 2
            )
            cost_label = font.render(str(cost), True, FONT_COLOR)
            screen.blit(cost_label, midpoint)

    # Draw nodes with distance to Bucharest
    for city, pos in city_positions.items():
        color = NODE_COLOR
        if city in visited:
            color = VISITED_COLOR
        if city in path:
            color = PATH_COLOR
        pygame.draw.circle(screen, color, pos, NODE_RADIUS)
        
        label = font.render(f"{city} ({distances_to_bucharest[city]})", True, FONT_COLOR)
        screen.blit(label, (pos[0] - 30, pos[1] - 40))
    
    pygame.display.flip()
    pygame.time.delay(DELAY_MS)


# BFS Algorithm
def bfs(graph, start, goal):
    queue = deque([(start, [start])])
    visited = set()
    visited_count = 0  # Count of visited nodes
    expanded_count = 0  # Count of expanded nodes
    
    while queue:
        current_city, path = queue.popleft()
        expanded_count += 1  # We are expanding this node
        
        if current_city == goal:
            total_cost = calculate_path_cost(graph, path)
            print(f"BFS: Visited {visited_count} nodes, Expanded {expanded_count} nodes.")
            return path, total_cost

        if current_city not in visited:
            visited.add(current_city)
            visited_count += 1

        for neighbor in graph[current_city]:
            if neighbor not in visited and neighbor not in [city for city, _ in queue]:
                queue.append((neighbor, path + [neighbor]))
        
        draw_graph(graph, visited, path)  # Draw progress
    return None, 0


# DFS Algorithm
def dfs(graph, start, goal):
    stack = [(start, [start])]
    visited = set()
    visited_count = 0  # Count of visited nodes
    expanded_count = 0  # Count of expanded nodes
    
    while stack:
        current_city, path = stack.pop()
        expanded_count += 1  # We are expanding this node
        
        if current_city == goal:
            total_cost = calculate_path_cost(graph, path)
            print(f"DFS: Visited {visited_count} nodes, Expanded {expanded_count} nodes.")
            return path, total_cost

        if current_city not in visited:
            visited.add(current_city)
            visited_count += 1

        for neighbor in graph[current_city]:
            if neighbor not in visited and neighbor not in [city for city, _ in stack]:
                stack.append((neighbor, path + [neighbor]))
        
        draw_graph(graph, visited, path)  # Draw progress
    return None, 0


# UCS Algorithm
def ucs(graph, start, goal):
    queue = [(0, start, [start])]
    visited = set()
    visited_count = 0  # Count of visited nodes
    expanded_count = 0  # Count of expanded nodes
    
    while queue:
        cost, current_city, path = heapq.heappop(queue)
        expanded_count += 1  # We are expanding this node
        
        if current_city == goal:
            print(f"UCS: Visited {visited_count} nodes, Expanded {expanded_count} nodes.")
            return path, cost

        if current_city not in visited:
            visited.add(current_city)
            visited_count += 1

        for neighbor, neighbor_cost in graph[current_city].items():
            if neighbor not in visited:
                heapq.heappush(queue, (cost + neighbor_cost, neighbor, path + [neighbor]))
        
        draw_graph(graph, visited, path)  # Draw progress
    return None, 0


# A* Algorithm
def a_star(graph, start, goal):
    # A heuristic function: straight line distance approximation
    def heuristic(city):
        return distances_to_bucharest[city]

    queue = [(0, start, [start])]
    visited = set()
    visited_count = 0  # Count of visited nodes
    expanded_count = 0  # Count of expanded nodes
    
    while queue:
        cost, current_city, path = heapq.heappop(queue)
        expanded_count += 1  # We are expanding this node
        
        if current_city == goal:
            print(f"A*: Visited {visited_count} nodes, Expanded {expanded_count} nodes.")
            return path, cost

        if current_city not in visited:
            visited.add(current_city)
            visited_count += 1

        for neighbor, neighbor_cost in graph[current_city].items():
            if neighbor not in visited:
                total_cost = cost + neighbor_cost + heuristic(neighbor)
                heapq.heappush(queue, (total_cost, neighbor, path + [neighbor]))

        draw_graph(graph, visited, path)  # Draw progress
    return None, 0


# Utility to calculate path cost
def calculate_path_cost(graph, path):
    total_cost = 0
    for i in range(len(path) - 1):
        total_cost += graph[path[i]][path[i + 1]]
    return total_cost


# Main loop to run algorithms and display results
def main():
    algorithms = [("BFS", bfs), ("DFS", dfs), ("UCS", ucs), ("A*", a_star)]
    start_city, goal_city = "Arad", "Bucharest"

    for name, algorithm in algorithms:
        print(f"Running {name}...")
        path, total_cost = algorithm(romania_map, start_city, goal_city)
        print(f"Path found by {name}: {path} with total cost: {total_cost}")
        draw_graph(romania_map, path, path)  # Final path display
        pygame.time.delay(2000)  # Pause for 2 seconds before next algorithm

    pygame.quit()


if __name__ == "__main__":
    main()
