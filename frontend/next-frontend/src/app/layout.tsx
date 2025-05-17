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

const drawerWidth = 220;

const navLinks = [
  { to: '/', label: 'Dashboard', icon: <HomeIcon /> },
  { to: '/teams', label: 'Teams', icon: <GroupIcon /> },
  { to: '/roles', label: 'Role Templates', icon: <AssignmentIcon /> },
  { to: '/settings', label: 'Settings', icon: <SettingsIcon /> },
  { to: '/help', label: 'Help', icon: <HelpIcon /> },
];

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <Box sx={{ display: 'flex' }}>
          <AppBar position="fixed" sx={{ zIndex: 1201 }}>
            <Toolbar>
              <Typography variant="h6" noWrap component="div">
                TEAM AI Dashboard
              </Typography>
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
          <Box component="main" sx={{ flexGrow: 1, bgcolor: 'background.default', p: 3, ml: `${drawerWidth}px` }}>
            <Toolbar />
            {children}
          </Box>
        </Box>
      </body>
    </html>
  );
}
