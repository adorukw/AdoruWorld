<template>
    <!-- Grid 视图：完整 3D 蓝光实体盒 -->
    <router-link v-if="viewMode === 'grid'" :to="`/dex/${entry.slug}`" class="group block perspective-box">

        <!-- 3D 盒子容器 -->
        <div class="bd-volume relative w-full aspect-11/14 bg-black cursor-pointer">

            <!-- 左侧书脊 (Spine) -->
            <div
                class="bd-spine absolute left-0 top-0 bottom-0 w-4 origin-left bg-linear-to-r from-blue-950 via-blue-900 to-blue-800 flex flex-col items-center justify-between py-2 border-l border-blue-500/30">
                <span class="text-[6px] text-white/40 font-bold tracking-widest rotate-90 mt-4">BLU-RAY</span>
                <!-- 侧边编号模拟 -->
                <span class="text-[8px] text-white/50 font-mono rotate-90 mb-4">{{ formattedIndex }}</span>
            </div>

            <!-- 右侧开口边 (Right Edge) - 模拟蓝色塑料壳边缘 -->
            <div
                class="bd-right absolute right-0 top-0 bottom-0 w-4 origin-right bg-linear-to-r from-blue-400 to-blue-600 border-r border-blue-300/40">
                <div
                    class="w-full h-full bg-[linear-gradient(to_bottom,rgba(255,255,255,0.2)_50%,transparent_50%)] bg-size-[100%_6px]">
                </div>
            </div>

            <!-- 顶部边 (Top Edge) -->
            <div
                class="bd-top absolute top-0 left-0 right-0 h-4 origin-top bg-linear-to-b from-blue-600 to-blue-800 border-t border-blue-400/50">
            </div>

            <!-- 底部边 (Bottom Edge) -->
            <div class="bd-bottom absolute bottom-0 left-0 right-0 h-4 origin-bottom bg-blue-950"></div>

            <!-- 正面封面 (Front Face) -->
            <div
                class="bd-front absolute inset-0 bg-linear-to-b from-blue-400/90 to-blue-600/90 p-0.5 z-10 overflow-hidden">
                <!-- 塑封反光层 -->
                <div class="bd-shine absolute inset-0 z-20 pointer-events-none mix-blend-overlay"></div>

                <!-- 内部印刷封面区 -->
                <div class="bg-black relative flex flex-col h-full w-full">
                    <!-- 顶部蓝光 Banner -->
                    <div
                        class="h-6 w-full bg-linear-to-r from-blue-950 via-blue-600 to-blue-950 flex items-center justify-center border-b border-blue-400/40 z-10 shrink-0">
                        <span class="text-white/90 text-[9px] font-bold tracking-widest uppercase bd-logo-font">
                            Blu-ray Disc
                        </span>
                    </div>

                    <!-- 封面图及信息 -->
                    <div class="relative flex-1 w-full overflow-hidden">
                        <img :src="entry.coverImage" :alt="entry.title"
                            class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105" />

                        <!-- 底部渐变信息区 -->
                        <div
                            class="absolute bottom-0 left-0 right-0 p-3 pt-12 bg-linear-to-t from-black via-black/90 to-transparent z-10">
                            <div class="flex justify-between items-end mb-1">
                                <span class="text-white/70 text-xs font-mono">#{{ formattedIndex }}</span>
                                <div v-if="entry.rating > 0"
                                    class="text-yellow-400 text-xs tracking-widest drop-shadow-md">
                                    {{ getRatingStars(entry.rating) }}
                                </div>
                            </div>

                            <h3 class="text-white! font-bold text-sm leading-tight line-clamp-2 mb-2 drop-shadow-lg">
                                {{ entry.title }}
                            </h3>

                            <!-- 徽章 -->
                            <div class="flex flex-wrap gap-1.5">
                                <span
                                    class="text-[10px] px-1.5 py-0.5 rounded-sm text-white shadow-sm border border-white/10"
                                    :style="{ backgroundColor: categoryInfo?.color || 'rgba(239, 68, 68, 0.9)' }">
                                    {{ categoryInfo?.icon }} {{ categoryInfo?.name }}
                                </span>
                                <span
                                    class="text-[10px] px-1.5 py-0.5 rounded-sm text-white shadow-sm border border-white/10"
                                    :style="{ backgroundColor: statusInfo?.color || 'rgba(107, 114, 128, 0.9)' }">
                                    {{ statusInfo?.icon }} {{ statusInfo?.name }}
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </router-link>

    <!-- List 视图：带有永久 3D 透视的小蓝光盒 -->
    <router-link v-else :to="`/dex/${entry.slug}`" class="block group">
        <div
            class="p-3 bg-white rounded-lg shadow-sm border border-gray-100 flex gap-4 items-center transition-all duration-300 group-hover:shadow-md group-hover:border-blue-200">

            <!-- 迷你 3D 盒子缩略图 -->
            <div class="perspective-box w-24 shrink-0 py-2 pl-2">
                <div class="bd-volume-list relative w-full aspect-11/14 bg-black">
                    <!-- 缩略图书脊 -->
                    <div class="absolute left-0 top-0 bottom-0 w-2.5 origin-left bg-blue-900 border-l border-blue-500/30 flex items-center justify-center"
                        style="transform: rotateY(-90deg);"></div>
                    <!-- 缩略图顶部 -->
                    <div class="absolute top-0 left-0 right-0 h-2.5 origin-top bg-blue-700"
                        style="transform: rotateX(90deg);"></div>
                    <!-- 缩略图正面 -->
                    <div class="absolute inset-0 bg-blue-500 p-px z-10" style="transform: translateZ(0.5px);">
                        <div class="bd-shine absolute inset-0 z-20 pointer-events-none mix-blend-overlay"></div>
                        <div class="bg-black flex flex-col h-full w-full overflow-hidden">
                            <div
                                class="h-2.5 w-full bg-linear-to-r from-blue-900 via-blue-500 to-blue-900 border-b border-blue-400/40">
                            </div>
                            <img :src="entry.coverImage" :alt="entry.title" class="w-full h-full object-cover" />
                        </div>
                    </div>
                </div>
            </div>

            <!-- 内容区域 (保持原样) -->
            <div class="flex-1 min-w-0 pr-2">
                <div class="flex items-center gap-2 mb-1">
                    <span class="text-gray-400 text-sm font-mono font-medium">#{{ formattedIndex }}</span>
                    <h3 class="text-gray-800 font-bold text-lg truncate group-hover:text-blue-600 transition-colors">
                        {{ entry.title }}
                    </h3>
                </div>

                <p v-if="entry.originalTitle" class="text-gray-500 text-sm mb-2 truncate">
                    {{ entry.originalTitle }}
                </p>

                <div class="flex flex-wrap items-center gap-2">
                    <span class="text-xs px-2 py-0.5 rounded-sm text-white shadow-sm"
                        :style="{ backgroundColor: categoryInfo?.color || '#EF4444' }">
                        {{ categoryInfo?.name }}
                    </span>
                    <span class="text-xs px-2 py-0.5 rounded-sm text-white shadow-sm"
                        :style="{ backgroundColor: statusInfo?.color || '#6B7280' }">
                        {{ statusInfo?.name }}
                    </span>
                    <span v-if="entry.year" class="text-gray-400 text-sm ml-auto">
                        {{ entry.year }}
                    </span>
                </div>
            </div>

            <!-- 右侧评分 -->
            <div class="hidden sm:block shrink-0 text-right w-24">
                <div v-if="entry.rating > 0" class="text-yellow-500 text-sm mb-1 tracking-widest">
                    {{ getRatingStars(entry.rating) }}
                </div>
                <div class="w-full h-1.5 bg-gray-100 rounded-full overflow-hidden mt-2">
                    <div class="h-full transition-all duration-500 rounded-full"
                        :style="{ backgroundColor: categoryInfo?.color || '#3B82F6', width: `${(entry.rating / 5) * 100}%` }" />
                </div>
            </div>
        </div>
    </router-link>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { DexEntryResponse } from '@/types'
