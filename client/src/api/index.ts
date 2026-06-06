import { request } from '@/utils'
import type {
  PostCategoryResponse, PostCategoryCreate, PostCategoryUpdate,
  PostTagResponse, PostTagCreate, PostTagUpdate,
  PostResponse, PostListItem, ArchiveItem, PostCreate, PostUpdate,
  DexEntryResponse, DexEntryCreate, DexEntryUpdate, DexStats,
  DexGenreResponse, DexGenreCreate, DexGenreUpdate,
  MediaTagResponse, MediaTagCreate, MediaTagUpdate,
  MediaResponse, MediaCreate, MediaUpdate, MediaUploadResponse
} from '@/types'

export const api = {
  system: {
    systemInfo: () => request<any>('/system/info'),
  },
  postCategories: {
    // 获取所有分类
    list: () => request<PostCategoryResponse[]>('/post_categories'),

    // 根据 slug 获取分类
    getBySlug: (slug: string) => request<PostCategoryResponse>(`/post_categories/slug/${slug}`),

    // 根据 ID 获取分类
    getById: (id: string) => request<PostCategoryResponse>(`/post_categories/${id}`),

    // 创建分类
    create: (data: PostCategoryCreate) => request<PostCategoryResponse>('/post_categories', {
      method: 'POST',
      body: JSON.stringify(data)
    }),

    // 更新分类
    update: (id: string, data: PostCategoryUpdate) => request<PostCategoryResponse>(`/post_categories/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data)
    }),

    // 删除分类
    delete: (id: string) => request<void>(`/post_categories/${id}`, {
      method: 'DELETE'
    })
  },
  postTags: {
    list: () => request<PostTagResponse[]>('/post_tags'),
    getBySlug: (slug: string) => request<PostTagResponse>(`/post_tags/slug/${slug}`),
    getById: (id: string) => request<PostTagResponse>(`/post_tags/${id}`),
    create: (data: PostTagCreate) => request<PostTagResponse>('/post_tags', {
      method: 'POST',
      body: JSON.stringify(data)
    }),
    update: (id: string, data: PostTagUpdate) => request<PostTagResponse>(`/post_tags/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data)
    }),
    delete: (id: string) => request<void>(`/post_tags/${id}`, {
      method: 'DELETE'
    })
  },
  posts: {
    // 获取文章列表
    list: (params?: {
      published?: boolean
      featured?: boolean
      category?: string
      tag?: string
      skip?: number
      limit?: number
    }) => {
      const query = params ? '?' + new URLSearchParams(params as Record<string, string>).toString() : ''
      return request<PostListItem[]>(`/posts${query}`)
    },

    // 获取归档
    archives: () => request<ArchiveItem[]>('/posts/archives'),

    // 根据 slug 获取文章
    getBySlug: (slug: string) => request<PostResponse>(`/posts/slug/${slug}`),

    // 根据 ID 获取文章
    getById: (id: string) => request<PostResponse>(`/posts/${id}`),

    // 创建文章
    create: (data: PostCreate) => request<PostResponse>('/posts', {
      method: 'POST',
      body: JSON.stringify(data)
    }),

    // 更新文章
    update: (id: string, data: PostUpdate) => request<PostResponse>(`/posts/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data)
    }),

    // 删除文章
    delete: (id: string) => request<void>(`/posts/${id}`, {
      method: 'DELETE'
    }),
    incrementViews: (id: string) => request<void>(`/posts/increment-views/${id}`, {
      method: 'POST',
    }),
    totalPostsCount: () => request<number>(`/posts/total-posts-count`),
    totalWords: () => request<number>(`/posts/total-words`),
    totalViews: () => request<number>(`/posts/total-views`),
  },
  dexs: {
    list: (params?: {
      category?: string
      status?: string
      skip?: number
      limit?: number
    }) => {
      const query = params ? '?' + new URLSearchParams(params as Record<string, string>).toString() : ''
      return request<DexEntryResponse[]>(`/dexs${query}`)
    },
    getBySlug: (slug: string) => request<DexEntryResponse>(`/dexs/slug/${slug}`),
    getById: (id: string) => request<DexEntryResponse>(`/dexs/${id}`),
    create: (data: DexEntryCreate) => request<DexEntryResponse>('/dexs', {
      method: 'POST',
      body: JSON.stringify(data)
    }),
    update: (id: string, data: DexEntryUpdate) => request<DexEntryResponse>(`/dexs/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data)
    }),
    delete: (id: string) => request<void>(`/dexs/${id}`, {
      method: 'DELETE'
    }),
    stats: () => request<DexStats>(`/dexs/stats`)
  },
  dexGenres: {
    list: () => request<DexGenreResponse[]>('/dex_genres'),
    getBySlug: (slug: string) => request<DexGenreResponse>(`/dex_genres/slug/${slug}`),
    getById: (id: string) => request<DexGenreResponse>(`/dex_genres/${id}`),
    create: (data: DexGenreCreate) => request<DexGenreResponse>('/dex_genres', {
      method: 'POST',
      body: JSON.stringify(data)
    }),
    update: (id: string, data: DexGenreUpdate) => request<DexGenreResponse>(`/dex_genres/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data)
    }),
    delete: (id: string) => request<void>(`/dex_genres/${id}`, {
      method: 'DELETE'
    })
  },
  mediaTags: {
    list: () => request<MediaTagResponse[]>('/media_tags'),
    getBySlug: (slug: string) => request<MediaTagResponse>(`/media_tags/slug/${slug}`),
    getById: (id: string) => request<MediaTagResponse>(`/media_tags/${id}`),
    create: (data: MediaTagCreate) => request<MediaTagResponse>('/media_tags', {
      method: 'POST',
      body: JSON.stringify(data)
    }),
    update: (id: string, data: MediaTagUpdate) => request<MediaTagResponse>(`/media_tags/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data)
    }),
    delete: (id: string) => request<void>(`/media_tags/${id}`, {
      method: 'DELETE'
    })
  },
  media: {
    upload: async (file: File): Promise<MediaUploadResponse> => {
      const formData = new FormData()
      formData.append('file', file)
      return request<MediaUploadResponse>('/medias/upload', {
        method: 'POST',
        body: formData
      })
    },
    // 获取媒体列表
    list: (params?: {
      media_type?: string
      tag_slug?: string
      skip?: number
      limit?: number
    }) => {
      const query = params ? '?' + new URLSearchParams(params as Record<string, string>).toString() : ''
      return request<MediaResponse[]>(`/medias${query}`)
    },

    // 根据 slug 获取媒体
    getBySlug: (slug: string) => request<MediaResponse>(`/medias/slug/${slug}`),

    // 根据 ID 获取媒体
    getById: (id: string) => request<MediaResponse>(`/medias/${id}`),

    // 创建媒体记录
    create: (data: MediaCreate) => request<MediaResponse>('/medias', {
      method: 'POST',
      body: JSON.stringify(data)
    }),

    // 更新媒体记录
    update: (id: string, data: MediaUpdate) => request<MediaResponse>(`/medias/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data)
    }),

    // 删除媒体记录
    delete: (id: string) => request<void>(`/medias/${id}`, {
      method: 'DELETE'
    })
  }
}
