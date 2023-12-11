const TrafficCanvas = function(canvasWidth, canvasHeight, gridWidth, gridHeight, ctx) {

   const cellWidth = Math.floor(canvasWidth / gridWidth)
   const cellHeight = Math.floor(canvasHeight / gridHeight)

   // Maximum radius that can be fit into a cell
   const maxR = Math.min(cellHeight, cellWidth) / 2 - 1;
   const arrowR = 0.7 * maxR

   /*
   Draws a rectangle in the specified location.
      x, y : grid coordinates
      w, h : width and height in number of cells
      color : fill color
   */
   this.drawRectangle = (x, y, w, h, color) => {
      x = x * cellWidth;
      y = y * cellHeight;
      w = w * cellWidth;
      h = h * cellHeight;

      ctx.beginPath();
      ctx.fillStyle = color;
      ctx.fillRect(x, y, w, h);
   };

   this.drawRoad = () => {
      // Background
      this.drawRectangle(0, 0, gridWidth, gridHeight, '#262626');

      // Boardwalks
      this.drawRectangle(Math.floor(gridWidth / 2) - 2, 0, 5, gridHeight, '#666666');
      this.drawRectangle(0, Math.floor(gridHeight / 2) - 2, gridWidth, 5, '#666666');

      // Roads
      this.drawRectangle(Math.floor(gridWidth / 2) - 1, 0, 3, gridHeight, '#ebebeb');
      this.drawRectangle(0, Math.floor(gridHeight / 2) - 1, gridWidth, 3, '#ebebeb');
   };

   this.drawAgents = (objects) => {
      objects.forEach((p) => {
         this.drawVehicle(p.x, p.y, p.angle, p.color);
      });
   };

   /*
   Drawing ⮝
   The points of the path are, in order:
      - top tip
      - bottom left tip
      - center inwards tip
      - bottom right tip
   */
   this.drawArrowHead = () => {
      const out_coef = 0.3  // how much out the inwards tip is

      ctx.beginPath();
      ctx.moveTo(0, -arrowR);
      ctx.lineTo(-arrowR, arrowR);
      ctx.lineTo(0, out_coef * arrowR);
      ctx.lineTo(arrowR, arrowR);
      ctx.closePath();

      ctx.lineWidth = 2
      ctx.strokeStyle = 'black'
      ctx.stroke()
   };

   /*
   Draws a vehicle as an arrowhead with the angle appropriate to its
   direction.
   */
   this.drawVehicle = (x, y, angle, color) => {
      const cx = (x + 0.5) * cellWidth;
      const cy = (y + 0.5) * cellHeight;

      // Save default state
      ctx.save();

      // Draw vehicle with its rotation
      ctx.translate(cx, cy);
      ctx.rotate(angle)
      this.drawArrowHead()
      ctx.fillStyle = color;
      ctx.fill();

      // Restore default state
      ctx.restore();
   }

   this.resetCanvas = () => {
      ctx.clearRect(0, 0, canvasWidth, canvasHeight);
      ctx.beginPath();
   };
};
