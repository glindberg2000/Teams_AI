FROM node:20-bullseye

# system deps + jq
RUN apt-get update && \
    apt-get install -y wget curl ca-certificates tar gzip git docker.io jq && \
    rm -rf /var/lib/apt/lists/*

# put entrypoint in place
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["sleep", "infinity"]  # Windsurf will override with its own server start 