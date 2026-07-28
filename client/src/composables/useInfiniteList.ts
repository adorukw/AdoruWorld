import { ref, type Ref } from "vue";

interface InfiniteListOptions<T, P extends Record<string, any>> {
  fetchFn: (params: P & { skip: number; limit: number }) => Promise<T[]>;
  pageSize: number;
  initialParams?: P;
}

export function useInfiniteList<T, P extends Record<string, any> = {}>(
  options: InfiniteListOptions<T, P>,
) {
  const items = ref<T[]>([]) as Ref<T[]>;
  const loading = ref(false);
  const error = ref<string | null>(null);
  const hasMore = ref(true);
  const pageSize = options.pageSize ?? 12;
  const params = ref(options.initialParams ?? {}) as Ref<P>;

  async function loadMore() {
    if (!hasMore.value || loading.value) return;
    loading.value = true;
    error.value = null;
    try {
      const newItems = await options.fetchFn({
        ...params.value,
        skip: items.value.length,
        limit: pageSize,
      });
      hasMore.value = newItems.length >= pageSize;
      items.value.push(...newItems);
    } catch (err: any) {
      error.value = err.message || "加载失败";
    } finally {
      loading.value = false;
    }
  }

  async function refresh(newParams?: P) {
    items.value = [];
    hasMore.value = true;
    if (newParams) params.value = newParams;
    await loadMore();
  }

  function reset() {
    items.value = [];
    hasMore.value = true;
    loading.value = false;
    error.value = null;
  }

  return { items, loading, error, hasMore, loadMore, refresh, reset };
}
