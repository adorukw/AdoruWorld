<script setup lang="ts">
import { ref, onMounted } from "vue";
import { userApi } from "@/api";
import { useAuthStore } from "@/store";
import { ROLE_LABELS } from "@/types";
import type { UserResponse, UserRole } from "@/types";

const auth = useAuthStore();
const items = ref<UserResponse[] | null>(null);

const ROLE_COLORS: Record<UserRole, string> = {
  admin: "bg-red-400",
  editor: "bg-sky-400",
  viewer: "bg-gray-300",
};

async function refresh() {
    items.value = await userApi.list();
}

onMounted(refresh);

async function changeRole(item: UserResponse, event: Event) {
    const role = (event.target as HTMLSelectElement).value as UserRole;
    try {
        await userApi.update(item.id, { role });
        await refresh();
    } catch (e: any) {
        alert(e.message || "修改失败");
        await refresh();
    }
}

async function toggleActive(item: UserResponse) {
    try {
        await userApi.update(item.id, { isActive: !item.isActive });
        await refresh();
    } catch (e: any) {
        alert(e.message || "操作失败");
    }
}

async function handleDelete(item: UserResponse) {
    if (!confirm(`确定删除用户 "${item.username}" 吗？`)) return;
    try {
        await userApi.delete(item.id);
        await refresh();
    } catch (e: any) {
        alert(e.message || "删除失败");
    }
}
</script>

<template>
    <div class="flex justify-between items-center mb-6">
        <span>共 {{ items?.length }} 个用户</span>
    </div>

    <div class="pixel-card">
        <div class="overflow-x-auto">
            <table class="w-full">
                <thead class="bg-gray-100 border-b-4 border-black">
                    <tr>
                        <th class="p-4 text-left pixel-text">用户名</th>
                        <th class="p-4 text-left pixel-text">邮箱</th>
                        <th class="p-4 text-left pixel-text">角色</th>
                        <th class="p-4 text-left pixel-text">状态</th>
                        <th class="p-4 text-left pixel-text">最近登录</th>
                        <th class="p-4 text-left pixel-text">操作</th>
                    </tr>
                </thead>
                <tbody>
                    <tr
                        v-for="item in items"
                        :key="item.id"
                        class="border-b-2 border-gray-200 hover:bg-gray-50"
                    >
                        <td class="p-4 font-medium">
                            {{ item.displayName || item.username }}
                            <span
                                v-if="item.id === auth.user?.id"
                                class="text-xs text-sky-700"
                                >（我）</span
                            >
                        </td>
                        <td class="p-4 text-gray-600">
                            {{ item.email }}
                            <span
                                v-if="!item.emailVerified"
                                class="text-xs text-orange-500 ml-1"
                                >未验证</span
                            >
                        </td>
                        <td class="p-4">
                            <span
                                class="px-2 py-1 border-2 border-black text-xs"
                                :class="ROLE_COLORS[item.role]"
                            >
                                {{ ROLE_LABELS[item.role] }}
                            </span>
                            <select
                                v-if="auth.isAdmin && item.id !== auth.user?.id"
                                :value="item.role"
                                class="ml-2 p-1 border-2 border-black text-xs bg-white"
                                @change="changeRole(item, $event)"
                            >
                                <option value="viewer">访客</option>
                                <option value="editor">编辑者</option>
                                <option value="admin">管理员</option>
                            </select>
                        </td>
                        <td class="p-4">
                            <button
                                class="pixel-btn-small text-xs"
                                :class="
                                    item.isActive
                                        ? 'bg-green-300'
                                        : 'bg-gray-300'
                                "
                                :disabled="item.id === auth.user?.id"
                                @click="toggleActive(item)"
                            >
                                {{ item.isActive ? "正常" : "已禁用" }}
                            </button>
                        </td>
                        <td class="p-4 text-gray-600 text-sm">
                            {{
                                item.lastLoginAt
                                    ? new Date(
                                          item.lastLoginAt,
                                      ).toLocaleString("zh-CN")
                                    : "从未登录"
                            }}
                        </td>
                        <td class="p-4">
                            <button
                                v-if="item.id !== auth.user?.id"
                                class="pixel-btn-small bg-red-500 text-white"
                                @click="handleDelete(item)"
                            >
                                删除
                            </button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>
