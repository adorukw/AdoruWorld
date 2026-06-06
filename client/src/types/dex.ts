import type { DexGenreResponse } from './dex-genre'

export type DexCategory = 'anime' | 'movie' | 'tv' | 'game' | 'book' | 'music' | 'other'

export type DexStatus = 'completed' | 'watching' | 'playing' | 'reading' | 'listening' | 'doing' | 'dropped' | 'planned'

export interface DexCategoryInfo {
    id: DexCategory,
    name: string,
    slug: string,
    icon: string,
    color: string,
    bgColor: string
}

export interface DexStatusInfo {
    id: DexStatus,
    name: string,
    slug: string,
    icon: string,
    color: string
}

export interface DexEntryResponse {
    id: string,
    slug: string,
    title: string,
    originalTitle?: string,
    coverImage: string,
    category: DexCategory,
    status: DexStatus,
    rating: number,
    startDate?: string,
    finishDate?: string,
    comment?: string,
    summary?: string,
    creator?: string,
    year?: number,
    genres?: DexGenreResponse[]
}

export interface DexEntryCreate {
    slug: string,
    title: string,
    originalTitle?: string,
    coverImage: string,
    category: DexCategory,
    status: DexStatus,
    rating: number,
    startDate?: string,
    finishDate?: string,
    comment?: string,
    summary?: string,
    creator?: string,
    year?: number,
    genreIds?: string[]
}

export interface DexEntryUpdate {
    slug?: string,
    title?: string,
    originalTitle?: string,
    coverImage?: string,
    category?: DexCategory,
    status?: DexStatus,
    rating?: number,
    startDate?: string,
    finishDate?: string,
    comment?: string,
    summary?: string,
    creator?: string,
    year?: number,
    genreIds?: string[]
}

export interface DexStats {
    total: number
    byCategory: Record<string, number>
    byStatus: Record<string, number>
    averageRating: number
}