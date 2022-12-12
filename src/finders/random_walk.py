from .base import WorldClass

class RandomWalkPathFinder(WorldClass):
  def __init__(self, world_size=(9,9), max_timesteps=9, world=None):
      super().__init__(world_size, max_timesteps, world)
  
  def find_path(self):
      pass