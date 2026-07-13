# AdoruWorld Docker 配置与部署指南

> 基于项目现有架构（FastAPI + Vue 3 + SQLite）的 Docker 方案。
> 核心思路：不用改一行项目代码，直接容器化。

---

## 目录

1. [项目架构回顾](#1-项目架构回顾)
2. [方案选择](#2-方案选择)
3. [方案一：docker-compose 双容器（推荐生产）](#3-方案一docker-compose-双容器推荐生产)
4. [方案二：单容器全栈（轻量部署）](#4-方案二单容器全栈轻量部署)
5. [开发模式：用 Docker 跑后端，本地跑前端](#5-开发模式用-docker-跑后端本地跑前端)
6. [数据持久化与备份](#6-数据持久化与备份)
7. [部署 Checklist](#7-部署-checklist)

---

## 1. 项目架构回顾

```
用户浏览器
     │
     ├── /adoru-world/           → 前端静态文件（SPA）
     ├── /adoru-world/api/v1/*   → 反向代理 → FastAPI (:8000)
     └── /adoru-world/uploads/*  → 反向代理 → FastAPI 静态文件
                          │
                     ┌────┴────┐
                     │ SQLite  │  uploads/
                     └─────────┘
```

**关键配置（全部无需修改）：**

| 配置项 | 当前值 | 说明 |
|--------|--------|------|
| API 前缀 | `/api/v1` | 代码里写死的，容器化不用动 |
| 前端 base | `/adoru-world/` | Vite 配置，不变 |
| 生产 API 地址 | `/adoru-world/api/v1` | `client/src/config/index.ts` 已正确处理 |
| 数据库 | SQLite 文件 | 无需额外数据库容器 |
| Upload 前缀 | `/adoru-world/uploads` | Nginx 层处理 |

---

## 2. 方案选择

| 方案 | 适用场景 | 复杂度 |
|------|---------|--------|
| **docker-compose 双容器** | 生产部署、持久化运行 | ⭐⭐ |
| **单容器全栈** | 轻量部署、迁移到别的机器 | ⭐ |
| **开发模式：仅后端 Docker** | 本地开发不想污染本机环境 | ⭐ |

以下逐一给出完整配置。

---

## 3. 方案一：docker-compose 双容器（推荐生产）

### 3.1 项目根目录下创建文件

#### `server/Dockerfile`

```dockerfile
# ===== 后端 Dockerfile =====
FROM python:3.11-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制源码
COPY app/ ./app/
COPY scripts/ ./scripts/
COPY manage.py .

# 创建 uploads 目录（运行时挂载 volume 会覆盖它）
RUN mkdir -p uploads

# 健康检查
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/')" || exit 1

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

> **注意**：生产环境不要用 `--reload`。

#### `client/Dockerfile`

```dockerfile
# ===== 前端构建 + Nginx 运行 =====
# --- 第一阶段：构建 ---
FROM node:22-alpine AS builder

WORKDIR /build
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build

# --- 第二阶段：Nginx 运行 ---
FROM nginx:alpine

# 复制构建产物
COPY --from=builder /build/dist /usr/share/nginx/html

# Nginx 配置（后面会创建）
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

#### `client/nginx.conf`

```nginx
server {
    listen 80;
    server_name _;

    # 前端文件大小限制（上传相关）
    client_max_body_size 50M;

    # 前端静态文件
    root /usr/share/nginx/html;
    index index.html;

    # SPA 路由：所有非文件请求返回 index.html
    location /adoru-world/ {
        try_files $uri $uri/ /adoru-world/index.html;
    }

    # API 反向代理到后端容器
    location /adoru-world/api/ {
        proxy_pass http://backend:8000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Upload 文件反向代理到后端容器
    location /adoru-world/uploads/ {
        proxy_pass http://backend:8000/uploads/;
        proxy_set_header Host $host;
        # 对上传的文件启用缓存（减少后端压力）
        proxy_cache_valid 200 1d;
        add_header Cache-Control "public, max-age=86400";
    }

    # 后端文档（开发时方便查看）
    location /docs {
        proxy_pass http://backend:8000/docs;
    }
    location /openapi.json {
        proxy_pass http://backend:8000/openapi.json;
    }
}
```

#### `docker-compose.yml`（项目根目录）

```yaml
version: "3.9"

services:
  backend:
    build:
      context: ./server
      dockerfile: Dockerfile
    container_name: adoruworld-backend
    restart: unless-stopped
    environment:
      # SQLite 数据库路径：指向 volume 挂载点
      - DATABASE_URL=sqlite+aiosqlite:///data/adoruworld.db
      - SITE_START_DATE=2025-01-01
    volumes:
      # 持久化：数据库文件
      - adoruworld-data:/data
      # 持久化：上传文件
      - adoruworld-uploads:/app/uploads
    networks:
      - adoruworld-net

  nginx:
    build:
      context: ./client
      dockerfile: Dockerfile
    container_name: adoruworld-nginx
    restart: unless-stopped
    ports:
      - "80:80"        # HTTP
      # - "443:443"    # HTTPS（有证书时取消注释）
    depends_on:
      - backend
    networks:
      - adoruworld-net

networks:
  adoruworld-net:
    driver: bridge

volumes:
  adoruworld-data:      # 数据库持久化
  adoruworld-uploads:   # 上传文件持久化
```

### 3.2 初始化数据（首次部署）

首次部署时数据库是空的，需要导入已有数据：

```bash
# 1. 先构建并启动（数据库表会自动创建，但没数据）
docker compose up -d

# 2. 把已有的数据库文件复制到 volume 中
# 方法 A：直接替换数据库文件
docker cp /path/to/your/adoruworld.db adoruworld-backend:/data/adoruworld.db

# 方法 B：通过导出导入脚本
# 在本机导出数据
cd /home/adorukw/AAAPAN/Project/AdoruWorld/server
python scripts/export_all.py -o backup.zip
# 复制到容器并导入
docker cp backup.zip adoruworld-backend:/app/
docker exec adoruworld-backend python scripts/import_all.py /app/backup.zip

# 3. 重启使数据生效
docker compose restart

# 4. 把本机的 uploads 也复制过去
docker cp /path/to/your/server/uploads/. adoruworld-backend:/app/uploads/
```

### 3.3 日常操作

```bash
# 启动
docker compose up -d

# 查看日志（后端）
docker compose logs -f backend

# 查看日志（Nginx）
docker compose logs -f nginx

# 重启
docker compose restart

# 停止
docker compose down

# 完全清理（会删 volume 数据，小心！）
docker compose down -v
```

### 3.4 加上 HTTPS（正式域名）

在 `docker-compose.yml` 同目录下创建 `docker-compose.prod.yml`：

```yaml
version: "3.9"

services:
  nginx:
    ports:
      - "80:80"
      - "443:443"
    volumes:
      # 挂载证书和 HTTPS 配置
      - ./ssl:/etc/nginx/ssl:ro
      - ./nginx-ssl.conf:/etc/nginx/conf.d/default.conf:ro
```

然后用 `docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d` 启动。

> 或者更简单的做法：在宿主机上装 certbot，证书用 volume 挂进容器。

---

## 4. 方案二：单容器全栈（轻量部署）

如果不想管理两个容器，可以用一个镜像装全部东西。适合迁移到 VPS 或送给朋友部署。

#### `Dockerfile`（项目根目录）

```dockerfile
# ===== 单容器全栈：前端构建 + Python 后端 + Caddy =====
# 使用 Caddy 是因为它比 Nginx 更轻，一行配置就能自动 HTTPS

# --- 第一阶段：构建前端 ---
FROM node:22-alpine AS frontend-builder

WORKDIR /build
COPY client/package.json client/package-lock.json ./
RUN npm ci
COPY client/ .
RUN npm run build

# --- 第二阶段：运行环境 ---
FROM python:3.11-slim

# 安装 Caddy（轻量 Web 服务器）
RUN apt-get update && apt-get install -y debian-keyring debian-archive-keyring apt-transport-https \
    && curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg \
    && curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | tee /etc/apt/sources.list.d/caddy-stable.list \
    && apt-get update && apt-get install -y caddy \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 安装 Python 依赖
COPY server/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制后端源码
COPY server/app/ ./app/
COPY server/scripts/ ./scripts/
COPY server/manage.py .

# 复制前端构建产物
COPY --from=frontend-builder /build/dist /app/frontend

# 创建必要目录
RUN mkdir -p /app/uploads /app/data

# Caddy 配置
COPY Caddyfile /etc/caddy/Caddyfile

EXPOSE 80 443

CMD ["caddy", "run", "--config", "/etc/caddy/Caddyfile", "--adapter", "caddyfile"]
```

#### `Caddyfile`（项目根目录）

```
# Caddy 会自动从 Let's Encrypt 申请证书（如果有域名）
# 没有域名就把 :80 写死

:80 {
    # 前端静态文件
    root * /app/frontend
    try_files {path} /adoru-world/index.html

    # API 反向代理
    reverse_proxy /adoru-world/api/* localhost:8000 {
        rewrite /adoru-world/api/* /api/{path}
    }

    # Uploads
    reverse_proxy /adoru-world/uploads/* localhost:8000 {
        rewrite /adoru-world/uploads/* /uploads/{path}
    }

    # 静态文件缓存
    header /adoru-world/uploads/* Cache-Control "public, max-age=86400"

    # 后端文档
    reverse_proxy /docs localhost:8000
    reverse_proxy /openapi.json localhost:8000

    # 文件大小限制
    request_body /adoru-world/api/upload/* 50MB
}

# 如果有域名，把 :80 替换成 yourdomain.com {
#     这样 Caddy 会自动配 HTTPS
# }
```

#### 启动命令

```bash
# 构建镜像
docker build -t adoruworld:latest .

# 运行（数据持久化）
docker run -d \
    --name adoruworld \
    -p 80:80 \
    -p 443:443 \
    -v adoruworld-data:/app/data \
    -v adoruworld-uploads:/app/uploads \
    -e DATABASE_URL=sqlite+aiosqlite:///data/adoruworld.db \
    -e SITE_START_DATE=2025-01-01 \
    adoruworld:latest

# 导入已有数据
docker cp adoruworld.db adoruworld:/app/data/
docker cp uploads/. adoruworld:/app/uploads/
docker restart adoruworld
```

> **单容器的优点：** 管理简单，迁移时只需要一个镜像 + 一个 volume 文件夹，很适合个人博客。

---

## 5. 开发模式：用 Docker 跑后端，本地跑前端

开发时让后端在 Docker 里跑，前端用 Vite 本地开发（带热更新）。这样：
- 本机不用装 Python 3.11 和一堆依赖
- 后端环境与生产一致
- 前端热更新不受影响

#### `docker-compose.dev.yml`

```yaml
version: "3.9"

services:
  backend:
    build:
      context: ./server
      dockerfile: Dockerfile
    container_name: adoruworld-backend-dev
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=sqlite+aiosqlite:///data/adoruworld.db
      - SITE_START_DATE=2025-01-01
    volumes:
      # 开发模式：挂载源码实现热更新
      - ./server/app:/app/app
      - ./server/scripts:/app/scripts
      - ./server/manage.py:/app/manage.py
      - adoruworld-dev-data:/data
      - adoruworld-dev-uploads:/app/uploads
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

volumes:
  adoruworld-dev-data:
  adoruworld-dev-uploads:
```

#### 使用方式

```bash
# 启动后端容器
docker compose -f docker-compose.dev.yml up -d

# 本地启动前端（带热更新）
cd client
npm run dev

# 前端 → localhost:5173
# Vite proxy 自动把 /api/v1 → localhost:8000（后端容器）
```

> **注意**：`--reload` 模式下文件改动会自动重启 uvicorn，配合 volume 挂载，本机改代码容器里立刻生效。

#### 调试数据库

```bash
# 进容器看数据库
docker exec -it adoruworld-backend-dev python
>>> from app.core.database import async_session
>>> from app.modules.post.model import Post
>>>
# 或者挂个 sqlite3 客户端
docker exec -it adoruworld-backend-dev sqlite3 /data/adoruworld.db
sqlite> SELECT title FROM posts LIMIT 5;
```

---

## 6. 数据持久化与备份

### 6.1 Volume 结构

```
adoruworld-data (volume)     → 容器内 /data/
  └── adoruworld.db          ← SQLite 数据库

adoruworld-uploads (volume)  → 容器内 /app/uploads/
  ├── media/image/
  └── media/audio/
```

### 6.2 备份与恢复

**备份脚本 `scripts/backup.sh`：**

```bash
#!/bin/bash
# 备份 AdoruWorld 数据到指定目录
# 用法: ./scripts/backup.sh /path/to/backup/dir

BACKUP_DIR="${1:-./backup}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
mkdir -p "$BACKUP_DIR/$TIMESTAMP"

echo "📦 备份数据库..."
docker run --rm -v adoruworld-data:/data -v "$BACKUP_DIR/$TIMESTAMP":/backup alpine \
    cp /data/adoruworld.db /backup/

echo "📦 备份上传文件..."
docker run --rm -v adoruworld-uploads:/uploads -v "$BACKUP_DIR/$TIMESTAMP":/backup alpine \
    cp -r /uploads /backup/

echo "✅ 备份完成：$BACKUP_DIR/$TIMESTAMP"
```

**恢复脚本 `scripts/restore.sh`：**

```bash
#!/bin/bash
# 用法: ./scripts/restore.sh /path/to/backup/folder
BACKUP_PATH="${1}"
if [ -z "$BACKUP_PATH" ]; then
    echo "❌ 请指定备份路径"
    exit 1
fi

echo "🔄 恢复数据库..."
docker run --rm -v adoruworld-data:/data -v "$BACKUP_PATH":/backup alpine \
    cp /backup/adoruworld.db /data/
echo "🔄 恢复上传文件..."
docker run --rm -v adoruworld-uploads:/uploads -v "$BACKUP_PATH":/backup alpine \
    cp -r /backup/uploads/. /uploads/
echo "✅ 恢复完成，请重启容器：docker compose restart"
```

### 6.3 定时备份（宿主机 crontab）

```bash
# 每天凌晨 3 点备份，保留最近 7 天
0 3 * * * /home/adorukw/AAAPAN/Project/AdoruWorld/scripts/backup.sh /home/adorukw/backups/adoruworld && find /home/adorukw/backups/adoruworld -type d -mtime +7 -exec rm -rf {} +
```

---

## 7. 部署 Checklist

首次部署按这个顺序检查：

- [ ] **Docker 已安装**
  ```bash
  docker --version && docker compose version
  ```
- [ ] **配置文件就绪**
  - `server/Dockerfile` 存在
  - `client/Dockerfile` 存在
  - `client/nginx.conf` 存在
  - `docker-compose.yml` 存在
- [ ] **环境变量确认**
  - `DATABASE_URL` 指向 volume 路径（不是容器内的相对路径）
  - `SITE_START_DATE` 正确
- [ ] **数据迁移**
  - 数据库文件已复制到 volume
  - uploads 目录已复制到 volume
- [ ] **端口未冲突**
  - 宿主机 80 端口没有被其他程序占用
- [ ] **防火墙放行**
  ```bash
  sudo ufw allow 80/tcp
  sudo ufw allow 443/tcp   # 如果有 HTTPS
  ```
- [ ] **启动验证**
  ```bash
  docker compose up -d
  docker compose ps                    # 两个容器都是 Up 状态
  curl http://localhost/api/v1/posts   # API 响应正常
  curl http://localhost/adoru-world/   # 前端 HTML 返回正常
  ```
- [ ] **日志无错误**
  ```bash
  docker compose logs backend | grep ERROR
  docker compose logs nginx | grep error
  ```

---

## 附：项目文件清单（Docker 相关）

```
AdoruWorld/
├── docker-compose.yml          ← 双容器编排（方案一）
├── docker-compose.dev.yml      ← 开发模式（方案二）
├── Dockerfile                  ← 单容器全栈（可选）
├── Caddyfile                   ← 单容器用的 Web 服务器配置
├── server/
│   ├── Dockerfile              ← 后端镜像
│   └── ...
├── client/
│   ├── Dockerfile              ← 前端构建 + Nginx 镜像
│   ├── nginx.conf              ← Nginx 配置
│   └── ...
└── scripts/
    ├── backup.sh               ← 数据备份脚本
    └── restore.sh              ← 数据恢复脚本
```

---

> **一句话总结：** 这个项目用 Docker 很简单，因为它用的是 SQLite（不需要单独的数据库容器）。一个后端容器 + 一个 Nginx 容器就能跑起来，数据用 volume 持久化。开发时还可以只容器化后端，前端继续用 Vite 热更新，两不耽误。ふふっ
