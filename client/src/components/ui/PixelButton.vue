<template>
    <button :type="type" :disabled="disabled" :class="[
        'pixel-btn',
        colorClass,
        sizeClass,
        disabled ? 'cursor-not-allowed opacity-70' : '',
        block ? 'w-full' : '',
        customClass
    ]" @click="$emit('click', $event)" @mouseenter="$emit('mouseenter', $event)"
        @mouseleave="$emit('mouseleave', $event)">
        <!-- 按钮内容插槽 -->
        <slot>
            {{ text }}
        </slot>

        <!-- 加载状态 -->
        <span v-if="loading" class="ml-2">
            <svg class="animate-spin h-4 w-4 inline" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
                </path>
            </svg>
        </span>
    </button>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
    // 颜色类型
    color?: 'red' | 'blue' | 'green' | 'yellow' | 'custom'
    // 按钮类型
    type?: 'button' | 'submit' | 'reset'
    // 尺寸
    size?: 'sm' | 'md' | 'lg'
    // 是否禁用
    disabled?: boolean
    // 是否显示为块级元素
    block?: boolean
    // 加载状态
    loading?: boolean
    // 按钮文本
    text?: string
    // 自定义类名
    customClass?: string
    // 自定义背景色
    customColor?: string
    // 自定义阴影颜色
    customShadow?: {
        insetTopLeft?: string
        insetBottomRight?: string
        outer?: string
    }
}

const props = withDefaults(defineProps<Props>(), {
    color: 'red',
    type: 'button',
    size: 'md',
    disabled: false,
    block: false,
    loading: false,
    text: '',
    customClass: '',
    customColor: '',
})

// 定义事件
const emit = defineEmits<{
    click: [event: MouseEvent]
    mouseenter: [event: MouseEvent]
    mouseleave: [event: MouseEvent]
}>()

// 计算颜色类
const colorClass = computed(() => {
    if (props.color === 'custom') return 'pixel-btn-custom'
    return `pixel-btn-${props.color}`
})

// 计算尺寸类
const sizeClass = computed(() => {
    switch (props.size) {
        case 'sm':
            return 'px-3 py-1 text-sm'
        case 'lg':
            return 'px-6 py-3 text-lg'
        case 'md':
        default:
            return 'px-4 py-2'
    }
})

// 自定义样式
// const customStyles = computed(() => {
//     if (props.color !== 'custom') return {}

//     const baseShadow = {
//         '--inset-top-left': props.customShadow?.insetTopLeft || '#9a2208',
//         '--inset-bottom-right': props.customShadow?.insetBottomRight || '#ff6b4a',
//         '--outer-shadow': props.customShadow?.outer || '#000000',
//     }

//     if (props.customColor) {
//         return {
//             ...baseShadow,
//             'background-color': props.customColor,
//         }
//     }

//     return baseShadow
// })
</script>

<style scoped>
.pixel-btn {
    position: relative;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background: #e3350d;
    color: white;
    border: 4px solid #000;
    box-shadow:
        inset -4px -4px 0px 0px var(--inset-top-left, #9a2208),
        inset 4px 4px 0px 0px var(--inset-bottom-right, #ff6b4a),
        4px 4px 0px 0px var(--outer-shadow, #000000);
    cursor: pointer;
    transition: all 0.1s ease;
    text-transform: uppercase;
    font-family: 'Press Start 2P', 'Courier New', monospace;
    letter-spacing: 1px;
    outline: none;
    user-select: none;
}

.pixel-btn:hover:not(:disabled) {
    background: #ff4422;
    transform: translateY(-2px);
    box-shadow:
        inset -4px -4px 0px 0px var(--inset-top-left, #9a2208),
        inset 4px 4px 0px 0px var(--inset-bottom-right, #ff6b4a),
        6px 6px 0px 0px var(--outer-shadow, #000000);
}

.pixel-btn:active:not(:disabled) {
    transform: translate(4px, 4px);
    box-shadow:
        inset -4px -4px 0px 0px var(--inset-top-left, #9a2208),
        inset 4px 4px 0px 0px var(--inset-bottom-right, #ff6b4a),
        0px 0px 0px 0px var(--outer-shadow, #000000);
}

.pixel-btn:disabled {
    background: #cccccc;
    cursor: not-allowed;
    box-shadow:
        inset -4px -4px 0px 0px #999999,
        inset 4px 4px 0px 0px #dddddd,
        4px 4px 0px 0px #666666;
}

/* 蓝色按钮 */
.pixel-btn-blue {
    background: #3b4cca;
    --inset-top-left: #1a2a7a;
    --inset-bottom-right: #6b7cfa;
    --outer-shadow: #000000;
}

.pixel-btn-blue:hover:not(:disabled) {
    background: #4a5fd8;
}

/* 绿色按钮 */
.pixel-btn-green {
    background: #4dad5b;
    --inset-top-left: #2d6b38;
    --inset-bottom-right: #7dd68a;
    --outer-shadow: #000000;
}

.pixel-btn-green:hover:not(:disabled) {
    background: #5bc06a;
}

/* 黄色按钮 */
.pixel-btn-yellow {
    background: #ffcb05;
    color: #000;
    --inset-top-left: #b39200;
    --inset-bottom-right: #ffe566;
    --outer-shadow: #000000;
}

.pixel-btn-yellow:hover:not(:disabled) {
    background: #ffd633;
}

/* 自定义按钮 */
.pixel-btn-custom {
    /* 通过内联样式或计算属性设置颜色 */
}
</style>