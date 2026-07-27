import React, { useEffect, useRef } from 'react';
import './Chart.css';

interface ChartProps {
  symbol: string;
}

export const Chart: React.FC<ChartProps> = ({ symbol }) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  // Simulated chart rendering
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const drawGrid = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.05)';
      ctx.lineWidth = 1;
      for (let i = 0; i < canvas.width; i += 40) {
        ctx.beginPath();
        ctx.moveTo(i, 0);
        ctx.lineTo(i, canvas.height);
        ctx.stroke();
      }
      for (let i = 0; i < canvas.height; i += 40) {
        ctx.beginPath();
        ctx.moveTo(0, i);
        ctx.lineTo(canvas.width, i);
        ctx.stroke();
      }
    };

    const drawCandles = () => {
      let x = 20;
      for (let i = 0; i < 20; i++) {
        const up = Math.random() > 0.5;
        const open = Math.random() * 100 + 100;
        const close = open + (Math.random() * 40 - 20);
        const high = Math.max(open, close) + Math.random() * 20;
        const low = Math.min(open, close) - Math.random() * 20;

        ctx.strokeStyle = up ? '#10b981' : '#ef4444';
        ctx.fillStyle = up ? '#10b981' : '#ef4444';

        // Wick
        ctx.beginPath();
        ctx.moveTo(x + 5, canvas.height - high);
        ctx.lineTo(x + 5, canvas.height - low);
        ctx.stroke();

        // Body
        const bodyHeight = Math.abs(open - close) || 1;
        const bodyY = canvas.height - Math.max(open, close);
        ctx.fillRect(x, bodyY, 10, bodyHeight);

        x += 30;
      }
    };

    const animate = () => {
      drawGrid();
      drawCandles();
    };

    animate();
    const interval = setInterval(animate, 2000);
    return () => clearInterval(interval);
  }, [symbol]);

  return (
    <div className="chart-container glass-panel">
      <div className="chart-header">
        <h3>{symbol}</h3>
        <div className="chart-controls">
          <button>1m</button>
          <button className="active">5m</button>
          <button>15m</button>
          <button>1H</button>
        </div>
      </div>
      <div className="canvas-wrapper">
        <canvas ref={canvasRef} width={800} height={400} />
      </div>
    </div>
  );
};
