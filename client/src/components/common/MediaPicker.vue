<!-- src/components/common/MediaPicker.vue -->
<script setup lang="ts">
import { ref} from 'vue'
import { useMediaStore } from '@/store/media'
import type { MediaResponse } from '@/types/media'

const props = defineProps<{
    modelValue: string
}>()

const emit = defineEmits<{
    'update:modelValue': [value: string]
}>()

const store = useMediaStore()
const showPicker = ref(false)
const mediaList = ref<MediaResponse[]>([])
const selectedPath = ref('')
const uploading = ref(false)

// 加载媒体库中的图片
async function loadMedia() {
    await store.getMedias({ mediaType: 'image' })
    mediaList.value = store.medias
}

function openPicker() {
    selectedPath.value = props.modelValue || ''
    loadMedia()
    showPicker.value = true
}

function selectMedia(media: MediaResponse) {
    selectedPath.value = selectedPath.value === media.filePath ? '' : media.filePath
}

function confirm() {
    emit('update:modelValue', selectedPath.value)
    showPicker.value = false
}

async function handleUpload(event: Event) {
    const input = event.target as HTMLInputElement
    if (!input.files?.length) return

    uploading.value = true
    try {
        const res = await store.uploadMedia(input.files[0])
        // 上传成功后再加载列表
        await loadMedia()
        // 自动选中刚上传的图片
        selectedPath.value = res.filePath
    } catch (e) {
        console.error('上传失败', e)
    } finally {
        uploading.value = false
        input.value = ''  // 清空 input 以便重复上传
    }
}

function getThumbnailUrl(filePath: string): string {
    // 根据你的文件服务调整
    return `http://localhost:8000${filePath}`
}
</script>

<template>
    <!-- 封面预览 + 选择按钮 -->
    <div class="space-y-2">
        <div v-if="modelValue" class="relative w-48 h-32 border-4 border-black overflow-hidden">
            <img :src="getThumbnailUrl(modelValue)" class="w-full h-full object-cover" alt="封面预览" />
            <button type="button" @click="emit('update:modelValue', '')"
                class="absolute top-1 right-1 bg-red-500 text-white px-2 py-1 text-xs pixel-text">
                ✕ 移除
            </button>
        </div>
        <button type="button" @click="openPicker" class="pixel-btn bg-sky text-sm">
            🖼️ {{ modelValue ? '更换封面' : '选择封面' }}
        </button>
    </div>

    <!-- 媒体选择器弹窗 -->
    <Teleport to="body">
        <div v-if="showPicker" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4"
            @click.self="showPicker = false">
            <div class="bg-white border-4 border-black w-full max-w-4xl max-h-[85vh] flex flex-col pixel-card">

                <!-- 头部 -->
                <div class="p-4 border-b-4 border-black flex items-center justify-between">
                    <h2 class="pixel-text text-lg">🖼️ 选择封面图片</h2>
                    <div class="flex items-center gap-3">
                        <!-- 上传新图片 -->
                        <label class="pixel-btn bg-green-400 text-sm cursor-pointer">
                            📤 上传新图片
                            <input type="file" accept=".jpg,.jpeg,.png,.gif,.webp" class="hidden" @change="handleUpload"
                                :disabled="uploading" />
                        </label>
                        <span v-if="uploading" class="text-sm text-blue-600">⏳ 上传中...</span>
                    </div>
                </div>

                <!-- 图片网格 -->
                <div class="flex-1 overflow-y-auto p-4">
                    <div v-if="mediaList.length === 0" class="text-center py-10 text-gray-400 pixel-text">
                        媒体库中还没有图片，请先上传 🖼️
                    </div>
                    <div class="grid grid-cols-4 md:grid-cols-5 lg:grid-cols-6 gap-3">
                        <div v-for="media in mediaList" :key="media.id" @click="selectMedia(media)"
                            class="relative border-4 cursor-pointer overflow-hidden aspect-square transition-all"
                            :class="selectedPath === media.filePath
                                ? 'border-sky ring-4 ring-sky/50 scale-105'
                                : 'border-black hover:border-gray-400'">
                            <img :src="getThumbnailUrl(media.filePath)" class="w-full h-full object-cover"
                                :alt="media.title" />
                            <!-- 预览文件名 -->
                            <div
                                class="absolute bottom-0 left-0 right-0 bg-black/60 text-white text-xs px-1 py-0.5 truncate">
                                {{ media.title }}
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 底部 -->
                <div class="p-4 border-t-4 border-black flex justify-end gap-3">
                    <button type="button" @click="showPicker = false" class="pixel-btn bg-gray-300">取消</button>
                    <button type="button" @click="confirm" class="pixel-btn bg-sky">确认选择</button>
                </div>
            </div>
        </div>
    </Teleport>
</template>