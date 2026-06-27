import { request } from "@/utils";
import type { MediaTagResponse, MediaTagCreate, MediaTagUpdate } from "@/types";

export const mediaTagApi = {
  list: () => request<MediaTagResponse[]>("/media_tags"),
  getBySlug: (slug: string) =>
    request<MediaTagResponse>(`/media_tags/slug/${slug}`),
  getById: (id: string) => request<MediaTagResponse>(`/media_tags/${id}`),
  create: (data: MediaTagCreate) =>
    request<MediaTagResponse>("/media_tags", {
      method: "POST",
      body: JSON.stringify(data),
    }),
  update: (id: string, data: MediaTagUpdate) =>
    request<MediaTagResponse>(`/media_tags/${id}`, {
      method: "PUT",
      body: JSON.stringify(data),
    }),
  delete: (id: string) =>
    request<void>(`/media_tags/${id}`, {
      method: "DELETE",
    }),
};
