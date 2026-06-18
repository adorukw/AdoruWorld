import type { PostCategoryCreate, PostCategoryUpdate } from '@/types'
import { usePostCategoryStore } from '@/store'

import type { FormConfig } from '@/types'

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
    saveApi: (data, id) => usePostCategoryStore().updatePostCategory(id!, data)
}
