# FROM node:20-slim

# # add curl for healthcheck
# RUN apt-get update && \
#     apt-get install -y --no-install-recommends curl tini && \
#     rm -rf /var/lib/apt/lists/*

# WORKDIR /usr/local/app

# # have nodemon available for local dev use (file watching)
# RUN npm install -g nodemon

# COPY package*.json ./

# RUN npm ci && \
#  npm cache clean --force && \
#  mv /usr/local/app/node_modules /node_modules

# COPY . .

# ENV PORT=80
# EXPOSE 80

# ENTRYPOINT ["/usr/bin/tini", "--"]
# CMD ["node", "server.js"]

#v2
# FROM node:20-slim

# RUN apt-get update && \
#     apt-get install -y --no-install-recommends curl tini && \
#     rm -rf /var/lib/apt/lists/*

# WORKDIR /usr/local/app

# COPY package*.json ./

# RUN npm ci --omit=dev

# COPY . .

# ENV PORT=80
# EXPOSE 80

# ENTRYPOINT ["/usr/bin/tini", "--"]
# CMD ["node", "server.js"]

#v3
# FROM node:20-slim

# RUN apt-get update && apt-get upgrade -y && \
#     apt-get install -y --no-install-recommends curl tini && \
#     rm -rf /var/lib/apt/lists/*

# WORKDIR /usr/local/app

# COPY package*.json ./

# RUN npm ci --omit=dev

# COPY . .

# ENV PORT=80
# EXPOSE 80

# ENTRYPOINT ["/usr/bin/tini", "--"]
# CMD ["node", "server.js"]

#v4
# FROM node:20-slim

# # update OS packages + security fixes
# RUN apt-get update && apt-get upgrade -y && \
#     apt-get install -y --no-install-recommends curl tini && \
#     rm -rf /var/lib/apt/lists/*

# WORKDIR /usr/local/app

# # copy dependency files first (better caching)
# COPY package.json package-lock.json ./

# # install production dependencies only
# RUN npm ci --omit=dev --no-audit --no-fund

# # copy source code
# COPY . .

# ENV NODE_ENV=production
# ENV PORT=80

# EXPOSE 80

# ENTRYPOINT ["/usr/bin/tini", "--"]
# CMD ["node", "server.js"]

#v5
# FROM node:20-slim

# RUN apt-get update && apt-get upgrade -y && \
#     apt-get install -y --no-install-recommends curl tini && \
#     rm -rf /var/lib/apt/lists/*

# WORKDIR /usr/local/app

# COPY package.json package-lock.json ./

# RUN npm ci --omit=dev

# COPY . .

# ENV NODE_ENV=production

# ENTRYPOINT ["/usr/bin/tini", "--"]
# CMD ["node", "server.js"]

#v6
# FROM node:20-slim

# RUN apt-get update && apt-get upgrade -y && \
#     apt-get install -y --no-install-recommends curl tini && \
#     rm -rf /var/lib/apt/lists/*

# WORKDIR /usr/local/app

# COPY package.json package-lock.json ./

# RUN npm ci --omit=dev --no-audit --no-fund

# COPY . .

# ENV NODE_ENV=production

# ENTRYPOINT ["/usr/bin/tini", "--"]
# CMD ["node", "server.js"]

#v7
# vFINAL CLEAN
# FROM node:22-bookworm-slim

# RUN apt-get update && apt-get upgrade -y && \
#     apt-get install -y --no-install-recommends tini ca-certificates && \
#     rm -rf /var/lib/apt/lists/*

# WORKDIR /usr/local/app

# # chỉ copy dependency trước để cache tốt hơn
# COPY package*.json ./

# # ép npm clean install
# RUN npm ci --omit=dev --no-audit --no-fund

# # copy source
# COPY . .

# # chạy non-root (giảm risk CVE exploit)
# RUN useradd -m appuser && chown -R appuser /usr/local/app
# USER appuser

# ENV PORT=80
# EXPOSE 80

# ENTRYPOINT ["tini", "--"]
# CMD ["node", "server.js"]

#v8
# FROM node:22-bookworm-slim

# RUN apt-get update && apt-get upgrade -y && \
#     apt-get install -y --no-install-recommends tini ca-certificates && \
#     rm -rf /var/lib/apt/lists/*

# # Cập nhật npm global lên bản mới nhất để xóa sạch CVE nội bộ của npm CLI
# RUN npm install -g npm@latest

# WORKDIR /usr/local/app

# # chỉ copy dependency trước để cache tốt hơn
# COPY package*.json ./

# # ép npm clean install (Giờ sẽ chạy thành công sau khi bạn làm Bước 1)
# #RUN npm ci --omit=dev --no-audit --no-fund
# # Thay thế npm ci bằng npm install
# RUN npm install --omit=dev --no-audit --no-fund
# # copy source
# COPY . .

# # chạy non-root (giảm risk CVE exploit)
# RUN useradd -m appuser && chown -R appuser /usr/local/app
# USER appuser

# ENV PORT=80
# EXPOSE 80

# ENTRYPOINT ["tini", "--"]
# CMD ["node", "server.js"]

#v9
FROM node:22-bookworm-slim

# 安装系统依赖
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y --no-install-recommends tini ca-certificates && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /usr/local/app

# Bước 1: Tạo user non-root SỚM để cô lập môi trường chạy
RUN useradd -m appuser && chown -R appuser /usr/local/app
USER appuser

# Bước 2: Cấu hình lại thư mục chứa npm global về thư mục của appuser (tránh lỗi permission)
ENV NPM_CONFIG_PREFIX=/home/appuser/.npm-global
ENV PATH=$NPM_CONFIG_PREFIX/bin:$PATH

# Bước 3: Cập nhật npm global bằng quyền appuser và CHẶN script độc hại bằng --ignore-scripts
RUN npm install -g npm@latest --ignore-scripts

# Chỉ copy dependency trước để tận dụng cache tốt hơn
COPY --chown=appuser:appuser package*.json ./

# Bước 4: Cài đặt thư viện ứng dụng kèm cờ --ignore-scripts để dập tắt cảnh báo SonarQube
RUN npm install --omit=dev --no-audit --no-fund --ignore-scripts

# Copy toàn bộ mã nguồn
COPY --chown=appuser:appuser . .

ENV PORT=80
EXPOSE 80

ENTRYPOINT ["tini", "--"]
CMD ["node", "server.js"]
