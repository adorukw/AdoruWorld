import { defineStore } from "pinia";
import { ref } from "vue";
import { searchApi as api } from "@/api";
import type { SearchResultItem } from "@/types";

export const useSearchStore = defineStore("search", () => {
  const items = ref<SearchResultItem[]>([]);
  const total = ref(0);
  const query = ref("");
  const entityType = ref<string | undefined>(undefined);
  const loading = ref(false);
  const error = ref<string | null>(null);
  const skip = ref(0);
  const limit = ref(20);

  const search = async (q: string, type?: string, reset = true) => {
    if (!q.trim()) return;

    loading.value = true;
    error.value = null;
    query.value = q;
    entityType.value = type;

    if (reset) {
      skip.value = 0;
      items.value = [];
    }

    try {
      const res = await api.search(q, type as any, skip.value, limit.value);
      if (reset) items.value = res.items;
      else {
        items.value.push(...res.items);
      }
      total.value = res.total;
      return res;
    } catch (err: any) {
      error.value = err.message || "搜索失败";
    } finally {
      loading.value = false;
    }
  };

  const loadMore = async () => {
    if (loading.value || items.value.length >= total.value) return;
    skip.value += limit.value;
    await search(query.value, entityType.value, false);
  };

  return {
    items,
    total,
    query,
    entityType,
    loading,
    error,
    skip,
    search,
    loadMore,
  };
});
