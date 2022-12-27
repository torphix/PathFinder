# Overview
Problem formulation:

- The agent exists in a grid world and starts in the upper-left corner. 
- Each time it moves to an adjacent cell, it spends as many timesteps on this cell as the number on this cell.
- The goal is to reach the bottom right square of the grid in as few steps as possible

## Implementation

### World Creation
**1) Task: Create an implementation of the game:**  it should be flexible allowing the programmer to specify the height and width as well as then max / min number of time steps per square

**Implementation:** Created a WorldClass that takes as inputs the desired height and width as well as the number min/max number of timesteps all subsequent path finder classes must inherit this class

**2) Task: Develop Your Own Heuristic Algorithm:** Does not have to optimized but should perform better than a randomwalk
**Implementation:** A simple nearest neighbour algorithm that scans the adjacent squares and has the agent take the smallest timestep value, note: an additional feature is that the agent will only head in the target direction in this case down and to the right

**3) Task: Implement Dijkstra's algorithm**

<!-- TODO -->
1) Allow different height and width sizes