export type DexGenreResponse = {
    id: string,
    name: string,
    slug: string,
    color?: string
}

export type DexGenreCreate = {
    name: string,
    slug: string,
    color?: string
}

export type DexGenreUpdate = {
    name?: string,
    slug?: string,
    color?: string
}