import { request } from "@/utils";
import type { SearchResponse } from "@/types";

export const searchApi = {
  search: async (
    q: string,
    type?: "post" | "dex" | "media",
    skip = 0,
    limit = 20,
  ) => {
    const params = new URLSearchParams({ q });
    if (type) params.set("type", type);
    params.set("skip", String(skip));
    params.set("limit", String(limit));
    return request<SearchResponse>(`/search?${params.toString()}`);
  },
};
