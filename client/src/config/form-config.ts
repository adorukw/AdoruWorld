import type {
    PostCreate, PostUpdate, PostCategoryCreate,
    PostCategoryUpdate, PostTagCreate, PostTagUpdate,
    DexEntryCreate, DexEntryUpdate, DexGenreCreate, DexGenreUpdate,
    MediaTagCreate, MediaTagUpdate, MediaCreate, MediaUpdate,
} from '@/types'
import {
    usePostStore, usePostCategoryStore, usePostTagStore, useDexStore, useDexGenreStore,
    useMediaTagStore, useMediaStore
} from '@/store'
import { dexCategories, dexStatuses} from '@/constants'

export interface FormField {
    key: string
    label: string
    type: 'text' | 'textarea' | 'select' | 'multiSelect' | 'switch' | 'number' | 'file'|'mediaPicker'
    required?: boolean
    rows?: number
    optionsGetter?: () => Promise<{ label: string; value: any }[]>
    placeholder?: string
    uploadApi?: (file: File) => Promise<any>
    accept?: string
}

export interface FormConfig<TData> {
    fields: FormField[]
    saveApi: (data: TData, id?: string) => Promise<any>
}

export const postCreateConfig: FormConfig<PostCreate> = {
    fields: [
        {
            key: 'title',
            label: '文章标题',
            type: 'text',
            required: true,
            placeholder: '请输入文章标题'
        },
        {
            key: 'slug',
            label: '文章别名',
            type: 'text',
            required: true,
            placeholder: '请输入文章别名'
        },
        {
            key: 'description',
            label: '文章描述',
            type: 'textarea',
            required: false,
            rows: 3,
            placeholder: '请输入文章描述'
        },
        {
            key: 'content',
            label: '文章内容',
            type: 'textarea',
            required: true,
            rows: 15,
            placeholder: '请输入文章内容'
        },
        {
            key: 'coverImage',
            label: '封面图片',
            type: 'mediaPicker',
            required: false,
        },
        {
            key: 'published',
            label: '立即发布',
            required: false,
            type: 'switch'
        },
        {
            key: 'categoryId',
            label: '分类',
            type: 'select',
            required: true,
            optionsGetter: async () => {
                const store = usePostCategoryStore()
                await store.getPostCategories?.()
                return store.postCategories.map(c => ({
                    label: c.name,
                    value: c.id
                }))
            }
        },
        {
            key: 'tagIds',
            label: '标签',
            type: 'multiSelect',
            required: true,
            optionsGetter: async () => {
                const store = usePostTagStore()
                await store.getPostTags?.()
                return store.postTags.map(t => ({
                    label: t.name,
                    value: t.id
                }))
            }
        }
    ],

    saveApi: (data) => usePostStore().createPost(data)
}

export const postUpdateConfig: FormConfig<PostUpdate> = {
    fields: [
        {
            key: 'title',
            label: '文章标题',
            type: 'text',
            required: false,
            placeholder: '请输入文章标题'
        },
        {
            key: 'slug',
            label: '文章别名',
            type: 'text',
            required: false,
            placeholder: '请输入文章别名'
        },
        {
            key: 'description',
            label: '文章描述',
            type: 'textarea',
            required: false,
            rows: 3,
            placeholder: '请输入文章描述'
        },
        {
            key: 'content',
            label: '文章内容',
            type: 'textarea',
            required: false,
            rows: 15,
            placeholder: '请输入文章内容'
        },
        {
            key: 'coverImage',
            label: '封面图片',
            type: 'mediaPicker',
            required: false,
        },
        {
            key: 'published',
            label: '立即发布',
            required: false,
            type: 'switch'
        },
        {
            key: 'categoryId',
            label: '分类',
            type: 'select',
            required: false,
            optionsGetter: async () => {
                const store = usePostCategoryStore()
                await store.getPostCategories?.()
                return store.postCategories.map(c => ({
                    label: c.name,
                    value: c.id
                }))
            }
        },
        {
            key: 'tagIds',
            label: '标签',
            type: 'multiSelect',
            required: false,
            optionsGetter: async () => {
                const store = usePostTagStore()
                await store.getPostTags?.()
                return store.postTags.map(t => ({
                    label: t.name,
                    value: t.id
                }))
            }
        }
    ],
    saveApi: (data, id) => usePostStore().updatePost(id!, data)
}

