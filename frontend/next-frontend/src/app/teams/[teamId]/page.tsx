"use client";
import { useRouter, useParams } from 'next/navigation';
import { useEffect, useState, useRef } from 'react';
import { Box, Typography, Card, Button, Dialog, DialogTitle, DialogContent, DialogActions, TextField, Select, MenuItem, Snackbar } from '@mui/material';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import ReactMarkdown from 'react-markdown';
import Paper from '@mui/material/Paper';
import IconButton from '@mui/material/IconButton';
import DeleteIcon from '@mui/icons-material/Delete';
import AddIcon from '@mui/icons-material/Add';
import ButtonGroup from '@mui/material/ButtonGroup';
import Chip from '@mui/material/Chip';
import Autocomplete from '@mui/material/Autocomplete';
import ThemedMarkdown from '../../components/ThemedMarkdown';

// Add a Team type for clarity
interface Team {
    name: string;
    description: string;
    commType?: string;
    template?: string;
    roles?: string[];
    [key: string]: any;
}

function OverviewTab({ team, onEdit, onDelete, onRolesChange }: { team: any, onEdit: () => void, onDelete: () => void, onRolesChange: (roles: string[]) => void }) {
    const [allRoles, setAllRoles] = useState<string[]>([]);
    const [addRole, setAddRole] = useState('');
    const [snackbar, setSnackbar] = useState<{ open: boolean, message: string, severity: 'success' | 'error' }>({ open: false, message: '', severity: 'success' });
    useEffect(() => {
        fetch('/api/roles').then(r => r.json()).then(data => setAllRoles(data.map((r: any) => r.name)));
    }, []);
    if (!team) return null;
    const handleRemoveRole = async (role: string) => {
        const newRoles = team.roles.filter((r: string) => r !== role);
        try {
            const res = await fetch(`/api/team/${team.name}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ ...team, roles: newRoles }),
            });
            if (!res.ok) throw new Error('Failed to update roles');
            setSnackbar({ open: true, message: `Removed role: ${role}`, severity: 'success' });
            onRolesChange(newRoles);
        } catch {
            setSnackbar({ open: true, message: 'Failed to remove role', severity: 'error' });
        }
    };
    const handleAddRole = async (role: string) => {
        if (!role || team.roles.includes(role)) return;
        const newRoles = [...team.roles, role];
        try {
            const res = await fetch(`/api/team/${team.name}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ ...team, roles: newRoles }),
            });
            if (!res.ok) throw new Error('Failed to update roles');
            setSnackbar({ open: true, message: `Added role: ${role}`, severity: 'success' });
            onRolesChange(newRoles);
            setAddRole('');
        } catch {
            setSnackbar({ open: true, message: 'Failed to add role', severity: 'error' });
        }
    };
    return (
        <Card sx={{ p: 3, mb: 3 }}>
            <Typography variant="body2" sx={{ mb: 1 }}>Communication: {team.commType}</Typography>
            <Typography variant="body2" sx={{ mb: 1 }}>Template: {team.template}</Typography>
            <Typography variant="body2" sx={{ mb: 1 }}>Roles:</Typography>
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mb: 2 }}>
                {team.roles && team.roles.map((role: string) => (
                    <Chip key={role} label={role} onDelete={() => handleRemoveRole(role)} color="primary" />
                ))}
            </Box>
            <Autocomplete
                options={allRoles.filter(r => !team.roles.includes(r))}
                value={addRole}
                onChange={(_, v) => v && handleAddRole(v)}
                inputValue={addRole}
                onInputChange={(_, v) => setAddRole(v)}
                renderInput={(params) => <TextField {...params} label="Add Role" variant="outlined" sx={{ mb: 2, minWidth: 220 }} />}
                freeSolo={false}
            />
            <Box sx={{ display: 'flex', gap: 2 }}>
                <Button variant="contained" onClick={onEdit}>Edit</Button>
                <Button variant="contained" color="error" onClick={onDelete}>Delete</Button>
            </Box>
            <Snackbar open={snackbar.open} autoHideDuration={3000} onClose={() => setSnackbar({ ...snackbar, open: false })} message={snackbar.message} anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }} />
        </Card>
    );
}

