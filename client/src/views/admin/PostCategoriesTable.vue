<script setup lang="ts">
import { ref, onMounted } from "vue";
import { usePostCategoryStore } from "@/store";
import CrudModal from "@/components/common/CrudModal.vue";
import PixelButton from "@/components/ui/PixelButton.vue";
import type { PostCategoryResponse } from "@/types";

const store = usePostCategoryStore();
const items = ref<PostCategoryResponse[] | null>(null);

const showModal = ref(false);
const modalMode = ref<"create" | "update">("create");
const editingItem = ref<PostCategoryResponse | null>(null);

onMounted(async () => {
    await store.getPostCategories();
    items.value = store.postCategories;
});

async function openCreateModal() {
    modalMode.value = "create";
    editingItem.value = null;
    showModal.value = true;
}

async function openEditModal(item: any) {
    modalMode.value = "update";
    editingItem.value = {
        ...item,
    };
    showModal.value = true;
}

async function handleModalSuccess() {
    showModal.value = false;
    await store.getPostCategories();
    items.value = store.postCategories;
}

async function handleDelete(item: any) {
    if (!confirm(`确定删除 "${item.name}" 吗？`)) return;
    try {
        await store.deletePostCategory(item.id);
        await store.getPostCategories();
        items.value = store.postCategories;
    } catch (e) {
        alert("删除失败");
    }
}
</script>

<template>
    <div class="flex justify-between items-center mb-6">
        <span class="">共 {{ items?.length }} 条记录</span>
        <PixelButton @click="openCreateModal">➕ 新增文章</PixelButton>
    </div>

    <div class="pixel-card">
        <div class="overflow-x-auto">
            <table class="w-full">
                <thead class="bg-gray-100 border-b-4 border-black">
                    <tr>
                        <th class="p-4 text-left pixel-text">名称</th>
                        <th class="p-4 text-left pixel-text">别名</th>
                        <th class="p-4 text-left pixel-text">图标</th>
                        <th class="p-4 text-left pixel-text">文章数</th>
                        <th class="p-4 text-left pixel-text">操作</th>
                    </tr>
                </thead>
                <tbody>
                    <tr
                        v-for="item in items"
                        :key="item.id"
                        class="border-b-2 border-gray-200 hover:bg-gray-50"
                    >
                        <td class="p-4 font-medium">{{ item.name }}</td>
                        <td class="p-4 text-gray-600">{{ item.slug }}</td>
                        <td class="p-4">{{ item.icon }}</td>
                        <td class="p-4">
                            <span
                                class="px-2 py-1 bg-grass-light border-2 border-black text-xs"
                            >
                                {{ item.count }} 篇
                            </span>
                        </td>
                        <td class="p-4">
                            <div class="flex gap-2">
                                <button
                                    @click="openEditModal(item)"
                                    class="pixel-btn-small bg-blue-500 text-white"
                                >
                                    编辑
                                </button>
                                <button
                                    @click="handleDelete(item)"
                                    class="pixel-btn-small bg-red-500 text-white"
                                >
                                    删除
                                </button>
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>
            <div v-if="items?.length === 0" class="text-center py-16">
                <div class="text-6xl mb-4">📭</div>
                <h3 class="pixel-text text-lg mb-2">暂无数据</h3>
                <p class="text-gray-600 mb-6">点击上方按钮添加新内容</p>
            </div>
        </div>
    </div>
    <CrudModal
        v-if="showModal"
        module="postCategories"
        :mode="modalMode"
        :initial-data="editingItem"
        @success="handleModalSuccess"
        @close="showModal = false"
    />
</template>
