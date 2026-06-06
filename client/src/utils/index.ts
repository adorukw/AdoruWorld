import { BASE_API_URL } from '@/config'

export async function request<T>(url: string, options?: RequestInit): Promise<T> {
  const isFormData = options?.body instanceof FormData

  const res = await fetch(`${BASE_API_URL}${url}`, {
    // headers: { 'Content-Type': 'application/json' },
    ...options,
    headers: isFormData
      ? options.headers
      : {
        'Content-Type': 'application/json',
        ...(options?.headers || {})
      }
  })
  if (res.status === 204) {
    return { "message": "删除成功" } as T
  }

  if (!res.ok) {
    const error = await res.json().catch(() => ({ error: res.statusText }))
    throw new Error(error.error || 'Request failed')
  }

  return res.json()
}