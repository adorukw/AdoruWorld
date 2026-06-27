import { request } from "@/utils";
import type { PostTagResponse, PostTagCreate, PostTagUpdate } from "@/types";

export const postTagApi = {
  list: () => request<PostTagResponse[]>("/post_tags"),
  getBySlug: (slug: string) =>
    request<PostTagResponse>(`/post_tags/slug/${slug}`),
  getById: (id: string) => request<PostTagResponse>(`/post_tags/${id}`),
  create: (data: PostTagCreate) =>
    request<PostTagResponse>("/post_tags", {
      method: "POST",
      body: JSON.stringify(data),
    }),
  update: (id: string, data: PostTagUpdate) =>
    request<PostTagResponse>(`/post_tags/${id}`, {
      method: "PUT",
      body: JSON.stringify(data),
    }),
  delete: (id: string) =>
    request<void>(`/post_tags/${id}`, {
      method: "DELETE",
    }),
};
