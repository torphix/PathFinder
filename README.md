# Overview

- The agent exists in a grid world and starts in the upper-left corner. 
- Each time it moves to an adjacent cell, it spends as many timesteps on this cell as the number on this cell.
- The goal is to reach the bottom right square of the grid in as few steps as possible


## Commands
Run a single type of pathfinder algorithm and view the output logs: --type can equal nearest_neighbour, dijkstra
required args: --type nearest_neighbour OR dijkstra
optional args: 
    --width (sets the width of the world default == 9)
    --height (sets the height of the world default == 9)
    --max (sets the maximum timestep possible == 9)
```python main.py run --type=nearest_neighbour```

To benchmark dijkstra vs nearest neighbour fill out the benchmark_config.yaml  and run command
```python main.py benchmark```


## Implementation

### World Creation
**1) Task: Create an implementation of the game:**  it should be flexible allowing the programmer to specify the height and width of the world

**Implementation:** Created a WorldClass that takes as inputs the desired height and width as well as the number min/max number of timesteps all subsequent path finder classes must inherit this class

**2) Task: Develop Your Own Heuristic Algorithm:** Does not have to optimized but should perform better than a randomwalk
**Implementation:** A simple nearest neighbour algorithm that scans the adjacent squares and has the agent take the smallest timestep value, note: an additional feature is that the agent will only head in the target direction in this case down or to the right

**3) Task: Implement Dijkstra's algorithm:**
**Implementation:** 
    - Formulate the world as a graph with the nodes being individual square and the edges being the amount of time to spend on each square
    - Start by setting the start node to 0
    - Get all adjoining edges to the node and add their value to the nodes value updating there value
    - Select the minmum node and repeat