function EnvironmentTab({ teamId }: { teamId: string }) {
    const [env, setEnv] = useState('');
    const [editEnv, setEditEnv] = useState('');
    const [editing, setEditing] = useState(false);
    const [maskSecrets, setMaskSecrets] = useState(true);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    useEffect(() => {
        setLoading(true);
        fetch(`/api/team/${teamId}/config/env`).then(r => r.ok ? r.text() : '').then(env => {
            setEnv(env); setEditEnv(env); setLoading(false);
        }).catch(() => { setError('Failed to load env'); setLoading(false); });
    }, [teamId]);
    if (loading) return <Typography>Loading...</Typography>;
    if (error) return <Typography color="error">{error}</Typography>;

    // Helper to mask secrets
    const maskLine = (line: string) => {
        if (!maskSecrets) return line;
        if (/KEY|TOKEN|SECRET/i.test(line) && /=/.test(line)) {
            const [k] = line.split('=', 1);
            return k + '=********';
        }
        return line;
    };

    return <Box>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2, gap: 2 }}>
            <Button variant={editing ? 'outlined' : 'contained'} onClick={() => setEditing(!editing)}>{editing ? 'Cancel' : 'Edit Env'}</Button>
            {editing && <Button variant="contained" color="primary" onClick={async () => {
                await fetch(`/api/team/${teamId}/config/env`, { method: 'PUT', headers: { 'Content-Type': 'text/plain' }, body: editEnv });
                setEnv(editEnv); setEditing(false);
            }}>Save</Button>}
            <Box sx={{ ml: 2 }}>
                <label>
                    <input type="checkbox" checked={maskSecrets} onChange={e => setMaskSecrets(e.target.checked)} /> Mask secrets
                </label>
            </Box>
        </Box>
        {editing ? (
            <TextField multiline minRows={12} value={editEnv} onChange={e => setEditEnv(e.target.value)} fullWidth sx={{ mb: 2, fontFamily: 'monospace' }} />
        ) : (
            <Box sx={{ whiteSpace: 'pre-line', bgcolor: '#f5f5f5', p: 2, borderRadius: 1, mb: 2, fontFamily: 'monospace', fontSize: 15 }}>
                {env.split('\n').map((line, i) => maskLine(line)).join('\n')}
            </Box>
        )}
        {/* TODO: Table-based editing for env, advanced secret masking UI */}
    </Box>;
}

function ChecklistTab({ teamId }: { teamId: string }) {
    const [checklist, setChecklist] = useState('');
    const [editing, setEditing] = useState(false);
    const [editChecklist, setEditChecklist] = useState('');
    const [loading, setLoading] = useState(true);
    useEffect(() => {
        setLoading(true);
        fetch(`/api/team/${teamId}/config/checklist`).then(r => r.ok ? r.text() : '').then(setChecklist).finally(() => setLoading(false));
    }, [teamId]);
    const handleSave = async () => {
        await fetch(`/api/team/${teamId}/config/checklist`, { method: 'PUT', headers: { 'Content-Type': 'text/plain' }, body: editChecklist });
        setChecklist(editChecklist);
        setEditing(false);
    };
    if (loading) return <Typography>Loading...</Typography>;
    return (
        <Box>
            <Box sx={{ mb: 2 }}>
                {editing ? (
                    <>
                        <TextField multiline minRows={10} value={editChecklist} onChange={e => setEditChecklist(e.target.value)} fullWidth sx={{ mb: 2 }} />
                        <Button variant="contained" color="primary" sx={{ mr: 1 }} onClick={handleSave}>Save</Button>
                        <Button variant="outlined" onClick={() => setEditing(false)}>Cancel</Button>
                    </>
                ) : (
                    <Button variant="outlined" onClick={() => { setEditChecklist(checklist); setEditing(true); }}>Edit Checklist</Button>
                )}
            </Box>
            {!editing && (
                <Paper elevation={2} sx={{ p: 3, maxWidth: 900, margin: '0 auto', bgcolor: '#fafbfc' }}>
                    <ThemedMarkdown>{checklist}</ThemedMarkdown>
                </Paper>
            )}
        </Box>
    );
}

