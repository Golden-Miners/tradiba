import { useState, useEffect } from 'react';
import { Box, Typography, Card, CardContent } from '@mui/material';
import { LightweightChart } from '../charts/LightweightChart';
import type { CandleData } from '../charts/LightweightChart';


export const ChartsView = () => {
  const [data, setData] = useState<CandleData[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // In a real app we would fetch actual historical data
    // For now we'll fetch from a generic endpoint or mock if backend doesn't have a /history endpoint yet
    const fetchHistory = async () => {
      try {
        // Just mocking data since we don't have a specific historical OHLC REST endpoint documented in Sprint 18
        // If we did, it would look like: const res = await apiClient.get('/market/history?symbol=EURUSD');
        
        const mockData: CandleData[] = [
          { time: '2026-07-20T00:00:00Z', open: 1.1, high: 1.12, low: 1.09, close: 1.11 },
          { time: '2026-07-21T00:00:00Z', open: 1.11, high: 1.15, low: 1.10, close: 1.14 },
          { time: '2026-07-22T00:00:00Z', open: 1.14, high: 1.16, low: 1.13, close: 1.15 },
          { time: '2026-07-23T00:00:00Z', open: 1.15, high: 1.15, low: 1.11, close: 1.12 },
          { time: '2026-07-24T00:00:00Z', open: 1.12, high: 1.13, low: 1.08, close: 1.09 },
        ];
        setData(mockData);
      } catch (err) {
        console.error('Failed to fetch history', err);
      } finally {
        setLoading(false);
      }
    };
    fetchHistory();
  }, []);

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Trading Charts (with SMC Overlay)
      </Typography>
      <Card>
        <CardContent>
          {loading ? (
            <Typography>Loading chart data...</Typography>
          ) : (
            <LightweightChart data={data} height={500} />
          )}
        </CardContent>
      </Card>
    </Box>
  );
};
