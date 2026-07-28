<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useDexGenreStore } from "@/store";
import CrudModal from "@/components/common/CrudModal.vue";
import PixelButton from "@/components/ui/PixelButton.vue";
import type { DexGenreResponse } from "@/types";

const store = useDexGenreStore();
const items = ref<DexGenreResponse[] | null>(null);

const showModal = ref(false);
const modalMode = ref<"create" | "update">("create");
const editingItem = ref<DexGenreResponse | null>(null);

onMounted(async () => {
    await store.getDexGenres();
    items.value = store.dexGenres;
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
        categoryId: item.category?.id,
        tagIds: item.tags?.map((t: any) => t.id) || [],
    };
    showModal.value = true;
}

async function handleModalSuccess() {
    showModal.value = false;
    await store.getDexGenres();
    items.value = store.dexGenres;
}

async function handleDelete(item: any) {
    if (!confirm(`确定删除 "${item.title}" 吗？`)) return;
    try {
        await store.deleteDexGenre(item.id);
        await store.getDexGenres();
        items.value = store.dexGenres;
    } catch (e) {
        alert("删除失败");
    }
}
</script>

<template>
    <!-- 操作栏 -->
    <div class="flex justify-between items-center mb-6">
        <span class="">共 {{ items?.length }} 条记录</span>
        <PixelButton @click="openCreateModal">➕ 新增文章</PixelButton>
    </div>

    <!-- 表格 -->
    <div class="pixel-card">
        <div class="overflow-x-auto">
            <table class="w-full">
                <thead class="bg-gray-100 border-b-4 border-black">
                    <tr>
                        <th class="p-4 text-left pixel-text">名称</th>
                        <th class="p-4 text-left pixel-text">颜色</th>
                        <th class="p-4 text-left pixel-text text-sm">操作</th>
                    </tr>
                </thead>
                <tbody>
                    <tr
                        v-for="item in items"
                        :key="item.id"
                        class="border-b-2 border-gray-200 hover:bg-gray-50"
                    >
                        <td class="p-4 font-medium">{{ item.name }}</td>
                        <td class="p-4">
                            <div class="flex items-center gap-2">
                                <div
                                    class="w-6 h-6 border-2 border-black"
                                    :style="{ backgroundColor: item.color }"
                                ></div>
                                <span class="font-mono">{{ item.color }}</span>
                            </div>
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
        module="dexGenres"
        :mode="modalMode"
        :initial-data="editingItem"
        @success="handleModalSuccess"
        @close="showModal = false"
    />
</template>
