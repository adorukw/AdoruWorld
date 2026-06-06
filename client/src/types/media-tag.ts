export type MediaTagResponse = {
    id: string,
    name: string,
    slug: string,
    color?: string
}

export type MediaTagCreate = {
    name?: string,
    slug?: string,
    color?: string
}

export type MediaTagUpdate = {
    name?: string,
    slug?: string,
    color?: string
}