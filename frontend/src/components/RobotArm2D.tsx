import React, { useRef, useState, useCallback, useEffect } from 'react';
import { P5Canvas, type P5CanvasInstance } from '@p5-wrapper/react';

interface RobotArm2DProps {
  initialAngle1?: number; // Initial angle for joint 1 in degrees
  initialAngle2?: number; // Initial angle for joint 2 in degrees
  linkLength1?: number;   // Length of the first link
  linkLength2?: number;   // Length of the second link
  canvasWidth?: number;
  canvasHeight?: number;
}

const RobotArm2D: React.FC<RobotArm2DProps> = ({
  initialAngle1 = 45,
  initialAngle2 = -45,
  linkLength1 = 100,
  linkLength2 = 80,
  canvasWidth = 400,
  canvasHeight = 400,
}) => {
  const [angle1, setAngle1] = useState(initialAngle1);
  const [angle2, setAngle2] = useState(initialAngle2);
  const [endEffectorPos, setEndEffectorPos] = useState({ x: 0, y: 0 });

  const sketch = useCallback((p5: P5CanvasInstance) => {
    let currentAngle1 = p5.radians(angle1);
    let currentAngle2 = p5.radians(angle2);

    p5.setup = () => {
      p5.createCanvas(canvasWidth, canvasHeight);
      p5.angleMode(p5.RADIANS); // Ensure angles are treated as radians
      p5.rectMode(p5.CENTER); // For drawing sliders
    };

    p5.draw = () => {
      p5.background(220);
      p5.translate(canvasWidth / 2, canvasHeight / 2); // Move origin to center of canvas
      p5.strokeWeight(5);
      p5.stroke(0);

      // --- Draw Link 1 ---
      p5.push(); // Save current transformation state
      p5.rotate(currentAngle1);
      p5.line(0, 0, linkLength1, 0); // Draw first link
      p5.translate(linkLength1, 0); // Move to end of first link

      // --- Draw Link 2 ---
      p5.rotate(currentAngle2);
      p5.line(0, 0, linkLength2, 0); // Draw second link
      p5.pop(); // Restore original transformation state (before first push)

      // --- Calculate Forward Kinematics (End Effector Position) ---
      // Convert angles from degrees to radians for math functions
      const a1Rad = p5.radians(angle1);
      const a2Rad = p5.radians(angle2);

      // Position of end of first link relative to base
      const x1 = linkLength1 * p5.cos(a1Rad);
      const y1 = linkLength1 * p5.sin(a1Rad);

      // Position of end of second link relative to base (offset from end of first link)
      const x2 = x1 + linkLength2 * p5.cos(a1Rad + a2Rad);
      const y2 = y1 + linkLength2 * p5.sin(a1Rad + a2Rad);

      // Update React state for display
      setEndEffectorPos({ x: parseFloat(x2.toFixed(2)), y: parseFloat(y2.toFixed(2)) });
    };

  }, [angle1, angle2, linkLength1, linkLength2, canvasWidth, canvasHeight]); // Re-create sketch if these props/states change

  // Expose angle setters for external controls (sliders) in the next step
  // For now, just render the canvas and position
  return (
    <div style={{ margin: '20px 0', border: '1px solid #ddd', borderRadius: '5px', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
      <P5Canvas sketch={sketch} />
      <div style={{ padding: '10px', backgroundColor: '#f0f0f0', width: '100%', textAlign: 'center' }}>
        <p>End Effector Position (relative to center):</p>
        <p>X: {endEffectorPos.x}, Y: {endEffectorPos.y}</p>
      </div>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', padding: '10px', width: '100%', maxWidth: '400px' }}>
        <label>
          Joint 1 Angle ({angle1.toFixed(0)}°):
          <input
            type="range"
            min="-180"
            max="180"
            value={angle1}
            onChange={(e) => setAngle1(parseFloat(e.target.value))}
            style={{ width: '100%' }}
          />
        </label>
        <label>
          Joint 2 Angle ({angle2.toFixed(0)}°):
          <input
            type="range"
            min="-180"
            max="180"
            value={angle2}
            onChange={(e) => setAngle2(parseFloat(e.target.value))}
            style={{ width: '100%' }}
          />
        </label>
      </div>
    </div>
  );
};

export default RobotArm2D;
