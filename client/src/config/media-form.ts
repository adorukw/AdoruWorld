import type { MediaCreate, MediaUpdate } from '@/types'
import { useMediaTagStore, useMediaStore } from '@/store'
import type { FormConfig } from '@/types'

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
            required: true,
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
            key: 'tagIds',
            label: '标签',
            type: 'multiSelect',
            required: true,
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