import { request } from "@/utils";
import type { DexResponse, DexCreate, DexUpdate, DexStats } from "@/types";

export const dexApi = {
  list: (params?: {
    category?: string;
    status?: string;
    skip?: number;
    limit?: number;
  }) => {
    const query = params
      ? "?" +
        new URLSearchParams(
          Object.fromEntries(
            Object.entries(params)
              .filter(([_, v]) => v !== undefined)
              .map(([k, v]) => [k, String(v)]),
          ),
        ).toString()
      : "";
    return request<DexResponse[]>(`/dexs${query}`);
  },
  getBySlug: (slug: string) => request<DexResponse>(`/dexs/slug/${slug}`),
  getRelated: (slug: string) =>
    request<DexResponse[]>(`/dexs/slug/${slug}/related`),
  getById: (id: string) => request<DexResponse>(`/dexs/${id}`),
  create: (data: DexCreate) =>
    request<DexResponse>("/dexs", {
      method: "POST",
      body: JSON.stringify(data),
    }),
  update: (id: string, data: DexUpdate) =>
    request<DexResponse>(`/dexs/${id}`, {
      method: "PUT",
      body: JSON.stringify(data),
    }),
  delete: (id: string) =>
    request<void>(`/dexs/${id}`, {
      method: "DELETE",
    }),
  stats: () => request<DexStats>(`/dexs/stats`),
};