import { dexCategories, dexStatuses } from '@/constants'

interface Props {
    entry: DexEntryResponse
    index: number
    viewMode: 'grid' | 'list'
}

const props = defineProps<Props>()

const formattedIndex = computed(() => String(props.index + 1).padStart(3, '0'))
const categoryInfo = computed(() => dexCategories.find(category => category.id === props.entry.category))
const statusInfo = computed(() => dexStatuses.find(status => status.id === props.entry.status))

const getRatingStars = (rating: number): string => {
    const fullStars = Math.floor(rating)
    const hasHalfStar = rating % 1 >= 0.5
    let stars = ''
    for (let i = 0; i < 5; i++) {
        if (i < fullStars) stars += '★'
        else if (i === fullStars && hasHalfStar) stars += '☆'
        else stars += '☆'
    }
    return stars
}
</script>

<style scoped>
/* 3D 场景透视距离设置 */
.perspective-box {
    perspective: 1200px;
}

/* ============================
   Grid 大盒子 3D 核心逻辑 
   ============================ */
.bd-volume {
    transform-style: preserve-3d;
    /* 默认状态：向右微转、微微后仰，暴露出左侧的书脊(Spine)和顶部边缘 */
    transform: rotateY(18deg) rotateX(6deg) translateZ(-10px);
    transition: transform 0.6s cubic-bezier(0.2, 0.8, 0.2, 1), box-shadow 0.6s ease;
    /* 3D立体阴影，向左下方投射 */
    box-shadow: -15px 15px 20px -5px rgba(0, 0, 0, 0.5), -5px 5px 10px rgba(0, 0, 0, 0.3);
}

