import { request } from "@/utils";
import type {
  LoginRequest,
  RegisterRequest,
  TokenResponse,
  UserResponse,
  VerifyEmailRequest,
} from "@/types";

export const authApi = {
  login: (data: LoginRequest) =>
    request<TokenResponse>("/auth/login", {
      method: "POST",
      body: JSON.stringify(data),
    }),
  register: (data: RegisterRequest) =>
    request<{ message: string }>("/auth/register", {
      method: "POST",
      body: JSON.stringify(data),
    }),
  verifyEmail: (data: VerifyEmailRequest) =>
    request<{ message: string }>("/auth/verify-email", {
      method: "POST",
      body: JSON.stringify(data),
    }),
  resendCode: (email: string) =>
    request<{ message: string }>("/auth/resend-code", {
      method: "POST",
      body: JSON.stringify({ email, code: "000000" }),
    }),
  logout: (refreshToken: string) =>
    request<{ message: string }>("/auth/logout", {
      method: "POST",
      body: JSON.stringify({ refreshToken }),
    }),
  me: () => request<UserResponse>("/auth/me"),
};
