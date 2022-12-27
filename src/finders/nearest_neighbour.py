import time
import psutil
from decimal import Decimal
from .base import WorldClass


class NearestNeighbourPathFinder(WorldClass):
    def __init__(self, world_size=(9, 9), max_timesteps=9, world=None):
        super().__init__(world_size, max_timesteps, world)

    def find_path(self, print_out_logs=False):
        '''
        Select the min adjacent square with the constraints 
        of no loop back and only down / right squares are available
        '''

        current_idx = [0, 0]
        tgt_idx = [self.world.shape[0]-1, self.world.shape[1]-1]

        square_idxs_selected = []
        total_time_steps = 0
        loop_steps = 0
        start_time = time.perf_counter()
        start_ram = psutil.virtual_memory()[3]/1000000000
        while True:
            loop_steps += 1
            next_idx = None
            # Right square
            if current_idx[1]+1 > self.world_size[1]-1:
                # Agent is on far right column pick bottom
                next_idx = [current_idx[0]+1, current_idx[1]]
            else:
                right_square = [current_idx[0], current_idx[1]+1]
            # Bottom Square
            if current_idx[0]+1 > self.world_size[0]-1:
                # Agent is on bottom row choose right square as default
                next_idx = [current_idx[0], current_idx[1]+1]
            else:
                down_square = [current_idx[0]+1, current_idx[1]]
            # If agent is not on edge choose min adjacent square
            if next_idx is None:
                square_idxs = [right_square, down_square]
                square_values = [self.world[right_square[0], right_square[1]],
                                 self.world[down_square[0], down_square[1]]]
                min_value = min(square_values)
                next_idx = square_idxs[square_values.index(min_value)]

            square_idxs_selected.append(next_idx)
            total_time_steps += self.world[next_idx[0], next_idx[1]]
            if next_idx == tgt_idx:
                logs = self.output_logs(
                    total_time_steps, loop_steps, (time.perf_counter()-start_time)*1000, print_out_logs)
                logs['max_ram_used'] = Decimal(psutil.virtual_memory()[
                                               3]/1000000000) - Decimal(start_ram)
                return {
                    'visited_idxs': square_idxs_selected,
                    'output_logs': logs,
                }
            else:
                current_idx = next_idx
