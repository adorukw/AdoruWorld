import { request } from "@/utils";
import type {
  SeriesResponse,
  SeriesCreate,
  SeriesUpdate,
  SeriesPostResponse,
} from "@/types";

export const seriesApi = {
  list: () => request<SeriesResponse[]>("/series"),
  getBySlug: (slug: string) => request<SeriesResponse>(`/series/slug/${slug}`),
  getById: (id: string) => request<SeriesResponse>(`/series/${id}`),
  getPosts: (id: string, published?: boolean) =>
    request<SeriesPostResponse[]>(
      `/series/${id}/posts${published ? "?published=true" : ""}`,
    ),
  create: (data: SeriesCreate) =>
    request<SeriesResponse>("/series", {
      method: "POST",
      body: JSON.stringify(data),
    }),
  update: (id: string, data: SeriesUpdate) =>
    request<SeriesResponse>(`/series/${id}`, {
      method: "PUT",
      body: JSON.stringify(data),
    }),
  delete: (id: string) =>
    request<void>(`/series/${id}`, {
      method: "DELETE",
    }),
};
