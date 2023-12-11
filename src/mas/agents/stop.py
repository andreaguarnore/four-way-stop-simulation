from collections import Counter
from enum import Enum
from typing import List, Tuple

from mesa import Model

from mas.agents.traffic import Traffic
from mas.agents.vehicle import Vehicle


class Status(Enum):
   EMPTY    = 1  # No vehicles are waiting at the intersection or
                 # clearing it
   WAITING  = 2  # A vehicle is waiting at the intersection
   CLEARING = 3  # A vehicle is in the process of clearing the
                 # intersection


class Stop(Traffic):

   def __init__(
      self,
      unique_id:       int,
      model:           Model,
      stop_group:      int,
      turn:            bool,
      avoid_deadlocks: bool
   ) -> None:
      '''
      stop_group:
         One group for each cardinal point.
      turn:
         Whether this stop is on the lane to turn left.
      '''
      super().__init__(unique_id, model)
      self.stop_group = stop_group
      self.turn = turn
      self.status = Status.EMPTY
      self.last_vehicle = None
      self.wait_time = 0
      self.avoid_deadlocks = avoid_deadlocks

   def compute_stops_to_check(self) -> None:
      '''Each stop has to communicate with other stops in order to check
      if the vehicle has the right of way. Some need to be `EMPTY`, some
      not in the `CLEARING` status.
      '''
      sgs = self.model.stop_groups
      sg  = self.stop_group
      ns  = 4  # number of stop groups

      self.check_empty  = [*sgs[(sg + 3) % ns]]
      self.check_empty += [*sgs[(sg + 2) % ns]] if self.turn else []

      self.check_not_clearing  = [*sgs[(sg + 1) % ns]]
      self.check_not_clearing += [sgs[(sg + 2) % ns][1]] if not self.turn else []

   def approaching_intersection(self, vehicle: Vehicle) -> None:
      '''Acknowledge the vehicle that is waiting at the stop.
      '''
      if self.status == Status.EMPTY:
         self.status = Status.WAITING
         self.last_vehicle = vehicle
      elif self.status == Status.WAITING:
         self.wait_time += 1

   def right_of_way_step(self) -> None:
      '''Decide whether or not the vehicle waiting at the stop has right
      of way or not.
      '''
      if self.status == Status.WAITING:

         # Check that all stops on the right are empty
         for other_stop in self.check_empty:
            if other_stop.status == Status.WAITING or \
               other_stop.status == Status.CLEARING:
               return

         # Also check that no vehicle coming from the left is already
         # in the intersection
         for other_stop in self.check_not_clearing:
            if other_stop.status == Status.CLEARING:
               return

         # Vehicle has the right of way
         self.last_vehicle.proceed_into_intersection()
         self.status = Status.CLEARING

      # Check if the vehicle has cleared the intersection
      elif self.status == Status.CLEARING:
         if self.last_vehicle.has_cleared_intersection():
            self.status = Status.EMPTY
            self.wait_time = 0

   def avoid_deadlocks_step(self) -> None:
      '''To avoid deadlocks the stop group is used as priority level
      with 0 as the highest priority.
      In case of a deadlock, the stop group for which all stop groups
      with a higher priority are empty, and all stops with lower
      priority are not clearing the intersection, moves.
      '''
      if self.avoid_deadlocks:

         if self.status == Status.WAITING:

            for i in range(4):  # number of stop groups
               for other_stop in self.model.stop_groups[i]:
                  if i < self.stop_group and \
                     other_stop.status != Status.EMPTY:
                     return
                  elif i > self.stop_group and \
                     other_stop.status == Status.CLEARING:
                     return

            self.last_vehicle.proceed_into_intersection()
            self.status = Status.CLEARING
