<script setup lang="ts">
import { useRouter } from 'vue-router'
import TagBadge from '../ui/TagBadge.vue'
import { usePostStore, usePostTagStore, usePostCategoryStore } from '@/store'

const postStore = usePostStore()
const tagStore = usePostTagStore()
const categoryStore = usePostCategoryStore()
const { recentPosts } = postStore
const { postTags } = tagStore
const { postCategories } = categoryStore

const router = useRouter()

const handleTagClick = (tagSlug: string) => {
    router.push({
        path: '/post-search',
        query: { tag: tagSlug }
    })
}

const handleCategoryClick = (categorySlug: string) => {
    router.push({
        path: '/post-search',
        query: { category: categorySlug }
    })
}
</script>

<template>
    <aside class="space-y-6">
        <div class="border-2 border-gray-800 bg-white p-5 shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]">
            <div class="flex items-center gap-4 mb-4">
                <div class="relative">
                    <!-- <img
            :src="store.authorInfo.avatar"
            :alt="store.authorInfo.name"
            class="w-16 h-16 rounded-full border-4 border-gray-800 shadow-md"
          /> -->
                    <div
                        class="absolute inset-0 rounded-full bg-linear-to-b from-white/40 to-transparent pointer-events-none">
                    </div>
                </div>
                <div>
                    <h3 class="font-bold text-gray-900 text-xl font-mono">王</h3>
                    <p class="text-xl text-gray-600">中国</p>
                </div>
            </div>
            <p class="text-xl text-gray-600 leading-relaxed">
                范德萨龙卷风昆德拉数据反馈力度撒娇快乐
            </p>
        </div>

        <div class="border-2 border-gray-800 bg-white p-5 shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]">
            <h3 class="font-bold text-gray-900 text-xl mb-4 flex items-center gap-2 font-mono">
                <span class="text-blue-600">📁</span> 分类
            </h3>
            <div class="space-y-2">
                <div v-for="category in postCategories" :key="category.id"
                    class="flex items-center justify-between p-2 border-2 border-transparent hover:border-gray-800 hover:bg-yellow-100/50 cursor-pointer transition-all duration-100 rounded"
                    @click="handleCategoryClick(category.slug)">
                    <div class="flex items-center gap-2">
                        <span>{{ category.icon }}</span>
                        <span class="text-xl">{{ category.name }}</span>
                    </div>
                    <span class="text-xl text-gray-600 bg-gray-200 px-2 py-1 border-2 border-gray-800 shadow-sm">
                        {{ category.count }}
                    </span>
                </div>
            </div>
        </div>

        <div class="border-2 border-gray-800 bg-white p-5 shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]">
            <h3 class="font-bold text-gray-900 text-xl mb-4 flex items-center gap-2 font-mono">
                <span class="text-yellow-600">🏷️</span> 热门标签
            </h3>
            <div class="flex flex-wrap gap-2">
                <TagBadge v-for="tag in postTags.slice(0, 10)" :key="tag.id" :name="tag.name" :color="tag.color"
                    :count="tag.count" @click="handleTagClick(tag.slug)" />
            </div>
        </div>

        <div class="border-2 border-gray-800 bg-white p-5 shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]">
            <h3 class="font-bold text-gray-900 text-xl mb-4 flex items-center gap-2 font-mono">
                <span class="text-red-600">🔥</span> 最新文章
            </h3>
            <div class="space-y-3">
                <router-link v-for="post in recentPosts" :key="post.id" :to="`/post/${post.slug}`"
                    class="block p-2 border-2 border-transparent hover:border-gray-800 hover:bg-blue-100 transition-all duration-100 rounded">
                    <h4 class="text-xl text-gray-900 line-clamp-2 hover:text-blue-600">
                        {{ post.title }}
                    </h4>
                    <p class="text-xl text-gray-600 mt-1">{{ post.createdAt }}</p>
                </router-link>
            </div>
        </div>
    </aside>
</template>

<style>
.line-clamp-2 {
    display: -webkit-box;
    line-clamp: 2;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}
</style>