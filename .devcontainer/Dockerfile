FROM node:20-bullseye

# system deps + jq
RUN apt-get update && \
    apt-get install -y wget curl ca-certificates tar gzip git docker.io jq python3-venv && \
    rm -rf /var/lib/apt/lists/*

RUN echo "break cache $(date +%s)"

# Create workspace structure
RUN mkdir -p /workspaces/project/payload \
    /workspaces/project/docs \
    /root/.codeium/windsurf \
    /root/.ssh

WORKDIR /workspaces/project

# put entrypoint in place
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD sleep infinity  # Windsurf will override with its own server start 