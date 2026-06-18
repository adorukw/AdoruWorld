import type { PostTagCreate, PostTagUpdate } from '@/types'
import { usePostTagStore } from '@/store'

import type { FormConfig } from '@/types'

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
    saveApi: (data, id) => usePostTagStore().updatePostTag(id!, data)
}