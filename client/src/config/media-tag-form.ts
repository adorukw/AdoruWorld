import type { MediaTagCreate, MediaTagUpdate } from '@/types'
import { useMediaTagStore } from '@/store'

import type { FormConfig } from '@/types'

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
    saveApi: (data, id) => useMediaTagStore().updateMediaTag(id!, data)
}