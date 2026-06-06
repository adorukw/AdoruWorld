export interface PostTagResponse {
    id: string
    name: string
    slug: string
    color?: string
    count: number
}

export interface PostTagCreate {
    name: string
    slug: string
    color?: string
}

export interface PostTagUpdate {
    name?: string
    slug?: string
    color?: string
}