from typing import List

from mesa.visualization.ModularVisualization import VisualizationElement
from mesa import Model

from mas.agents.vehicle import Vehicle


# Colors used for the vehicles
html_color_names = [
   '#2f4f4f',  # dark slate gray
   '#191970',  # midnight blue
   '#4682b4',  # steel blue
   '#98fb98',  # pale green
   '#2e8b57',  # sea green
   '#9acd32',  # yellow green
   '#4b0082',  # indigo
   '#dc143c',  # crimson
   '#ff8c00',  # dark orange
   '#ff69b4'   # deep pink
]


class CanvasGridVisualization(VisualizationElement):
   '''For each vehicle, it generates a portrayal, which is a dictionary
   containing all relevant details about what shape to draw and where.
   It then passes this information to the JavaScript code that will
   render it on the web server.
   '''
   local_includes = ['vis/canvas/traffic_canvas.js', 'vis/canvas/module.js']

   def __init__(
      self,
      canvas_width:  int,
      canvas_height: int,
      grid_width:    int,
      grid_height:   int
   ) -> None:
      '''
      canvas_width, canvas_height:
         Size of the grid in pixels.
      grid_width, grid_height:
         Size of the grid in number of cells.
      '''
      new_element = ('new CanvasModule({}, {}, {}, {})'.format(
         canvas_width,
         canvas_height,
         grid_width,
         grid_height,
      ))
      self.js_code = 'elements.push(' + new_element + ');'

   def render(self, model: Model) -> List[dict]:
      '''Build visualization data from a model object.
      '''
      world_state = []

      for i, agent in enumerate(model.schedule.agents):

         # No need to print the stops
         if isinstance(agent, Vehicle):
            portrayal = {}

            x, y = agent.pos
            portrayal['x'] = x
            portrayal['y'] = y
            portrayal['angle'] = agent.direction.to_angle()
            portrayal['color'] = html_color_names[i % len(html_color_names)]

            world_state.append(portrayal)

      return world_state
