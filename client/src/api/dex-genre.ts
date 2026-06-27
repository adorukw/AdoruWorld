import { request } from "@/utils";
import type { DexGenreResponse, DexGenreCreate, DexGenreUpdate } from "@/types";

export const dexGenreApi = {
  list: () => request<DexGenreResponse[]>("/dex_genres"),
  getBySlug: (slug: string) =>
    request<DexGenreResponse>(`/dex_genres/slug/${slug}`),
  getById: (id: string) => request<DexGenreResponse>(`/dex_genres/${id}`),
  create: (data: DexGenreCreate) =>
    request<DexGenreResponse>("/dex_genres", {
      method: "POST",
      body: JSON.stringify(data),
    }),
  update: (id: string, data: DexGenreUpdate) =>
    request<DexGenreResponse>(`/dex_genres/${id}`, {
      method: "PUT",
      body: JSON.stringify(data),
    }),
  delete: (id: string) =>
    request<void>(`/dex_genres/${id}`, {
      method: "DELETE",
    }),
};
