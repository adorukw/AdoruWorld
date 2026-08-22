import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { authApi } from "@/api";
import type { UserResponse } from "@/types";

const ACCESS_KEY = "accessToken";
const REFRESH_KEY = "refreshToken";

export const useAuthStore = defineStore("auth", () => {
  const user = ref<UserResponse | null>(null);
  const loading = ref(false);

  const isLoggedIn = computed(() => !!localStorage.getItem(ACCESS_KEY));
  const isAdmin = computed(() => user.value?.role === "admin");
  const canWrite = computed(() =>
    ["admin", "editor"].includes(user.value?.role ?? ""),
  );

  function saveTokens(accessToken: string, refreshToken: string) {
    localStorage.setItem(ACCESS_KEY, accessToken);
    localStorage.setItem(REFRESH_KEY, refreshToken);
  }

  function clearAuth() {
    localStorage.removeItem(ACCESS_KEY);
    localStorage.removeItem(REFRESH_KEY);
    user.value = null;
  }

  async function login(account: string, password: string) {
    loading.value = true;
    try {
      const res = await authApi.login({ account, password });
      saveTokens(res.accessToken, res.refreshToken);
      user.value = res.user;
      return res.user;
    } finally {
      loading.value = false;
    }
  }

  async function logout() {
    const refreshToken = localStorage.getItem(REFRESH_KEY);
    if (refreshToken) {
      // 登出失败也不阻塞本地清理
      await authApi.logout(refreshToken).catch(() => {});
    }
    clearAuth();
  }

  async function fetchMe() {
    if (!isLoggedIn.value) return null;
    try {
      user.value = await authApi.me();
      return user.value;
    } catch {
      // token 失效且刷新也失败时，request 拦截器会清理
      return null;
    }
  }

  return {
    user,
    loading,
    isLoggedIn,
    isAdmin,
    canWrite,
    login,
    logout,
    fetchMe,
    clearAuth,
  };
});
