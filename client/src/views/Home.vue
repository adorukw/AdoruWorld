<template>
    <Layout>
        <section class="relative py-16 md:py-24 overflow-hidden border-b-2 border-dashed shadow-[0_2px_0_0_#000]
        min-h-[calc(100vh-4rem)]">
            <div class="absolute inset-0 wallpaper"></div>
            <div class="max-w-6xl mx-auto px-4 relative z-10">
                <div class="text-center">
                    <div class="inline-block mb-6">
                        <div class="w-24 h-24 bg-gold rounded-full border-4 mx-auto mb-4
                        flex items-center justify-center float-animation shadow-lg relative overflow-hidden">
                            <div class="absolute inset-0 bg-linear-to-b from-white/40 to-transparent"></div>
                            <span class=" font-bold text-4xl relative z-10">A</span>
                        </div>
                    </div>
                    <h1 class=" text-2xl md:text-4xl  mb-4 drop-shadow-sm">
                        AdoruWorld
                    </h1>
                    <p class=" text-lg md:text-xl max-w-2xl mx-auto mb-6">
                        口袋妖怪风格的像素艺术个人博客
                    </p>
                    <p class="text-sm max-w-xl mx-auto">
                        探索技术、生活、游戏与创意的像素世界
                    </p>
                </div>
            </div>
        </section>

        <section class="py-12">
            <div class="max-w-6xl mx-auto px-4">
                <div class="flex items-center gap-3 mb-8">
                    <span class="text-2xl">⭐</span>
                    <h2 class=" text-lg ">精选文章</h2>
                </div>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-12">
                    <router-link v-for="post in featuredPosts" :key="post.id" :to="`/post/${post.slug}`" class="block">
                        <PostCard :title="post.title" :cover-image="post.coverImage"
                            :tags="post.tags.map(tag => tag.name)" :category="post.category.name" :date="post.createdAt"
                            :reading-time="post.readingTime" :views="post.views" :featured="post.featured" />
                    </router-link>
                </div>

                <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
                    <div class="lg:col-span-2">
                        <div class="flex items-center gap-3 mb-6">
                            <span class="text-2xl">📝</span>
                            <h2 class=" text-lg ">最新文章</h2>
                        </div>
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <router-link v-for="post in recentPosts" :key="post.id" :to="`/post/${post.slug}`"
                                class="block">
                                <PostCard :title="post.title" :cover-image="post.coverImage"
                                    :tags="post.tags.map(tag => tag.name)" :category="post.category.name"
                                    :date="post.createdAt" :reading-time="post.readingTime" :views="post.views" />
                            </router-link>
                        </div>
                        <div class="mt-8 text-center">
                            <router-link to="/archives" class="text-white!">
                                <PixelButton>
                                    查看全部文章
                                </PixelButton>
                            </router-link>

                        </div>

                    </div>

                    <div class="lg:col-span-1">
                        <Sidebar />
                    </div>
                </div>
            </div>
        </section>

    </Layout>
</template>

<script setup lang="ts">
import Layout from "@/components/layout/Layout.vue"
import Sidebar from "@/components/layout/Sidebar.vue"
import PostCard from "@/components/ui/PostCard.vue"
import PixelButton from "@/components/ui/PixelButton.vue"
import { usePostStore } from "@/store"

const postStore = usePostStore()
const { featuredPosts, recentPosts } = postStore
</script>

<style scoped>
.wallpaper {
    background-image: url('../assets/picture/夏天与未白镇.gif');
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}
</style>