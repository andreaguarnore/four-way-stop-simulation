import random
from typing import Tuple

from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from mas.agents.vehicle import Vehicle
from mas.agents.stop import Stop
from mas.direction import Direction
from mas.activation import SimultaneousStagedActivation


def avg_wait_time(model: Model) -> float:
   n_stops = 8
   total_wait_time = 0.0
   stops_waiting = 0
   for i in range(n_stops):
      wait_time = model.schedule.agents[i].wait_time
      if wait_time > 0:
         total_wait_time += model.schedule.agents[i].wait_time
         stops_waiting += 1
   return total_wait_time / (stops_waiting if stops_waiting else 1)


class FourWayStop(Model):
   '''Four-way stop model. The vehicles abide to the rules, by giving
   right of way when necessary.
   '''

   def __init__(
      self,
      n_vehicles:      int,
      width:           int,
      height:          int,
      max_velocity:    int,
      avoid_deadlocks: bool
   ) -> None:
      '''
      n_vehicles:
         Number of vehicles.
      width, height:
         Size of the grid.
      '''
      self.n_vehicles = n_vehicles
      self.width = width
      self.height = height
      self.center = (self.width // 2, self.height // 2)
      self.schedule = SimultaneousStagedActivation(self, [
         'move_vehicles',
         'right_of_way',
         'avoid_deadlocks'
      ])
      self.grid = MultiGrid(
         width=self.width,
         height=self.height,
         torus=True
      )
      self.stop_groups = {k: [] for k in range(4)}
      self.make_stops(avoid_deadlocks)
      self.make_vehicles(n_vehicles, max_velocity)
      self.datacollector = DataCollector(
         model_reporters={'Average wait time': avg_wait_time}
      )
      self.running = True

   def get_coords(
      self,
      lane: int
   ) -> Tuple[Tuple[int, int], Direction]:
      '''Given a lane, returns the starting coordinates and the
      direction.

      Visualization of the intersection and the lanes. The `•` marks the
      center of the grid.
       ┃0 1  ┃
      ━┛     ┗━
              2
      7   •   3
      6        
      ━┓     ┏━
       ┃  5 4┃
      '''
      coords = (self.center[0] - 1, 0)               if lane == 0 else \
               (self.center[0], 0)                   if lane == 1 else \
               (self.width - 1, self.center[1] - 1)  if lane == 2 else \
               (self.width - 1, self.center[1])      if lane == 3 else \
               (self.center[0] + 1, self.height - 1) if lane == 4 else \
               (self.center[0], self.height - 1)     if lane == 5 else \
               (0, self.center[1] + 1)               if lane == 6 else \
               (0, self.center[1])                 # if lane == 7

      direction_as_str = 'S'   if lane < 2 else \
                         'W'   if lane < 4 else \
                         'N'   if lane < 6 else \
                         'E' # if lane < 8
      direction = Direction(direction_as_str)

      # Move vehicles while on top of an already spawned vehicle
      modifiers = direction.modifiers(1)
      while self.grid[coords] != []:
         coords = tuple(map(sum, zip(coords, modifiers)))

      return coords, direction

   def make_stops(self, avoid_deadlocks) -> None:
      '''Creates all stops.
      '''

      # Modifiers to obtain stop coordinates starting from the center
      # of the grid
      stop_modifiers = [
      #  right lane | left lane |  side
         (-1, -2),    ( 0, -2),  # top
         ( 2, -1),    ( 2,  0),  # right
         ( 1,  2),    ( 0,  2),  # bottom
         (-2,  1),    (-2,  0)   # left
      ]

      # Compute stop coordinates
      stop_coords = [tuple(map(sum, zip(self.center, sm))) for sm in stop_modifiers]

      # Create the agents
      for i, sc in enumerate(stop_coords):
         stop_group = i // 2
         agent = Stop(i, self, stop_group, i % 2, avoid_deadlocks)
         self.stop_groups[stop_group].append(agent)
         self.schedule.add(agent)
         self.grid.place_agent(agent, sc)

      # Have the stops compute which other stops they need to
      # communicate with
      for _, stop_group in self.stop_groups.items():
         for stop in stop_group:
            stop.compute_stops_to_check()

   def make_vehicles(
      self,
      n_vehicles:     int,
      max_velocity:   int
   ) -> None:
      '''Spawns `n_vehicles` vehicles at the start of randomly chosen
      lanes.
      '''
      n_lanes = 8
      for i in range(n_vehicles):
         lane = random.randrange(n_lanes)
         coords, direction = self.get_coords(lane)
         agent = Vehicle(
            n_lanes + i,
            self,
            direction,
            turn=lane % 2,
            max_velocity=max_velocity
         )
         self.schedule.add(agent)
         self.grid.place_agent(agent, coords)

   def step(self) -> None:
      self.datacollector.collect(self)
      self.schedule.step()
