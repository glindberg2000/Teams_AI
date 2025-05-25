import React, { useState, useEffect } from 'react';
import { Box, List, ListItemButton, ListItemIcon, ListItemText, IconButton, Typography, Tooltip, Divider, Dialog, DialogTitle, DialogContent, DialogActions, Button, TextField } from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import TagIcon from '@mui/icons-material/Tag';
import LockIcon from '@mui/icons-material/Lock';

// Channel type
export interface Channel {
    id: string;
    name: string;
    isPrivate?: boolean;
}

interface ChannelSidebarProps {
    teamId: string;
    channels: Channel[];
    selectedChannelId: string;
    onSelect: (id: string) => void;
    onAdd?: (name: string) => void;
    onRename?: (id: string, name: string) => void;
    onDelete?: (id: string) => void;
}

export default function ChannelSidebar({ teamId, channels, selectedChannelId, onSelect, onAdd, onRename, onDelete }: ChannelSidebarProps) {
    const [addOpen, setAddOpen] = useState(false);
    const [renameOpen, setRenameOpen] = useState<string | null>(null);
    const [deleteOpen, setDeleteOpen] = useState<string | null>(null);
    const [newName, setNewName] = useState('');

    // Responsive: collapse on mobile (future improvement)

    return (
        <Box sx={{ width: 260, bgcolor: 'background.paper', borderRight: '1px solid #eee', height: '100%', display: 'flex', flexDirection: 'column' }}>
            <Box sx={{ p: 2, pb: 1, display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <Typography variant="h6">Channels</Typography>
                {onAdd && (
                    <Tooltip title="Add Channel"><IconButton onClick={() => { setAddOpen(true); setNewName(''); }} size="small"><AddIcon /></IconButton></Tooltip>
                )}
            </Box>
            <Divider />
            <List sx={{ flex: 1, overflowY: 'auto', py: 0 }}>
                {channels.map((ch) => (
                    <ListItemButton
                        key={ch.id}
                        selected={ch.id === selectedChannelId}
                        onClick={() => onSelect(ch.id)}
                        sx={{ borderRadius: 1, mb: 0.5, mx: 1 }}
                    >
                        <ListItemIcon>
                            {ch.isPrivate ? <LockIcon fontSize="small" /> : <TagIcon fontSize="small" />}
                        </ListItemIcon>
                        <ListItemText primary={ch.name} primaryTypographyProps={{ noWrap: true }} />
                        {onRename && (
                            <Tooltip title="Rename"><IconButton size="small" onClick={e => { e.stopPropagation(); setRenameOpen(ch.id); setNewName(ch.name); }}><EditIcon fontSize="small" /></IconButton></Tooltip>
                        )}
                        {onDelete && (
                            <Tooltip title="Delete"><IconButton size="small" onClick={e => { e.stopPropagation(); setDeleteOpen(ch.id); }}><DeleteIcon fontSize="small" /></IconButton></Tooltip>
                        )}
                    </ListItemButton>
                ))}
            </List>
            {/* Add Channel Dialog */}
            {onAdd && (
                <Dialog open={addOpen} onClose={() => setAddOpen(false)}>
                    <DialogTitle>Add Channel</DialogTitle>
                    <DialogContent>
                        <TextField label="Channel Name" value={newName} onChange={e => setNewName(e.target.value)} autoFocus fullWidth />
                    </DialogContent>
                    <DialogActions>
                        <Button onClick={() => setAddOpen(false)}>Cancel</Button>
                        <Button variant="contained" onClick={() => { if (newName.trim()) { onAdd(newName.trim()); setAddOpen(false); } }}>Add</Button>
                    </DialogActions>
                </Dialog>
            )}
            {/* Rename Channel Dialog */}
            {onRename && (
                <Dialog open={!!renameOpen} onClose={() => setRenameOpen(null)}>
                    <DialogTitle>Rename Channel</DialogTitle>
                    <DialogContent>
                        <TextField label="New Name" value={newName} onChange={e => setNewName(e.target.value)} autoFocus fullWidth />
                    </DialogContent>
                    <DialogActions>
                        <Button onClick={() => setRenameOpen(null)}>Cancel</Button>
                        <Button variant="contained" onClick={() => { if (renameOpen && newName.trim()) { onRename(renameOpen, newName.trim()); setRenameOpen(null); } }}>Rename</Button>
                    </DialogActions>
                </Dialog>
            )}
            {/* Delete Channel Dialog */}
            {onDelete && (
                <Dialog open={!!deleteOpen} onClose={() => setDeleteOpen(null)}>
                    <DialogTitle>Delete Channel</DialogTitle>
                    <DialogContent>
                        <Typography>Are you sure you want to delete this channel?</Typography>
                    </DialogContent>
                    <DialogActions>
                        <Button onClick={() => setDeleteOpen(null)}>Cancel</Button>
                        <Button color="error" variant="contained" onClick={() => { if (deleteOpen) { onDelete(deleteOpen); setDeleteOpen(null); } }}>Delete</Button>
                    </DialogActions>
                </Dialog>
            )}
        </Box>
    );
} 