function SharedDocsTab({ teamId }: { teamId: string }) {
    const [files, setFiles] = useState<string[]>([]);
    const [selected, setSelected] = useState('');
    const [content, setContent] = useState('');
    const [editing, setEditing] = useState(false);
    const [newDocOpen, setNewDocOpen] = useState(false);
    const [newDocName, setNewDocName] = useState('');
    const [newDocContent, setNewDocContent] = useState('');
    const [importTemplate, setImportTemplate] = useState('');
    const [availableTemplates, setAvailableTemplates] = useState<string[]>([]);
    const [snackbar, setSnackbar] = useState<{ open: boolean, message: string, severity: 'success' | 'error' }>({ open: false, message: '', severity: 'success' });
    const fileInputRef = useRef<HTMLInputElement>(null);

    // Fetch shared docs and template list
    const refreshFiles = () => fetch(`/api/team/${teamId}/cline_docs_shared`).then(r => r.json()).then(setFiles);
    useEffect(() => { refreshFiles(); }, [teamId]);
    useEffect(() => {
        fetch('/api/cline_docs_shared/templates').then(r => r.json()).then(setAvailableTemplates);
    }, []);

    const openFile = (filename: string) => {
        fetch(`/api/team/${teamId}/cline_docs_shared/${filename}`).then(r => r.text()).then(c => { setSelected(filename); setContent(c); setEditing(false); });
    };
    const deleteFile = async (filename: string) => {
        await fetch(`/api/team/${teamId}/cline_docs_shared/${filename}`, { method: 'DELETE' });
        setFiles(files.filter(f => f !== filename));
        if (selected === filename) setSelected('');
        refreshFiles();
    };
    const propagateDoc = (filename: string) => {
        alert(`Propagate ${filename} to sessions (stub)`);
    };
    const handleImport = async (filename: string) => {
        try {
            await fetch(`/api/team/${teamId}/cline_docs_shared/import`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ filename })
            });
            setImportTemplate('');
            refreshFiles();
            setSelected(filename);
            fetch(`/api/team/${teamId}/cline_docs_shared/${filename}`).then(r => r.text()).then(setContent);
            setSnackbar({ open: true, message: `Imported template: ${filename}`, severity: 'success' });
        } catch {
            setSnackbar({ open: true, message: 'Failed to import template', severity: 'error' });
        }
    };
    const handleRestoreDefaults = async () => {
        try {
            await fetch(`/api/team/${teamId}/cline_docs_shared/restore-defaults`, { method: 'POST' });
            refreshFiles();
            setSnackbar({ open: true, message: 'Restored default docs', severity: 'success' });
        } catch {
            setSnackbar({ open: true, message: 'Failed to restore defaults', severity: 'error' });
        }
    };
    const handleCreate = async () => {
        await fetch(`/api/team/${teamId}/cline_docs_shared/${newDocName}`, {
            method: 'POST',
            headers: { 'Content-Type': 'text/plain' },
            body: newDocContent
        });
        setNewDocOpen(false); setNewDocName(''); setNewDocContent('');
        refreshFiles();
    };
    const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (!file) return;
        await fetch(`/api/team/${teamId}/cline_docs_shared/${file.name}`, {
            method: 'POST',
            body: await file.text(),
            headers: { 'Content-Type': 'text/plain' },
        });
        refreshFiles();
        if (fileInputRef.current) fileInputRef.current.value = '';
    };
    return <Box>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2, gap: 2 }}>
            <ButtonGroup variant="contained">
                <Button startIcon={<AddIcon />} onClick={() => setNewDocOpen(true)}>Create</Button>
                <Button onClick={() => fileInputRef.current?.click()}>Upload</Button>
            </ButtonGroup>
            <Select value={importTemplate} onChange={e => { setImportTemplate(e.target.value); if (e.target.value) handleImport(e.target.value); }} displayEmpty sx={{ minWidth: 180 }}>
                <MenuItem value=""><em>Import from Template</em></MenuItem>
                {availableTemplates.map(t => <MenuItem key={t} value={t}>{t}</MenuItem>)}
            </Select>
            <Button variant="outlined" onClick={handleRestoreDefaults}>Restore Defaults</Button>
            <input ref={fileInputRef} type="file" accept=".md" style={{ display: 'none' }} onChange={handleUpload} />
        </Box>
        <Box sx={{ display: 'flex', alignItems: 'flex-start', gap: 3 }}>
            <Box sx={{ minWidth: 220, maxHeight: 400, overflowY: 'auto', borderRight: '1px solid #eee', pr: 2 }}>
                {files.map(f => (
                    <Box key={f} sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                        <Button variant={selected === f ? 'contained' : 'text'} onClick={() => openFile(f)} sx={{ flex: 1, justifyContent: 'flex-start', textTransform: 'none' }}>{f}</Button>
                        <IconButton size="small" onClick={() => deleteFile(f)}><DeleteIcon fontSize="small" /></IconButton>
                    </Box>
                ))}
            </Box>
            <Box sx={{ flex: 1 }}>
                {selected && (
                    <Box>
                        <Box sx={{ display: 'flex', gap: 2, mb: 1 }}>
                            <Button variant="outlined" onClick={() => setEditing(!editing)}>{editing ? 'Cancel' : 'Edit'}</Button>
                            <Button variant="outlined" onClick={() => propagateDoc(selected)}>Propagate</Button>
                        </Box>
                        {editing ? (
                            <TextField multiline minRows={10} value={content} onChange={e => setContent(e.target.value)} fullWidth sx={{ mb: 2 }} />
                        ) : (
                            <Paper elevation={1} sx={{ p: 2, bgcolor: '#f5f5f5' }}>
                                <ThemedMarkdown>{content}</ThemedMarkdown>
                            </Paper>
                        )}
                        {editing && <Button variant="contained" color="primary" onClick={async () => {
                            await fetch(`/api/team/${teamId}/cline_docs_shared/${selected}`, { method: 'PUT', headers: { 'Content-Type': 'text/plain' }, body: content });
                            setEditing(false);
                            refreshFiles();
                        }}>Save</Button>}
                    </Box>
                )}
            </Box>
        </Box>
        <Dialog open={newDocOpen} onClose={() => setNewDocOpen(false)} maxWidth="sm" fullWidth>
            <DialogTitle>Create New Doc</DialogTitle>
            <DialogContent>
                <TextField label="Filename" value={newDocName} onChange={e => setNewDocName(e.target.value)} fullWidth sx={{ mb: 2 }} />
                <TextField label="Content" multiline minRows={8} value={newDocContent} onChange={e => setNewDocContent(e.target.value)} fullWidth />
            </DialogContent>
            <DialogActions>
                <Button onClick={() => setNewDocOpen(false)}>Cancel</Button>
                <Button variant="contained" onClick={handleCreate}>Create</Button>
            </DialogActions>
        </Dialog>
        <Snackbar open={snackbar.open} autoHideDuration={3000} onClose={() => setSnackbar({ ...snackbar, open: false })} message={snackbar.message} anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }} />
    </Box>;
}

