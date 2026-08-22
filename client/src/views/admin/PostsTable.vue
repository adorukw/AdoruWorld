<script setup lang="ts">
import { ref, onMounted } from "vue";
import { usePostStore } from "@/store";
import CrudModal from "@/components/common/CrudModal.vue";
import PixelButton from "@/components/ui/PixelButton.vue";
import type { PostResponse } from "@/types";
import { useInfiniteList } from "@/composables";

const postStore = usePostStore();

const showModal = ref(false);
const modalMode = ref<"create" | "update">("create");
const editingItem = ref<PostResponse | null>(null);

const {
    items: items,
    loading,
    hasMore,
    loadMore,
    refresh,
} = useInfiniteList({
    fetchFn: (params: { skip?: number; limit?: number }) =>
        postStore.getPosts(params),
    pageSize: 5,
});

onMounted(async () => {
    await refresh();
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
        seriesId: item.series?.id ?? "",
        seriesOrder: item.seriesOrder ?? "",
    };
    showModal.value = true;
}

async function handleModalSuccess() {
    showModal.value = false;
    await postStore.getPosts();
    items.value = postStore.posts;
}

async function handleDelete(item: any) {
    if (!confirm(`确定删除 "${item.title}" 吗？`)) return;
    try {
        await postStore.deletePost(item.id);
        await postStore.getPosts();
        items.value = postStore.posts;
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
                        <th class="p-4 text-left pixel-text">标题</th>
                        <th class="p-4 text-left pixel-text">分类</th>
                        <th class="p-4 text-left pixel-text">标签</th>
                        <th class="p-4 text-left pixel-text">创建时间</th>
                        <th class="p-4 text-left pixel-text">状态</th>
                        <th class="p-4 text-left pixel-text">操作</th>
                    </tr>
                </thead>
                <tbody>
                    <tr
                        v-for="item in items"
                        :key="item.id"
                        class="border-b-2 border-gray-200 hover:bg-gray-50 transition-colors"
                    >
                        <td class="p-4 font-medium truncate max-w-xs block">
                            {{ item.title }}
                        </td>
                        <td class="p-4">
                            <span
                                class="px-2 py-1 border-2 border-black text-xs"
                            >
                                {{ item.category.name }}
                            </span>
                        </td>
                        <td class="p-4">
                            <div class="flex flex-wrap gap-1">
                                <span
                                    v-for="tag in item.tags"
                                    :key="tag.id"
                                    class="px-2 py-0.5 bg-gold-light border border-black text-xs"
                                >
                                    {{ tag.name }}
                                </span>
                            </div>
                        </td>
                        <td class="p-4">{{ item.createdAt }}</td>
                        <td class="p-4">
                            <span
                                :class="`px-2 py-1 border-2 border-black  text-xs pixel-text`"
                            >
                                {{ item.published ? "已发布" : "未发布" }}
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

            <div
                v-if="hasMore && items.length > 0"
                class="flex justify-center mt-10 mb-4"
            >
                <button
                    class="px-8 py-3 ..."
                    :disabled="loading"
                    @click="loadMore()"
                >
                    <template v-if="loading"
                        >🔄 <PixelButton>加载中…</PixelButton></template
                    >
                    <template v-else>
                        <PixelButton
                            >📦 加载更多（已显示
                            {{ items.length }} 条）</PixelButton
                        >
                    </template>
                </button>
            </div>
            <div v-else class="flex justify-center mt-10 mb-4">
                <PixelButton>已经加载全部 {{ items.length }} 条</PixelButton>
            </div>
        </div>
    </div>
    <CrudModal
        v-if="showModal"
        module="posts"
        :mode="modalMode"
        :initial-data="editingItem"
        @success="handleModalSuccess"
        @close="showModal = false"
    />
</template>
