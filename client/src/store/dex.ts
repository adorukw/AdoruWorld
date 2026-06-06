import { defineStore } from 'pinia'
import { ref} from 'vue'
import { api } from '@/api'
import type { DexEntryResponse, DexStats, DexEntryCreate, DexEntryUpdate } from '@/types'

export const useDexStore = defineStore('dex', () => {
    const dexEntries = ref<DexEntryResponse[]>([])
    const currentDexEntry = ref<DexEntryResponse | null>(null)
    const dexStats = ref<DexStats>({
        total: 0,
        byCategory: {},
        byStatus: {},
        averageRating: 0
    })
    const loading = ref(false)
    const error = ref<string | null>(null)

    const getDexEntries = async (params?: {
        category?: string,
        status?: string,
        skip?: number,
        limit?: number
    }) => {
        loading.value = true
        error.value = null
        try {
            dexEntries.value = await api.dexs.list(params)
        }
        catch (err: any) {
            error.value = err.message || '获取图鉴列表失败'
        }
        finally {
            loading.value = false
        }
    }

    const getDexStats = async () => {
        loading.value = true
        error.value = null
        try {
            dexStats.value = await api.dexs.stats()
        }
        catch (err: any) {
            error.value = err.message || '获取图鉴统计失败'
        }
        finally {
            loading.value = false
        }
    }


    const getDexEntryBySlug = async (slug: string) => {
        loading.value = true
        error.value = null
        try {
            currentDexEntry.value = await api.dexs.getBySlug(slug)
        }
        catch (err: any) {
            error.value = err.message || '获取图鉴详情失败'
        }
        finally {
            loading.value = false
        }
    }

    const getDexEntryById = async (id: string) => {
        loading.value = true
        error.value = null
        try {
            currentDexEntry.value = await api.dexs.getById(id)
        }
        catch (err: any) {
            error.value = err.message || '获取图鉴详情失败'
        }
        finally {
            loading.value = false
        }
    }

    const createDexEntry = async (data: DexEntryCreate) => {
        loading.value = true
        error.value = null
        try {
            const newDexEntry = await api.dexs.create(data)
            dexEntries.value.unshift(newDexEntry)
            return newDexEntry
        }
        catch (err: any) {
            error.value = err.message || '创建图鉴失败'
            throw err
        }
        finally {
            loading.value = false
        }
    }

    const updateDexEntry = async (id: string, data: DexEntryUpdate) => {
        loading.value = true
        error.value = null
        try {
            const updateDexEntry = await api.dexs.update(id, data)
            const index = dexEntries.value.findIndex(entry => entry.id === id)
            if (index > -1) {
                dexEntries.value[index] = updateDexEntry
            }
            if (currentDexEntry.value?.id === id) {
                currentDexEntry.value = updateDexEntry
            }
            return updateDexEntry
        }
        catch (err: any) {
            error.value = err.message || '更新图鉴失败'
            throw err
        }
        finally {
            loading.value = false
        }
    }

    const deleteDexEntry = async (id: string) => {
        loading.value = true
        error.value = null
        try {
            await api.dexs.delete(id)
            dexEntries.value = dexEntries.value.filter(entry => entry.id !== id)
            if (currentDexEntry.value?.id === id) {
                currentDexEntry.value = null
            }
        }
        catch (err: any) {
            error.value = err.message || '删除图鉴失败'
            throw err
        }
        finally {
            loading.value = false
        }
    }
    return {
        dexEntries, dexStats, loading, error,
        getDexEntries, getDexEntryBySlug, getDexEntryById,
        createDexEntry, updateDexEntry, deleteDexEntry,
        getDexStats
    }

})