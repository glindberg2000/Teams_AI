import React from 'react';
import { Box, useTheme } from '@mui/material';
import ReactMarkdown from 'react-markdown';

export default function ThemedMarkdown({ children }: { children: string }) {
    const theme = useTheme();
    return (
        <Box
            sx={{
                p: 2,
                bgcolor: theme.palette.background.paper,
                color: theme.palette.text.primary,
                borderRadius: 1,
                overflowX: 'auto',
                '& h1, & h2, & h3, & h4, & h5, & h6': { color: theme.palette.text.primary },
                '& code': {
                    bgcolor: theme.palette.mode === 'dark' ? '#232b3b' : '#f5f5f5',
                    color: theme.palette.mode === 'dark' ? '#00bcd4' : '#1565c0',
                    borderRadius: 1,
                    px: 0.5,
                    py: 0.2,
                    fontSize: 14,
                },
                '& pre': {
                    bgcolor: theme.palette.mode === 'dark' ? '#181f2a' : '#f5f5f5',
                    color: theme.palette.text.primary,
                    borderRadius: 1,
                    p: 1,
                    fontSize: 14,
                    overflowX: 'auto',
                },
                '& blockquote': {
                    borderLeft: `4px solid ${theme.palette.primary.main}`,
                    bgcolor: theme.palette.mode === 'dark' ? '#181f2a' : '#f5f5f5',
                    color: theme.palette.text.secondary,
                    pl: 2,
                    my: 1,
                },
            }}
        >
            <ReactMarkdown>{children}</ReactMarkdown>
        </Box>
    );
} 