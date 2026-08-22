import { request } from "@/utils";
import type { UserResponse, UserRole } from "@/types";

export interface UserUpdateRequest {
  role?: UserRole;
  isActive?: boolean;
  displayName?: string;
  bio?: string;
}

export const userApi = {
  list: () => request<UserResponse[]>("/users"),
  update: (id: string, data: UserUpdateRequest) =>
    request<UserResponse>(`/users/${id}`, {
      method: "PUT",
      body: JSON.stringify(data),
    }),
  delete: (id: string) =>
    request<void>(`/users/${id}`, {
      method: "DELETE",
    }),
};
