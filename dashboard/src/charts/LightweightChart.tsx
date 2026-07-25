import React, { useEffect, useRef } from 'react';
import { createChart, ColorType, CandlestickSeries } from 'lightweight-charts';
import type { IChartApi, ISeriesApi, Time } from 'lightweight-charts';
import { Box } from '@mui/material';

export interface CandleData {
  time: string | number; // Assuming UNIX timestamp or ISO string mapped to what lightweight-charts expects
  open: number;
  high: number;
  low: number;
  close: number;
}

interface LightweightChartProps {
  data: CandleData[];
  width?: number;
  height?: number;
}

export const LightweightChart: React.FC<LightweightChartProps> = ({ data, width = 800, height = 400 }) => {
  const chartContainerRef = useRef<HTMLDivElement>(null);
  const chartRef = useRef<IChartApi | null>(null);
  const seriesRef = useRef<ISeriesApi<'Candlestick'> | null>(null);

  useEffect(() => {
    if (chartContainerRef.current) {
      const chart = createChart(chartContainerRef.current, {
        width,
        height,
        layout: {
          background: { type: ColorType.Solid, color: '#1e1e1e' },
          textColor: '#d1d4dc',
        },
        grid: {
          vertLines: { color: 'rgba(42, 46, 57, 0.5)' },
          horzLines: { color: 'rgba(42, 46, 57, 0.5)' },
        },
        timeScale: {
          timeVisible: true,
          secondsVisible: false,
        },
      });

      const candlestickSeries = (chart as any).addCandlestickSeries ? (chart as any).addCandlestickSeries({
        upColor: '#26a69a',
        downColor: '#ef5350',
        borderVisible: false,
        wickUpColor: '#26a69a',
        wickDownColor: '#ef5350',
      }) : (chart as any).addSeries(CandlestickSeries, {
        upColor: '#26a69a',
        downColor: '#ef5350',
        borderVisible: false,
        wickUpColor: '#26a69a',
        wickDownColor: '#ef5350',
      });

      // lightweight-charts expects time as UNIX timestamp in seconds or a Time string
      const formattedData = data.map(d => ({
        ...d,
        time: (typeof d.time === 'string' ? new Date(d.time).getTime() / 1000 : d.time) as Time,
      })).sort((a, b) => (a.time as number) - (b.time as number));

      candlestickSeries.setData(formattedData);

      chartRef.current = chart;
      seriesRef.current = candlestickSeries;

      return () => {
        chart.remove();
      };
    }
  }, [data, width, height]);

  // Handle resizing
  useEffect(() => {
    const handleResize = () => {
      if (chartContainerRef.current && chartRef.current) {
        chartRef.current.applyOptions({
          width: chartContainerRef.current.clientWidth,
        });
      }
    };
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return (
    <Box ref={chartContainerRef} sx={{ width: '100%', height: `${height}px` }} />
  );
};
