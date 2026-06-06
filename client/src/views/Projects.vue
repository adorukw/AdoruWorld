<script setup lang="ts">
import { computed } from 'vue'
import Layout from '@/components/layout/Layout.vue'
import PostCard from '@/components/ui/PostCard.vue'
import PixelButton from '@/components/ui/PixelButton.vue'
import SkyCloud from '@/components/ui/SkyCloud.vue'
import { projects } from '@/constants/mock'

const statusColors = {
    'completed': { bg: 'bg-grass', text: '已完成' },
    'in-progress': { bg: 'bg-gold', text: '进行中' },
    'archived': { bg: 'bg-gray', text: '已归档' }
}

const groupedProjects = computed(() => ({
    'in-progress': projects.filter(p => p.status === 'in-progress'),
    'completed': projects.filter(p => p.status === 'completed'),
    'archived': projects.filter(p => p.status === 'archived')
}))
</script>

<template>
    <Layout>
        <section class="relative py-16 overflow-hidden border-b-2 border-dashed">
            <SkyCloud></SkyCloud>
            <div class="max-w-6xl mx-auto px-4 text-center relative z-10">
                <h1 class="pixel-text text-2xl  mb-4 drop-shadow-sm">🚀 项目</h1>
                <p class="t">我的个人项目和作品集</p>
            </div>
        </section>

        <section class="py-12">
            <div class="max-w-6xl mx-auto px-4">
                <div v-if="groupedProjects['in-progress'].length" class="mb-12">
                    <h2 class="pixel-text text-lg  mb-6 flex items-center gap-3 border-4">
                        <span class="text-gold-dark ">⚡</span> 进行中
                    </h2>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div v-for="project in groupedProjects['in-progress']" :key="project.id">
                            <PostCard :title="project.name" :cover-image="project.image" :tags="project.tech"
                                :description="project.description" />
                            <div class="flex gap-3 ">
                                <PixelButton v-if="project.link">
                                    <a :href="project.link" target="_blank">访问</a>
                                </PixelButton>
                                <PixelButton v-if="project.github" target="_blank">
                                    <a :href="project.github" target="_blank">github</a>
                                </PixelButton>
                            </div>
                        </div>
                    </div>
                </div>

                <div v-if="groupedProjects['completed'].length" class="mb-12">
                    <h2 class="pixel-text text-lg  mb-6 flex items-center gap-3">
                        <span class="text-grass-dark">✅</span> 已完成
                    </h2>
                    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        <div v-for="project in groupedProjects['completed']" :key="project.id">
                            <PostCard :title="project.name" :cover-image="project.image" :tags="project.tech"
                                :description="project.description" />
                            <div class="flex gap-3 ">
                                <PixelButton v-if="project.link">
                                    <a :href="project.link" target="_blank">访问</a>
                                </PixelButton>
                                <PixelButton v-if="project.github" target="_blank">
                                    <a :href="project.github" target="_blank">github</a>
                                </PixelButton>
                            </div>
                        </div>
                    </div>
                </div>

                <div v-if="groupedProjects['archived'].length">
                    <h2 class="pixel-text text-lg  mb-6 flex items-center gap-3">
                        <span class="">📦</span> 已归档
                    </h2>
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div v-for="project in groupedProjects['archived']" :key="project.id"
                            class="pixel-card p-4 opacity-75 hover:opacity-100 transition-opacity">
                            <h3 class="text-sm  mb-1">{{ project.name }}</h3>
                            <p class="text-xs t">{{ project.description }}</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </Layout>
</template>

<style scoped>
.cloud {
    filter: blur(2px);
}
</style>
