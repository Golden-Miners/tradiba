import React, { useEffect, useRef, useState } from 'react';
import { wsService } from '@/services/websocket';
import './Chart.css';

interface ChartProps {
  symbol: string;
}

interface Candle {
  time: number;
  open: number;
  high: number;
  low: number;
  close: number;
}

export const Chart: React.FC<ChartProps> = ({ symbol }) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [candles, setCandles] = useState<Candle[]>([]);

  useEffect(() => {
    // Fetch initial historical candles
    fetch(`http://localhost:8000/api/market/candles?symbol=${symbol}&timeframe=M5&count=50`)
      .then(res => res.json())
      .then(data => {
         if (Array.isArray(data)) {
           setCandles(data);
         }
      })
      .catch(err => console.error('Failed to fetch candles:', err));

    // Subscribe to live ticks
    const handleTick = (payload: any) => {
      if (payload.symbol === symbol) {
        setCandles(prev => {
          if (prev.length === 0) return prev;
          const newCandles = [...prev];
          const lastCandle = { ...newCandles[newCandles.length - 1] };
          lastCandle.close = payload.price;
          lastCandle.high = Math.max(lastCandle.high, payload.price);
          lastCandle.low = Math.min(lastCandle.low, payload.price);
          newCandles[newCandles.length - 1] = lastCandle;
          return newCandles;
        });
      }
    };

    wsService.subscribe('MarketTickEvent', handleTick);

    return () => {
      wsService.unsubscribe('MarketTickEvent', handleTick);
    };
  }, [symbol]);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw Grid
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

    if (candles.length === 0) return;

    // Calculate scaling
    const minPrice = Math.min(...candles.map(c => c.low));
    const maxPrice = Math.max(...candles.map(c => c.high));
    const range = maxPrice - minPrice || 1;

    const padding = 20;
    const usableHeight = canvas.height - padding * 2;
    const getY = (price: number) => canvas.height - padding - ((price - minPrice) / range) * usableHeight;

    const candleWidth = Math.max(2, (canvas.width - padding * 2) / candles.length - 4);
    const spacing = Math.max(1, (canvas.width - padding * 2) / candles.length);
    
    // Draw Candles
    let x = padding;
    for (const candle of candles) {
      const isUp = candle.close >= candle.open;
      ctx.strokeStyle = isUp ? '#10b981' : '#ef4444';
      ctx.fillStyle = isUp ? '#10b981' : '#ef4444';

      // Wick
      ctx.beginPath();
      ctx.moveTo(x + candleWidth / 2, getY(candle.high));
      ctx.lineTo(x + candleWidth / 2, getY(candle.low));
      ctx.stroke();

      // Body
      const bodyY = getY(Math.max(candle.open, candle.close));
      const bodyHeight = Math.max(1, Math.abs(getY(candle.open) - getY(candle.close)));
      ctx.fillRect(x, bodyY, candleWidth, bodyHeight);

      x += spacing;
    }
  }, [candles]);

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
