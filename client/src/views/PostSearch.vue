<script setup lang="ts">
import { watch, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import Layout from '@/components/layout/Layout.vue'
import PostCard from '@/components/ui/PostCard.vue'
import { usePostStore } from '@/store'

const postStore = usePostStore()
const router = useRouter()
const route = useRoute()

const loadPosts = () => {
    if (Object.keys(route.query).length === 0) {
        router.push('/')
        return
    }

    const params: any = {
        published: true
    }

    if (route.query.category) {
        params.category = route.query.category as string
    }

    if (route.query.tag) {
        params.tag = route.query.tag as string
    }

    params.skip = ((Number(route.query.page) || 1) - 1) * 10
    params.limit = 10

    postStore.getPosts(params)
}


loadPosts()
const posts = computed(() => postStore.posts)

watch(
    () => route.query,
    () => loadPosts(),
    { immediate: true }
)

const clearFilters = () => {
    router.push('/')
}
</script>

<template>
    <Layout>
        <section class="relative py-16 overflow-hidden">

            <div class="max-w-6xl mx-auto px-4 text-center relative z-10">
                <h1 class="pixel-text text-2xl  mb-4 drop-shadow-sm">🔍 搜索</h1>
                <p class="">查找你感兴趣的内容</p>
            </div>
        </section>

        <section class="py-12">
            <div class="max-w-6xl mx-auto px-4">
                <div class="mb-8">
                    <div class="flex flex-wrap gap-2 items-center">
                        <span class="text-sm ">搜索条件：</span>
                        <span v-if="route.query.keyword" class="tag bg-sky text-white">
                            关键词: {{ route.query.keyword }}
                            <button @click="router.push({ query: { keyword: undefined } })" class="right-20 w-6 h-6 flex
                             items-center justify-center bg-gray-200 hover:bg-gray-300 border-2 border-black"
                                title="清空">
                                ✕
                            </button>
                        </span>
                        <span v-if="route.query.category">
                            分类: {{ route.query.category }}
                            <button @click="router.push({ query: { category: undefined } })" class="right-20 w-6 h-6 flex
                             items-center justify-center bg-gray-200 hover:bg-gray-300 border-2 border-black"
                                title="清空">
                                ✕
                            </button>
                        </span>
                        <span v-if="route.query.tag" class="tag bg-sky-light ">
                            标签: {{ route.query.tag }}
                            <button @click="router.push({ query: { tag: undefined } })" class="right-20 w-6 h-6 flex
                             items-center justify-center bg-gray-200 hover:bg-gray-300 border-2 border-black"
                                title="清空">
                                ✕
                            </button>
                        </span>
                        <button v-if="route.query.category || route.query.tag" @click="clearFilters"
                            class="text-xs text-sky-dark hover:underline">
                            清除全部
                        </button>
                    </div>
                </div>

                <div v-if="posts.length">
                    <p class="text-sm  mb-6">
                        找到 {{ posts.length }} 篇相关文章
                    </p>
                    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        <router-link v-for="post in posts" :key="post.id" :to="`/post/${post.slug}`" class="block">
                            <PostCard :title="post.title" :cover-image="post.coverImage"
                                :tags="post.tags.map(t => t.name)" :category="post.category.name" :date="post.createdAt"
                                :reading-time="post.readingTime" :views="post.views" />
                        </router-link>
                    </div>
                </div>

                <div v-else class="text-center py-16">
                    <div class="text-6xl mb-4">🔍</div>
                    <h2 class="pixel-text text-lg  mb-4">没有找到相关内容</h2>
                    <p class=" mb-6">试试其他关键词或浏览全部分类</p>
                    <div class="flex justify-center gap-4">
                        <router-link to="/categories" class="pixel-btn bg-sky text-white hover:bg-sky-dark">
                            浏览分类
                        </router-link>
                        <router-link to="/archives" class="pixel-btn bg-gold  hover:bg-gold-dark">
                            浏览归档
                        </router-link>
                    </div>
                </div>
            </div>
        </section>
    </Layout>
</template>

<style scoped></style>
