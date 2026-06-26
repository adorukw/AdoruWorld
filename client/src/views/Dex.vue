<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import Layout from '@/components/layout/Layout.vue'
import SearchInput from '@/components/ui/SearchInput.vue'
import DropdownMenu from '@/components/ui/DropdownMenu.vue'
import DexCard from '@/components/ui/DexCard.vue'
import PixelButton from '@/components/ui/PixelButton.vue'
import { dexCategories, dexStatuses } from '@/constants'
import type { DexCategory, DexStatus, DexStats } from '@/types'
import { useDexStore } from '@/store'
import { useInfiniteList } from '@/composables'

const dexStore = useDexStore()

const dexStats = ref<DexStats>({
    total: 0,
    byCategory: {},
    byStatus: {},
    averageRating: 0,
});

const { items: dexs, loading, hasMore, loadMore, refresh } = useInfiniteList({
    fetchFn: (params: {
        category?: string;
        status?: string;
        skip?: number;
        limit?: number;
    }) => dexStore.getDexs(params),
    pageSize: 12
})

onMounted(async () => {
    await refresh()
    await dexStore.getDexStats()
    dexStats.value = dexStore.dexStats
})

const selectedCategory = ref<DexCategory | 'all'>('all')
const selectedStatus = ref<DexStatus | 'all'>('all')
const searchQuery = ref('')
const viewMode = ref<'grid' | 'list'>('grid')

watch([selectedCategory, selectedStatus], async () => {
    refresh({
        category: selectedCategory.value === 'all' ? undefined : selectedCategory.value,
        status: selectedStatus.value === 'all' ? undefined : selectedStatus.value,
    })
})

const statusOptions = computed(() => {
    const options = [
        { label: '全部状态', value: 'all' }
    ]
    dexStatuses.forEach(s => {
        options.push({
            label: `${s.icon} ${s.name}`,
            value: s.id
        })
    })
    return options
})

// const getRatingStars = (rating: number) => {
//     if (rating === 0) return '☆☆☆☆☆☆☆☆☆☆'
//     return '★'.repeat(rating) + '☆'.repeat(10 - rating)
// }
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
                            <span class="text-4xl relative z-10">📖</span>
                        </div>
                    </div>
                    <h1 class="pixel-text text-2xl md:text-3xl mb-4 drop-shadow-sm">
                        图鉴 Dex
                    </h1>
                    <p class="pixel-text text-2xl! max-w-xl mx-auto">
                        记录我的读、看、玩、听、做
                    </p>
                </div>
            </div>
        </section>

        <section class="py-4 border-b-4  overflow-hidden relative">
            <div class="max-w-6xl mx-auto px-4 relative z-10">
                <div class="grid grid-cols-3 md:grid-cols-7 gap-3">
                    <div v-for="cat in dexCategories" :key="cat.id"
                        class="text-center p-3 cursor-pointer transition-all border-4" :class="selectedCategory === cat.id
                            ? ' shadow-md'
                            : 'border-transparent hover:bg-black/5'" :style="{
                                backgroundColor: selectedCategory === cat.id ? cat.bgColor : 'rgba(255,255,255,0.8)'
                            }" @click="selectedCategory = selectedCategory === cat.id ? 'all' : cat.id">
                        <div class="text-2xl mb-1">{{ cat.icon }}</div>
                        <div class="pixel-text text-xs" :style="{ color: cat.color }">{{ cat.name }}</div>
                        <div class="text-xs  mt-1">{{ dexStats.byCategory[cat.slug] || 0 }}</div>
                    </div>
                </div>
            </div>
        </section>

        <section class="py-8">
            <div class="max-w-6xl mx-auto px-4">
                <div class="flex flex-wrap items-center justify-between gap-4 mb-6">
                    <div class="flex items-center gap-4">
                        <SearchInput v-model="searchQuery" placeholder="搜索图鉴..." />
                        <DropdownMenu v-model="selectedStatus" :options="statusOptions" placeholder="全部状态"
                            class="text-sm py-2" width="w-48"></DropdownMenu>
                    </div>

                    <div class="flex items-center gap-2">
                        <button class="p-2 border-4  transition-all"
                            :class="viewMode === 'grid' ? 'bg-gold' : 'bg-white '" @click="viewMode = 'grid'">
                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
                            </svg>
                        </button>
                        <button class="p-2 border-4  transition-all"
                            :class="viewMode === 'list' ? 'bg-gold' : 'bg-white '" @click="viewMode = 'list'">
                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M4 6h16M4 10h16M4 14h16M4 18h16" />
                            </svg>
                        </button>
                    </div>
                </div>

                <div class="flex items-center gap-4 mb-6 p-4 bg-white border-4 ">
                    <div class="flex items-center gap-2">
                        <span class="pixel-text text-xs ">总计:</span>
                        <span class="pixel-text text-lg text-sky-dark">{{ dexStats.total }}</span>
                    </div>
                    <div class="w-px h-6 "></div>
                    <div class="flex items-center gap-2">
                        <span class="pixel-text text-xs">平均评分:</span>
                        <span class="pixel-text text-lg text-gold-dark">{{ dexStats.averageRating }}</span>
                    </div>
                    <div class="w-px h-6 "></div>
                    <div class="flex items-center gap-2">
                        <span class="pixel-text text-xs ">已完成:</span>
                        <span class="pixel-text text-lg text-grass-dark">{{ dexStats.byStatus.completed }}</span>
                    </div>
                </div>

                <!-- Grid 视图 -->
                <div v-if="viewMode === 'grid'"
                    class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-4 gap-4">
                    <DexCard v-for="(entry, index) in dexs" :key="entry.id" :entry="entry" :index="index"
                        :view-mode="'grid'" />
                </div>

                <!-- List 视图 -->
                <div v-else class="space-y-3">
                    <DexCard v-for="(entry, index) in dexs" :key="entry.id" :entry="entry" :index="index"
                        :view-mode="'list'" />
                </div>

                <div v-if="!searchQuery && hasMore && dexs.length > 0" class="flex justify-center mt-10 mb-4">
                    <button class="px-8 py-3 ..." :disabled="loading" @click="loadMore()">
                        <template v-if="loading">🔄 <PixelButton>加载中…</PixelButton></template>
                        <template v-else>
                            <PixelButton>📦 加载更多（已显示 {{ dexs.length }} 条）</PixelButton>
                        </template>
                    </button>
                </div>
                <div v-else class="flex justify-center mt-10 mb-4">
                    <PixelButton>已经加载全部 {{ dexs.length }} 条</PixelButton>
                </div>

                <div v-if="dexs.length === 0" class="text-center py-16">
                    <div class="text-6xl mb-4">🔍</div>
                    <h2 class="pixel-text text-lg ">没有找到记录</h2>
                    <p class="">尝试更换筛选条件或搜索其他关键词</p>
                </div>
            </div>
        </section>
    </Layout>
</template>

<style scoped></style>
