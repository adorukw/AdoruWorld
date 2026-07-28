<script setup lang="ts">
import { onMounted, ref } from "vue";
const bgmPlayer = ref<HTMLAudioElement | null>(null);
let hasInteracted = false;

const startBGM = () => {
    if (bgmPlayer.value && !hasInteracted) {
        bgmPlayer.value.play().catch((e) => console.log("播放失败:", e));
        hasInteracted = true;
    }
};

onMounted(() => {
    // 监听页面首次交互
    document.addEventListener("click", startBGM, { once: true });
    document.addEventListener("keydown", startBGM, { once: true });
    document.addEventListener("touchstart", startBGM, { once: true });
});
</script>

<template>
    <audio ref="bgmPlayer" loop preload="auto" style="display: none">
        <source src="./assets/audio/未白镇.mp3" type="audio/mpeg" />
    </audio>
    <router-view />
</template>
