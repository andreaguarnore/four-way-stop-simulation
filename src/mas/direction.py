from typing import Tuple

import numpy as np


class Direction:
   '''Auxiliary class to handle the direction and angle of the vehicles.
   '''

   def __init__(self, direction: str) -> None:
      '''
      direction:
         Possible values are the four main compass directions.
      '''
      self.all = [
         'N', 'NE', 'E', 'SE',
         'S', 'SW', 'W', 'NW'
      ]
      self.direction = self.all.index(direction)

   def to_angle(self) -> float:
      '''Returns the angle in radians, assuming that 0 radians equals
      facing north.
      '''
      return 2 * np.pi * self.direction / len(self.all)

   def turn_left(self) -> None:
      '''Turn vehicle 45° to the left.
      '''
      self.direction = self.direction - 1 if self.direction != 0 else len(self.all) - 1

   def modifiers(self, velocity: int) -> Tuple[int, int]:
      '''Returns how much `x` and `y` coordinates change according to
      the given the current velocity.
      '''
      das = self.all[self.direction]  # direction as string
      xmod = +velocity if das[-1] == 'E' else \
             -velocity if das[-1] == 'W' else 0
      ymod = +velocity if das[0]  == 'S' else \
             -velocity if das[0]  == 'N' else 0
      return xmod, ymod

