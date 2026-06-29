<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Layout from '@/components/layout/Layout.vue'
import SearchInput from '@/components/ui/SearchInput.vue'
import SearchResultCard from '@/components/ui/SearchResultCard.vue'
import { useSearchStore } from '@/store'
import type { SearchResultItem } from '@/types'

const route = useRoute()
const router = useRouter()
const store = useSearchStore()

const keyword = ref('')
const selectedType = ref<string | undefined>(undefined)

const typeOptions = [
    { value: undefined, label: '全部', icon: '🔍' },
    { value: 'post', label: '文章', icon: '📝' },
    { value: 'dex', label: '图鉴', icon: '📖' },
    { value: 'media', label: '媒体', icon: '📁' },
]

const doSearch = async () => {
    if (!keyword.value.trim()) return
    await store.search(keyword.value, selectedType.value)

    // 同步到 URL（让用户可分享/收藏搜索页）
    router.replace({
        query: {
            q: keyword.value,
            ...(selectedType.value ? { type: selectedType.value } : {}),
        },
    })
}

// const routerLink = computed(() => {
//     const { type, slug } = props.item
//     if (type === 'post') return `/posts/${slug}`
//     if (type === 'dex') return `/dexes/${slug}`
//     return '/admin/medias'
// })

const getRouterLink = (item: SearchResultItem) => {
    const { type, slug } = item
    if (type === 'post') return `/post/${slug}`
    if (type === 'dex') return `/dex/${slug}`
    return '/admin/medias'
}

const switchType = (type: string | undefined) => {
    selectedType.value = type
    doSearch()
}

// 从 URL 恢复搜索
onMounted(() => {
    if (route.query.q) {
        keyword.value = route.query.q as string
        selectedType.value = route.query.type as string | undefined
        doSearch()
    }
})

watch(
    () => route.query.q,
    (q) => {
        if (q && q !== keyword.value) {
            keyword.value = q as string
            doSearch()
        }
    },
)
</script>

<template>
    <Layout>
        <!-- 搜索头部 -->
        <section class="relative py-12 overflow-hidden">
            <div class="max-w-3xl mx-auto px-4 text-center relative z-10">
                <h1 class="pixel-text text-2xl mb-4">🔍 全局搜索</h1>
                <p class="text-gray-600 mb-6">
                    输入关键词，搜文章、图鉴、媒体——什么都有
                </p>

                <!-- 搜索输入框 -->
                <SearchInput v-model="keyword" placeholder="输入关键词搜索…" button-text="搜索" @search="doSearch" />
            </div>
        </section>

        <!-- 筛选栏 -->
        <section class="py-4">
            <div class="max-w-3xl mx-auto px-4">
                <div class="flex flex-wrap gap-2 justify-center">
                    <button v-for="opt in typeOptions" :key="opt.value || 'all'" @click="switchType(opt.value)"
                        class="px-4 py-2 border-2 border-black text-sm transition-all" :class="{
                            'bg-sky-500 text-white shadow-[4px_4px_0px_0px_rgba(0,0,0,0.8)]':
                                selectedType === opt.value,
                            'bg-white text-black shadow-[2px_2px_0px_0px_rgba(0,0,0,0.5)]':
                                selectedType !== opt.value,
                        }">
                        {{ opt.icon }} {{ opt.label }}
                    </button>
                </div>
            </div>
        </section>

        <!-- 结果区 -->
        <section class="py-8">
            <div class="max-w-3xl mx-auto px-4">
                <!-- 加载中 -->
                <div v-if="store.loading" class="text-center py-16">
                    <div class="text-4xl mb-4 animate-pulse">⏳</div>
                    <p>搜索中……</p>
                </div>

                <!-- 结果数量 -->
                <div v-else-if="store.items.length > 0" class="mb-6 text-sm text-gray-500">
                    共找到
                    <strong class="text-black">{{ store.total }}</strong> 条结果
                    <span v-if="store.query">（关键词：{{ store.query }}）</span>
                </div>

                <!-- 结果列表 -->
                <div v-if="store.items.length > 0" class="space-y-4">
                    <router-link v-for="item in store.items" :key="item.id" :to="getRouterLink(item)">
                        <SearchResultCard :key="item.id" :item="item" />
                    </router-link>

                    <!-- 加载更多 -->
                    <div v-if="store.items.length < store.total" class="text-center">
                        <button @click="store.loadMore()" :disabled="store.loading"
                            class="pixel-btn px-6 py-2 bg-gray-800 text-white border-2 border-black">
                            {{ store.loading ? '加载中…' : '加载更多' }}
                        </button>
                    </div>
                </div>

                <!-- 无结果 -->
                <div v-else-if="!store.loading && keyword" class="text-center py-16">
                    <div class="text-6xl mb-4">🔍</div>
                    <h2 class="text-lg font-bold mb-2">没有找到相关内容</h2>
                    <p class="text-gray-500 mb-6">
                        试试其他关键词吧
                    </p>
                </div>

                <!-- 初次进入未搜索 -->
                <div v-else-if="!keyword" class="text-center py-16 text-gray-400">
                    <div class="text-6xl mb-4">🐦</div>
                    <p>输入关键词开始搜索</p>
                </div>
            </div>
        </section>
    </Layout>
</template>