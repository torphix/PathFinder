from tqdm import tqdm
import matplotlib.pyplot as plt
from .finders.dijkstra import DijkstrasPathFinder
from .finders.nearest_neighbour import NearestNeighbourPathFinder

class Benchmarker():
  def __init__(self, world_sizes:list=[(9,9)], max_timesteps:int=9):
    '''
    Given a list of world_sizes & max_timesteps benchmark the different 
    approaches: random, naive (nearest neighbour) & Dijkstra's 
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
      nnpf = NearestNeighbourPathFinder(world_sizes[i], max_timesteps)
      dijkstras = DijkstrasPathFinder(world_size=world_sizes[i], max_timesteps=max_timesteps, world=nnpf.world)
      self.nearest_neighbour_path_finders.append(nnpf)
      self.dijkstras_path_finders.append(dijkstras)

  def run(self):
    # Compute the nearest neighbours first
    naive_logs, dijkstras_logs = [], []
    for i in tqdm(range(len(self.nearest_neighbour_path_finders))):
      naive_logs.append(self.nearest_neighbour_path_finders[i].find_path(print_out_logs=False))
      dijkstras_logs.append(self.dijkstras_path_finders[i].find_path(print_out_logs=False))
    return naive_logs, dijkstras_logs

  def visualise_results(self, logs):
    '''
    For each benchmark type plot a lineplot histogram
    using the largest and smallest value in order to preserve 
    visualse scale.
    '''
    total_time_steps = [log['output_logs']['total_time_steps'] for log in logs]
    end_times = [log['output_logs']['end_time'] for log in logs]
    print('Num steps', total_time_steps, 'Run Time', end_times)
    # vis_logs = {}
    # # Prepare logs
    # for log in logs:
    #   for k,v in log['output_logs'].items():
    #     if k not in list(vis_logs.keys()):
    #       vis_logs[k] = [v]
    #     else:
    #       vis_logs[k] += [v]

    # # Plot logs
    # for i, (k,v) in enumerate(vis_logs.items()):
    #   plt.plot(list(map(str, self.world_sizes)), v, label=k)
    # plt.legend(list(vis_logs.values()), list(vis_logs.keys()))
    # plt.show()
    


