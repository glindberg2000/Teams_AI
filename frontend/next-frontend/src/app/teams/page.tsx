"use client";
import GroupIcon from '@mui/icons-material/Group';
import { Box, Typography, Card, Avatar, Grid, Button, CircularProgress, Alert, Dialog, DialogTitle, DialogContent, DialogActions, TextField, MenuItem, Select, IconButton, Snackbar } from '@mui/material';
import { useEffect, useState } from 'react';
import AddIcon from '@mui/icons-material/Add';
import Link from 'next/link';
import React from 'react';

interface Team {
    id: string;
    name: string;
    description: string;
    // Add more fields as needed for modal details
}

interface TeamTemplate {
    name: string;
    displayName?: string;
    description?: string;
    // Add more fields as needed
}

export default function TeamsPage() {
    const [teams, setTeams] = useState<Team[]>([]);
    const [templates, setTemplates] = useState<TeamTemplate[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [instantiateOpen, setInstantiateOpen] = useState(false);
    const [newTeam, setNewTeam] = useState({ name: '', description: '', commType: 'internal', template: '' });
    const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' });

    useEffect(() => {
        fetch('/api/teams')
            .then((res) => {
                if (!res.ok) throw new Error('Failed to fetch teams');
                return res.json();
            })
            .then((data) => {
                setTeams(data);
                setLoading(false);
            })
            .catch((err) => {
                setError(err.message);
                setLoading(false);
            });
        fetch('/api/team-templates')
            .then((res) => res.json())
            .then((data) => setTemplates(data));
    }, []);

    const handleInstantiate = () => {
        setNewTeam({ name: '', description: '', commType: 'internal', template: '' });
        setInstantiateOpen(true);
    };

    const handleSubmitInstantiate = async () => {
        if (!newTeam.name || !newTeam.template) {
            setSnackbar({ open: true, message: 'Team name and template are required', severity: 'error' });
            return;
        }
        try {
            const res = await fetch('/api/instantiate-team', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(newTeam),
            });
            if (!res.ok) throw new Error('Failed to instantiate team');
            setSnackbar({ open: true, message: 'Team created', severity: 'success' });
            setInstantiateOpen(false);
            refreshTeams();
        } catch (e) {
            setSnackbar({ open: true, message: 'Error creating team', severity: 'error' });
        }
    };

    const refreshTeams = () => {
        fetch('/api/teams')
            .then((res) => res.json())
            .then((data) => setTeams(data));
    };

    return (
        <Box sx={{ p: 4 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                <Typography variant="h4">Your Teams</Typography>
                <Button startIcon={<AddIcon />} variant="contained" color="primary" size="large" sx={{ borderRadius: 2 }} onClick={handleInstantiate}>
                    Instantiate from Template
                </Button>
            </Box>
            {loading && <CircularProgress />}
            {error && <Alert severity="error">{error}</Alert>}
            <Grid container spacing={2}>
                {teams.length === 0 && !loading && !error ? (
                    <Typography variant="body1" color="text.secondary">No teams yet. Instantiate a team to get started.</Typography>
                ) : (
                    teams.map((team) => (
                        <Grid item xs={12} key={team.id}>
                            <Link href={`/teams/${encodeURIComponent(team.name)}`} style={{ textDecoration: 'none' }}>
                                <Card
                                    variant="outlined"
                                    sx={{ display: 'flex', alignItems: 'center', p: 2, cursor: 'pointer', transition: 'box-shadow 0.2s', '&:hover': { boxShadow: 4 } }}
                                >
                                    <Avatar sx={{ mr: 2, width: 48, height: 48 }}><GroupIcon sx={{ bgcolor: '#0288d1', color: '#fff' }} /></Avatar>
                                    <Box>
                                        <Typography variant="h6">{team.name}</Typography>
                                        <Typography variant="body2" color="text.secondary">{team.description}</Typography>
                                    </Box>
                                </Card>
                            </Link>
                        </Grid>
                    ))
                )}
            </Grid>
            <Dialog open={instantiateOpen} onClose={() => setInstantiateOpen(false)} maxWidth="sm" fullWidth>
                <DialogTitle>Instantiate Team from Template</DialogTitle>
                <DialogContent>
                    <Select
                        label="Template"
                        value={newTeam.template}
                        onChange={e => setNewTeam({ ...newTeam, template: e.target.value })}
                        fullWidth
                        sx={{ mb: 2 }}
                    >
                        <MenuItem value=""><em>Select a template</em></MenuItem>
                        {templates.map((tpl) => (
                            <MenuItem key={tpl.name} value={tpl.name}>{tpl.displayName || tpl.name}</MenuItem>
                        ))}
                    </Select>
                    <TextField label="Team Name" value={newTeam.name} onChange={e => setNewTeam({ ...newTeam, name: e.target.value })} fullWidth sx={{ mb: 2 }} />
                    <TextField label="Description" value={newTeam.description} onChange={e => setNewTeam({ ...newTeam, description: e.target.value })} fullWidth sx={{ mb: 2 }} />
                    <Select
                        label="Communication Type"
                        value={newTeam.commType}
                        onChange={e => setNewTeam({ ...newTeam, commType: e.target.value })}
                        fullWidth
                    >
                        <MenuItem value="internal">Internal Chat</MenuItem>
                        <MenuItem value="discord">Discord</MenuItem>
                        <MenuItem value="slack">Slack</MenuItem>
                    </Select>
                </DialogContent>
                <DialogActions>
                    <Button onClick={() => setInstantiateOpen(false)}>Cancel</Button>
                    <Button variant="contained" onClick={handleSubmitInstantiate}>Create Team</Button>
                </DialogActions>
            </Dialog>
            <Snackbar open={snackbar.open} autoHideDuration={3000} onClose={() => setSnackbar({ ...snackbar, open: false })} message={snackbar.message} anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }} />
        </Box>
    );
} 