function SessionsTab({ teamId }: { teamId: string }) {
    const [sessions, setSessions] = useState<string[]>([]);
    const [loading, setLoading] = useState(true);
    const [snackbar, setSnackbar] = useState<{ open: boolean, message: string, severity: 'success' | 'error' }>({ open: false, message: '', severity: 'success' });
    const [overwrite, setOverwrite] = useState(false);
    const [generateSSH, setGenerateSSH] = useState(true);
    const [selectedSession, setSelectedSession] = useState<string | null>(null);
    const [genLog, setGenLog] = useState<any>(null);
    const [logOpen, setLogOpen] = useState(false);
    const fetchSessions = async () => {
        setLoading(true);
        const res = await fetch(`/api/team/${teamId}/sessions`);
        if (res.ok) {
            const data = await res.json();
            setSessions(data);
        } else {
            setSessions([]);
        }
        setLoading(false);
    };
    useEffect(() => { fetchSessions(); }, [teamId]);
    const handleGenerate = async () => {
        setLoading(true);
        const res = await fetch(`/api/team/${teamId}/generate-sessions`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ overwrite, generate_ssh_key: generateSSH }),
        });
        let log = null;
        if (res.ok) {
            log = await res.json();
            setSnackbar({ open: true, message: 'Sessions generated!', severity: 'success' });
            fetchSessions();
        } else {
            log = await res.json();
            setSnackbar({ open: true, message: 'Failed to generate sessions', severity: 'error' });
        }
        setGenLog(log);
        setLogOpen(true);
        setLoading(false);
    };
    if (loading) return <Box p={2}><Typography>Loading...</Typography></Box>;
    return <Box p={2}>
        <Box sx={{ mb: 2 }}>
            <label>
                <input type="checkbox" checked={overwrite} onChange={e => setOverwrite(e.target.checked)} /> Overwrite existing sessions
            </label>
            <label style={{ marginLeft: 24 }}>
                <input type="checkbox" checked={generateSSH} onChange={e => setGenerateSSH(e.target.checked)} /> Generate new SSH keys
            </label>
            <Button variant="contained" color="primary" onClick={handleGenerate} sx={{ ml: 3 }}>Generate Sessions</Button>
            {genLog && <Button variant="outlined" sx={{ ml: 2 }} onClick={() => setLogOpen(true)}>View Log</Button>}
        </Box>
        <Typography variant="h6" sx={{ mb: 2 }}>Sessions</Typography>
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2 }}>
            {sessions.map(s => (
                <Card key={s} sx={{ minWidth: 220, maxWidth: 300, p: 2, mb: 2 }}>
                    <Typography variant="subtitle1" sx={{ mb: 1 }}>{s}</Typography>
                    <Button variant="outlined" size="small" onClick={() => setSelectedSession(s)}>Open Session</Button>
                </Card>
            ))}
        </Box>
        {/* Log Modal */}
        <Dialog open={logOpen} onClose={() => setLogOpen(false)} maxWidth="md" fullWidth>
            <DialogTitle>Session Generation Log</DialogTitle>
            <DialogContent dividers>
                {genLog && (
                    <Box>
                        <Typography variant="subtitle2">Created Sessions:</Typography>
                        <ul>{genLog.created && genLog.created.map((s: string) => <li key={s}>{s}</li>)}</ul>
                        <Typography variant="subtitle2">Skipped Sessions:</Typography>
                        <ul>{genLog.skipped && genLog.skipped.map((s: string) => <li key={s}>{s}</li>)}</ul>
                        <Typography variant="subtitle2">Errors:</Typography>
                        <ul>{genLog.errors && genLog.errors.map((e: string, i: number) => <li key={i}>{e}</li>)}</ul>
                        <Typography variant="subtitle2" sx={{ mt: 2 }}>CLI Stdout:</Typography>
                        <Paper sx={{ p: 1, bgcolor: '#f5f5f5', mb: 2, maxHeight: 200, overflow: 'auto' }}>
                            <ThemedMarkdown>{genLog.stdout}</ThemedMarkdown>
                        </Paper>
                        <Typography variant="subtitle2">CLI Stderr:</Typography>
                        <Paper sx={{ p: 1, bgcolor: '#f5f5f5', maxHeight: 100, overflow: 'auto' }}>
                            <ThemedMarkdown>{genLog.stderr}</ThemedMarkdown>
                        </Paper>
                    </Box>
                )}
            </DialogContent>
            <DialogActions>
                <Button onClick={() => setLogOpen(false)}>Close</Button>
            </DialogActions>
        </Dialog>
        <Snackbar open={snackbar.open} autoHideDuration={3000} onClose={() => setSnackbar({ ...snackbar, open: false })} message={snackbar.message} anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }} />
    </Box>;
}

