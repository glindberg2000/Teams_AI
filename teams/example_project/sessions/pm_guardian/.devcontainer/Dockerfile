FROM node:20-bullseye

# system deps + jq
RUN apt-get update && \
    apt-get install -y wget curl ca-certificates tar gzip git docker.io jq && \
    rm -rf /var/lib/apt/lists/*

# Set up workspace
WORKDIR /workspaces/project

# Keep container running
CMD ["sleep", "infinity"] 