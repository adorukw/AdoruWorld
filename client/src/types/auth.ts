export type UserRole = "admin" | "editor" | "viewer";

export interface UserResponse {
  id: string;
  username: string;
  email: string;
  role: UserRole;
  isActive: boolean;
  emailVerified: boolean;
  displayName?: string;
  avatar?: string;
  bio?: string;
  createdAt: string;
  lastLoginAt?: string;
}

export interface TokenResponse {
  accessToken: string;
  refreshToken: string;
  tokenType: string;
  user: UserResponse;
}

export interface LoginRequest {
  account: string;
  password: string;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
}

export interface VerifyEmailRequest {
  email: string;
  code: string;
}

export const ROLE_LABELS: Record<UserRole, string> = {
  admin: "管理员",
  editor: "编辑者",
  viewer: "访客",
};
