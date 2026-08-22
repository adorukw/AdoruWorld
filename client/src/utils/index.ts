import { BASE_API_URL } from "@/config";

const ACCESS_KEY = "accessToken";
const REFRESH_KEY = "refreshToken";

/** 用 refresh token 换新的一对 token；失败返回 null（顺带清理本地凭证） */
async function tryRefresh(): Promise<string | null> {
  const refreshToken = localStorage.getItem(REFRESH_KEY);
  if (!refreshToken) return null;

  const res = await fetch(`${BASE_API_URL}/auth/refresh`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ refreshToken }),
  });

  if (!res.ok) {
    localStorage.removeItem(ACCESS_KEY);
    localStorage.removeItem(REFRESH_KEY);
    return null;
  }

  const data = await res.json();
  localStorage.setItem(ACCESS_KEY, data.accessToken);
  localStorage.setItem(REFRESH_KEY, data.refreshToken);
  return data.accessToken as string;
}

async function rawRequest(url: string, options?: RequestInit): Promise<Response> {
  const isFormData = options?.body instanceof FormData;
  const accessToken = localStorage.getItem(ACCESS_KEY);

  return fetch(`${BASE_API_URL}${url}`, {
    ...options,
    headers: {
      // FormData 让浏览器自动设置带 boundary 的 Content-Type
      ...(isFormData ? {} : { "Content-Type": "application/json" }),
      ...(accessToken ? { Authorization: `Bearer ${accessToken}` } : {}),
      ...(options?.headers || {}),
    },
  });
}

export async function request<T>(url: string, options?: RequestInit): Promise<T> {
  let res = await rawRequest(url, options);

  // access token 过期：静默刷新后重试一次（登录/刷新接口本身不重试，防死循环）
  if (
    res.status === 401 &&
    !url.startsWith("/auth/login") &&
    !url.startsWith("/auth/refresh")
  ) {
    const newToken = await tryRefresh();
    if (newToken) {
      res = await rawRequest(url, options);
    } else {
      // 刷新也失败 → 踢回登录页
      window.location.href = "/adoru-world/login";
      throw new Error("登录已过期");
    }
  }

  if (res.status === 204) {
    return { message: "删除成功" } as T;
  }

  if (!res.ok) {
    const error = await res.json().catch(() => ({ error: res.statusText }));
    throw new Error(error.detail || error.error || "Request failed");
  }

  return res.json();
}
