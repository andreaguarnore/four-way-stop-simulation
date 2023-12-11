const CanvasModule = function(canvasWidth, canvasHeight, gridWidth, gridHeight) {

   // Create HTML tags
   const canvas_tag =
      '<canvas \
         width="' + canvasWidth + '" \
         height="' + canvasHeight + '"> \
      </canvas>';
   const parent_div_tag =
      '<div \
         style="height:' + canvasHeight + 'px;" \
         class="world-grid-parent"> \
      </div>';

   // Append them to the body
   const canvas_elem = $(canvas_tag)[0];
   const parent_elem = $(parent_div_tag)[0];

   $('#elements').append(parent_elem);
   parent_elem.append(canvas_elem);

   // Create the context and the drawing controller
   const ctx = canvas_elem.getContext('2d');
   const canvas = new TrafficCanvas(canvasWidth, canvasHeight, gridHeight, gridWidth, ctx);

   this.render = function(data) {
      canvas.resetCanvas();
      canvas.drawRoad();
      canvas.drawAgents(data);
   };

   this.reset = function() {
      canvas.resetCanvas();
   };

};