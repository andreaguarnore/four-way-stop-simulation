from typing import List

from mesa import Model
from mesa.time import BaseScheduler


class SimultaneousStagedActivation(BaseScheduler):
   '''Scheduler which allows agent activation to be divided in multiple
   stages. Each of the stage is activated simultaneously.

   The scheduler requires all agents to implement two methods for each
   stage: `<stage_name>_step()` and `<stage_name>_advance()`.
   The `step()` method computes the necessary changes, while `advance()`
   applies them.
   '''

   def __init__(
      self,
      model:      Model,
      stage_list: List[str]
   ) -> None:
      super().__init__(model)
      self.stage_list = stage_list
      self.stage_time = 1 / len(self.stage_list)

   def step(self) -> None:
      agent_keys = list(self._agents.keys())

      for stage in self.stage_list:
         for substep in ['_step', '_advance']:
            for ak in agent_keys:
               getattr(self._agents[ak], stage + substep)()
         self.time += self.stage_time

      self.steps += 1
