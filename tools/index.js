const { MCPServer, tool } = require('@modelcontextprotocol/server');
const WebSocket = require('ws');

const port = process.env.CHAT_PORT || 8000;
const teamId = process.env.TEAM_ID || 'team-8';
const wsUrl = `ws://localhost:${port}/ws/${teamId}`;

const mcp = new MCPServer();

tool(mcp, 'send_message', {
    description: 'Send a message to the team chat',
    parameters: {
        user: { type: 'string', description: 'User name' },
        message: { type: 'string', description: 'Message text' }
    },
    async handler({ user, message }) {
        return new Promise((resolve, reject) => {
            const ws = new WebSocket(wsUrl);
            ws.on('open', () => {
                ws.send(JSON.stringify({ user, message }));
                ws.close();
                resolve({ status: 'ok' });
            });
            ws.on('error', reject);
        });
    }
});

tool(mcp, 'get_unread_messages', {
    description: 'Get unread messages from the team chat',
    parameters: {},
    async handler() {
        return new Promise((resolve, reject) => {
            const ws = new WebSocket(wsUrl);
            let messages = [];
            ws.on('message', (data) => {
                messages.push(JSON.parse(data));
            });
            ws.on('close', () => resolve({ messages }));
            ws.on('error', reject);
            setTimeout(() => ws.close(), 1000);
        });
    }
});

mcp.listen(); 