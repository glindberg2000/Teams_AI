"use client";
import { useEffect, useState } from 'react';
import AssignmentIndIcon from '@mui/icons-material/AssignmentInd';
import StorageIcon from '@mui/icons-material/Storage';
import CodeIcon from '@mui/icons-material/Code';
import RateReviewIcon from '@mui/icons-material/RateReview';
import PythonIcon from '@mui/icons-material/Code';
import { Box, Typography, Card, Avatar, Grid, CircularProgress, Alert, Accordion, AccordionSummary, AccordionDetails, Button, Dialog, DialogTitle, DialogContent, DialogActions, TextField, Snackbar, IconButton } from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import AddIcon from '@mui/icons-material/Add';
import ReactMarkdown from 'react-markdown';
import { useTheme } from '@mui/material/styles';
import ThemedMarkdown from '../components/ThemedMarkdown';

const roleIcons = {
    pm_guardian: <AssignmentIndIcon sx={{ bgcolor: '#1976d2', color: '#fff' }} />,
    db_guardian: <StorageIcon sx={{ bgcolor: '#388e3c', color: '#fff' }} />,
    full_stack_dev: <CodeIcon sx={{ bgcolor: '#fbc02d', color: '#fff' }} />,
    reviewer: <RateReviewIcon sx={{ bgcolor: '#7b1fa2', color: '#fff' }} />,
    python_coder: <PythonIcon sx={{ bgcolor: '#0288d1', color: '#fff' }} />,
};

function PrettyCodeBlock({ content }: { content: string }) {
    let formatted = content;
    let isJson = false;
    try {
        const parsed = JSON.parse(content);
        formatted = JSON.stringify(parsed, null, 2);
        isJson = true;
    } catch (e) {
        // Not JSON, show as plain text
    }
    return (
        <Box sx={{ fontFamily: 'monospace', fontSize: 14, bgcolor: '#f5f5f5', p: 2, borderRadius: 1, overflowX: 'auto' }}>
            <pre style={{ margin: 0, whiteSpace: 'pre-wrap', wordBreak: 'break-all', color: isJson ? '#1565c0' : undefined }}>{formatted}</pre>
        </Box>
    );
}

function PrettyEnvBlock({ content }: { content: string }) {
    // Remove leading/trailing quotes and unescape newlines if needed
    let formatted = content;
    if (formatted && typeof formatted === 'string') {
        if (formatted.startsWith('"') && formatted.endsWith('"')) {
            formatted = formatted.slice(1, -1);
        }
        formatted = formatted.replace(/\\n/g, '\n');
    }
    return (
        <Box sx={{ fontFamily: 'monospace', fontSize: 14, bgcolor: '#f5f5f5', p: 2, borderRadius: 1, overflowX: 'auto' }}>
            <pre style={{ margin: 0, whiteSpace: 'pre-wrap', wordBreak: 'break-all' }}>{formatted || 'No .env.sample available.'}</pre>
        </Box>
    );
}

function EditDialog({ open, title, value, onClose, onSave, multiline = false, prettifyJson = false }) {
    const [text, setText] = useState('');
    useEffect(() => {
        if (prettifyJson) {
            try {
                setText(JSON.stringify(JSON.parse(value), null, 2));
            } catch {
                setText(value || '');
            }
        } else {
            setText(value || '');
        }
    }, [value, prettifyJson]);
    return (
        <Dialog open={open} onClose={() => onClose()} maxWidth="md" fullWidth>
            <DialogTitle>{title}</DialogTitle>
            <DialogContent>
                <TextField
                    value={text}
                    onChange={e => setText(e.target.value)}
                    fullWidth
                    multiline={true}
                    minRows={8}
                    variant="outlined"
                />
            </DialogContent>
            <DialogActions>
                <Button onClick={() => onClose()}>Cancel</Button>
                <Button onClick={() => onSave(text)} variant="contained">Save</Button>
            </DialogActions>
        </Dialog>
    );
}

function ConfirmDialog({ open, title, message, onClose, onConfirm }) {
    return (
        <Dialog open={open} onClose={() => onClose()}>
            <DialogTitle>{title}</DialogTitle>
            <DialogContent><Typography>{message}</Typography></DialogContent>
            <DialogActions>
                <Button onClick={() => onClose()}>Cancel</Button>
                <Button onClick={onConfirm} color="error" variant="contained">Delete</Button>
            </DialogActions>
        </Dialog>
    );
}

