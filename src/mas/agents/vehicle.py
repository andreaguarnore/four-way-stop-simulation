from itertools import product
from typing import Generator, Tuple

from mesa import Model

from mas.direction import Direction
from mas.agents.traffic import Traffic


class Vehicle(Traffic):
   '''Vehicle agent. Will go straight if no stop sign is found,
   otherwise it will communicate with the stop in order to give the
   right of way correctly.
   '''

   def __init__(
      self,
      unique_id:      int,
      model:          Model,
      direction:      Direction,
      turn:           bool,
      max_velocity:   int   = 10
   ) -> None:
      '''
      direction:
         Starting direction.
      turn:
         Whether the vehicle is on the lane to turn left or not.
      max_velocity:
         Maximum velocity of the vehicle.
      '''
      super().__init__(unique_id, model)
      self.direction = direction
      self.turn = turn
      self.velocity = 0
      self.max_velocity = max_velocity
      self.intersection_step = -1

   def possible_neighbors(
      self,
      x:    int,
      y:    int,
      xmod: int,
      ymod: int
   ) -> Generator[int, None, None]:
      '''Generates all possible coordinates towards the current
      direction where another vehicle with distance `velocity` at most
      can be.
      '''
      def range_args(idx):
         step = 1 if idx >= 0 else -1
         start = 0 if idx == 0 else step
         return start, idx + step, step
      for t_xmod, t_ymod in product(
         range(*range_args(xmod)),
         range(*range_args(ymod))
      ):
         yield x + t_xmod, y + t_ymod

   def put_in_correct_lane(
      self,
      new_pos:       Tuple[int, int],
      new_pos_torus: Tuple[int, int]
   ) -> Tuple[int, int]:
      '''Vehicles that turn left find themselves in the right lane after
      the intersection. When going off screen and then back, they should
      be put back in the left lane.
      '''
      new_pos_torus = list(new_pos_torus)
      if new_pos[0] > new_pos_torus[0]:
         new_pos_torus[1] -= 1
      elif new_pos[0] < new_pos_torus[0]:
         new_pos_torus[1] += 1
      elif new_pos[1] > new_pos_torus[1]:
         new_pos_torus[0] += 1
      else: # if new_pos[1] < new_pos_torus[1]:
         new_pos_torus[0] -= 1
      return tuple(new_pos_torus)

   def move_vehicles_step(self) -> None:
      '''Search neighbors and compute new position accordingly.
      '''
      if self.intersection_step == -1:
         x, y = self.pos
         xmod, ymod = self.direction.modifiers(self.velocity + 1)

         # Find closest agent
         distance_to_next = 1
         neighbor = None
         for neighbor_pos in self.possible_neighbors(x, y, xmod, ymod):
            torus_pos = self.model.grid.torus_adj(neighbor_pos)
            if not self.model.grid.is_cell_empty(torus_pos):
               neighbor = self.model.grid[torus_pos][0]
               break
            distance_to_next += 1
         else:
            # No close agent, accelerate
            self.velocity += 1 if self.velocity != self.max_velocity else 0

         # Slow down due to closeness to other agents
         if neighbor != None:
            self.velocity = distance_to_next - 1

            # If at the stop sign
            if distance_to_next == 1 and not isinstance(neighbor, Vehicle):
               neighbor.approaching_intersection(self)
               return

         # Find new position
         xmod, ymod = self.direction.modifiers(self.velocity)
         new_pos = (x + xmod, y + ymod)
         new_pos_torus = self.model.grid.torus_adj(new_pos)
         if new_pos != new_pos_torus and self.turn:
            new_pos_torus = self.put_in_correct_lane(new_pos, new_pos_torus)

         self.new_pos = new_pos_torus

   def move_vehicles_advance(self) -> None:
      '''Move to the new position previously computed in
      `move_vehicles_step`.
      '''
      self.model.grid.move_agent(self, self.new_pos)

   def proceed_into_intersection(self) -> None:
      '''The vehicle has right of way, so it now prepares itself to
      clear the intersection.
      '''
      self.intersection_step = 0

   def has_cleared_intersection(self) -> bool:
      return self.intersection_step == -1

   def right_of_way_advance(self) -> None:
      '''If the vehicle has right of way, it moves into the
      intersection.
      '''
      if self.intersection_step != -1:

         # If the vehicle has to turn
         if self.turn and 2 < self.intersection_step < 5:
            self.direction.turn_left()

         # Move vehicle
         mod = self.direction.modifiers(1)
         self.new_pos = tuple(map(sum, zip(self.pos, mod)))
         self.move_vehicles_advance()

         self.intersection_step += 1
         if self.intersection_step == 6:
            self.intersection_step = -1

   def avoid_deadlocks_advance(self) -> None:
      '''The vehicle has priority in this deadlock, advance as if it had
      right of way.
      '''
      self.right_of_way_advance()

