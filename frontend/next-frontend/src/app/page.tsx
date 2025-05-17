"use client";
import { useState, useEffect } from 'react';
import styles from "./page.module.css";
import GroupIcon from '@mui/icons-material/Group';
import FolderIcon from '@mui/icons-material/Folder';
import AssignmentIndIcon from '@mui/icons-material/AssignmentInd';
import StorageIcon from '@mui/icons-material/Storage';
import CodeIcon from '@mui/icons-material/Code';
import RateReviewIcon from '@mui/icons-material/RateReview';
import PythonIcon from '@mui/icons-material/Code'; // No native Python icon, use CodeIcon
import { Box, Typography, Card, CardContent, CardHeader, Avatar, Button, Grid } from '@mui/material';

// Mocked data for roles and teams (replace with backend fetch in production)
const roles = [
  {
    id: 'pm_guardian',
    name: 'PM Guardian',
    description: 'Project management, task tracking, and team coordination.',
    icon: <AssignmentIndIcon sx={{ bgcolor: '#1976d2', color: '#fff' }} />,
  },
  {
    id: 'db_guardian',
    name: 'DB Guardian',
    description: 'Database schema design, backup/restore, and query optimization.',
    icon: <StorageIcon sx={{ bgcolor: '#388e3c', color: '#fff' }} />,
  },
  {
    id: 'full_stack_dev',
    name: 'Full Stack Dev',
    description: 'Backend APIs, frontend features, and code quality.',
    icon: <CodeIcon sx={{ bgcolor: '#fbc02d', color: '#fff' }} />,
  },
  {
    id: 'reviewer',
    name: 'Reviewer',
    description: 'Code review, quality assurance, and standards enforcement.',
    icon: <RateReviewIcon sx={{ bgcolor: '#d32f2f', color: '#fff' }} />,
  },
  {
    id: 'python_coder',
    name: 'Python Coder',
    description: 'Python backend development, code quality, and test coverage.',
    icon: <PythonIcon sx={{ bgcolor: '#512da8', color: '#fff' }} />,
  },
];

const teams = [
  {
    id: 'LedgerFlow_AI',
    name: 'LedgerFlow_AI',
    description: 'LedgerFlow_AI',
    icon: <GroupIcon sx={{ bgcolor: '#0288d1', color: '#fff' }} />,
    // Add more metadata as needed
  },
  // Add more teams as needed
];

export default function Home() {
  return (
    <Box sx={{ p: 4 }}>
      <Typography variant="h3" gutterBottom>TEAM AI Dashboard</Typography>
      <Typography variant="subtitle1" gutterBottom>
        Welcome! This is your unified workspace for managing teams, roles, and agent sessions.
      </Typography>
      <Grid container spacing={4} sx={{ my: 2 }}>
        <Grid item xs={12} md={6}>
          <Card variant="outlined">
            <CardContent>
              <Typography variant="h6" gutterBottom>Quick Links</Typography>
              <Box sx={{ display: 'flex', gap: 2, mt: 2 }}>
                <Button
                  variant="contained"
                  color="primary"
                  startIcon={<GroupIcon />}
                  href="/teams"
                  sx={{ borderRadius: 2 }}
                >
                  View Teams
                </Button>
                <Button
                  variant="contained"
                  color="secondary"
                  startIcon={<AssignmentIndIcon />}
                  href="/roles"
                  sx={{ borderRadius: 2 }}
                >
                  View Roles
                </Button>
              </Box>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={6}>
          <Card variant="outlined">
            <CardContent>
              <Typography variant="h6" gutterBottom>Recent Activity</Typography>
              <Typography variant="body2" color="text.secondary">
                (Recent activity and stats widgets coming soon)
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
      <Box sx={{ mt: 4 }}>
        <Card variant="outlined">
          <CardContent>
            <Typography variant="h6" gutterBottom>Overview</Typography>
            <Typography variant="body2" color="text.secondary">
              Use the navigation links to manage your teams and roles. This dashboard will soon display system stats, recent changes, and more.
            </Typography>
          </CardContent>
        </Card>
      </Box>
    </Box>
  );
}
