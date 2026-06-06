import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { api } from '@/api'
import type { PostCategoryResponse, PostCategoryCreate, PostCategoryUpdate } from '@/types'

export const usePostCategoryStore = defineStore('post-categories', () => {
    const postCategories = ref<PostCategoryResponse[]>([])
    const currentPostCategory = ref<PostCategoryResponse | null>(null)
    const loading = ref(false)
    const error = ref<string | null>(null)

    const postCategoryMap = computed(() => {
        return postCategories.value.reduce((map, category) => {
            map[category.slug] = category
            return map
        }, {} as Record<string, PostCategoryResponse>)
    })

    const getPostCategories = async () => {
        loading.value = true
        error.value = null
        try {
            postCategories.value = await api.postCategories.list()
        }
        catch (err: any) {
            error.value = err.message || '获取分类失败'
        }
        finally {
            loading.value = false
        }
    }

    const getPostCategoryBySlug = async (slug: string) => {
        loading.value = true
        error.value = null
        try {
            currentPostCategory.value = await api.postCategories.getBySlug(slug)
        }
        catch (err: any) {
            error.value = err.message || '获取分类失败'
        }
        finally {
            loading.value = false
        }
    }

    const getPostCategoryById = async (id: string) => {
        loading.value = true
        error.value = null
        try {
            currentPostCategory.value = await api.postCategories.getById(id)
        }
        catch (err: any) {
            error.value = err.message || '获取分类失败'
        }
        finally {
            loading.value = false
        }
    }

    const createPostCategory = async (data: PostCategoryCreate) => {
        loading.value = true
        error.value = null
        try {
            const newCategory = await api.postCategories.create(data)
            postCategories.value.push(newCategory)
            return newCategory
        }
        catch (err: any) {
            error.value = err.message || '创建分类失败'
        }
        finally {
            loading.value = false
        }
    }

    const updatePostCategory = async (id: string, data: PostCategoryUpdate) => {
        loading.value = true
        error.value = null
        try {
            const updatedCategory = await api.postCategories.update(id, data)
            const index = postCategories.value.findIndex(category => category.id === id)
            if (index !== -1) {
                postCategories.value[index] = updatedCategory
            }
            if (currentPostCategory.value?.id === id) {
                currentPostCategory.value = updatedCategory
            }
            return updatedCategory
        }
        catch (err: any) {
            error.value = err.message || '更新分类失败'
        }
        finally {
            loading.value = false
        }
    }

    const deletePostCategory = async (id: string) => {
        loading.value = true
        error.value = null
        try {
            await api.postCategories.delete(id)
            postCategories.value = postCategories.value.filter(c => c.id !== id)
            if (currentPostCategory.value?.id === id) {
                currentPostCategory.value = null
            }
        }
        catch (err: any) {
            error.value = err.message || '删除分类失败'
            throw err
        }
        finally {
            loading.value = false
        }
    }

    return {
        postCategories, currentPostCategory, loading, error, categoryMap: postCategoryMap,
        getPostCategories, getPostCategoryBySlug, getPostCategoryById, createPostCategory,
        updatePostCategory, deletePostCategory
    }
})