// --- ChatTab: Team Internal Chat (WebSocket MVP) ---
function ChatTab({ teamId }: { teamId: string }) {
    const [messages, setMessages] = useState<{ user: string, message: string }[]>([]);
    const [input, setInput] = useState("");
    const ws = useRef<WebSocket | null>(null);
    const [connected, setConnected] = useState(false);
    // Always use backend port 8000 for chat WebSocket
    const port = 8000;
    useEffect(() => {
        if (typeof window === "undefined") return;
        ws.current = new WebSocket(`ws://localhost:${port}/ws/${teamId}`);
        ws.current.onopen = () => setConnected(true);
        ws.current.onclose = () => setConnected(false);
        ws.current.onmessage = (event) => {
            try {
                const msg = JSON.parse(event.data);
                setMessages((msgs) => [...msgs, msg]);
            } catch { }
        };
        return () => { ws.current && ws.current.close(); };
    }, [teamId, port]);

    const send = () => {
        if (ws.current && input.trim()) {
            ws.current.send(JSON.stringify({ user: "You", message: input }));
            setInput("");
        }
    };

    return (
        <Box>
            <Typography variant="h6" sx={{ mb: 1 }}>Team Chat</Typography>
            <Box sx={{ minHeight: 200, maxHeight: 350, overflowY: 'auto', border: '1px solid #ccc', mb: 2, p: 2, borderRadius: 1, bgcolor: '#fafbfc' }}>
                {messages.length === 0 ? <Typography color="text.secondary">No messages yet.</Typography> :
                    messages.map((msg, i) => (
                        <Box key={i} sx={{ mb: 1 }}><b>{msg.user}:</b> {msg.message}</Box>
                    ))}
            </Box>
            <Box sx={{ display: 'flex', gap: 1 }}>
                <TextField value={input} onChange={e => setInput(e.target.value)} onKeyDown={e => e.key === "Enter" && send()} fullWidth size="small" placeholder="Type a message..." />
                <Button variant="contained" onClick={send} disabled={!connected || !input.trim()}>Send</Button>
            </Box>
            {!connected && <Typography color="error" sx={{ mt: 1 }}>Not connected to chat server.</Typography>}
        </Box>
    );
}

