import { useState, useEffect } from 'react';
import { Box, Typography, Card, CardContent, Chip } from '@mui/material';
import { apiClient } from '../api/axios';

interface SystemHealth {
  status: 'healthy' | 'warning' | 'critical';
  database: string;
  event_bus: string;
  active_jobs: number;
}

export const System = () => {
  const [health, setHealth] = useState<SystemHealth | null>(null);

  useEffect(() => {
    const fetchHealth = async () => {
      try {
        const res = await apiClient.get('/health');
        setHealth(res.data);
      } catch (err) {
        setHealth({ status: 'critical', database: 'unknown', event_bus: 'unknown', active_jobs: 0 });
      }
    };
    fetchHealth();
    const interval = setInterval(fetchHealth, 10000);
    return () => clearInterval(interval);
  }, []);

  const getStatusColor = (status: string) => {
    if (status === 'healthy') return 'success';
    if (status === 'warning') return 'warning';
    return 'error';
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        System Health
      </Typography>
      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 3 }}>
        <Box sx={{ flex: '1 1 50%', maxWidth: '100%' }}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Overall Status
              </Typography>
              {health ? (
                <Chip 
                  label={health.status.toUpperCase()} 
                  color={getStatusColor(health.status)} 
                  sx={{ mb: 2 }}
                />
              ) : (
                <Typography>Loading...</Typography>
              )}
              
              <Typography>
                <strong>Database:</strong> {health?.database || '...'}
              </Typography>
              <Typography>
                <strong>Event Bus:</strong> {health?.event_bus || '...'}
              </Typography>
              <Typography>
                <strong>Active Background Jobs:</strong> {health?.active_jobs ?? '...'}
              </Typography>
            </CardContent>
          </Card>
        </Box>
      </Box>
    </Box>
  );
};
