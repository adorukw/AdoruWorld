import type { SeriesCreate, SeriesUpdate } from '@/types'
import { useSeriesStore } from '@/store'

import type { FormConfig } from '@/types'

export const seriesCreateConfig: FormConfig<SeriesCreate> = {
    fields: [
        {
            key: 'name',
            label: '系列名称',
            type: 'text',
            required: true,
            placeholder: '如：EVA 深度解析系列'
        },
        {
            key: 'slug',
            label: '系列别名',
            type: 'text',
            required: true,
            placeholder: '请输入系列别名'
        },
        {
            key: 'description',
            label: '系列描述',
            type: 'textarea',
            required: false,
            rows: 3,
            placeholder: '请输入系列描述'
        },
        {
            key: 'coverImage',
            label: '系列封面',
            type: 'mediaPicker',
            required: false
        }
    ],
    saveApi: (data) => useSeriesStore().createSeries(data)
}

export const seriesUpdateConfig: FormConfig<SeriesUpdate> = {
    fields: [
        {
            key: 'name',
            label: '系列名称',
            type: 'text',
            required: true,
            placeholder: '如：EVA 深度解析系列'
        },
        {
            key: 'slug',
            label: '系列别名',
            type: 'text',
            required: true,
            placeholder: '请输入系列别名'
        },
        {
            key: 'description',
            label: '系列描述',
            type: 'textarea',
            required: false,
            rows: 3,
            placeholder: '请输入系列描述'
        },
        {
            key: 'coverImage',
            label: '系列封面',
            type: 'mediaPicker',
            required: false
        }
    ],
    saveApi: (data, id) => useSeriesStore().updateSeries(id!, data)
}