export const postCategoryCreateConfig: FormConfig<PostCategoryCreate> = {
    fields: [
        {
            key: 'name',
            label: '分类名称',
            type: 'text',
            required: true,
            placeholder: '请输入分类名称'
        },
        {
            key: 'slug',
            label: '分类别名',
            type: 'text',
            required: true,
            placeholder: '请输入分类别名'
        },
        {
            key: 'description',
            label: '分类描述',
            type: 'textarea',
            required: false,
            rows: 3,
            placeholder: '请输入分类描述'
        },
        {
            key: 'icon',
            label: '分类图标',
            type: 'text',
            required: false,
            placeholder: '请输入分类图标URL'
        },
        {
            key: 'color',
            label: '分类颜色',
            type: 'text',
            required: false,
            placeholder: '请输入分类颜色'
        }
    ],
    saveApi: (data) => usePostCategoryStore().createPostCategory(data)
}

export const postCategoryUpdateConfig: FormConfig<PostCategoryUpdate> = {
    fields: [
        {
            key: 'name',
            label: '分类名称',
            type: 'text',
            required: false,
            placeholder: '请输入分类名称'
        },
        {
            key: 'slug',
            label: '分类别名',
            type: 'text',
            required: false,
            placeholder: '请输入分类别名'
        },
        {
            key: 'description',
            label: '分类描述',
            type: 'textarea',
            required: false,
            rows: 3,
            placeholder: '请输入分类描述'
        },
        {
            key: 'icon',
            label: '分类图标',
            type: 'text',
            required: false,
            placeholder: '请输入分类图标URL'
        },
        {
            key: 'color',
            label: '分类颜色',
            type: 'text',
            required: false,
            placeholder: '请输入分类颜色'
        }
    ],
    saveApi: (data, id) => usePostCategoryStore().updatePostCategory(id!, data)
}

export const postTagCreateConfig: FormConfig<PostTagCreate> = {
    fields: [
        {
            key: 'name',
            label: '标签名称',
            type: 'text',
            required: true,
            placeholder: '请输入标签名称'
        },
        {
            key: 'slug',
            label: '标签别名',
            type: 'text',
            required: true,
            placeholder: '请输入标签别名'
        },
        {
            key: 'color',
            label: '标签颜色',
            type: 'text',
            required: false,
            placeholder: '请输入标签颜色'
        }
    ],
    saveApi: (data) => usePostTagStore().createPostTag(data)
}

export const postTagUpdateConfig: FormConfig<PostTagUpdate> = {
    fields: [
        {
            key: 'name',
            label: '标签名称',
            type: 'text',
            required: false,
            placeholder: '请输入标签名称'
        },
        {
            key: 'slug',
            label: '标签别名',
            type: 'text',
            required: false,
            placeholder: '请输入标签别名'
        },
        {
            key: 'color',
            label: '标签颜色',
            type: 'text',
            required: false,
            placeholder: '请输入标签颜色'
        }
    ],
    saveApi: (data, id) => usePostTagStore().updatePostTag(id!, data)
}

export const dexEntryCreateConfig: FormConfig<DexEntryCreate> = {
    fields: [
        {
            key: 'slug',
            label: '作品别名',
            type: 'text',
            required: true,
            placeholder: '请输入作品别名'
        },
        {
            key: 'title',
            label: '作品名称',
            type: 'text',
            required: true,
            placeholder: '请输入作品名称'
        },
        {
            key: 'originalTitle',
            label: '作品原名',
            type: 'text',
            required: false,
            placeholder: '请输入作品原名'
        },
        {
            key: 'coverImage',
            label: '封面图片',
            type: 'mediaPicker',
            required: true,
        },
        {
            key: 'category',
            label: '作品类型',
            type: 'select',
            required: true,
            optionsGetter: async () => {
                return dexCategories.map(c => ({
                    label: c.name,
                    value: c.id
                }))
            },
        },
        {
            key: 'status',
            label: '作品状态',
            type: 'select',
            required: true,
            optionsGetter: async () => {
                return dexStatuses.map(s => ({
                    label: s.name,
                    value: s.id
                }))
            },
        },
        {
            key: 'rating',
            label: '作品评分',
            type: 'number',
            required: true,
            placeholder: '请输入作品评分'
        },
        {
            key: 'startDate',
            label: '开始日期',
            type: 'text',
            required: false,
            placeholder: '请输入开始日期'
        },
        {
            key: 'finishDate',
            label: '结束日期',
            type: 'text',
            required: false,
            placeholder: '请输入结束日期'
        },
        {
            key: 'comment',
            label: '作品评论',
            type: 'textarea',
            required: false,
            rows: 3,
            placeholder: '请输入作品评论'
        },
        {
            key: 'summary',
            label: '作品简介',
            type: 'textarea',
            required: false,
            rows: 10,
            placeholder: '请输入作品简介'
        },
        {
            key: 'creator',
            label: '作品创作者',
            type: 'text',
            required: false,
            placeholder: '请输入作品创作者'
        },
        {
            key: 'year',
            label: '作品年份',
            type: 'number',
            required: false,
            placeholder: '请输入作品年份'
        },
        {
            key: 'genreIds',
            label: '作品类型',
            type: 'multiSelect',
            required: false,
            optionsGetter: async () => {
                const store = useDexGenreStore()
                await store.getDexGenres?.()
                return store.dexGenres.map(g => ({
                    label: g.name,
                    value: g.id
                }))
            },
        }
    ],
    saveApi: (data) => useDexStore().createDexEntry(data)
}

