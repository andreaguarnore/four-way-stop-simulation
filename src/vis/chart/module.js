const ChartModule = function(chartTitle, canvasWidth, canvasHeight) {

   // Create HTML tag
   const canvas_tag =
      '<canvas \
         width="' + canvasWidth + '" \
         height="' + canvasHeight + '" \
         style="margin: 10px;"> \
      </canvas>';

   // Append it to the body
   const canvas_elem = $(canvas_tag)[0];

   $('#elements').append(canvas_elem);

   // Create the context and the drawing controller
   const ctx = canvas_elem.getContext('2d');

   // Prepare the chart properties
   const dataset = {
      borderColor: 'rgb(0, 0, 0, 0.4)',
      backgroundColor: 'rgb(0, 0, 0, 0.6)',
      data: []
   }

   const chartData = {
      labels: [],
      datasets: [dataset]
   };

   const chartOptions = {
      responsive: true,
      tooltips: {
         enabled: false
      },
      hover: {
         mode: 'nearest',
         intersect: true
      },
      plugins: {
         legend: {
            display: false
         },
         title: {
            display: true,
            text: chartTitle
         }
      },
      scales: {
         x: {
            min: 0,
            display: true,
            title: {
               display: false
            },
            ticks: {
               maxTicksLimit: 5
            }
         },
         y: {
            min: 0,
            display: true,
            title: {
               display: false
            }
         }
      }
   };

   const chart = new Chart(ctx, {
      type: 'line',
      data: chartData,
      options: chartOptions
   });

   this.render = (data) => {
      chart.data.labels.push(control.tick);
      chart.data.datasets[0].data.push(data[0])
      chart.update();
   }

   this.reset = () => {
      while (chart.data.labels.length) {
         chart.data.labels.pop();
      }
      var dataset = chart.data.datasets[0].data
      while (dataset.length) {
         dataset.data.pop();
      }
      chart.update();
   }

}
