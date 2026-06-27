import { request } from "@/utils";
import type {
  PostCategoryResponse,
  PostCategoryCreate,
  PostCategoryUpdate,
} from "@/types";

export const postCategoryApi = {
  list: () => request<PostCategoryResponse[]>("/post_categories"),
  getBySlug: (slug: string) =>
    request<PostCategoryResponse>(`/post_categories/slug/${slug}`),
  getById: (id: string) =>
    request<PostCategoryResponse>(`/post_categories/${id}`),
  create: (data: PostCategoryCreate) =>
    request<PostCategoryResponse>("/post_categories", {
      method: "POST",
      body: JSON.stringify(data),
    }),
  update: (id: string, data: PostCategoryUpdate) =>
    request<PostCategoryResponse>(`/post_categories/${id}`, {
      method: "PUT",
      body: JSON.stringify(data),
    }),
  delete: (id: string) =>
    request<void>(`/post_categories/${id}`, {
      method: "DELETE",
    }),
};
