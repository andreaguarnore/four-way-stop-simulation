from mesa import Agent, Model


class Traffic(Agent):
   '''Generic traffic agent. Contains abstract steps for all stages
   '''

   def __init__(self, unique_id: int, model: Model) -> None:
      super().__init__(unique_id, model)

   def move_vehicles_step(self) -> None:
      pass

   def move_vehicles_advance(self) -> None:
      pass

   def right_of_way_step(self) -> None:
      pass

   def right_of_way_advance(self) -> None:
      pass

   def avoid_deadlocks_step(self) -> None:
      pass

   def avoid_deadlocks_advance(self) -> None:
      pass
