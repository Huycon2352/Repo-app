FROM node:20-bookworm-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl tini && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /usr/local/app

COPY package.json package-lock.json ./

RUN npm ci --omit=dev

COPY . .

ENV PORT=80
EXPOSE 80

ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["node", "server.js"]

# FROM node:20-bookworm-slim

# RUN apt-get update && \
#     apt-get upgrade -y && \
#     apt-get install -y --no-install-recommends curl tini && \
#     rm -rf /var/lib/apt/lists/*

# WORKDIR /usr/local/app

# COPY package.json package-lock.json ./

# RUN npm ci --omit=dev

# COPY . .

# ENV PORT=80
# EXPOSE 80

# USER node

# ENTRYPOINT ["/usr/bin/tini", "--"]
# CMD ["node", "server.js"]
