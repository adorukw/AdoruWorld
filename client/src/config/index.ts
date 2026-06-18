export * from './post-form.ts'
export * from './post-category-form.ts'
export * from './post-tag-form.ts'
export * from './dex-form.ts'
export * from './dex-genre-form.ts'
export * from './media-form.ts'
export * from './media-tag-form.ts'

export const BASE_API_URL = import.meta.env.DEV
  ? '/api/v1'              // 开发模式 → Vite proxy
  : '/adoru-world/api/v1'; // 生产模式 → nginx
console.log("DEVELOPMENT MODE:", import.meta.env.DEV)
console.log("BASE_API_URL:", BASE_API_URL)