const tabLabels = [
    'Overview',
    'Environment',
    'Checklist',
    'Shared Docs',
    'Sessions',
];

export default function TeamDetailsPage() {
    const router = useRouter();
    const params = useParams();
    // Ensure teamId is always a string
    const teamId = typeof params.teamId === 'string' ? params.teamId : Array.isArray(params.teamId) ? params.teamId[0] : '';
    const [team, setTeam] = useState<Team | null>(null);
    const [loading, setLoading] = useState(true);
    const [editOpen, setEditOpen] = useState(false);
    const [editForm, setEditForm] = useState({ name: '', description: '', commType: 'internal' });
    const [deleteOpen, setDeleteOpen] = useState(false);
    const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' });
    const [tab, setTab] = useState(0);

    useEffect(() => {
        fetch(`/api/team/${teamId}`)
            .then(res => res.json())
            .then(data => { setTeam(data); setLoading(false); });
    }, [teamId]);

    // Use TEAM_ID from backend if available, else normalize team.name
    function normalizeTeamId(name: string) {
        return name.toLowerCase().replace(/\s+/g, '-').replace(/[^a-z0-9_-]/g, '');
    }
    const teamChatId = team?.TEAM_ID || (team?.name ? normalizeTeamId(team.name) : '');

    const handleEdit = () => {
        if (!team) return;
        setEditForm({
            name: team.name,
            description: team.description,
            commType: team.commType || 'internal',
        });
        setEditOpen(true);
    };

    const handleSave = async () => {
        if (!team) return;
        try {
            const res = await fetch(`/api/team/${teamId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ ...team, ...editForm }),
            });
            if (!res.ok) throw new Error('Failed to update team');
            setSnackbar({ open: true, message: 'Team updated', severity: 'success' });
            setEditOpen(false);
            setTeam({ ...team, ...editForm });
        } catch (e) {
            setSnackbar({ open: true, message: 'Error updating team', severity: 'error' });
        }
    };

    const handleDelete = async () => {
        try {
            const res = await fetch(`/api/team/${teamId}`, { method: 'DELETE' });
            if (!res.ok) throw new Error('Failed to delete team');
            setSnackbar({ open: true, message: 'Team deleted', severity: 'success' });
            setDeleteOpen(false);
            setTimeout(() => router.push('/teams'), 1000);
        } catch (e) {
            setSnackbar({ open: true, message: 'Error deleting team', severity: 'error' });
        }
    };

    if (loading) return <Box sx={{ p: 4 }}><Typography>Loading...</Typography></Box>;
    if (!team || (team as any).error) return <Box sx={{ p: 4 }}><Typography color="error">Team not found.</Typography></Box>;

    return (
        <Box>
            <Typography variant="h4" sx={{ mb: 2 }}>{team?.name}</Typography>
            <Tabs value={tab} onChange={(_, v) => setTab(v)} sx={{ mb: 3 }}>
                <Tab label="Overview" />
                <Tab label="Chat" />
                <Tab label="Sessions" />
                <Tab label="Tasks" />
                <Tab label="Shared Docs" />
                <Tab label="Checklist" />
                <Tab label="Environment" />
            </Tabs>
            {tab === 0 && team && <OverviewTab team={team} onEdit={handleEdit} onDelete={() => setDeleteOpen(true)} onRolesChange={(roles) => setTeam({ ...team, roles })} />}
            {tab === 1 && teamChatId && <ChatTab teamId={teamChatId} />}
            {tab === 2 && teamId && <SessionsTab teamId={teamId} />}
            {tab === 3 && teamId && <Typography sx={{ p: 2 }}>Tasks coming soon.</Typography>}
            {tab === 4 && teamId && <SharedDocsTab teamId={teamId} />}
            {tab === 5 && teamId && <ChecklistTab teamId={teamId} />}
            {tab === 6 && teamId && <EnvironmentTab teamId={teamId} />}
            <Dialog open={editOpen} onClose={() => setEditOpen(false)} maxWidth="sm" fullWidth>
                <DialogTitle>Edit Team</DialogTitle>
                <DialogContent>
                    <TextField label="Team Name" value={editForm.name} onChange={e => setEditForm({ ...editForm, name: e.target.value })} fullWidth sx={{ mb: 2 }} />
                    <TextField label="Description" value={editForm.description} onChange={e => setEditForm({ ...editForm, description: e.target.value })} fullWidth sx={{ mb: 2 }} />
                    <Select label="Communication Type" value={editForm.commType} onChange={e => setEditForm({ ...editForm, commType: e.target.value })} fullWidth>
                        <MenuItem value="internal">Internal Chat</MenuItem>
                        <MenuItem value="discord">Discord</MenuItem>
                        <MenuItem value="slack">Slack</MenuItem>
                    </Select>
                </DialogContent>
                <DialogActions>
                    <Button onClick={() => setEditOpen(false)}>Cancel</Button>
                    <Button variant="contained" onClick={handleSave}>Save</Button>
                </DialogActions>
            </Dialog>
            <Dialog open={deleteOpen} onClose={() => setDeleteOpen(false)}>
                <DialogTitle>Delete Team</DialogTitle>
                <DialogContent>
                    <Typography>Are you sure you want to delete this team? This cannot be undone.</Typography>
                </DialogContent>
                <DialogActions>
                    <Button onClick={() => setDeleteOpen(false)}>Cancel</Button>
                    <Button color="error" variant="contained" onClick={handleDelete}>Delete</Button>
                </DialogActions>
            </Dialog>
            <Snackbar open={snackbar.open} autoHideDuration={3000} onClose={() => setSnackbar({ ...snackbar, open: false })} message={snackbar.message} anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }} />
        </Box>
    );
} 