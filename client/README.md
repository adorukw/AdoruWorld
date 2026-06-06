# Vue 3 + TypeScript + Vite

This template should help get you started developing with Vue 3 and TypeScript in Vite. The template uses Vue 3 `<script setup>` SFCs, check out the [script setup docs](https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup) to learn more.

Learn more about the recommended Project Setup and IDE Support in the [Vue Docs TypeScript Guide](https://vuejs.org/guide/typescript/overview.html#project-setup).

---

## 开发记录

### 1. 初始化项目
1. 创建前端框架
```bash
npm create vite@latest AdoruWorld --template vue-ts
```
2. 安装依赖
```bash
# 核心依赖
npm install vue-router pinia marked highlight.js

# Tailwind CSS v4（注意 v4 的安装方式与 v3 不同）
npm install tailwindcss @tailwindcss/vite

# 开发依赖
npm install -D @types/node
```

3. 修改`vite.config.ts`文件，添加以下内容：
```typescript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'
import { fileURLToPath, URL } from 'node:url'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue(),tailwindcss()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:3002',
        changeOrigin: true
      },
      '/uploads': {
        target: 'http://localhost:3002',
        changeOrigin: true
      }
    }
  }
})
```

4. 配置tailwindcss
在 `src/style.css` 顶部引入 Tailwind：
```css
@import "tailwindcss";
```

5. 配置入口html
在 `index.html` 的 `<head>` 中引入像素字体：
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&family=ZCOOL+KuaiLe&display=swap" rel="stylesheet">
```

6. 创建后端框架
```bash
mkdir server
cd server
npm init -y
```
修改 `server/package.json` 中的关键字段：
```json
{
  "type": "commonjs",
  "scripts": {
    "dev": "tsx watch src/index.ts",
    "build": "tsc",
    "start": "node dist/index.js",
    "db:migrate": "npx prisma migrate dev",
    "db:seed": "tsx prisma/seed.ts",
    "db:studio": "npx prisma studio",
    "db:generate": "npx prisma generate"
  }
}
```

7. 安装后端依赖
```bash
cd server

# 核心依赖
npm install express @prisma/client prisma cors multer marked uuid

# 开发依赖
npm install -D typescript tsx @types/express @types/cors @types/multer @types/uuid
```

8. 初始化Prisma + SQLite
```bash
cd server

# 初始化 Prisma（使用 SQLite）
npx prisma init --datasource-provider sqlite
# 写好prisma之后
cd server

# 生成 Prisma Client
npx prisma generate

# 创建数据库并运行迁移
npx prisma migrate dev --name init

# 插入种子数据
tsx prisma/seed.ts
```