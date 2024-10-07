## Directed Search Demonstrations

This project has the purpose of demonstrating different directed search algorithms, so the user can see how much each consumes resources when exploring the labyrinth.

### In order to run this project do the following:

1. Once the project has been downloaded, issue the command `python -m venv venv`
2. Then issue `source ./venv/bin/activate`
3. Then install dependencies `pip install -r requirements.txt`
4. Now issue the command `python <algorithm you want to watch>_app.py`

### Project Composition:

* app.py - common initial implementation visualizing on terminal itself (with A*).
* a_star_app.py - demonstration in PyGame relying upon A* algorithm, whereas each square of the labyrinth may be traversible or a wall. Each square has the distance from start (normal distance in algorithms), and the distance from exit (the heuristic scent that A* relies upon).
* dijkstra_app.py - demonstration in PyGame relying upon Dijkstra algorithm.
* bfs_app.py - demonstration in PyGame relying upon BFS algorithm.
* dfs_app.py - demonstration in PyGame relying upon DFS algorithm.

#### Output Files Saving:
* Last screen of final path will be saved in the root folder of this project for future analysis.