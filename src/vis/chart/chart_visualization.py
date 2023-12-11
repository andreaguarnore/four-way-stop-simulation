import json
from typing import List

from mesa.visualization.ModularVisualization import VisualizationElement
from mesa import Model


class ChartVisualization(VisualizationElement):
   local_includes = ['vis/chart/Chart.min.js', 'vis/chart/module.js']

   def __init__(
      self,
      chart_title,
      canvas_width:  int,
      canvas_height: int,
      data_collector_name='datacollector'
   ) -> None:
      '''
      chart_title:
         Title of the chart.
      canvas_width, canvas_height:
         Size of the chart in pixels.
      data_collector_name:
         Name of the `DataCollector` to use.
      '''
      self.chart_title = chart_title
      self.data_collector_name = data_collector_name

      new_element = 'new ChartModule({}, {}, {})'
      new_element = new_element.format(
         '"' + self.chart_title + '"',
         canvas_width,
         canvas_height
      )
      self.js_code = 'elements.push(' + new_element + ');'

   def render(self, model: Model) -> List[dict]:
      '''Add new data point.
      '''
      current_values = []
      data_collector = getattr(model, self.data_collector_name)

      try:
         val = data_collector.model_vars[self.chart_title][-1]  # latest value
      except (IndexError, KeyError):
         val = 0
      current_values.append(val)

      return current_values
