"use client";
import { Box, Typography, Card, Grid, Button, Dialog, DialogTitle, DialogContent, DialogActions, TextField, Chip, IconButton, Snackbar, DialogContentText } from '@mui/material';
import { useEffect, useState } from 'react';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import AddIcon from '@mui/icons-material/Add';

export default function TeamTemplatesPage() {
    const [templates, setTemplates] = useState([]);
    const [roles, setRoles] = useState([]);
    const [templateModalOpen, setTemplateModalOpen] = useState(false);
    const [editingTemplate, setEditingTemplate] = useState(null);
    const [templateForm, setTemplateForm] = useState({ name: '', displayName: '', description: '', roles: [], teamDocs: '' });
    const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
    const [templateToDelete, setTemplateToDelete] = useState(null);
    const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' });
    const [instantiateOpen, setInstantiateOpen] = useState(false);
    const [selectedTemplate, setSelectedTemplate] = useState(null);
    const [newTeam, setNewTeam] = useState({ name: '', description: '', commType: 'internal' });

    useEffect(() => {
        fetch('/api/team-templates')
            .then((res) => res.json())
            .then((data) => setTemplates(data));
        fetch('/api/roles')
            .then((res) => res.json())
            .then((data) => setRoles(data));
    }, []);

    const refreshTemplates = () => {
        fetch('/api/team-templates')
            .then((res) => res.json())
            .then((data) => setTemplates(data));
    };

    const handleEditTemplate = (tpl) => {
        setEditingTemplate(tpl);
        setTemplateForm({
            name: tpl.name,
            displayName: tpl.displayName || '',
            description: tpl.description || '',
            roles: tpl.roles || [],
            teamDocs: tpl.teamDocs || '',
        });
        setTemplateModalOpen(true);
    };

    const handleCreateTemplate = () => {
        setEditingTemplate(null);
        setTemplateForm({ name: '', displayName: '', description: '', roles: [], teamDocs: '' });
        setTemplateModalOpen(true);
    };

    const handleSaveTemplate = async () => {
        if (!templateForm.name) {
            setSnackbar({ open: true, message: 'Template name is required', severity: 'error' });
            return;
        }
        const method = editingTemplate ? 'PUT' : 'POST';
        const url = editingTemplate ? `/api/team-template/${templateForm.name}` : '/api/team-template';
        const body = { ...templateForm };
        try {
            const res = await fetch(url, {
                method,
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body),
            });
            if (!res.ok) throw new Error('Failed to save template');
            setSnackbar({ open: true, message: 'Template saved', severity: 'success' });
            setTemplateModalOpen(false);
            refreshTemplates();
        } catch (e) {
            setSnackbar({ open: true, message: 'Error saving template', severity: 'error' });
        }
    };

    const handleDeleteTemplate = async () => {
        if (!templateToDelete) return;
        try {
            const res = await fetch(`/api/team-template/${templateToDelete.name}`, { method: 'DELETE' });
            if (!res.ok) throw new Error('Failed to delete template');
            setSnackbar({ open: true, message: 'Template deleted', severity: 'success' });
            setDeleteDialogOpen(false);
            setTemplateToDelete(null);
            refreshTemplates();
        } catch (e) {
            setSnackbar({ open: true, message: 'Error deleting template', severity: 'error' });
        }
    };

    const handleRoleToggle = (roleId) => {
        setTemplateForm((prev) => ({
            ...prev,
            roles: prev.roles.includes(roleId)
                ? prev.roles.filter((r) => r !== roleId)
                : [...prev.roles, roleId],
        }));
    };

    const handleInstantiate = (tpl) => {
        setSelectedTemplate(tpl);
        setNewTeam({ name: '', description: '', commType: 'internal' });
        setInstantiateOpen(true);
    };

    return (
        <Box sx={{ p: 4 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Typography variant="h4" sx={{ flex: 1 }}>Team Templates</Typography>
                <Button startIcon={<AddIcon />} variant="contained" onClick={handleCreateTemplate}>Create Template</Button>
            </Box>
            <Grid container spacing={2} sx={{ mb: 4 }}>
                {templates.length === 0 ? (
                    <Typography variant="body1" color="text.secondary">No team templates yet.</Typography>
                ) : (
                    templates.map((tpl) => (
                        <Grid item xs={12} md={6} key={tpl.name}>
                            <Card variant="outlined" sx={{ p: 2, mb: 2, position: 'relative' }}>
                                <Box sx={{ position: 'absolute', top: 8, right: 8, display: 'flex', gap: 1 }}>
                                    <IconButton size="small" onClick={() => handleEditTemplate(tpl)}><EditIcon fontSize="small" /></IconButton>
                                    <IconButton size="small" onClick={() => { setTemplateToDelete(tpl); setDeleteDialogOpen(true); }}><DeleteIcon fontSize="small" /></IconButton>
                                </Box>
                                <Typography variant="h6">{tpl.displayName || tpl.name}</Typography>
                                <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>{tpl.description}</Typography>
                                <Box sx={{ mb: 1 }}>
                                    {tpl.roles && tpl.roles.map((roleId) => {
                                        const role = roles.find(r => r.id === roleId);
                                        return role ? <Chip key={roleId} label={role.name} sx={{ mr: 1, mb: 1 }} /> : null;
                                    })}
                                </Box>
                                <Button variant="contained" sx={{ mt: 2 }} onClick={() => handleInstantiate(tpl)}>Instantiate</Button>
                            </Card>
                        </Grid>
                    ))
                )}
            </Grid>
            <Dialog open={templateModalOpen} onClose={() => setTemplateModalOpen(false)} maxWidth="sm" fullWidth>
                <DialogTitle>{editingTemplate ? 'Edit Team Template' : 'Create Team Template'}</DialogTitle>
                <DialogContent>
                    <TextField label="Template Name" value={templateForm.name} onChange={e => setTemplateForm({ ...templateForm, name: e.target.value })} fullWidth sx={{ mb: 2 }} disabled={!!editingTemplate} />
                    <TextField label="Display Name" value={templateForm.displayName} onChange={e => setTemplateForm({ ...templateForm, displayName: e.target.value })} fullWidth sx={{ mb: 2 }} />
                    <TextField label="Description (Markdown)" value={templateForm.description} onChange={e => setTemplateForm({ ...templateForm, description: e.target.value })} fullWidth multiline minRows={3} sx={{ mb: 2 }} />
                    <Typography variant="subtitle2" sx={{ mb: 1 }}>Roles</Typography>
                    <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mb: 2 }}>
                        {roles.map((role) => (
                            <Chip
                                key={role.id}
                                label={role.name}
                                color={templateForm.roles.includes(role.id) ? 'primary' : 'default'}
                                onClick={() => handleRoleToggle(role.id)}
                                sx={{ cursor: 'pointer' }}
                            />
                        ))}
                    </Box>
                    <TextField label="Team Docs (Markdown)" value={templateForm.teamDocs} onChange={e => setTemplateForm({ ...templateForm, teamDocs: e.target.value })} fullWidth multiline minRows={4} sx={{ mb: 2 }} />
                </DialogContent>
                <DialogActions>
                    <Button onClick={() => setTemplateModalOpen(false)}>Cancel</Button>
                    <Button variant="contained" onClick={handleSaveTemplate}>{editingTemplate ? 'Save' : 'Create'}</Button>
                </DialogActions>
            </Dialog>
            <Dialog open={deleteDialogOpen} onClose={() => setDeleteDialogOpen(false)}>
                <DialogTitle>Delete Team Template</DialogTitle>
                <DialogContent>
                    <DialogContentText>Are you sure you want to delete the template '{templateToDelete?.displayName || templateToDelete?.name}'? This cannot be undone.</DialogContentText>
                </DialogContent>
                <DialogActions>
                    <Button onClick={() => setDeleteDialogOpen(false)}>Cancel</Button>
                    <Button color="error" variant="contained" onClick={handleDeleteTemplate}>Delete</Button>
                </DialogActions>
            </Dialog>
            <Snackbar open={snackbar.open} autoHideDuration={3000} onClose={() => setSnackbar({ ...snackbar, open: false })} message={snackbar.message} anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }} />
            <Dialog open={instantiateOpen} onClose={() => setInstantiateOpen(false)} maxWidth="sm" fullWidth>
                <DialogTitle>Instantiate Team from Template</DialogTitle>
                <DialogContent>
                    <Typography variant="subtitle1" sx={{ mb: 2 }}>{selectedTemplate?.description}</Typography>
                    <TextField label="Team Name" value={newTeam.name} onChange={e => setNewTeam({ ...newTeam, name: e.target.value })} fullWidth sx={{ mb: 2 }} />
                    <TextField label="Description" value={newTeam.description} onChange={e => setNewTeam({ ...newTeam, description: e.target.value })} fullWidth sx={{ mb: 2 }} />
                </DialogContent>
                <DialogActions>
                    <Button onClick={() => setInstantiateOpen(false)}>Cancel</Button>
                    <Button variant="contained" onClick={() => setInstantiateOpen(false)}>Next</Button>
                </DialogActions>
            </Dialog>
        </Box>
    );
} 