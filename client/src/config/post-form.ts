import type { PostCreate, PostUpdate } from '@/types'
import { usePostStore, usePostCategoryStore, usePostTagStore } from '@/store'
import type { FormConfig } from '@/types'

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
            key: 'featured',
            label: '精选',
            required: false,
            type: 'switch'
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
            key: 'featured',
            label: '精选',
            required: false,
            type: 'switch'
        },
        {
            key: 'published',
            label: '立即发布',
            required: true,
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
    saveApi: (data, id) => usePostStore().updatePost(id!, data)
}