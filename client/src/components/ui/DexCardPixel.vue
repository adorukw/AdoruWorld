<!-- @ts-nocheck -->

<template>
    <!-- Grid 视图卡片 -->
    <router-link v-if="viewMode === 'grid'" :to="`/dex/${entry.slug}`" class="group block">
        <div class="pixel-card bg-yellow-300 p-4 w-full transition-all duration-200 hover:-translate-y-1 hover:shadow-[6px_6px_0px_0px_rgba(0,0,0,0.8)] relative"
            :style="cardStyle">
            <!-- 编号和分类 -->
            <div class="flex justify-between items-start mb-3">
                <span class=" text-gray-800 text-xl">#{{ formattedIndex }}</span>
                <!-- 状态徽章 -->
                <span class=" px-2 py-1 text-white" :style="statusBadgeStyle">
                    {{ statusInfo?.icon }}
                </span>
                <!-- 分类徽章 -->
                <span class=" px-2 py-1 text-white" :style="categoryBadgeStyle">
                    {{ categoryInfo?.icon }} {{ categoryInfo?.name }}
                </span>
            </div>

            <!-- 图片区域 -->
            <div class="aspect-square  overflow-hidden mb-4 flex items-center justify-center border-2 border-black ">
                <div class="w-full h-full bg-yellow-200 flex items-center justify-center relative">
                    <img :src="entry.coverImage" :alt="entry.title"
                        class="w-full h-full object-cover transition-transform duration-300 group-hover:scale-110"
                        style="image-rendering: auto;" />
                    <!-- 状态徽章 -->
                    <!-- <div class="absolute top-2 right-2">
                        <span class=" px-2 py-1 text-white" :style="statusBadgeStyle">
                            {{ statusInfo?.icon }}
                        </span>
                    </div> -->
                </div>
            </div>

            <!-- 标题和评分 -->
            <div class="h-14 flex items-center justify-center mb-2">
                <h3 class="text-lg text-center text-gray-900 line-clamp-2 overflow-hidden">
                    {{ entry.title }}
                </h3>
            </div>

            <!-- 评分 -->
            <div v-if="entry.rating > 0" class="text-center text-gold-dark  mb-2">
                {{ getRatingStars(entry.rating) }}
            </div>

            <!-- 查看详情按钮 -->
            <button
                class="w-full bg-red-500 hover:bg-red-600 text-white py-2  font-bold relative active:translate-x-[2px] active:translate-y-[2px] active:shadow-[2px_2px_0px_0px_rgba(0,0,0,0.8)] transition-all duration-100"
                :style="buttonStyle">
                查看详情
            </button>
        </div>
    </router-link>

    <!-- List 视图卡片 -->
    <router-link v-else :to="`/dex/${entry.slug}`" class="block">
        <div class="pixel-card p-4 flex gap-4 items-center bg-white">
            <!-- 封面图 -->
            <div class="w-35 h-35 flex-shrink-0 overflow-hidden rounded border-2 border-black">
                <img :src="entry.coverImage" :alt="entry.title" class="w-full h-full object-cover"
                    style="image-rendering: auto;" />
            </div>

            <!-- 内容区域 -->
            <div class="flex-1 min-w-0">
                <div class="flex items-center gap-2 mb-1">
                    <span class="pixel-text  text-pokemon-dark-gray">
                        #{{ formattedIndex }}
                    </span>
                    <h3 class="pixel-text  text-pokemon-black truncate">
                        {{ entry.title }}
                    </h3>
                </div>

                <p v-if="entry.originalTitle" class=" text-pokemon-dark-gray mb-2 truncate">
                    {{ entry.originalTitle }}
                </p>

                <div class="flex flex-wrap items-center gap-2">
                    <span class=" px-2 py-0.5 text-white" :style="categoryBadgeStyle">
                        {{ categoryInfo?.name }}
                    </span>
                    <span class=" px-2 py-0.5 text-white" :style="statusBadgeStyle">
                        {{ statusInfo?.name }}
                    </span>
                    <span v-if="entry.year" class=" text-pokemon-dark-gray">
                        {{ entry.year }}
                    </span>
                </div>
            </div>

            <!-- 右侧信息 -->
            <div class="flex-shrink-0 text-right">
                <div v-if="entry.rating > 0" class="text-gold-dark  mb-1">
                    {{ getRatingStars(entry.rating) }}
                </div>
                <div class="w-20 h-2 bg-pokemon-gray rounded-full overflow-hidden border mt-1">
                    <div class="h-full transition-all" :style="progressBarStyle" />
                </div>
            </div>
        </div>
    </router-link>
