import type { DexCreate, DexUpdate } from '@/types'
import { useDexStore, useDexGenreStore, useMediaStore } from '@/store'
import { dexCategories, dexStatuses } from '@/constants'
import type { FormConfig } from '@/types'
export const dexCreateConfig: FormConfig<DexCreate> = {
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
            key: 'externalUrl',
            label: '外部链接',
            type: 'text',
            required: false,
            placeholder: '豆瓣/官网/购买页/网易云等链接'
        },
        {
            key: 'genreIds',
            label: '作品类型',
            type: 'multiSelect',
            required: true,
            optionsGetter: async () => {
                const store = useDexGenreStore()
                await store.getDexGenres?.()
                return store.dexGenres.map(g => ({
                    label: g.name,
                    value: g.id
                }))
            },
        },
        {
            key: 'mediaIds',
            label: '关联资源',
            type: 'multiSelect',
            required: false,
            optionsGetter: async () => {
                const store = useMediaStore()
                await store.getMedias?.()
                return store.medias.map(m => ({
                    label: `[${m.mediaType}] ${m.title}`,
                    value: m.id
                }))
            },
        }
    ],
    saveApi: (data) => useDexStore().createDex(data)
}

export const dexUpdateConfig: FormConfig<DexUpdate> = {
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
            key: 'externalUrl',
            label: '外部链接',
            type: 'text',
            required: false,
            placeholder: '豆瓣/官网/购买页/网易云等链接'
        },
        {
            key: 'genreIds',
            label: '作品类型',
            type: 'multiSelect',
            required: true,
            optionsGetter: async () => {
                const store = useDexGenreStore()
                await store.getDexGenres?.()
                return store.dexGenres.map(g => ({
                    label: g.name,
                    value: g.id
                }))
            },
        },
        {
            key: 'mediaIds',
            label: '关联资源',
            type: 'multiSelect',
            required: false,
            optionsGetter: async () => {
                const store = useMediaStore()
                await store.getMedias?.()
                return store.medias.map(m => ({
                    label: `[${m.mediaType}] ${m.title}`,
                    value: m.id
                }))
            },
        }
    ],
    saveApi: (data, id) => useDexStore().updateDex(id!, data)
}
