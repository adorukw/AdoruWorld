import type { MediaTagResponse } from './media-tag'

export type MediaType = 'image' | 'audio' | 'book' | 'video'

export interface MediaTypeInfo {
    id: string,
    name: string,
    slug: string,
    icon: string,
    color: string
}

export interface MediaCreate {
    slug: string,
    title: string,
    filePath: string,
    fileSize: number,
    mimeType: string,
    mediaType: MediaType,
    metaData?: Record<string, any>,
    tagIds?: string[]
}

export interface MediaUpdate {
    title?: string,
    metaData?: Record<string, any>,
    tagIds?: string[]
}

export interface MediaResponse {
    id: string
    slug: string
    title: string
    filePath: string    
    fileSize: number
    mediaType: MediaType
    mimeType: string
    extension: string
    metaData: Record<string, any>
    uploadedAt: string
    tags: MediaTagResponse[]
}

export interface MediaUploadResponse {
    filePath: string
    fileSize: number
    mimeType: string
    extension: string
    mediaType: MediaType
}