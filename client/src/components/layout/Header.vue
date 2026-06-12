<template>
    <nav class="sticky top-0 z-50 bg-[#ee1515] border-b-4 border-black shadow-[0_4px_0_0_#000]">
        <div class="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between">
            <div class="flex items-center gap-4">
                <div class="w-10 h-10 bg-white border-4 border-black flex items-center justify-center">
                    <span class="text-black text-lg">A</span>
                    <!-- <div class="pixel-pokeball"></div> -->
                </div>
                <div class="text-white pixel-text md:text-2xl tracking-widest ">AdoruWorld</div>
            </div>
            <div class="hidden md:flex items-center gap-6 text-xl">
                <router-link v-for="navItem in navItems" :key="navItem.path" :to="navItem.path"
                    class=" !hover:text-yellow-300 transition-colors! no-underline">
                    <span>{{ navItem.icon }}</span>
                    <span>{{ navItem.name }}</span>
                </router-link>
            </div>
            <!-- 移动端菜单按钮 -->
            <button class="md:hidden pixel-btn text-xs px-3 py-2">☰</button>
        </div>
    </nav>
</template>

<script setup lang="ts">
import { navItems } from '@/constants'

</script>

<style scoped>
.pixel-pokeball {
    width: 16px;
    height: 16px;
    position: relative;
    image-rendering: pixelated;
}

.pixel-pokeball::before {
    content: '';
    position: absolute;
    width: 16px;
    height: 16px;
    background:
        /* 红色上半部分 */
        linear-gradient(to bottom,
            #EF5350 0%, #EF5350 8px,
            transparent 8px, transparent 16px),
        /* 白色下半部分 */
        linear-gradient(to bottom,
            transparent 0%, transparent 8px,
            #FFFFFF 8px, #FFFFFF 16px),
        /* 黑色边框 */
        linear-gradient(to bottom,
            #000 0%, #000 1px,
            transparent 1px, transparent 15px,
            #000 15px, #000 16px),
        linear-gradient(to right,
            #000 0%, #000 1px,
            transparent 1px, transparent 15px,
            #000 15px, #000 16px);
    background-size: 16px 16px;
    border-radius: 50%;
}

.pixel-pokeball::after {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    width: 8px;
    height: 8px;
    background:
        radial-gradient(circle at center, #FFF 2px, #000 3px, transparent 3px),
        radial-gradient(circle at center, #000 4px, transparent 4px);
    border-radius: 50%;
    transform: translate(-50%, -50%);
}
</style>