</template>

<script setup lang="ts">
// @ts-nocheck
import { computed } from 'vue'
import type { DexEntryResponse } from '@/types'

interface Props {
    entry: DexEntryResponse
    index: number
    viewMode: 'grid' | 'list'
}

const props = defineProps<Props>()

// 格式化索引（三位数）
const formattedIndex = computed(() => {
    return String(props.index + 1).padStart(3, '0')
})

// 获取分类信息
const categoryInfo = computed(() => {
    return getCategoryInfo(props.entry.category)
})

// 获取状态信息
const statusInfo = computed(() => {
    return getStatusInfo(props.entry.status)
})

// 卡片样式（Grid 视图）
const cardStyle = computed(() => ({
    border: '4px solid #000',
    boxShadow: '4px 4px 0px 0px rgba(0, 0, 0, 0.8)',
    backgroundImage: `
    linear-gradient(45deg, rgba(255,255,255,0.3) 25%, transparent 25%),
    linear-gradient(-45deg, rgba(255,255,255,0.3) 25%, transparent 25%),
    linear-gradient(45deg, transparent 75%, rgba(255,255,255,0.3) 75%),
    linear-gradient(-45deg, transparent 75%, rgba(255,255,255,0.3) 75%)
  `,
    backgroundSize: '4px 4px',
    backgroundPosition: '0 0, 0 2px, 2px -2px, -2px 0px',
    backgroundColor: categoryInfo.value?.color || '#FBBF24' // 使用分类颜色
}))

// 分类徽章样式
const categoryBadgeStyle = computed(() => ({
    backgroundColor: categoryInfo.value?.color || '#EF4444',
    border: '2px solid #000',
    boxShadow: '2px 2px 0px 0px rgba(0,0,0,0.5)'
}))

// 状态徽章样式
const statusBadgeStyle = computed(() => ({
    backgroundColor: statusInfo.value?.color || '#6B7280',
    border: '2px solid #000',
    boxShadow: '2px 2px 0px 0px rgba(0,0,0,0.5)'
}))

// 按钮样式
const buttonStyle = computed(() => ({
    border: '2px solid #000',
    boxShadow: '4px 4px 0px 0px rgba(0,0,0,0.8)'
}))

// 进度条样式
const progressBarStyle = computed(() => ({
    backgroundColor: categoryInfo.value?.color || '#FBBF24',
    width: `${(props.entry.rating / 5) * 100}%`
}))

// 评分星星
const getRatingStars = (rating: number): string => {
    const fullStars = Math.floor(rating)
    const hasHalfStar = rating % 1 >= 0.5
    let stars = ''

    for (let i = 0; i < 5; i++) {
        if (i < fullStars) {
            stars += '★'
        } else if (i === fullStars && hasHalfStar) {
            stars += '☆'
        } else {
            stars += '☆'
        }
    }

    return stars
}
</script>

<style scoped>
.pixel-card {
    border: 4px solid #000;
    box-shadow: 4px 4px 0px 0px rgba(0, 0, 0, 0.8);
}

/* 确保图片不会变形 */
/* .aspect-\[3\/4\] {
    aspect-ratio: 3 / 4;
} */

/* 文本截断 */
.line-clamp-2 {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}
</style>