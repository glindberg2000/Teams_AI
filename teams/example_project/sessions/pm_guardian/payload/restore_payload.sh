#!/bin/bash
set -e

echo "Starting payload restoration process..."

# Function to verify file/directory exists
verify_exists() {
    if [ -e "$1" ]; then
        echo "✅ Verified: $2 exists at $1"
    else
        echo "❌ Error: $2 not found at $1"
        return 1
    fi
}

# Move and verify SSH key setup
echo "Setting up SSH keys..."
if [ -d "/workspaces/project/payload/.ssh" ]; then
    mkdir -p /root/.ssh
    cp -r /workspaces/project/payload/.ssh/* /root/.ssh/
    chmod 600 /root/.ssh/id_rsa
    verify_exists "/root/.ssh/id_rsa" "SSH private key"
    verify_exists "/root/.ssh/id_rsa.pub" "SSH public key"
    echo "SSH key permissions set to 600"
else
    echo "⚠️ Warning: No SSH directory found in payload"
fi

# Move and verify environment file
echo "Setting up environment file..."
if [ -f "/workspaces/project/payload/.env" ]; then
    cp /workspaces/project/payload/.env /workspaces/project/.env
    verify_exists "/workspaces/project/.env" "Environment file"
    
    # Verify key environment variables
    source /workspaces/project/.env
    for var in ANTHROPIC_API_KEY PERPLEXITY_API_KEY GITHUB_PERSONAL_ACCESS_TOKEN SLACK_BOT_TOKEN SLACK_TEAM_ID; do
        if [ -n "${!var}" ]; then
            echo "✅ $var is set"
        else
            echo "⚠️ Warning: $var is not set in .env"
        fi
    done
else
    echo "❌ Error: No .env file found in payload"
fi

# Move and verify MCP config
echo "Setting up MCP configuration..."
if [ -f "/workspaces/project/payload/mcp_config.json" ]; then
    mkdir -p /root/.codeium/windsurf
    cp /workspaces/project/payload/mcp_config.json /root/.codeium/windsurf/mcp_config.json
    verify_exists "/root/.codeium/windsurf/mcp_config.json" "MCP config"
    
    # Verify MCP config contains required servers
    if grep -q "taskmaster-ai" "/root/.codeium/windsurf/mcp_config.json"; then
        echo "✅ Task Master configuration found in MCP config"
    else
        echo "⚠️ Warning: Task Master configuration missing from MCP config"
    fi
else
    echo "❌ Error: No MCP config found in payload"
fi

# Move and verify docs directory
echo "Setting up documentation..."
if [ -d "/workspaces/project/payload/docs" ]; then
    mkdir -p /workspaces/project/docs
    cp -r /workspaces/project/payload/docs/* /workspaces/project/docs/
    verify_exists "/workspaces/project/docs" "Documentation directory"
    
    # Verify key documentation files
    for dir in global role; do
        if [ -d "/workspaces/project/docs/$dir" ]; then
            echo "✅ $dir documentation directory exists"
            echo "   Contents: $(ls -A /workspaces/project/docs/$dir)"
        else
            echo "⚠️ Warning: $dir documentation directory not found"
        fi
    done
else
    echo "⚠️ Warning: No docs directory found in payload"
fi

# Move global rules if they exist (legacy support)
echo "Checking for legacy global rules..."
if [ -f "/workspaces/project/payload/global_rules.md" ]; then
    cp /workspaces/project/payload/global_rules.md /workspaces/project/docs/global_rules.md
    verify_exists "/workspaces/project/docs/global_rules.md" "Legacy global rules"
    echo "⚠️ Note: Using legacy global rules format"
fi

echo "Payload restoration complete!"
echo "Summary of restored components:"
echo "-----------------------------"
ls -la /workspaces/project/.env 2>/dev/null || echo "❌ No .env file"
ls -la /root/.ssh/id_rsa 2>/dev/null || echo "❌ No SSH key"
ls -la /root/.codeium/windsurf/mcp_config.json 2>/dev/null || echo "❌ No MCP config"
ls -la /workspaces/project/docs 2>/dev/null || echo "❌ No docs directory" 