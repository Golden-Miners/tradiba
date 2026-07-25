import React from 'react';
import { Outlet, useNavigate } from 'react-router-dom';
import { Box, Drawer, AppBar, Toolbar, Typography, List, ListItem, ListItemButton, ListItemIcon, ListItemText, CssBaseline, Button } from '@mui/material';
import DashboardIcon from '@mui/icons-material/Dashboard';
import ShowChartIcon from '@mui/icons-material/ShowChart';
import AccountBalanceWalletIcon from '@mui/icons-material/AccountBalanceWallet';
import SettingsIcon from '@mui/icons-material/Settings';
import LogoutIcon from '@mui/icons-material/Logout';
import SmartToyIcon from '@mui/icons-material/SmartToy';
import { useAuthStore } from '../stores/authStore';
import { useWebSocket } from '../hooks/useWebSocket';
import { usePortfolioStore } from '../stores/portfolioStore';
import { wsManager } from '../websocket/WebSocketManager';

const drawerWidth = 240;

export const DashboardLayout = () => {
  const navigate = useNavigate();
  const logout = useAuthStore(state => state.logout);
  const updatePortfolio = usePortfolioStore(state => state.updatePortfolio);
  
  // Connect WebSocket
  useWebSocket();

  // Listen to WebSocket events
  React.useEffect(() => {
    const unsub = wsManager.subscribe('PortfolioUpdatedEvent', (payload) => {
      // payload corresponds to the Portfolio domain object serialized
      if (payload) {
        updatePortfolio({
          equity: payload.equity,
          balance: payload.balance,
          free_margin: payload.free_margin,
          positions_count: payload.open_positions
        });
      }
    });

    return () => {
      unsub();
    };
  }, [updatePortfolio]);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const menuItems = [
    { text: 'Dashboard', icon: <DashboardIcon />, path: '/' },
    { text: 'Portfolio', icon: <AccountBalanceWalletIcon />, path: '/portfolio' },
    { text: 'Charts', icon: <ShowChartIcon />, path: '/charts' },
    { text: 'Strategies', icon: <SmartToyIcon />, path: '/strategies' },
    { text: 'System', icon: <SettingsIcon />, path: '/system' },
  ];

  return (
    <Box sx={{ display: 'flex' }}>
      <CssBaseline />
      <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}>
        <Toolbar>
          <Typography variant="h6" noWrap component="div" sx={{ flexGrow: 1 }}>
            Tradiba Production Dashboard
          </Typography>
          <Button color="inherit" onClick={handleLogout} startIcon={<LogoutIcon />}>
            Logout
          </Button>
        </Toolbar>
      </AppBar>
      <Drawer
        variant="permanent"
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          [`& .MuiDrawer-paper`]: { width: drawerWidth, boxSizing: 'border-box' },
        }}
      >
        <Toolbar />
        <Box sx={{ overflow: 'auto' }}>
          <List>
            {menuItems.map((item) => (
              <ListItem key={item.text} disablePadding>
                <ListItemButton onClick={() => navigate(item.path)}>
                  <ListItemIcon>{item.icon}</ListItemIcon>
                  <ListItemText primary={item.text} />
                </ListItemButton>
              </ListItem>
            ))}
          </List>
        </Box>
      </Drawer>
      <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
        <Toolbar />
        <Outlet />
      </Box>
    </Box>
  );
};
