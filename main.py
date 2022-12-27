import sys
import yaml
import logging
import argparse
from src.benchmarker import Benchmarker
from src.finders.dijkstra import DijkstrasPathFinder
from src.finders.nearest_neighbour import NearestNeighbourPathFinder


if __name__ == '__main__':

    cmd = sys.argv[1]

    if cmd == 'benchmark':
        logging.info('Running Multiple Experiments from benchmark_config.yaml')

        with open('benchmark_config.yaml', 'r') as f:
            config = yaml.load(f.read(), Loader=yaml.FullLoader)

        benchmarker = Benchmarker(world_sizes=config['world_sizes'], 
                                  world_dists=config['distribution'])
        logs = benchmarker.run()
        benchmarker.visualise_results(logs)

    elif cmd == 'run':
        logging.info('Running a single experiment as specified in args')
        parser = argparse.ArgumentParser()
        parser.add_argument('-t', '--type', required=True, choices=['nearest_neighbour', 'dijkstra'])
        parser.add_argument('--timestep_dist', default='uniform', choices=['normal', 'uniform', 'exponential'])
        parser.add_argument('--width', type=int, default=9)
        parser.add_argument('--height', type=int, default=9)
        parser.add_argument('-ma', '--max', help='Max int to use in grid world', type=int, default=9)

        args, lf_args = parser.parse_known_args()

        if args.type == 'nearest_neighbour':
            print('Using Nearest Neighbour')
            path_finder = NearestNeighbourPathFinder((args.width, args.height), args.max, world_dist=args.timestep_dist)
            logs = path_finder.find_path(True)
            path_finder.display_world(path_finder.world, logs['visited_idxs'])
        elif args.type == 'dijkstra':
            print('Using Dijkstra')
            path_finder = DijkstrasPathFinder(world_size=(args.width, args.height), max_timesteps=args.max, world_dist=args.timestep_dist)
            logs = path_finder.find_path(True)
            path_finder.display_world(logs['world_vis'], logs['visited_node_grid_idxs'])

    else:
        logging.error('Only commands "benchmark" and "run" are supported ')
