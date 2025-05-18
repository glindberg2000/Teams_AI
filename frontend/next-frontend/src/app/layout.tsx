"use client";
import * as React from 'react';
import Link from 'next/link';
import Box from '@mui/material/Box';
import Drawer from '@mui/material/Drawer';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import Typography from '@mui/material/Typography';
import HomeIcon from '@mui/icons-material/Home';
import ChatIcon from '@mui/icons-material/Chat';
import GroupIcon from '@mui/icons-material/Group';
import AssignmentIcon from '@mui/icons-material/Assignment';
import KeyIcon from '@mui/icons-material/VpnKey';
import AccessTimeIcon from '@mui/icons-material/AccessTime';
import ListAltIcon from '@mui/icons-material/ListAlt';
import SettingsIcon from '@mui/icons-material/Settings';
import HelpIcon from '@mui/icons-material/Help';
import ListItemButton from '@mui/material/ListItemButton';
import './globals.css';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import IconButton from '@mui/material/IconButton';
import Brightness4Icon from '@mui/icons-material/Brightness4';
import Brightness7Icon from '@mui/icons-material/Brightness7';

const drawerWidth = 220;

const navLinks = [
  { to: '/', label: 'Dashboard', icon: <HomeIcon /> },
  { to: '/teams', label: 'Teams', icon: <GroupIcon /> },
  { to: '/roles', label: 'Role Templates', icon: <AssignmentIcon /> },
  { to: '/settings', label: 'Settings', icon: <SettingsIcon /> },
  { to: '/help', label: 'Help', icon: <HelpIcon /> },
];

const lightPalette = {
  mode: 'light',
  primary: { main: '#1976d2' }, // Futuristic blue
  secondary: { main: '#00bcd4' }, // Cyan
  background: { default: '#f5f7fa', paper: '#ffffff' },
  text: { primary: '#171717', secondary: '#4f5b62' },
  divider: '#e3e8ee',
};
const darkPalette = {
  mode: 'dark',
  primary: { main: '#00bcd4' }, // Cyan
  secondary: { main: '#7c4dff' }, // Futuristic purple
  background: { default: '#101624', paper: '#181f2a' },
  text: { primary: '#ededed', secondary: '#b0b8c1' },
  divider: '#232b3b',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  const [mode, setMode] = React.useState<'light' | 'dark'>(
    typeof window !== 'undefined' && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
  );
  const theme = React.useMemo(() => createTheme({ palette: mode === 'dark' ? darkPalette : lightPalette }), [mode]);

  React.useEffect(() => {
    // Listen for system color scheme changes
    const mq = window.matchMedia('(prefers-color-scheme: dark)');
    const handler = (e: MediaQueryListEvent) => setMode(e.matches ? 'dark' : 'light');
    mq.addEventListener('change', handler);
    return () => mq.removeEventListener('change', handler);
  }, []);

  return (
    <html lang="en">
      <body>
        <ThemeProvider theme={theme}>
          <Box sx={{ display: 'flex', bgcolor: 'background.default', color: 'text.primary', minHeight: '100vh' }}>
            <AppBar position="fixed" sx={{ zIndex: 1201, bgcolor: 'background.paper', color: 'text.primary' }}>
              <Toolbar>
                <Typography variant="h6" noWrap component="div" sx={{ flexGrow: 1 }}>
                  TEAM AI Dashboard
                </Typography>
                <IconButton color="inherit" onClick={() => setMode(mode === 'dark' ? 'light' : 'dark')}>
                  {mode === 'dark' ? <Brightness7Icon /> : <Brightness4Icon />}
                </IconButton>
              </Toolbar>
            </AppBar>
            <Drawer
              variant="permanent"
              sx={{
                width: drawerWidth,
                flexShrink: 0,
                [`& .MuiDrawer-paper`]: {
                  width: drawerWidth,
                  boxSizing: 'border-box',
                  bgcolor: 'background.paper',
                  color: 'text.primary',
                },
              }}
            >
              <Toolbar />
              <Box sx={{ overflow: 'auto' }}>
                <List>
                  {navLinks.map((link) => (
                    <ListItem key={link.to} disablePadding>
                      <ListItemButton component={Link} href={link.to}>
                        <ListItemIcon sx={{ color: 'inherit' }}>{link.icon}</ListItemIcon>
                        <ListItemText primary={link.label} />
                      </ListItemButton>
                    </ListItem>
                  ))}
                </List>
              </Box>
            </Drawer>
            <Box component="main" sx={{ flexGrow: 1, bgcolor: 'background.default', p: 3, ml: `${drawerWidth}px`, color: 'text.primary', minHeight: '100vh' }}>
              <Toolbar />
              {children}
            </Box>
          </Box>
        </ThemeProvider>
      </body>
    </html>
  );
}
