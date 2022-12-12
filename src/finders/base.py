import abc
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap



class WorldClass(abc.ABC):
    def __init__(self, world_size=(9,9), max_timesteps=9, world=None):
        self.world_size = world_size
        self.max_timesteps = max_timesteps
        if world is None:
          self.world = self.create_world(world_size, max_timesteps)
        else:
          self.world = world

    def create_world(self, grid_size, max_timesteps):
        world = np.random.randint(0, max_timesteps, grid_size)
        return world

    def display_world(self, array, path_idxs=None):
        '''
        Uses matplotlibs animation lib to display the agents path
        '''
        colors = ListedColormap(["grey"])
        fig, ax = plt.subplots()
        ax.matshow(array, cmap=colors)
        for (i, j), z in np.ndenumerate(array):
          if path_idxs is None:
            color = 'white'
          else:
            path_idxs.insert(0, [0,0])
            if [i,j] in path_idxs:
              color = 'black'
            else: 
              color = 'white'
          ax.text(j, i, '{:0.1f}'.format(z), ha='center', va='center', color=color)
        plt.show()

    def find_path(self):
      raise NotImplemented

    def output_logs(self, total_time_steps, loop_steps, end_time, print_out_logs):
      if print_out_logs:
        print('Target square found!')
        print(f'Total time steps: {total_time_steps}')
        print(f'Total loop steps: {loop_steps}')
        print(f'Time in milliseconds: {end_time}')
      return {
            'total_time_steps':total_time_steps,
            'loop_steps':loop_steps,
            'end_time':end_time,
        }