.group:hover .bd-volume {
    /* 鼠标悬停时：盒子转正并向屏幕前浮出 */
    transform: rotateY(0deg) rotateX(0deg) translateZ(30px);
    box-shadow: 0px 25px 35px -10px rgba(0, 0, 0, 0.7);
}

/* 构建厚度六面体：利用 origin 旋转贴合边缘 */
.bd-spine {
    transform: rotateY(-90deg);
}

.bd-right {
    transform: rotateY(90deg);
}

.bd-top {
    transform: rotateX(90deg);
}

.bd-bottom {
    transform: rotateX(-90deg);
}

/* 为了防止 Z-fighting，正面轻微拉出 0.5px */
.bd-front {
    transform: translateZ(0.5px);
}


/* ============================
   List 小盒子 3D 核心逻辑 (静态展示厚度)
   ============================ */
.bd-volume-list {
    transform-style: preserve-3d;
    transform: rotateY(22deg) rotateX(8deg) translateZ(-5px);
    transition: transform 0.4s ease;
    box-shadow: -8px 8px 12px -3px rgba(0, 0, 0, 0.4);
}

.group:hover .bd-volume-list {
    transform: rotateY(10deg) rotateX(2deg) translateZ(5px);
    box-shadow: -12px 12px 16px -5px rgba(0, 0, 0, 0.5);
}


/* ============================
   塑料塑封膜高光扫过效果 
   ============================ */
.bd-shine {
    background: linear-gradient(105deg,
            transparent 20%,
            rgba(255, 255, 255, 0.35) 25%,
            rgba(255, 255, 255, 0.1) 28%,
            transparent 32%);
    background-size: 250% 100%;
    background-position: 100% 0;
    transition: background-position 0.8s cubic-bezier(0.2, 0.8, 0.2, 1);
}

.group:hover .bd-shine {
    background-position: -100% 0;
}


/* 字体修饰 */
.bd-logo-font {
    font-family: 'Arial', sans-serif;
    letter-spacing: 0.15em;
}

.line-clamp-2 {
    display: -webkit-box;
    line-clamp: 2;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}
</style>