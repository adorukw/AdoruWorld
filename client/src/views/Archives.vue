<script setup lang="ts">
import { computed } from 'vue'
import Layout from '@/components/layout/Layout.vue'
import SkyCloud from '@/components/ui/SkyCloud.vue'
import { usePostStore } from '@/store'

const postStore = usePostStore()
const { allPosts } = postStore

const groupedPosts = computed(() => {
    const groups: { [key: string]: { year: number; month: number; posts: typeof allPosts }[] } = {}

    const sortedPosts = [...allPosts].sort((a, b) =>
        new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()
    )

    sortedPosts.forEach(post => {
        const date = new Date(post.createdAt)
        const year = date.getFullYear()
        const month = date.getMonth() + 1

        if (!groups[year]) {
            groups[year] = []
        }

        let monthGroup = groups[year].find(g => g.month === month)
        if (!monthGroup) {
            monthGroup = { year, month, posts: [] }
            groups[year].push(monthGroup)
        }

        monthGroup.posts.push(post)
    })

    return Object.entries(groups)
        .sort((a, b) => Number(b[0]) - Number(a[0]))
        .map(([year, months]) => ({
            year: Number(year),
            months: months.sort((a, b) => b.month - a.month)
        }))
})

const monthNames = ['一月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '十一月', '十二月']
</script>

<template>
    <Layout>
        <section class="relative py-16 overflow-hidden border-b-2 border-dashed">
            <SkyCloud></SkyCloud>>

            <div class="max-w-6xl mx-auto px-4 text-center relative z-10">
                <h1 class=" text-2xl  mb-4 drop-shadow-sm">📚 归档</h1>
                <p class="">按时间浏览所有文章</p>
            </div>
        </section>

        <section class="py-12">
            <div class="max-w-4xl mx-auto px-4">
                <div v-for="yearGroup in groupedPosts" :key="yearGroup.year" class="mb-12">
                    <div class="flex items-center gap-4 mb-6">
                        <div
                            class="pixel-card border-2 border-gray-800 bg-white p-5 shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]">
                            <span class=" text-lg ">{{ yearGroup.year }}</span>
                        </div>
                        <div class="flex-1 h-1 /20"></div>
                    </div>

                    <div v-for="monthGroup in yearGroup.months" :key="`${yearGroup.year}-${monthGroup.month}`"
                        class="mb-8">
                        <h3 class=" text-sm  mb-4 flex items-center gap-2">
                            <span class="text-sky-dark">◆</span>
                            {{ monthNames[monthGroup.month - 1] }}
                            <span class="text-xs ">({{ monthGroup.posts.length }}篇)</span>
                        </h3>

                        <div class="space-y-4 ml-4 border-l-4 border-gold pl-6">
                            <router-link v-for="post in monthGroup.posts" :key="post.id" :to="`/post/${post.slug}`"
                                class="pixel-card block border-2 border-gray-800 bg-white p-5 shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]  hover:translate-x-2 transition-transform">
                                <div class="flex flex-wrap items-start justify-between gap-2">
                                    <div class="flex-1">
                                        <h4 class=" font-medium hover:text-sky-dark transition-colors">
                                            {{ post.title }}
                                        </h4>
                                        <div class="flex flex-wrap gap-2 mt-2">
                                            <span v-for="tag in post.tags.slice(0, 3)" :key="tag.id"
                                                class="text-xs px-2 py-0.5 bg-sky-light/50 rounded ">
                                                #{{ tag.name }}
                                            </span>
                                        </div>
                                    </div>
                                    <div class="text-right text-xs ">
                                        <div>{{ post.createdAt }}</div>
                                        <div class="mt-1">{{ post.readingTime }} 分钟</div>
                                    </div>
                                </div>
                            </router-link>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </Layout>
</template>

<style scoped></style>
