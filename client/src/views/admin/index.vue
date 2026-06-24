<script setup lang="ts">
import { ref } from 'vue'
import Layout from '@/components/layout/Layout.vue'
import PostsTable from './PostsTable.vue'
import PostCategoriesTable from './PostCategoriesTable.vue'
import PostTagsTable from './PostTagsTable.vue'
import DexsTable from './DexsTable.vue'
import DexGenresTable from './DexGenresTable.vue'
import MediasTable from './MediasTable.vue'
import MediaTagsTable from './MediaTagsTable.vue'
type TabId = 'posts' | 'postCategories' | 'postTags' | 'dexs' | 'dexGenres' | 'medias' | 'mediaTags'
interface TabItem {
    id: TabId
    icon: string
    label: string
}

const activeTab = ref<TabId>('posts')
const tabs: TabItem[] = [
    { id: 'posts', icon: '📝', label: '文章' },
    { id: 'postCategories', icon: '📁', label: '文章分类' },
    { id: 'postTags', icon: '🏷️', label: '文章标签' },
    { id: 'dexs', icon: '📖', label: '图鉴' },
    { id: 'dexGenres', icon: '🎭', label: '图鉴题材' },
    { id: 'medias', icon: '🖼️', label: '媒体库' },
    { id: 'mediaTags', icon: '🏷️', label: '媒体标签' },
]
</script>

<template>
    <Layout>
        <section class="relative py-4 overflow-hidden border-b-4">
            <div class="max-w-6xl mx-auto px-4 relative z-10">
                <div class="text-center">
                    <div class="inline-block mb-4">
                        <div class="w-20 h-20 border-4  mx-auto mb-4
            flex items-center justify-center shadow-lg relative overflow-hidden">
                            <div class="absolute inset-0 bg-linear-to-b from-white/30 to-transparent"></div>
                            <span class="text-4xl relative z-10">⚙️</span>
                        </div>
                    </div>
                    <h1 class="pixel-text text-2xl md:text-3xl mb-4 drop-shadow-sm">管理 Admin</h1>
                    <p class="pixel-text text-2xl! max-w-xl mx-auto">管理文章、分类、标签、图鉴、媒体等。</p>
                </div>
            </div>
        </section>

        <section class="py-4 border-b-4  overflow-hidden relative">
            <div class="max-w-6xl mx-auto px-4 relative z-10">
                <div class="flex flex-wrap gap-2 p-4 bg-white/80 border-4 border-black">
                    <button v-for="tab in tabs" :key="tab.id" @click="activeTab = tab.id"
                        class="pixel-btn px-4 py-2 transition-all"
                        :class="activeTab === tab.id ? 'bg-sky text-white' : 'bg-white hover:bg-gray-100'">
                        {{ tab.icon }} {{ tab.label }}
                    </button>
                </div>
            </div>
        </section>

        <section class="py-8">
            <div class="max-w-6xl mx-auto px-4">
                <PostsTable v-if="activeTab === 'posts'" />
                <PostCategoriesTable v-if="activeTab === 'postCategories'" />
                <PostTagsTable v-if="activeTab === 'postTags'" />
                <DexsTable v-if="activeTab === 'dexs'" />
                <DexGenresTable v-if="activeTab === 'dexGenres'" />
                <MediasTable v-if="activeTab === 'medias'" />
                <MediaTagsTable v-if="activeTab === 'mediaTags'" />
            </div>
        </section>
    </Layout>
</template>

<style scoped>
.pixel-btn-small:hover {
    transform: translate(-1px, -1px);
    box-shadow: 2px 2px 0px 0px rgba(0, 0, 0, 1);
}

.pixel-btn-small:active {
    transform: translate(1px, 1px);
    box-shadow: none;
}

/* 表格行悬停效果 */
tbody tr:hover {
    background-color: rgba(135, 206, 235, 0.1);
}

/* 模态框动画 */
.fixed {
    animation: fadeIn 0.2s ease-out;
}

@keyframes fadeIn {
    from {
        opacity: 0;
    }

    to {
        opacity: 1;
    }
}
</style>