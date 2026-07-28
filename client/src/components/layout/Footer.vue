<template>
    <footer
        class="border-t-4 mt-auto overflow-hidden relative bg-yellow-500 border-black shadow-[0_-4px_0_0_#000]"
    >
        <div
            class="max-w-6xl mx-auto px-4 py-8 relative z-10 h-full flex flex-col"
        >
            <div class="grid grid-cols-1 md:grid-cols-3 gap-8 flex-1">
                <div class="text-center md:text-left">
                    <div
                        class="flex items-center justify-center md:justify-start gap-3 mb-4"
                    >
                        <div
                            class="w-10 h-10 bg-sky rounded-full border-4 flex items-center justify-center shadow-md relative overflow-hidden"
                        >
                            <span
                                class="text-white font-bold text-lg relative z-10"
                                >A</span
                            >
                        </div>
                        <span class="drop-shadow-sm">AdoruWorld</span>
                    </div>
                    <p class=" ">口袋妖怪风格的像素艺术个人博客</p>
                </div>

                <div class="text-center">
                    <h3 class="mb-4">网站统计</h3>
                    <div class="grid grid-cols-2 gap-4">
                        <div
                            class="pixel-box bg-white/80 rounded p-3 relative overflow-hidden"
                        >
                            <div class="text-lg relative z-10">
                                {{ totalPostsCount }}
                            </div>
                            <div class="relative z-10">总文章数</div>
                        </div>
                        <div
                            class="pixel-box bg-white/80 rounded p-3 relative overflow-hidden"
                        >
                            <div class="text-lg relative z-10">
                                {{ totalWordCount }}
                            </div>
                            <div class="relative z-10">总字数</div>
                        </div>
                        <div
                            class="pixel-box bg-white/80 rounded p-3 relative overflow-hidden"
                        >
                            <div class="text-lg relative z-10">
                                {{ totalViewsCount }}
                            </div>
                            <div class="relative z-10">总阅览次数</div>
                        </div>
                        <div
                            class="pixel-box bg-white/80 rounded p-3 relative overflow-hidden"
                        >
                            <div class="text-lg relative z-10">
                                {{ shortUptime }}
                            </div>
                            <div class="relative z-10">运行时长</div>
                        </div>
                    </div>
                </div>

                <div class="text-center md:text-right">
                    <h3 class="mb-4">社交媒体</h3>
                    <div class="flex justify-center md:justify-end gap-3">
                        <div
                            v-for="socialLink in socialLinks"
                            :key="socialLink.name"
                        >
                            <a
                                :href="socialLink.url"
                                target="_blank"
                                class="text-blue-500 hover:text-blue-700"
                            >
                                <div
                                    class="pixel-box p-1! w-12 h-12 shrink-0"
                                    v-html="socialLink.icon"
                                ></div>
                                {{ socialLink.name }}
                            </a>
                        </div>
                    </div>
                </div>
            </div>

            <div
                class="border-t-2 border-gray-300 mt-8 pt-6 text-center relative z-10"
            >
                <p class="text-base">
                    © {{ 2026 }} AdoruWorld. All rights reserved.
                </p>
                <p class="text-base mt-2">Made with ❤️ and pixel art magic</p>
                <p class="text-sm mt-2 text-gray-600">
                    已运行：{{ formattedUptime }}
                </p>
            </div>
        </div>
    </footer>
</template>
<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from "vue";
import { usePostStore } from "@/store";
import { storeToRefs } from "pinia";
import { systemApi } from "@/api";
import { socialLinks } from "@/constants/index";

const postStore = usePostStore();

const { totalPostsCount, totalWordCount, totalViewsCount } =
    storeToRefs(postStore);

const launchDate = ref<Date>(new Date("2026-01-01T00:00:00Z"));

const getLaunchDate = async () => {
    const response = await systemApi.systemInfo();
    launchDate.value = new Date(response.launch_date);
};

onMounted(async () => {
    await Promise.all([
        postStore.getTotalPostsCount(),
        postStore.getTotalWords(),
        postStore.getTotalViews(),
    ]);
    await getLaunchDate();
});

const uptimeSeconds = ref(0);
let uptimeTimer: number | null = null;

const calculateUptime = () => {
    const now = new Date();
    const diffInSeconds = Math.floor(
        (now.getTime() - launchDate.value.getTime()) / 1000,
    );
    uptimeSeconds.value = diffInSeconds;
};

const formattedUptime = computed(() => {
    const seconds = uptimeSeconds.value;

    const days = Math.floor(seconds / (24 * 60 * 60));
    const hours = Math.floor((seconds % (24 * 60 * 60)) / (60 * 60));
    const minutes = Math.floor((seconds % (60 * 60)) / 60);
    const secs = seconds % 60;

    if (days > 0) {
        return `${days}天 ${hours.toString().padStart(2, "0")}小时 ${minutes.toString().padStart(2, "0")}分 ${secs.toString().padStart(2, "0")}秒`;
    } else if (hours > 0) {
        return `${hours}小时 ${minutes.toString().padStart(2, "0")}分 ${secs.toString().padStart(2, "0")}秒`;
    } else if (minutes > 0) {
        return `${minutes}分 ${secs.toString().padStart(2, "0")}秒`;
    } else {
        return `${secs}秒`;
    }
});

const shortUptime = computed(() => {
    const seconds = uptimeSeconds.value;
    const days = Math.floor(seconds / (24 * 60 * 60));
    const hours = Math.floor((seconds % (24 * 60 * 60)) / (60 * 60));
    const minutes = Math.floor((seconds % (60 * 60)) / 60);
    const secs = seconds % 60;

    if (days > 0) {
        return `${days}天`;
    } else if (hours > 0) {
        return `${hours}小时`;
    } else if (minutes > 0) {
        return `${minutes}分`;
    } else {
        return `${secs}秒`;
    }
});

onMounted(() => {
    calculateUptime();
    uptimeTimer = window.setInterval(() => {
        calculateUptime();
    }, 1000);
});

onUnmounted(() => {
    if (uptimeTimer) {
        clearInterval(uptimeTimer);
        uptimeTimer = null;
    }
});
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
</style>
