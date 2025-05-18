import React from 'react';
import { Box, useTheme } from '@mui/material';

export default function ThemedMarkdown({ children }: { children: string }) {
    const theme = useTheme();
    return (
        <Box
            component="pre"
            sx={{
                p: 2,
                bgcolor: theme.palette.mode === 'dark' ? '#181f2a' : '#f5f5f5',
                color: theme.palette.mode === 'dark' ? '#ededed' : '#171717',
                borderRadius: 1,
                overflowX: 'auto',
                fontFamily: 'monospace',
                fontSize: 15,
                whiteSpace: 'pre-wrap',
                wordBreak: 'break-word',
                m: 0,
            }}
        >
            {children}
        </Box>
    );
} 