import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { dexGenreApi as api } from "@/api";
import type { DexGenreResponse, DexGenreCreate, DexGenreUpdate } from "@/types";

export const useDexGenreStore = defineStore("dex-genre", () => {
  const dexGenres = ref<DexGenreResponse[]>([]);
  const currentDexGenre = ref<DexGenreResponse | null>(null);
  const loading = ref<boolean>(false);
  const error = ref<string | null>(null);

  const dexGenreMap = computed(() => {
    return dexGenres.value.reduce(
      (map, genre) => {
        map[genre.slug] = genre;
        return map;
      },
      {} as Record<string, DexGenreResponse>,
    );
  });

  const getDexGenres = async () => {
    loading.value = true;
    error.value = null;
    try {
      dexGenres.value = await api.list();
    } catch (err: any) {
      error.value = err.message || "获取题材失败";
    } finally {
      loading.value = false;
    }
  };

  const getDexGenreBySlug = async (slug: string) => {
    loading.value = true;
    error.value = null;
    try {
      currentDexGenre.value = await api.getBySlug(slug);
    } catch (err: any) {
      error.value = err.message || "获取题材失败";
    } finally {
      loading.value = false;
    }
  };

  const getDexGenreById = async (id: string) => {
    loading.value = true;
    error.value = null;
    try {
      currentDexGenre.value = await api.getById(id);
    } catch (err: any) {
      error.value = err.message || "获取题材失败";
    } finally {
      loading.value = false;
    }
  };

  const createDexGenre = async (data: DexGenreCreate) => {
    loading.value = true;
    error.value = null;
    try {
      const newDexGenre = await api.create(data);
      dexGenres.value.push(newDexGenre);
      return newDexGenre;
    } catch (err: any) {
      error.value = err.message || "创建题材失败";
    } finally {
      loading.value = false;
    }
  };

  const updateDexGenre = async (id: string, data: DexGenreUpdate) => {
    loading.value = true;
    error.value = null;
    try {
      const updatedDexGenre = await api.update(id, data);
      const index = dexGenres.value.findIndex((genre) => genre.id === id);
      if (index !== -1) {
        dexGenres.value[index] = updatedDexGenre;
      }
      if (currentDexGenre.value?.id === id) {
        currentDexGenre.value = updatedDexGenre;
      }
      return updatedDexGenre;
    } catch (err: any) {
      error.value = err.message || "更新题材失败";
    } finally {
      loading.value = false;
    }
  };

  const deleteDexGenre = async (id: string) => {
    loading.value = true;
    error.value = null;
    try {
      await api.delete(id);
      dexGenres.value = dexGenres.value.filter((genre) => genre.id !== id);
      if (currentDexGenre.value && currentDexGenre.value.id === id) {
        currentDexGenre.value = null;
      }
    } catch (err: any) {
      error.value = err.message || "删除题材失败";
    } finally {
      loading.value = false;
    }
  };

  return {
    dexGenres,
    currentDexGenre,
    loading,
    error,
    dexGenreMap,
    getDexGenres,
    getDexGenreBySlug,
    getDexGenreById,
    createDexGenre,
    updateDexGenre,
    deleteDexGenre,
  };
});
