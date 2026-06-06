import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { api } from '@/api'
import type { PostResponse, PostListItem, ArchiveItem, PostCreate, PostUpdate } from '@/types'

export const usePostStore = defineStore('post', () => {
    // ==================== State ====================
    const posts = ref<PostListItem[]>([])
    const allPosts = ref<PostListItem[]>([])
    const currentPost = ref<PostResponse | null>(null)
    const archives = ref<ArchiveItem[]>([])
    const totalPostsCount = ref<number>(0)
    const totalWordCount = ref<number>(0)
    const totalViewsCount = ref<number>(0)
    const loading = ref(false)
    const error = ref<string | null>(null)

    // ==================== Getters ====================
    const publishedPosts = computed(() =>
        allPosts.value.filter(p => p.published)
    )

    const featuredPosts = computed(() =>
        allPosts.value.filter(p => p.featured)
    )

    const recentPosts = computed(() =>
        [...allPosts.value].sort((a, b) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()).slice(0, 5)
    )

    const postsByCategory = computed(() => {
        return (categorySlug: string) =>
            allPosts.value.filter(p => p.category.slug === categorySlug)
    })

    // ==================== Actions ====================
    const getAllPosts = async () => {
        loading.value = true
        error.value = null
        try {
            allPosts.value = await api.posts.list()
        } catch (err: any) {
            error.value = err.message || '获取文章列表失败'
        } finally {
            loading.value = false
        }
    }

    const getPosts = async (params?: {
        published?: boolean
        featured?: boolean
        category?: string
        tag?: string
        skip?: number
        limit?: number
    }) => {
        loading.value = true
        error.value = null
        try {
            posts.value = await api.posts.list(params)
        } catch (err: any) {
            error.value = err.message || '获取文章列表失败'
        } finally {
            loading.value = false
        }
    }

    const getArchives = async () => {
        loading.value = true
        error.value = null
        try {
            archives.value = await api.posts.archives()
        } catch (err: any) {
            error.value = err.message || '获取归档失败'
        } finally {
            loading.value = false
        }
    }

    const getPostBySlug = async (slug: string) => {
        loading.value = true
        error.value = null
        try {
            currentPost.value = await api.posts.getBySlug(slug)
        } catch (err: any) {
            error.value = err.message || '获取文章失败'
        } finally {
            loading.value = false
        }
    }

    const getPostById = async (id: string) => {
        loading.value = true
        error.value = null
        try {
            currentPost.value = await api.posts.getById(id)
        } catch (err: any) {
            error.value = err.message || '获取文章失败'
        } finally {
            loading.value = false
        }
    }

    const createPost = async (data: PostCreate) => {
        loading.value = true
        error.value = null
        try {
            const newPost = await api.posts.create(data)
            posts.value.unshift(newPost)
            return newPost
        } catch (err: any) {
            error.value = err.message || '创建文章失败'
            throw err
        } finally {
            loading.value = false
        }
    }

    const updatePost = async (id: string, data: PostUpdate) => {
        loading.value = true
        error.value = null
        try {
            const updatedPost = await api.posts.update(id, data)
            const index = posts.value.findIndex(p => p.id === id)
            if (index !== -1) {
                posts.value[index] = updatedPost
            }
            if (currentPost.value?.id === id) {
                currentPost.value = updatedPost
            }
            return updatedPost
        } catch (err: any) {
            error.value = err.message || '更新文章失败'
            throw err
        } finally {
            loading.value = false
        }
    }

    const deletePost = async (id: string) => {
        loading.value = true
        error.value = null
        try {
            await api.posts.delete(id)
            posts.value = posts.value.filter(p => p.id !== id)
            if (currentPost.value?.id === id) {
                currentPost.value = null
            }
        } catch (err: any) {
            error.value = err.message || '删除文章失败'
            throw err
        } finally {
            loading.value = false
        }
    }

    const incrementViews = async (id: string) => {
        loading.value = true
        error.value = null
        try {
            await api.posts.incrementViews(id)
        }
        catch (err: any) {
            error.value = err.message || '获取文章列表失败'
        }
        finally {
            loading.value = false
        }
    }

    const getTotalPostsCount = async () => {
        loading.value = true
        error.value = null
        try {
            const count = await api.posts.totalPostsCount()
            totalPostsCount.value = count
        } catch (err: any) {
            error.value = err.message || '获取文章列表失败'
        }
        finally {
            loading.value = false
        }
    }

    const getTotalWords = async () => {
        loading.value = true
        error.value = null
        try {
            const count = await api.posts.totalWords()
            totalWordCount.value = count
        } catch (err: any) {
            error.value = err.message || '获取文章列表失败'
        }
        finally {
            loading.value = false
        }
    }

    const getTotalViews = async () => {
        loading.value = true
        error.value = null
        try {
            const count = await api.posts.totalViews()
            totalViewsCount.value = count
        } catch (err: any) {
            error.value = err.message || '获取文章列表失败'
        }
        finally {
            loading.value = false
        }
    }

    // 返回所有需要暴露的内容
    return {
        // State
        posts, allPosts, currentPost, archives, loading, error,
        totalPostsCount, totalWordCount, totalViewsCount,
        // Getters
        publishedPosts, featuredPosts, postsByCategory, recentPosts,
        // Actions
        getAllPosts, getPosts, getArchives, getPostBySlug, getPostById,
        createPost, updatePost, deletePost, incrementViews,
        getTotalPostsCount, getTotalWords, getTotalViews,
    }
})