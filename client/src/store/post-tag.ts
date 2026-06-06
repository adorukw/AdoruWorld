import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { api } from '@/api'
import type { PostTagResponse, PostTagCreate, PostTagUpdate } from '@/types'

export const usePostTagStore = defineStore('post-tag', () => {
    const postTags = ref<PostTagResponse[]>([])
    const currentPostTag = ref<PostTagResponse | null>(null)
    const loading = ref(false)
    const error = ref<string | null>(null)

    const postTagMap = computed(() => {
        return postTags.value.reduce((map, tag) => {
            map[tag.slug] = tag
            return map
        }, {} as Record<string, PostTagResponse>)
    })

    const getPostTags = async () => {
        loading.value = true
        error.value = null
        try {
            postTags.value = await api.postTags.list()
        } catch (err: any) {
            error.value = err.message || '获取标签失败'
        } finally {
            loading.value = false
        }
    }

    const getPostTagBySlug = async (slug: string) => {
        loading.value = true
        error.value = null
        try {
            currentPostTag.value = await api.postTags.getBySlug(slug)
        } catch (err: any) {
            error.value = err.message || '获取标签失败'
        } finally {
            loading.value = false
        }
    }

    const getPostTagById = async (id: string) => {
        loading.value = true
        error.value = null
        try {
            currentPostTag.value = await api.postTags.getById(id)
        } catch (err: any) {
            error.value = err.message || '获取标签失败'
        } finally {
            loading.value = false
        }
    }

    const createPostTag = async (data: PostTagCreate) => {
        loading.value = true
        error.value = null
        try {
            const newTag = await api.postTags.create(data)
            postTags.value.push(newTag)
            return newTag
        } catch (err: any) {
            error.value = err.message || '创建标签失败'
            throw err
        } finally {
            loading.value = false
        }
    }

    const updatePostTag = async (id: string, data: PostTagUpdate) => {
        loading.value = true
        error.value = null
        try {
            const updatedTag = await api.postTags.update(id, data)
            const index = postTags.value.findIndex(t => t.id === id)
            if (index !== -1) {
                postTags.value[index] = updatedTag
            }
            if (currentPostTag.value?.id === id) {
                currentPostTag.value = updatedTag
            }
            return updatedTag
        } catch (err: any) {
            error.value = err.message || '更新标签失败'
            throw err
        } finally {
            loading.value = false
        }
    }

    const deletePostTag = async (id: string) => {
        loading.value = true
        error.value = null
        try {
            await api.postTags.delete(id)
            postTags.value = postTags.value.filter(t => t.id !== id)
            if (currentPostTag.value?.id === id) {
                currentPostTag.value = null
            }
        } catch (err: any) {
            error.value = err.message || '删除标签失败'
            throw err
        } finally {
            loading.value = false
        }
    }

    return {
        postTags, currentPostTag, loading, error, postTagMap,
        getPostTags, getPostTagBySlug, getPostTagById, createPostTag,
        updatePostTag, deletePostTag
    }
})