export const dexEntryUpdateConfig: FormConfig<DexEntryUpdate> = {
    fields: [
        {
            key: 'slug',
            label: '作品别名',
            type: 'text',
            required: false,
            placeholder: '请输入作品别名'
        },
        {
            key: 'title',
            label: '作品名称',
            type: 'text',
            required: false,
            placeholder: '请输入作品名称'
        },
        {
            key: 'originalTitle',
            label: '作品原名',
            type: 'text',
            required: false,
            placeholder: '请输入作品原名'
        },
        {
            key: 'coverImage',
            label: '封面图片',
            type: 'mediaPicker',
            required: false,
        },
        {
            key: 'category',
            label: '作品类型',
            type: 'select',
            required: false,
            optionsGetter: async () => {
                return dexCategories.map(c => ({
                    label: c.name,
                    value: c.id
                }))
            },
        },
        {
            key: 'status',
            label: '作品状态',
            type: 'select',
            required: false,
            optionsGetter: async () => {
                return dexStatuses.map(s => ({
                    label: s.name,
                    value: s.id
                }))
            },
        },
        {
            key: 'rating',
            label: '作品评分',
            type: 'number',
            required: false,
            placeholder: '请输入作品评分'
        },
        {
            key: 'startDate',
            label: '开始日期',
            type: 'text',
            required: false,
            placeholder: '请输入开始日期'
        },
        {
            key: 'finishDate',
            label: '结束日期',
            type: 'text',
            required: false,
            placeholder: '请输入结束日期'
        },
        {
            key: 'comment',
            label: '作品评论',
            type: 'textarea',
            required: false,
            rows: 3,
            placeholder: '请输入作品评论'
        },
        {
            key: 'summary',
            label: '作品简介',
            type: 'textarea',
            required: false,
            rows: 10,
            placeholder: '请输入作品简介'
        },
        {
            key: 'creator',
            label: '作品创作者',
            type: 'text',
            required: false,
            placeholder: '请输入作品创作者'
        },
        {
            key: 'year',
            label: '作品年份',
            type: 'number',
            required: false,
            placeholder: '请输入作品年份'
        },
        {
            key: 'genreIds',
            label: '作品类型',
            type: 'multiSelect',
            required: false,
            optionsGetter: async () => {
                const store = useDexGenreStore()
                await store.getDexGenres?.()
                return store.dexGenres.map(g => ({
                    label: g.name,
                    value: g.id
                }))
            },
        }
    ],
    saveApi: (data, id) => useDexStore().updateDexEntry(id!, data)
}

export const dexGenreCreateConfig: FormConfig<DexGenreCreate> = {
    fields: [
        {
            key: 'name',
            label: '题材名称',
            type: 'text',
            required: true,
            placeholder: '请输入题材名称'
        },
        {
            key: 'slug',
            label: '题材别名',
            type: 'text',
            required: true,
            placeholder: '请输入题材别名'
        },
        {
            key: 'color',
            label: '题材颜色',
            type: 'text',
            required: false,
            placeholder: '请输入题材颜色'
        }
    ],
    saveApi: (data) => useDexGenreStore().createDexGenre(data)
}

