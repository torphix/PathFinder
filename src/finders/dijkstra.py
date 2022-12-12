import time
import psutil
import numpy as np
from decimal import Decimal
from .base import WorldClass




class Graph():
  def __init__(self, world_grid):
    '''
    Constructs a graph object from the world grid numpy array
    nodes = {
      idx (0): {grid_idx: (0,0), edges:[[0,1], [1,0]], edge_weights:[[4, 5]]}
    }
    '''
    nodes_tmp = [(j,i) for j in range(world_grid.shape[1])  for i in range(world_grid.shape[0])]
    nodes_idx_dict = {v:i for i,v in enumerate(nodes_tmp)}
    self.nodes = {}
    for node, i in nodes_idx_dict.items():
      edges, weights = [], []
      # Up connection
      if (node[0] == 0)== False:
        edges.append((i, nodes_idx_dict[(node[0]-1, node[1])]))
        weights.append(world_grid[node[0]-1, node[1]])
      # Right connection
      if (node[1] == world_grid.shape[1]-1) == False:
        edges.append((i, nodes_idx_dict[(node[0], node[1]+1)]))
        weights.append(world_grid[node[0], node[1]+1])
      # Down connection
      if (node[0] == world_grid.shape[0]-1) == False:
        edges.append((i, nodes_idx_dict[(node[0]+1, node[1])]))
        weights.append(world_grid[node[0]+1, node[1]])
      # Left connection
      if (node[1] == 0) == False:
        edges.append((i, nodes_idx_dict[(node[0], node[1]-1)]))
        weights.append(world_grid[node[0], node[1]-1])

      self.nodes[i] = {'grid_idx':node, 'edges': edges, 'edge_weights':weights, 'node_weight': np.inf}
    self.nodes[0]['node_weight'] = 0

  def select_min_unvisited_node(self, visisted_nodes):
    min_node, min_node_value = 0, np.inf
    for k,v in self.nodes.items():
      if v['node_weight'] == np.inf: continue
      if k in visisted_nodes: continue
      if v['node_weight'] < min_node_value:
        min_node = k
        min_node_value = v['node_weight']
    return min_node, min_node_value

class DijkstrasPathFinder(WorldClass):
  def __init__(self, world_size=(9,9), max_timesteps=9, world=None):
      super().__init__(world_size, max_timesteps, world)
      self.graph_world = Graph(self.world)

  def min_value_in_array(self, array):
    '''
    Finds the min non zero value in array returns the idx and the value
    '''
    array[array == 0] = np.inf
    out_idx = array.argmin()
    out_idxs = np.unravel_index(out_idx, array.shape)
    return out_idxs
  
  def find_path(self, print_out_logs=False):
    '''
    Dijkstras assumes each cell is a node in a graph with edges between nodes
    as the weighting of the values of the cell.. this makes it useful for solving
    non grid structures as well as grid structures 
    1) Get current node
    2) Get connecting edges
    3) Update connected nodes with the edge weights
    4) Add the current node to visited nodes
    5) Set new current node to the minimum connecting node 
    6) Repeat
    '''
    world_vis = np.zeros_like(self.world)

    loop_steps = 0
    current_node = 0
    start_time = time.perf_counter()
    target_node = list(self.graph_world.nodes.keys())[-1]
    visited_nodes, visited_node_grid_idxs = [0], [(0,0)]
    start_ram = psutil.virtual_memory()[3]/1000000000
    while True:
      loop_steps += 1
      current_node_values = self.graph_world.nodes[current_node]
      edges = current_node_values['edges']
      for i, edge in enumerate(edges):
        old_node_weight = self.graph_world.nodes[edge[1]]['node_weight']
        new_node_weight = current_node_values['node_weight'] + current_node_values['edge_weights'][i]
        # Update connected nodes weights
        if old_node_weight == np.inf:
          self.graph_world.nodes[edge[1]]['node_weight'] = new_node_weight
      # Select the minimum node value
      new_node, new_node_value = self.graph_world.select_min_unvisited_node(visited_nodes)
      current_node = new_node
      visited_nodes.append(new_node)
      visited_node_grid_idxs.append(list(self.graph_world.nodes[new_node]['grid_idx']))
      world_vis[self.graph_world.nodes[current_node]['grid_idx'][0], self.graph_world.nodes[current_node]['grid_idx'][1]] = new_node_value
      if current_node == target_node:
        logs = self.output_logs(world_vis[-1,-1], loop_steps, (time.perf_counter()-start_time)*1000, print_out_logs)
        logs['max_ram_used'] = Decimal(psutil.virtual_memory()[3]/1000000000) - Decimal(start_ram)
        return {
            'visited_nodes': visited_nodes,
            'visited_node_grid_idxs': visited_node_grid_idxs,
            'world_vis': world_vis,
            'output_logs': logs
        }

  def get_path_idxs_for_world(self, world):
    '''
    Gets the shortest path idxs from the passed world
    '''