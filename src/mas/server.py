from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

from mas.model import FourWayStop
from vis.canvas.grid_visualization import CanvasGridVisualization
from vis.chart.chart_visualization import ChartVisualization


grid_width = 40
grid_height = 40

canvas = CanvasGridVisualization(
   canvas_width=500,
   canvas_height=500,
   grid_width=grid_width,
   grid_height=grid_height
)

chart = ChartVisualization(
   chart_title='Average wait time',
   canvas_width=200,
   canvas_height=50,
   data_collector_name='datacollector'
)

server = ModularServer(
   model_cls=FourWayStop,
   visualization_elements=[canvas, chart],
   name='Four-way stop',
   model_params={
      'n_vehicles': UserSettableParameter(
         param_type='slider',
         name='Number of vehicles',
         value=10,
         min_value=1,
         max_value=20,
         step=1
      ),
      'width': grid_width,
      'height': grid_height,
      'max_velocity': UserSettableParameter(
         param_type='slider',
         name='Max velocity',
         value=5,
         min_value=1,
         max_value=10,
         step=1
      ),
      'avoid_deadlocks': UserSettableParameter(
         param_type='checkbox',
         name='Avoid deadlocks',
         value=True
      )
   }
)
