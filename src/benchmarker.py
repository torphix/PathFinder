import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
from .finders.dijkstra import DijkstrasPathFinder
from .finders.nearest_neighbour import NearestNeighbourPathFinder


class Benchmarker():
    def __init__(self, world_sizes: list = [(9, 9)], max_timesteps: int = 9, world_dists: list = ['uniform']):
        '''
        Given a list of world_sizes & max_timesteps benchmark the different 
        approaches: naive (nearest neighbour) & Dijkstra's 
        Benchmarks are:
          - Total time steps
          - Number of loop iterations (main loop only)
          - Time in milliseconds 
          - Benchmark RAM used
          - Benchmark CPU utilisation
        Visualisations are:
          - Plot the time increase as world grid size increase (scatter)
          - Plot histogram of time comparisons between different world size (comparison of each approach)
        '''
        self.world_sizes = world_sizes

        # Initialise the worlds
        self.nearest_neighbour_path_finders, self.dijkstras_path_finders = [], []
        for i in range(len(world_sizes)):
            nnpf = NearestNeighbourPathFinder(world_sizes[i], max_timesteps, world_dist=world_dists[i])
            dijkstras = DijkstrasPathFinder(
                world_size=world_sizes[i], max_timesteps=max_timesteps, world=nnpf.world)
            self.nearest_neighbour_path_finders.append(nnpf)
            self.dijkstras_path_finders.append(dijkstras)

    def run(self):
        # Compute the nearest neighbours first
        naive_logs, dijkstras_logs = [], []
        for i in tqdm(range(len(self.nearest_neighbour_path_finders))):
            naive_logs.append(
                self.nearest_neighbour_path_finders[i].find_path(print_out_logs=False))
            dijkstras_logs.append(
                self.dijkstras_path_finders[i].find_path(print_out_logs=False))
        return {
            'nearest_neighbour': naive_logs,
            'dijkstra': dijkstras_logs
        }

    def visualise_results(self, logs: dict):
        '''
        For each benchmark type plot a lineplot histogram
        using the largest and smallest value in order to preserve 
        visualse scale.
        '''
        output_logs = {'nearest_neighbour': {}, 'dijkstra': {}}
        # Print out logged values
        for k, v in logs.items():
            output_logs[k]['total_time_steps'] = [
                log['output_logs']['total_time_steps'] for log in v]
            output_logs[k]['end_times'] = [
                log['output_logs']['end_time'] for log in v]
            print('Num steps', output_logs[k]['total_time_steps'],
                  'Run Time', output_logs[k]['end_times'])

        # Plot logged values as logs vs hyperparameters grid size
        X = self.world_sizes
        fig, (ax1, ax2) = plt.subplots(1, 2)

        X_axis = np.arange(len(X))
        ax1.bar(X_axis - 0.2, output_logs['nearest_neighbour']
                ['total_time_steps'], 0.4, label='nearest_neighbour')
        ax1.bar(X_axis + 0.2, output_logs['dijkstra']
                ['total_time_steps'], 0.4, label='dijkstra')
        ax1.set_xticks(X_axis, X)
        ax1.set_xlabel("World Size")
        ax1.set_ylabel("Number of Timesteps")
        ax1.set_title("Effect of grid size on number of time steps")
        ax1.legend()

        X_axis = np.arange(len(X))
        ax2.bar(X_axis - 0.2, output_logs['nearest_neighbour']
                ['end_times'], 0.4, label='nearest_neighbour')
        ax2.bar(X_axis + 0.2, output_logs['dijkstra']
                ['end_times'], 0.4, label='dijkstra')
        ax2.set_xticks(X_axis, X)
        ax2.set_xlabel("World Size")
        ax2.set_ylabel("Run Time In Milliseconds")
        ax2.set_title("Effect of grid size on run time")
        ax2.legend()

        plt.show()
