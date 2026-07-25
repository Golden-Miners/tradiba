import { useState, useEffect } from 'react';
import { Box, Typography, Card, Table, TableBody, TableCell, TableHead, TableRow, Switch, Snackbar, Alert } from '@mui/material';
import { apiClient } from '../api/axios';

interface Strategy {
  name: string;
  is_active: boolean;
  active_signals: number;
}

export const Strategies = () => {
  const [strategies, setStrategies] = useState<Strategy[]>([]);
  const [error, setError] = useState<string | null>(null);

  const fetchStrategies = async () => {
    try {
      const res = await apiClient.get('/strategies');
      setStrategies(res.data);
    } catch (err: any) {
      setError(err.message || 'Failed to fetch strategies');
    }
  };

  useEffect(() => {
    fetchStrategies();
  }, []);

  const handleToggle = async (name: string, currentActive: boolean) => {
    try {
      if (currentActive) {
        await apiClient.post(`/strategies/${name}/disable`);
      } else {
        await apiClient.post(`/strategies/${name}/enable`);
      }
      fetchStrategies(); // Refresh the list
    } catch (err: any) {
      setError(err.response?.data?.message || 'Failed to toggle strategy');
    }
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Strategies
      </Typography>
      <Card>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Strategy Name</TableCell>
              <TableCell align="center">Status</TableCell>
              <TableCell align="center">Active Signals</TableCell>
              <TableCell align="right">Toggle</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {strategies.map((strat) => (
              <TableRow key={strat.name}>
                <TableCell>{strat.name}</TableCell>
                <TableCell align="center">
                  <Typography color={strat.is_active ? 'success.main' : 'textSecondary'}>
                    {strat.is_active ? 'ACTIVE' : 'INACTIVE'}
                  </Typography>
                </TableCell>
                <TableCell align="center">{strat.active_signals}</TableCell>
                <TableCell align="right">
                  <Switch 
                    checked={strat.is_active} 
                    onChange={() => handleToggle(strat.name, strat.is_active)} 
                  />
                </TableCell>
              </TableRow>
            ))}
            {strategies.length === 0 && (
              <TableRow>
                <TableCell colSpan={4} align="center">No strategies found</TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </Card>
      
      <Snackbar open={!!error} autoHideDuration={6000} onClose={() => setError(null)}>
        <Alert severity="error" onClose={() => setError(null)}>
          {error}
        </Alert>
      </Snackbar>
    </Box>
  );
};
