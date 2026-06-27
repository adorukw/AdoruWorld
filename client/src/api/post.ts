import { request } from "@/utils";
import type {
  PostResponse,
  ArchiveItem,
  PostCreate,
  PostUpdate,
} from "@/types";

export const postApi = {
  list: (params?: {
    published?: boolean;
    featured?: boolean;
    category?: string;
    tag?: string;
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
    return request<PostResponse[]>(`/posts${query}`);
  },

  archives: () => request<ArchiveItem[]>("/posts/archives"),

  getBySlug: (slug: string) => request<PostResponse>(`/posts/slug/${slug}`),

  getRelated: (slug: string) =>
    request<PostResponse[]>(`/posts/slug/${slug}/related`),

  getById: (id: string) => request<PostResponse>(`/posts/${id}`),

  create: (data: PostCreate) =>
    request<PostResponse>("/posts", {
      method: "POST",
      body: JSON.stringify(data),
    }),

  update: (id: string, data: PostUpdate) =>
    request<PostResponse>(`/posts/${id}`, {
      method: "PUT",
      body: JSON.stringify(data),
    }),

  delete: (id: string) =>
    request<void>(`/posts/${id}`, {
      method: "DELETE",
    }),
  incrementViews: (id: string) =>
    request<void>(`/posts/increment-views/${id}`, {
      method: "POST",
    }),
  totalPostsCount: () => request<number>(`/posts/total-posts-count`),
  totalWords: () => request<number>(`/posts/total-words`),
  totalViews: () => request<number>(`/posts/total-views`),
};