function CreateRoleDialog({ open, onClose, onCreate }) {
    const [roleName, setRoleName] = useState('');
    return (
        <Dialog open={open} onClose={() => onClose()}>
            <DialogTitle>Create New Role</DialogTitle>
            <DialogContent>
                <TextField
                    label="Role Name"
                    value={roleName}
                    onChange={e => setRoleName(e.target.value)}
                    fullWidth
                    autoFocus
                />
            </DialogContent>
            <DialogActions>
                <Button onClick={() => onClose()}>Cancel</Button>
                <Button onClick={() => { onCreate(roleName); setRoleName(''); }} variant="contained">Create</Button>
            </DialogActions>
        </Dialog>
    );
}

function RoleDetails({ role, onRoleUpdated, onRoleDeleted }) {
    const [overview, setOverview] = useState('');
    const [envSample, setEnvSample] = useState('');
    const [mcpConfig, setMcpConfig] = useState('');
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [editField, setEditField] = useState(null);
    const [editValue, setEditValue] = useState('');
    const [saving, setSaving] = useState(false);
    const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' });
    const [confirmDelete, setConfirmDelete] = useState(false);
    const theme = useTheme();

    useEffect(() => {
        setLoading(true);
        Promise.all([
            fetch(`/api/role/${role.id}/overview`).then(r => r.ok ? r.text() : ''),
            fetch(`/api/role/${role.id}/env-sample`).then(r => r.ok ? r.text() : ''),
            fetch(`/api/role/${role.id}/mcp-config`).then(r => r.ok ? r.text() : ''),
        ]).then(([overview, envSample, mcpConfig]) => {
            setOverview(overview);
            setEnvSample(envSample);
            setMcpConfig(mcpConfig);
            setLoading(false);
        }).catch(e => {
            setError('Failed to load role details');
            setLoading(false);
        });
    }, [role.id]);

    const handleEdit = (field, value) => {
        if (field === 'mcp') {
            // Pretty-print JSON for editing
            try {
                setEditValue(JSON.stringify(JSON.parse(value), null, 2));
            } catch {
                setEditValue(value || '');
            }
        } else if (field === 'env') {
            // Show env as-is, preserving newlines
            let formatted = value;
            if (formatted && typeof formatted === 'string') {
                if (formatted.startsWith('"') && formatted.endsWith('"')) {
                    formatted = formatted.slice(1, -1);
                }
                formatted = formatted.replace(/\\n/g, '\n');
            }
            setEditValue(formatted || '');
        } else {
            setEditValue(value || '');
        }
        setEditField(field);
    };
    const handleSave = async (newValue) => {
        setSaving(true);
        let url, method = 'PUT', body = newValue;
        if (editField === 'overview') url = `/api/role/${role.id}/overview`;
        if (editField === 'env') url = `/api/role/${role.id}/env-sample`;
        if (editField === 'mcp') {
            url = `/api/role/${role.id}/mcp-config`;
            // Minify JSON before saving
            try {
                body = JSON.stringify(JSON.parse(newValue));
            } catch {
                body = newValue;
            }
        }
        try {
            const res = await fetch(url, { method, headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
            if (!res.ok) throw new Error('Failed to save');
            setSnackbar({ open: true, message: 'Saved!', severity: 'success' });
            setEditField(null);
            onRoleUpdated && onRoleUpdated();
        } catch (e) {
            setSnackbar({ open: true, message: 'Error saving', severity: 'error' });
        } finally {
            setSaving(false);
        }
    };
    const handleDelete = async () => {
        setSaving(true);
        try {
            const res = await fetch(`/api/role/${role.id}`, { method: 'DELETE' });
            if (!res.ok) throw new Error('Failed to delete');
            setSnackbar({ open: true, message: 'Role deleted', severity: 'success' });
            setConfirmDelete(false);
            onRoleDeleted && onRoleDeleted();
        } catch (e) {
            setSnackbar({ open: true, message: 'Error deleting', severity: 'error' });
        } finally {
            setSaving(false);
        }
    };

    if (loading) return <CircularProgress size={24} />;
    if (error) return <Alert severity="error">{error}</Alert>;

    return (
        <Box>
            <Accordion>
                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                    <Typography>Role Overview</Typography>
                </AccordionSummary>
                <AccordionDetails>
                    {overview && overview.trim().startsWith('#') ? (
                        <ThemedMarkdown>{overview}</ThemedMarkdown>
                    ) : (
                        <Box sx={{ fontFamily: 'monospace', fontSize: 14, bgcolor: '#f5f5f5', p: 2, borderRadius: 1, overflowX: 'auto' }}>
                            <pre style={{ margin: 0, whiteSpace: 'pre-wrap', wordBreak: 'break-all' }}>{overview || 'No overview available.'}</pre>
                        </Box>
                    )}
                    <Box sx={{ display: 'flex', justifyContent: 'flex-end', mt: 1 }}>
                        <IconButton size="small" onClick={() => handleEdit('overview', overview)}><EditIcon fontSize="small" /></IconButton>
                    </Box>
                </AccordionDetails>
            </Accordion>
            <Accordion>
                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                    <Typography>Environment Sample</Typography>
                </AccordionSummary>
                <AccordionDetails>
                    <PrettyEnvBlock content={envSample} />
                    <Box sx={{ display: 'flex', justifyContent: 'flex-end', mt: 1 }}>
                        <IconButton size="small" onClick={() => handleEdit('env', envSample)}><EditIcon fontSize="small" /></IconButton>
                    </Box>
                </AccordionDetails>
            </Accordion>
            <Accordion>
                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                    <Typography>MCP Config Template</Typography>
                </AccordionSummary>
                <AccordionDetails>
                    <PrettyCodeBlock content={mcpConfig || 'No mcp_config.template.json available.'} />
                    <Box sx={{ display: 'flex', justifyContent: 'flex-end', mt: 1 }}>
                        <IconButton size="small" onClick={() => handleEdit('mcp', mcpConfig)}><EditIcon fontSize="small" /></IconButton>
                    </Box>
                </AccordionDetails>
            </Accordion>
            <Button startIcon={<DeleteIcon />} color="error" sx={{ mt: 2 }} onClick={() => setConfirmDelete(true)}>Delete Role</Button>
            <EditDialog
                open={!!editField}
                title={`Edit ${editField === 'overview' ? 'Role Overview' : editField === 'env' ? '.env.sample' : 'MCP Config'}`}
                value={editValue}
                onClose={() => setEditField(null)}
                onSave={handleSave}
                multiline={true}
                prettifyJson={editField === 'mcp'}
            />
            <ConfirmDialog
                open={confirmDelete}
                title="Delete Role"
                message={`Are you sure you want to delete the role '${role.id}'? This cannot be undone.`}
                onClose={() => setConfirmDelete(false)}
                onConfirm={handleDelete}
            />
            <Snackbar
                open={snackbar.open}
                autoHideDuration={3000}
                onClose={() => setSnackbar({ ...snackbar, open: false })}
                message={snackbar.message}
                anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
            />
        </Box>
    );
}

export default function RolesPage() {
    const [roles, setRoles] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [createOpen, setCreateOpen] = useState(false);
    const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' });

    useEffect(() => {
        fetch('/api/roles')
            .then((res) => {
                if (!res.ok) throw new Error('Failed to fetch roles');
                return res.json();
            })
            .then((data) => {
                setRoles(data);
                setLoading(false);
            })
            .catch((err) => {
                setError(err.message);
                setLoading(false);
            });
    }, []);

    const refreshRoles = () => {
        setLoading(true);
        fetch('/api/roles')
            .then((res) => {
                if (!res.ok) throw new Error('Failed to fetch roles');
                return res.json();
            })
            .then((data) => {
                setRoles(data);
                setLoading(false);
            })
            .catch((err) => {
                setError(err.message);
                setLoading(false);
            });
    };

    const handleCreate = async (roleName) => {
        if (!roleName) return;
        try {
            const res = await fetch('/api/role', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(roleName) });
            if (!res.ok) throw new Error('Failed to create role');
            setSnackbar({ open: true, message: 'Role created', severity: 'success' });
            setCreateOpen(false);
            refreshRoles();
        } catch (e) {
            setSnackbar({ open: true, message: 'Error creating role', severity: 'error' });
        }
    };

    if (loading) return <Box sx={{ p: 4 }}><CircularProgress /></Box>;
    if (error) return <Box sx={{ p: 4 }}><Alert severity="error">{error}</Alert></Box>;

    return (
        <Box sx={{ p: 4 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Typography variant="h4" gutterBottom sx={{ flex: 1 }}>Roles</Typography>
                <Button startIcon={<AddIcon />} variant="contained" onClick={() => setCreateOpen(true)}>Create Role</Button>
            </Box>
            <Grid container spacing={4}>
                {roles.map((role) => (
                    <Grid item xs={12} md={6} key={role.id}>
                        <Card sx={{ p: 2, display: 'flex', alignItems: 'center', mb: 2 }}>
                            <Avatar sx={{ mr: 2 }}>
                                {roleIcons[role.id] || <AssignmentIndIcon />}
                            </Avatar>
                            <Box sx={{ flex: 1 }}>
                                <Typography variant="h6">{role.name}</Typography>
                                <RoleDetails role={role} onRoleUpdated={refreshRoles} onRoleDeleted={refreshRoles} />
                            </Box>
                        </Card>
                    </Grid>
                ))}
            </Grid>
            <CreateRoleDialog open={createOpen} onClose={() => setCreateOpen(false)} onCreate={handleCreate} />
            <Snackbar
                open={snackbar.open}
                autoHideDuration={3000}
                onClose={() => setSnackbar({ ...snackbar, open: false })}
                message={snackbar.message}
                anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
            />
        </Box>
    );
} 