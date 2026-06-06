import type { PostCategoryResponse } from './post-category'
import type { PostTagResponse } from './post-tag'

export interface PostResponse {
    id: string
    slug: string
    title: string
    description?: string
    content: string
    coverImage?: string
    createdAt: string
    updatedAt: string
    published: boolean
    featured: boolean
    category: PostCategoryResponse
    tags: PostTagResponse[]
    readingTime: number
    wordCount: number
    views: number
}

export interface PostListItem {
    id: string
    slug: string
    title: string
    description?: string
    content: string
    coverImage?: string
    createdAt: string
    published: boolean
    featured: boolean
    category: PostCategoryResponse
    tags: PostTagResponse[]
    readingTime: number
    wordCount: number
    views: number
}

export interface ArchiveItem {
    year: number
    month: number
    posts: PostListItem[]
}

export interface PostCreate {
    title: string
    slug: string
    description?: string
    content: string
    coverImage?: string
    published?: boolean
    featured?: boolean
    categoryId: string
    tagIds: string[]
}

export interface PostUpdate {
    title?: string
    slug?: string
    description?: string
    content?: string
    coverImage?: string
    published?: boolean
    featured?: boolean
    categoryId?: string
    tagIds?: string[]
}