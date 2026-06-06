import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { api } from '@/api'
import type { MediaTagResponse, MediaTagCreate, MediaTagUpdate } from '@/types'

export const useMediaTagStore = defineStore('media-tag', () => {
    const mediaTags = ref<MediaTagResponse[]>([])
    const currentMediaTag = ref<MediaTagResponse | null>(null)
    const loading = ref(false)
    const error = ref(null)

    const mediaTagMap = computed(() => {
        return mediaTags.value.reduce((map, tag) => {
            map[tag.slug] = tag
            return map
        }, {} as Record<string, MediaTagResponse>)
    })

    const getMediaTags = async () => {
        loading.value = true
        error.value = null
        try {
            mediaTags.value = await api.mediaTags.list()
        }
        catch (err: any) {
            error.value = err.message || '获取标签失败'
        }
        finally {
            loading.value = false
        }
    }

    const getMediaTagBySlug = async (slug: string) => {
        loading.value = true
        error.value = null
        try {
            currentMediaTag.value = await api.mediaTags.getBySlug(slug)
        }
        catch (err: any) {
            error.value = err.message || '获取标签失败'
        }
        finally {
            loading.value = false
        }
    }

    const getMediaTagById = async (id: string) => {
        loading.value = true
        error.value = null
        try {
            currentMediaTag.value = await api.mediaTags.getById(id)
        }
        catch (err: any) {
            error.value = err.message || '获取标签失败'
        }
        finally {
            loading.value = false
        }
    }

    const createMediaTag = async (data: MediaTagCreate) => {
        loading.value = true
        error.value = null
        try {
            const newTag = await api.mediaTags.create(data)
            mediaTags.value.push(newTag)
            return newTag
        }
        catch (err: any) {
            error.value = err.message || '创建标签失败'
        }
        finally {
            loading.value = false
        }
    }

    const updateMediaTag = async (id: string, data: MediaTagUpdate) => {
        loading.value = true
        error.value = null
        try {
            const updatedTag = await api.mediaTags.update(id, data)
            const index = mediaTags.value.findIndex(tag => tag.id === id)
            if (index > -1) {
                mediaTags.value[index] = updatedTag
            }
            if (currentMediaTag.value?.id === id) {
                currentMediaTag.value = updatedTag
            }
            return updatedTag
        }
        catch (err: any) {
            error.value = err.message || '更新标签失败'
        }
        finally {
            loading.value = false
        }
    }

    const deleteMediaTag = async (id: string) => {
        loading.value = true
        error.value = null
        try {
            await api.mediaTags.delete(id)
            mediaTags.value = mediaTags.value.filter(tag => tag.id !== id)
            if (currentMediaTag.value?.id === id) {
                currentMediaTag.value = null
            }
        }
        catch (err: any) {
            error.value = err.message || '删除标签失败'
        }
        finally {
            loading.value = false
        }
    }

    return {
        mediaTags, currentMediaTag, loading, error, mediaTagMap,
        getMediaTags, getMediaTagBySlug, getMediaTagById,
        createMediaTag, updateMediaTag, deleteMediaTag
    }
})