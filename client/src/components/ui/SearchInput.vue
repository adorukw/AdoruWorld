<!-- SearchInput.vue -->
<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'

interface Props {
    placeholder?: string
    modelValue?: string
    buttonText?: string
    buttonIcon?: string
    disabled?: boolean
    autoFocus?: boolean
}

const props = withDefaults(defineProps<Props>(), {
    placeholder: '搜索...',
    buttonText: '搜索',
    buttonIcon: '🔍',
    modelValue: '',
    disabled: false,
    autoFocus: false
})

const emit = defineEmits<{
    'update:modelValue': [value: string]
    'search': [value: string]
    'clear': []
}>()

const searchQuery = ref(props.modelValue)
const inputRef = ref<HTMLInputElement | null>(null)

// 监听外部 modelValue 变化
watch(() => props.modelValue, (newValue) => {
    searchQuery.value = newValue
})

// 同步到外部
const updateValue = (value: string) => {
    searchQuery.value = value
    emit('update:modelValue', value)
}

// 搜索按钮点击
const handleSearch = () => {
    emit('search', searchQuery.value)
}

// 清空搜索
const clearSearch = () => {
    updateValue('')
    emit('clear')
    inputRef.value?.focus()
}

// 回车键触发搜索
const handleKeydown = (event: KeyboardEvent) => {
    if (event.key === 'Enter') {
        handleSearch()
    }
}

// 自动聚焦
onMounted(() => {
    if (props.autoFocus && inputRef.value) {
        inputRef.value.focus()
    }
})
</script>

<template>
    <div class="search-container">
        <div class="relative w-full">
            <!-- 搜索输入框 -->
            <input ref="inputRef" v-model="searchQuery" type="text" :placeholder="placeholder" :disabled="disabled"
                class="pixel-input w px-4 py-3 text-xs md:text-sm placeholder-gray-500 pr-24"
                @input="updateValue(($event.target as HTMLInputElement).value)" @keydown="handleKeydown" />

            <!-- 清空按钮 -->
            <button v-if="searchQuery" @click="clearSearch"
                class=" absolute top-1/2 -translate-y-1/2 right-20 w-6 h-6 flex items-center justify-center text-xs bg-gray-200 hover:bg-gray-300 border-2 border-black transition-colors"
                title="清空">
                ✕
            </button>

            <!-- 搜索按钮 -->
            <button @click="handleSearch" :disabled="disabled"
                class="pixel-btn px-2 py-1 text-xs right-4 absolute top-1/2 -translate-y-1/2"
                :class="{ 'opacity-50 cursor-not-allowed': disabled }">
                <span v-if="buttonIcon">{{ buttonIcon }}</span>
                <span v-if="buttonText" class="hidden sm:inline">{{ buttonText }}</span>
            </button>
        </div>

        <!-- 搜索结果数量提示 -->
        <slot name="hint"></slot>

        <!-- 搜索历史（可选的插槽） -->
        <slot name="history"></slot>
    </div>
</template>

<style scoped>
.search-container {
    position: relative;
}

/* 继承像素风格 */
.pixel-input {
    background: #ffffff;
    border: 4px solid #000000;
    box-shadow:
        inset 4px 4px 0px 0px #b0b0b0,
        inset -4px -4px 0px 0px #ffffff,
        4px 4px 0px 0px #000000;
    outline: none;
    transition: all 0.1s;
}

.pixel-input:focus {
    background: #fffbe6;
    box-shadow:
        inset 4px 4px 0px 0px #d0c0a0,
        inset -4px -4px 0px 0px #ffffff,
        4px 4px 0px 0px #000000;
}

.pixel-input:disabled {
    background: #f0f0f0;
    color: #999;
    cursor: not-allowed;
}

.pixel-btn {
    display: inline-block;
    background: #3b4cca;
    color: white;
    border: 4px solid #000;
    box-shadow:
        inset -4px -4px 0px 0px #1a2a7a,
        inset 4px 4px 0px 0px #6b7cfa,
        4px 4px 0px 0px #000000;
    cursor: pointer;
    transition: none;
    text-transform: uppercase;
}

.pixel-btn:hover:not(:disabled) {
    background: #4a5fd8;
}

.pixel-btn:active:not(:disabled) {
    transform: translate(4px, 4px);
    box-shadow:
        inset -4px -4px 0px 0px #1a2a7a,
        inset 4px 4px 0px 0px #6b7cfa,
        0px 0px 0px 0px #000000;
}

.pixel-btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}
</style>