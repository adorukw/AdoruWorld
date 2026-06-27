import { request } from "@/utils";
import type {
  MediaResponse,
  MediaCreate,
  MediaUpdate,
  MediaUploadResponse,
} from "@/types";

export const mediaApi = {
  upload: async (file: File): Promise<MediaUploadResponse> => {
    const formData = new FormData();
    formData.append("file", file);
    return request<MediaUploadResponse>("/medias/upload", {
      method: "POST",
      body: formData,
    });
  },
  // 获取媒体列表
  list: (params?: {
    media_type?: string;
    tag_slug?: string;
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
    return request<MediaResponse[]>(`/medias${query}`);
  },

  // 根据 slug 获取媒体
  getBySlug: (slug: string) => request<MediaResponse>(`/medias/slug/${slug}`),

  // 根据 ID 获取媒体
  getById: (id: string) => request<MediaResponse>(`/medias/${id}`),

  // 创建媒体记录
  create: (data: MediaCreate) =>
    request<MediaResponse>("/medias", {
      method: "POST",
      body: JSON.stringify(data),
    }),

  // 更新媒体记录
  update: (id: string, data: MediaUpdate) =>
    request<MediaResponse>(`/medias/${id}`, {
      method: "PUT",
      body: JSON.stringify(data),
    }),

  // 删除媒体记录
  delete: (id: string) =>
    request<void>(`/medias/${id}`, {
      method: "DELETE",
    }),
};
