import type { DexGenreCreate, DexGenreUpdate } from '@/types'
import { useDexGenreStore } from '@/store'
import type { FormConfig } from '@/types'

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
    saveApi: (data, id) => useDexGenreStore().updateDexGenre(id!, data)
}
