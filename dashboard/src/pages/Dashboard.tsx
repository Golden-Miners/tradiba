import { useEffect } from 'react';
import { Card, CardContent, Typography, Box, Table, TableBody, TableCell, TableHead, TableRow } from '@mui/material';
import { usePortfolioStore } from '../stores/portfolioStore';
import { apiClient } from '../api/axios';

export const Dashboard = () => {
  const { equity, balance, free_margin, positions_count, active_positions, updatePortfolio, updatePositions } = usePortfolioStore();

  useEffect(() => {
    // Initial fetch via REST before websocket takes over/augments
    const fetchPortfolio = async () => {
      try {
        const portRes = await apiClient.get('/portfolio');
        updatePortfolio(portRes.data);
        
        const posRes = await apiClient.get('/portfolio/positions');
        updatePositions(posRes.data);
      } catch (err) {
        console.error('Failed to fetch portfolio', err);
      }
    };
    fetchPortfolio();
  }, [updatePortfolio, updatePositions]);

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Live Dashboard
      </Typography>
      
      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 3, mb: 4 }}>
        <Box sx={{ flex: '1 1 20%' }}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Equity
              </Typography>
              <Typography variant="h5">
                ${equity.toFixed(2)}
              </Typography>
            </CardContent>
          </Card>
        </Box>
        <Box sx={{ flex: '1 1 20%' }}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Balance
              </Typography>
              <Typography variant="h5">
                ${balance.toFixed(2)}
              </Typography>
            </CardContent>
          </Card>
        </Box>
        <Box sx={{ flex: '1 1 20%' }}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Free Margin
              </Typography>
              <Typography variant="h5">
                ${free_margin.toFixed(2)}
              </Typography>
            </CardContent>
          </Card>
        </Box>
        <Box sx={{ flex: '1 1 20%' }}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Open Positions
              </Typography>
              <Typography variant="h5">
                {positions_count}
              </Typography>
            </CardContent>
          </Card>
        </Box>
      </Box>

      <Typography variant="h6" gutterBottom>
        Active Positions
      </Typography>
      <Card>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Symbol</TableCell>
              <TableCell>Ticket</TableCell>
              <TableCell>Type</TableCell>
              <TableCell align="right">Volume</TableCell>
              <TableCell align="right">Entry Price</TableCell>
              <TableCell align="right">Current Price</TableCell>
              <TableCell align="right">PnL</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {active_positions.map((pos) => (
              <TableRow key={pos.ticket}>
                <TableCell>{pos.symbol}</TableCell>
                <TableCell>{pos.ticket}</TableCell>
                <TableCell>{pos.type}</TableCell>
                <TableCell align="right">{pos.volume}</TableCell>
                <TableCell align="right">{pos.price_open}</TableCell>
                <TableCell align="right">{pos.current_price}</TableCell>
                <TableCell align="right" sx={{ color: pos.profit >= 0 ? 'success.main' : 'error.main' }}>
                  ${pos.profit.toFixed(2)}
                </TableCell>
              </TableRow>
            ))}
            {active_positions.length === 0 && (
              <TableRow>
                <TableCell colSpan={7} align="center">No active positions</TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </Card>
    </Box>
  );
};
