import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { seriesApi as api } from "@/api";
import type {
  SeriesResponse,
  SeriesCreate,
  SeriesUpdate,
} from "@/types";

export const useSeriesStore = defineStore("series", () => {
  const seriesList = ref<SeriesResponse[]>([]);
  const currentSeries = ref<SeriesResponse | null>(null);
  const loading = ref(false);
  const error = ref<string | null>(null);

  const seriesMap = computed(() => {
    return seriesList.value.reduce(
      (map, s) => {
        map[s.slug] = s;
        return map;
      },
      {} as Record<string, SeriesResponse>,
    );
  });

  const getSeriesList = async () => {
    loading.value = true;
    error.value = null;
    try {
      seriesList.value = await api.list();
    } catch (err: any) {
      error.value = err.message || "获取系列失败";
    } finally {
      loading.value = false;
    }
  };

  const getSeriesBySlug = async (slug: string) => {
    loading.value = true;
    error.value = null;
    try {
      currentSeries.value = await api.getBySlug(slug);
    } catch (err: any) {
      error.value = err.message || "获取系列失败";
    } finally {
      loading.value = false;
    }
  };

  const createSeries = async (data: SeriesCreate) => {
    loading.value = true;
    error.value = null;
    try {
      const newSeries = await api.create(data);
      seriesList.value.push(newSeries);
      return newSeries;
    } catch (err: any) {
      error.value = err.message || "创建系列失败";
    } finally {
      loading.value = false;
    }
  };

  const updateSeries = async (id: string, data: SeriesUpdate) => {
    loading.value = true;
    error.value = null;
    try {
      const updatedSeries = await api.update(id, data);
      const index = seriesList.value.findIndex((s) => s.id === id);
      if (index !== -1) {
        seriesList.value[index] = updatedSeries;
      }
      if (currentSeries.value?.id === id) {
        currentSeries.value = updatedSeries;
      }
      return updatedSeries;
    } catch (err: any) {
      error.value = err.message || "更新系列失败";
    } finally {
      loading.value = false;
    }
  };

  const deleteSeries = async (id: string) => {
    loading.value = true;
    error.value = null;
    try {
      await api.delete(id);
      seriesList.value = seriesList.value.filter((s) => s.id !== id);
      if (currentSeries.value?.id === id) {
        currentSeries.value = null;
      }
    } catch (err: any) {
      error.value = err.message || "删除系列失败";
      throw err;
    } finally {
      loading.value = false;
    }
  };

  return {
    seriesList,
    currentSeries,
    loading,
    error,
    seriesMap,
    getSeriesList,
    getSeriesBySlug,
    createSeries,
    updateSeries,
    deleteSeries,
  };
});
