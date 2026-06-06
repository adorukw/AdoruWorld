<!-- DropdownMenu.vue -->
<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'

interface Props {
    options: Array<{ label: string; value: string }>
    modelValue?: string
    placeholder?: string
    disabled?: boolean
    autoFocus?: boolean
    width?: string
}

const props = withDefaults(defineProps<Props>(), {
    placeholder: '请选择...',
    options: () => [],
    modelValue: '',
    disabled: false,
    autoFocus: false,
    width: 'w-full'
})

const emit = defineEmits<{
    'update:modelValue': [value: string]
    'change': [value: string, option: { label: string; value: string }]
}>()

const isOpen = ref(false)
const dropdownRef = ref<HTMLDivElement | null>(null)
const selectedOption = ref<{ label: string; value: string } | null>(
    props.options.find(option => option.value === props.modelValue) || null
)

// 计算显示文本
const displayText = computed(() => {
    return selectedOption.value ? selectedOption.value.label : props.placeholder
})

// 切换下拉菜单
const toggleDropdown = () => {
    if (!props.disabled) {
        isOpen.value = !isOpen.value
    }
}

// 选择选项
const selectOption = (option: { label: string; value: string }) => {
    selectedOption.value = option
    emit('update:modelValue', option.value)
    emit('change', option.value, option)
    isOpen.value = false
}

// 点击外部关闭下拉菜单
const handleClickOutside = (event: MouseEvent) => {
    if (dropdownRef.value && !dropdownRef.value.contains(event.target as Node)) {
        isOpen.value = false
    }
}

// 监听外部 modelValue 变化
watch(() => props.modelValue, (newValue) => {
    selectedOption.value = props.options.find(option => option.value === newValue) || null
})

// 键盘事件处理
const handleKeydown = (event: KeyboardEvent) => {
    if (event.key === 'Escape') {
        isOpen.value = false
    }
}

// 自动聚焦
onMounted(() => {
    if (props.autoFocus) {
        // 可以在这里添加聚焦逻辑
    }
    document.addEventListener('click', handleClickOutside)
    document.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
    document.removeEventListener('click', handleClickOutside)
    document.removeEventListener('keydown', handleKeydown)
})
</script>

<template>
    <div class="dropdown-container" :class="width">
        <div ref="dropdownRef" class="relative" :class="{ 'pointer-events-none': props.disabled }">
            <!-- 下拉按钮 -->
            <button @click="toggleDropdown" :disabled="disabled"
                class="pixel-dropdown w-full px-4 py-3 text-xs md:text-sm text-left flex items-center justify-between"
                :class="{ 'opacity-50 cursor-not-allowed': disabled }">
                <span :class="{ 'text-gray-500': !selectedOption }">{{ displayText }}</span>
                <span class="dropdown-arrow ml-2">{{ isOpen ? '▲' : '▼' }}</span>
            </button>

            <!-- 下拉选项列表 -->
            <div v-show="isOpen" class="absolute left-0 right-0 mt-1 z-50 pixel-dropdown-list"
                :class="{ 'pointer-events-none': !isOpen }">
                <div v-for="option in props.options" :key="option.value" @click="selectOption(option)"
                    class="pixel-dropdown-item" :class="{ 'selected': selectedOption?.value === option.value }">
                    {{ option.label }}
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.dropdown-container {
    position: relative;
}

/* 下拉按钮样式 - 匹配 SearchInput 风格 */
.pixel-dropdown {
    background: #ffffff;
    border: 4px solid #000000;
    box-shadow:
        inset 4px 4px 0px 0px #b0b0b0,
        inset -4px -4px 0px 0px #ffffff,
        4px 4px 0px 0px #000000;
    outline: none;
    transition: all 0.1s;
    color: #333;
    text-align: left;
}

.pixel-dropdown:focus {
    background: #fffbe6;
    box-shadow:
        inset 4px 4px 0px 0px #d0c0a0,
        inset -4px -4px 0px 0px #ffffff,
        4px 4px 0px 0px #000000;
}

.pixel-dropdown:disabled {
    background: #f0f0f0;
    color: #999;
    cursor: not-allowed;
}

/* 下拉箭头 */
.dropdown-arrow {
    font-size: 0.7em;
    transition: transform 0.2s;
}

/* 下拉选项列表 */
.pixel-dropdown-list {
    background: #ffffff;
    border: 4px solid #000000;
    box-shadow:
        inset 4px 4px 0px 0px #b0b0b0,
        inset -4px -4px 0px 0px #ffffff,
        4px 4px 0px 0px #000000;
    max-height: 200px;
    overflow-y: auto;
}

/* 下拉选项项 */
.pixel-dropdown-item {
    padding: 8px 12px;
    cursor: pointer;
    border-bottom: 2px solid #e0e0e0;
    transition: all 0.1s;
}

.pixel-dropdown-item:last-child {
    border-bottom: none;
}

.pixel-dropdown-item:hover {
    background: #f0f0f0;
}

.pixel-dropdown-item.selected {
    background: #e0e0ff;
    font-weight: bold;
}

/* 滚动条样式 */
.pixel-dropdown-list::-webkit-scrollbar {
    width: 8px;
}

.pixel-dropdown-list::-webkit-scrollbar-track {
    background: #f0f0f0;
    border-left: 2px solid #000;
}

.pixel-dropdown-list::-webkit-scrollbar-thumb {
    background: #b0b0b0;
    border: 2px solid #000;
}

.pixel-dropdown-list::-webkit-scrollbar-thumb:hover {
    background: #808080;
}
</style>