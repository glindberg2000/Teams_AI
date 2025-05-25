FROM mcr.microsoft.com/devcontainers/python:0-3.11-bullseye

# Ensure Node.js, npm, and npx are available
RUN apt-get update && \
    apt-get install -y nodejs npm && \
    npm install -g npx

# system deps + jq
RUN apt-get update && \
    apt-get install -y wget curl ca-certificates tar gzip git docker.io jq && \
    rm -rf /var/lib/apt/lists/*

# Create workspace structure
RUN mkdir -p /workspaces/project/payload \
    /workspaces/project/docs \
    /root/.codeium/windsurf \
    /root/.ssh

WORKDIR /workspaces/project

# put entrypoint in place
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Always upgrade to Node.js 20 (LTS) for MCP/Windsurf compatibility
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs

# Always upgrade npm to v9 (stable for npx usage)
RUN npm install -g npm@9

# Remove any global npx v10+ if present (safety)
RUN rm -f /usr/local/bin/npx

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD sleep infinity  # Windsurf will override with its own server start 