import { defineStore } from "pinia";
import { ref } from "vue";
import { api } from "@/api";
import type { DexResponse, DexStats, DexCreate, DexUpdate } from "@/types";

export const useDexStore = defineStore("dex", () => {
  const dexs = ref<DexResponse[]>([]);
  const relatedDexs = ref<DexResponse[]>([]);
  const currentDex = ref<DexResponse | null>(null);
  const dexStats = ref<DexStats>({
    total: 0,
    byCategory: {},
    byStatus: {},
    averageRating: 0,
  });
  const loading = ref(false);
  const error = ref<string | null>(null);

  const getDexs = async (params?: {
    category?: string;
    status?: string;
    skip?: number;
    limit?: number;
  }) => {
    loading.value = true;
    error.value = null;
    try {
      dexs.value = await api.dexs.list(params);
    } catch (err: any) {
      error.value = err.message || "获取图鉴列表失败";
    } finally {
      loading.value = false;
    }
  };

  const getDexStats = async () => {
    loading.value = true;
    error.value = null;
    try {
      dexStats.value = await api.dexs.stats();
    } catch (err: any) {
      error.value = err.message || "获取图鉴统计失败";
    } finally {
      loading.value = false;
    }
  };

  const getDexBySlug = async (slug: string) => {
    loading.value = true;
    error.value = null;
    try {
      currentDex.value = await api.dexs.getBySlug(slug);
    } catch (err: any) {
      error.value = err.message || "获取图鉴详情失败";
    } finally {
      loading.value = false;
    }
  };

  const getRelatedDexs = async (slug: string) => {
    loading.value = true;
    error.value = null;
    try {
      relatedDexs.value = await api.dexs.getRelated(slug);
    } catch (err: any) {
      error.value = err.message || "获取相关图鉴失败";
    } finally {
      loading.value = false;
    }
  };

  const getDexById = async (id: string) => {
    loading.value = true;
    error.value = null;
    try {
      currentDex.value = await api.dexs.getById(id);
    } catch (err: any) {
      error.value = err.message || "获取图鉴详情失败";
    } finally {
      loading.value = false;
    }
  };

  const createDex = async (data: DexCreate) => {
    loading.value = true;
    error.value = null;
    try {
      const newDex = await api.dexs.create(data);
      dexs.value.unshift(newDex);
      return newDex;
    } catch (err: any) {
      error.value = err.message || "创建图鉴失败";
      throw err;
    } finally {
      loading.value = false;
    }
  };

  const updateDex = async (id: string, data: DexUpdate) => {
    loading.value = true;
    error.value = null;
    try {
      const updateDex = await api.dexs.update(id, data);
      const index = dexs.value.findIndex((entry) => entry.id === id);
      if (index > -1) {
        dexs.value[index] = updateDex;
      }
      if (currentDex.value?.id === id) {
        currentDex.value = updateDex;
      }
      return updateDex;
    } catch (err: any) {
      error.value = err.message || "更新图鉴失败";
      throw err;
    } finally {
      loading.value = false;
    }
  };

  const deleteDex = async (id: string) => {
    loading.value = true;
    error.value = null;
    try {
      await api.dexs.delete(id);
      dexs.value = dexs.value.filter((entry) => entry.id !== id);
      if (currentDex.value?.id === id) {
        currentDex.value = null;
      }
    } catch (err: any) {
      error.value = err.message || "删除图鉴失败";
      throw err;
    } finally {
      loading.value = false;
    }
  };
  return {
    dexs,
    relatedDexs,
    currentDex,
    dexStats,
    loading,
    error,

    getDexs,
    getDexBySlug,
    getRelatedDexs,
    getDexById,
    createDex,
    updateDex,
    deleteDex,
    getDexStats,
  };
});
