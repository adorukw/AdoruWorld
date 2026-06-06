export interface PostCategoryResponse {
    id: string
    name: string
    slug: string
    description?: string
    count: number
    icon?: string
    color?: string
}

export interface PostCategoryCreate {
    name: string
    slug: string
    description?: string
    icon?: string
    color?: string
}

export interface PostCategoryUpdate {
    name?: string
    slug?: string
    description?: string
    icon?: string
    color?: string
}