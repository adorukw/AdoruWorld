<template>
    <!-- Footer主容器：顶部边框、自动上边距、相对定位 -->
    <footer class="border-t-4 mt-auto overflow-hidden relative bg-yellow-500 border-black shadow-[0_-4px_0_0_#000]">

        <!-- 主要内容容器：最大宽度、内边距、相对定位 -->
        <div class="max-w-6xl mx-auto px-4 py-8 relative z-10 h-full flex flex-col">
            <!-- 三栏网格布局 -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-8 flex-1">

                <!-- 第一栏：Logo和网站描述 -->
                <div class="text-center md:text-left">
                    <!-- Logo和网站名称 -->
                    <div class="flex items-center justify-center md:justify-start gap-3 mb-4">
                        <!-- Logo圆形图标 -->
                        <div
                            class="w-10 h-10 bg-sky rounded-full border-4  flex items-center justify-center shadow-md relative overflow-hidden">
                            <!-- Logo字母 -->
                            <span class="text-white font-bold text-lg relative z-10">A</span>
                        </div>
                        <!-- 网站名称 -->
                        <span class="  drop-shadow-sm">AdoruWorld</span>
                    </div>
                    <!-- 网站描述 -->
                    <p class=" ">
                        口袋妖怪风格的像素艺术个人博客
                    </p>
                </div>

                <!-- 第二栏：网站统计数据 -->
                <div class="text-center">
                    <h3 class="mb-4">网站统计</h3>
                    <!-- 统计数据网格：2x2布局 -->
                    <div class="grid grid-cols-2 gap-4">
                        <!-- 文章数卡片 -->
                        <px-card round class=" bg-white/80 rounded p-3 relative overflow-hidden">
                            <div class="  text-sky-dark text-lg relative z-10">{{ totalPostsCount }}
                            </div>
                            <div class="  relative z-10">总文章数</div>
                        </px-card>
                        <!-- 总字数卡片 -->
                        <px-card round class=" bg-white/80 rounded p-3 relative overflow-hidden">
                            <div class="  text-sky-dark text-lg relative z-10">{{ totalWordCount }}
                            </div>
                            <div class="  relative z-10">总字数</div>
                        </px-card>
                        <!-- 阅读量卡片 -->
                        <px-card round class=" bg-white/80 rounded p-3 relative overflow-hidden">
                            <div class="  text-sky-dark text-lg relative z-10">{{ totalViewsCount }}
                            </div>
                            <div class="  relative z-10">总阅览次数</div>
                        </px-card>
                        <!-- 运行天数卡片 -->
                        <px-card round class=" bg-white/80 rounded p-3 relative overflow-hidden">
                            <div class="  text-sky-dark text-lg relative z-10">{{ shortUptime }}</div>
                            <div class="  relative z-10">运行时长</div>
                        </px-card>
                    </div>
                </div>

                <!-- 第三栏：社交媒体链接 -->
                <div class="text-center md:text-right">
                    <h3 class="  text-pokemon-black   mb-4">社交媒体</h3>
                    <!-- 社交媒体图标容器 -->
                    <div class="flex justify-center md:justify-end gap-3">
                        <!-- GitHub链接 -->
                        <px-button circle size="large" title="GitHub">
                            <a href="#" target="_blank">
                                <!-- GitHub SVG图标 -->
                                <px-icon icon="github" size="30" class="w-5 h-5 relative z-10" />
                            </a>
                        </px-button>
                        <px-button circle size="large" title="GitHub">
                            <a href="#" target="_blank">
                                <span class="text-black! w-5 h-5 relative z-10">B站</span>
                            </a>
                        </px-button>
                        <px-button circle size="large" title="GitHub">
                            <a href="#" target="_blank">
                                <px-icon icon="envelope" size="30" class="w-5 h-5 relative z-10" />
                            </a>
                        </px-button>
                    </div>
                </div>
            </div>

            <!-- 底部版权信息区域 -->
            <div class="border-t-2 border-gray-300 mt-8 pt-6 text-center relative z-10">
                <!-- 版权信息 -->
                <p class="text-base  ">
                    © {{ 2026 }} AdoruWorld. All rights reserved.
                </p>
                <!-- 标语 -->
                <p class="text-base mt-2">
                    Made with ❤️ and pixel art magic
                </p>
                <p class="text-sm mt-2 text-gray-600">
                    已运行：{{ formattedUptime }}
                </p>
            </div>
        </div>
    </footer>
</template>
<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { usePostStore } from '@/store'
import { api } from '@/api'

const postStore = usePostStore()

const { totalPostsCount, totalWordCount, totalViewsCount } = postStore

const LAUNCH_DATE = ref<Date>(new Date('2026-01-01T00:00:00Z'))

const getLaunchDate = async () => {
    const response = await api.system.systemInfo()
    LAUNCH_DATE.value = new Date(response.launch_date)
}

onMounted(async () => {
    await getLaunchDate()
})

const uptimeSeconds = ref(0)
let uptimeTimer: number | null = null

const calculateUptime = () => {
    const now = new Date()
    const diffInSeconds = Math.floor((now.getTime() - LAUNCH_DATE.value.getTime()) / 1000)
    uptimeSeconds.value = diffInSeconds
}

// 格式化运行时长
const formattedUptime = computed(() => {
    const seconds = uptimeSeconds.value

    const days = Math.floor(seconds / (24 * 60 * 60))
    const hours = Math.floor((seconds % (24 * 60 * 60)) / (60 * 60))
    const minutes = Math.floor((seconds % (60 * 60)) / 60)
    const secs = seconds % 60

    // 格式：XX天 XX小时 XX分 XX秒
    if (days > 0) {
        return `${days}天 ${hours.toString().padStart(2, '0')}小时 ${minutes.toString().padStart(2, '0')}分 ${secs.toString().padStart(2, '0')}秒`
    } else if (hours > 0) {
        return `${hours}小时 ${minutes.toString().padStart(2, '0')}分 ${secs.toString().padStart(2, '0')}秒`
    } else if (minutes > 0) {
        return `${minutes}分 ${secs.toString().padStart(2, '0')}秒`
    } else {
        return `${secs}秒`
    }
})

// 简化的短格式（用于卡片显示）
const shortUptime = computed(() => {
    const seconds = uptimeSeconds.value
    const days = Math.floor(seconds / (24 * 60 * 60))
    const hours = Math.floor((seconds % (24 * 60 * 60)) / (60 * 60))
    const minutes = Math.floor((seconds % (60 * 60)) / 60)
    const secs = seconds % 60

    if (days > 0) {
        return `${days}天`
    } else if (hours > 0) {
        return `${hours}小时`
    } else if (minutes > 0) {
        return `${minutes}分`
    } else {
        return `${secs}秒`
    }
})

// 组件挂载时启动计时器
onMounted(() => {
    calculateUptime() // 立即计算一次
    uptimeTimer = window.setInterval(() => {
        calculateUptime()
    }, 1000) // 每秒更新一次
})

// 组件卸载时清除计时器
onUnmounted(() => {
    if (uptimeTimer) {
        clearInterval(uptimeTimer)
        uptimeTimer = null
    }
})
</script>

<style scoped>
@keyframes pulse {

    0%,
    100% {
        opacity: 1;
    }

    50% {
        opacity: 0.7;
    }
}

.uptime-seconds {
    animation: pulse 1s infinite;
}

/* 卡片悬停效果 */
.px-card {
    transition: transform 0.2s, box-shadow 0.2s;
}

.px-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
</style>