<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import Layout from '@/components/layout/Layout.vue'
import { dexCategories, dexStatuses } from '@/constants'
import { useDexStore } from '@/store'
import type { DexResponse } from '@/types'
import PixelButton from '@/components/ui/PixelButton.vue'

const dexStore = useDexStore()

const route = useRoute()

const dex = ref<DexResponse | null>(null)
const relatedDexs = ref<DexResponse[]>([])

watch(() => route.params.slug, async (newSlug) => {
    if (!newSlug) return
    const slug = newSlug as string

    await dexStore.getDexBySlug(slug)
    dex.value = dexStore.currentDex

    await dexStore.getRelatedDexs(slug)
    relatedDexs.value = dexStore.relatedDexs
}, { immediate: true })

const dexIndex = computed(() => {
    if (!dex.value) return 0
    return dexStore.dexs.findIndex(e => e.id === dex.value!.id) + 1
})

const categoryInfo = computed(() => {
    return dexCategories.find(c => c.id === dex.value?.category)
})
const statusInfo = computed(() => {
    return dexStatuses.find(s => s.id === dex.value?.status)
})

const getRatingStars = (rating: number) => {
    if (rating === 0) return '☆☆☆☆☆☆☆☆☆☆'
    return '★'.repeat(rating) + '☆'.repeat(10 - rating)
}

</script>

<template>
    <Layout>
        <template v-if="dex">
            <section class="relative py-4 overflow-hidden">
                <div class="absolute inset-0" :style="{ backgroundColor: categoryInfo?.bgColor }"></div>

                <div class="max-w-4xl mx-auto px-4 relative z-10">
                    <div class="flex items-center gap-2 mb-4">
                        <router-link to="/dex">
                            <span class=" text-sm ">
                                <PixelButton>返回图鉴</PixelButton>
                            </span>
                        </router-link>
                    </div>
                </div>
            </section>

            <section class="py-8">
                <div class="max-w-4xl mx-auto px-4">
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                        <div class="md:col-span-1">
                            <div class="pixel-card overflow-hidden sticky top-24">
                                <div class="relative aspect-3/4">
                                    <img :src="dex.coverImage" :alt="dex.title" class="w-full h-full object-coverImage"
                                        style="image-rendering: auto;" />
                                    <div class="absolute inset-0 bg-linear-to-t from-black/30 to-transparent"></div>

                                    <div class="absolute top-3 left-3 right-3 flex justify-between">
                                        <span class="text-sm px-3 py-1 border-3 text-white pixel-text"
                                            :style="{ backgroundColor: categoryInfo?.color }">
                                            {{ categoryInfo?.icon }} {{ categoryInfo?.name }}
                                        </span>
                                    </div>

                                    <div class="absolute bottom-3 left-3 right-3">
                                        <div class="bg-white/90 backdrop-blur-sm rounded border-3p-2">
                                            <div class=" text-xs">
                                                #{{ String(dexIndex).padStart(3, '0') }}
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <div v-if="dex.summary" class="pixel-card p-5 mt-6">
                                <h2 class=" text-sm mb-3 flex items-center gap-2">
                                    <span>📖</span> 作品简介
                                </h2>
                                <p class="text-sm leading-relaxed whitespace-pre-line">
                                    {{ dex.summary }}
                                </p>
                            </div>
                        </div>

                        <div class="md:col-span-2">
                            <div class="pixel-card p-6 mb-6">
                                <div class="flex items-start justify-between gap-4 mb-4">
                                    <div>
                                        <h1 class=" text-xl mb-2">{{ dex.title }}</h1>
                                        <p v-if="dex.originalTitle" class="">
                                            {{ dex.originalTitle }}
                                        </p>
                                    </div>
                                    <span class="shrink-0 text-sm px-4 py-2 border-4  text-white pixel-text"
                                        :style="{ backgroundColor: statusInfo?.color }">
                                        {{ statusInfo?.icon }} {{ statusInfo?.name }}
                                    </span>
                                </div>

                                <div v-if="dex.rating > 0" class="mb-6">
                                    <div class="flex items-center gap-3 mb-2">
                                        <span class=" text-xs">评分</span>
                                        <span class=" text-lg text-gold-dark">{{ dex.rating }}/10</span>
                                    </div>
                                    <div class="text-gold text-lg tracking-wider">
                                        {{ getRatingStars(dex.rating) }}
                                    </div>
                                </div>

                                <div class="grid grid-cols-2 gap-4 mb-6">
                                    <div v-if="dex.creator" class="bg-[#7893e9] p-3 rounded border-2 ">
                                        <div class=" text-xs mb-1">创作者</div>
                                        <div class="text-sm">{{ dex.creator }}</div>
                                    </div>
                                    <div v-if="dex.year" class="bg-[#d79769] p-3 rounded border-2">
                                        <div class=" text-xs mb-1">年份</div>
                                        <div class="text-sm ">{{ dex.year }}</div>
                                    </div>
                                    <div v-if="dex.startDate" class="bg-[#e66a6a] p-3 rounded border-2">
                                        <div class=" text-xs mb-1">开始日期</div>
                                        <div class="text-sm ">{{ dex.startDate }}</div>
                                    </div>
                                </div>

                                <div v-if="dex.genres?.length" class="mb-6">
                                    <div class=" text-xs mb-3">题材</div>
                                    <div class="flex flex-wrap gap-2">
                                        <span v-for="g in dex.genres" :key="g.id"
                                            class="colortext-sm px-3 py-1 bg-gold-light border-2  rounded"
                                            :style="{ backgroundColor: g.color }">
                                            {{ g.name }}
                                        </span>
                                    </div>
                                </div>
                            </div>

                            <div v-if="dex.comment" class="pixel-card p-6 mb-6">
                                <h2 class=" text-sm mb-4 flex items-center gap-2">
                                    <span>💬</span> 短评
                                </h2>
                                <p class=" leading-relaxed">{{ dex.comment }}</p>
                            </div>

                            <div v-if="relatedDexs.length" class="pixel-card p-6">
                                <h2 class=" text-sm mb-4 flex items-center gap-2">
                                    <span>🔗</span> 相关推荐
                                </h2>
                                <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
                                    <router-link v-for="related in relatedDexs" :key="related.id"
                                        :to="`/dex/${related.slug}`" class="group">
                                        <div class="aspect-3/4 overflow-hidden rounded border-2 mb-2">
                                            <img :src="related.coverImage" :alt="related.title"
                                                class="w-full h-full object-coverImage transition-transform group-hover:scale-110"
                                                style="image-rendering: auto;" />
                                        </div>
                                        <div class=" text-xs line-clamp-1 group-hover:text-sky-dark">
                                            {{ related.title }}
                                        </div>
                                    </router-link>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
        </template>

        <template v-else>
            <div class="min-h-[60vh] flex items-center justify-center">
                <div class="text-center">
                    <div class="text-6xl mb-4">🔍</div>
                    <h2 class=" text-xl mb-4">记录未找到</h2>
                    <p class=" mb-6">这个条目可能不存在或已被删除。</p>
                    <router-link to="/dex" class="pixel-btn bg-sky text-white">
                        返回图鉴
                    </router-link>
                </div>
            </div>
        </template>
    </Layout>
</template>