export const dexGenreUpdateConfig: FormConfig<DexGenreUpdate> = {
    fields: [
        {
            key: 'name',
            label: '题材名称',
            type: 'text',
            required: false,
            placeholder: '请输入题材名称'
        },
        {
            key: 'slug',
            label: '题材别名',
            type: 'text',
            required: false,
            placeholder: '请输入题材别名'
        },
        {
            key: 'color',
            label: '题材颜色',
            type: 'text',
            required: false,
            placeholder: '请输入题材颜色'
        }
    ],
    saveApi: (data, id) => useDexGenreStore().updateDexGenre(id!, data)
}

export const mediaTagCreateConfig: FormConfig<MediaTagCreate> = {
    fields: [
        {
            key: 'name',
            label: '标签名称',
            type: 'text',
            required: true,
            placeholder: '请输入标签名称'
        },
        {
            key: 'slug',
            label: '标签别名',
            type: 'text',
            required: true,
            placeholder: '请输入标签别名'
        },
        {
            key: 'color',
            label: '标签颜色',
            type: 'text',
            required: false,
            placeholder: '请输入标签颜色'
        }
    ],
    saveApi: (data) => useMediaTagStore().createMediaTag(data)
}

export const mediaTagUpdateConfig: FormConfig<MediaTagUpdate> = {
    fields: [
        {
            key: 'name',
            label: '标签名称',
            type: 'text',
            required: false,
            placeholder: '请输入标签名称'
        },
        {
            key: 'slug',
            label: '标签别名',
            type: 'text',
            required: false,
            placeholder: '请输入标签别名'
        },
        {
            key: 'color',
            label: '标签颜色',
            type: 'text',
            required: false,
            placeholder: '请输入标签颜色'
        }
    ],
    saveApi: (data, id) => useMediaTagStore().updateMediaTag(id!, data)
}

export const mediaCreateConfig: FormConfig<MediaCreate> = {
    fields: [
        {
            key: 'title',
            label: '媒体标题',
            type: 'text',
            required: true,
            placeholder: '请输入媒体标题'
        },
        {
            key: 'slug',
            label: '媒体别名',
            type: 'text',
            required: true,
            placeholder: '请输入媒体别名'
        },
        {
            key: 'file',
            label: '上传文件',
            type: 'file',
            required: true,
            accept: '.jpg,.jpeg,.png,.gif,.webp,.mp3,.wav,.flac,.pdf,.epub,.mobi',
            uploadApi: async (file: File) => {
                const store = useMediaStore()
                return await store.uploadMedia(file)
            }
        },
        {
            key: 'tagIds',
            label: '标签',
            type: 'multiSelect',
            required: false,
            optionsGetter: async () => {
                const store = useMediaTagStore()
                await store.getMediaTags?.()
                return store.mediaTags.map(t => ({
                    label: t.name,
                    value: t.id
                }))
            }
        }
    ],
    saveApi: async (data: MediaCreate) => {
        const store = useMediaStore()
        if (!data.filePath) {
            throw new Error('请先上传文件')
        }
        const mediaData: MediaCreate = {
            slug: data.slug,
            title: data.title,
            filePath: data.filePath,
            fileSize: data.fileSize,
            mimeType: data.mimeType,
            mediaType: data.mediaType,  // 自动填充，不需要用户选择
            metaData: data.metaData || {},  // 自动分析，不需要用户填写
            tagIds: data.tagIds || []
        }

        return await store.createMedia(mediaData)

    }
}

// 媒体更新配置
export const mediaUpdateConfig: FormConfig<MediaUpdate> = {
    fields: [
        {
            key: 'title',
            label: '媒体标题',
            type: 'text',
            required: false,
            placeholder: '请输入媒体标题'
        },
        {
            key: 'slug',
            label: '媒体别名',
            type: 'text',
            required: false,
            placeholder: '请输入媒体别名'
        },
        {
            key: 'tagIds',
            label: '标签',
            type: 'multiSelect',
            required: false,
            optionsGetter: async () => {
                const store = useMediaTagStore()
                await store.getMediaTags?.()
                return store.mediaTags.map(t => ({
                    label: t.name,
                    value: t.id
                }))
            }
        }
    ],
    saveApi: (data, id) => useMediaStore().updateMedia(id!, data)
}