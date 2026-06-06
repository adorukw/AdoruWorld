<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { usePostCategoryStore, usePostTagStore, usePostStore, useDexStore, useDexGenreStore, useMediaStore, useMediaTagStore } from '@/store'

const bgmPlayer = ref<HTMLAudioElement | null>(null)
let hasInteracted = false

const postCategoryStore = usePostCategoryStore()
const postTagStore = usePostTagStore()
const postStore = usePostStore()
const dexStore = useDexStore()
const dexGenreStore = useDexGenreStore()
const mediaStore = useMediaStore()
const mediaTagStore = useMediaTagStore()

const startBGM = () => {
    if (bgmPlayer.value && !hasInteracted) {
        bgmPlayer.value.play().catch(e => console.log('播放失败:', e))
        hasInteracted = true
    }
}

onMounted(() => {
    // 监听页面首次交互
    document.addEventListener('click', startBGM, { once: true })
    document.addEventListener('keydown', startBGM, { once: true })
    document.addEventListener('touchstart', startBGM, { once: true })
})

onMounted(async () => {
    await Promise.all([
        postCategoryStore.getPostCategories(),
        postTagStore.getPostTags(),
        postStore.getAllPosts(),
        postStore.getArchives(),
        dexStore.getDexEntries(),
        dexStore.getDexStats(),
        dexGenreStore.getDexGenres(),
        postStore.getTotalPostsCount(),
        postStore.getTotalWords(),
        postStore.getTotalViews(),
        mediaStore.getMedias(),
        mediaTagStore.getMediaTags()
    ])
})

</script>

<template>
    <audio ref="bgmPlayer" loop preload="auto" style="display: none;">
        <source src="./assets/audio/未白镇.mp3" type="audio/mpeg">
    </audio>
    <router-view />
</template>
