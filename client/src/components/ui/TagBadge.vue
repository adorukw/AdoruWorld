<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
    name: string
    color?: string
    count?: number
    active?: boolean
}>()

const tagStyle = computed(() => ({
    backgroundColor: props.active ? props.color : `${props.color}20`,
    borderColor: props.color,
    color: props.active ? '#fff' : props.color
}))
</script>

<template>
    <span class="tag cursor-pointer" :style="tagStyle">
        #{{ name }}
        <span v-if="count" class="ml-1 opacity-70">({{ count }})</span>
    </span>
</template>

<style scoped>
.tag {
    display: inline-flex;
    align-items: center;
    padding: 6px 14px;
    border: 3px solid #2C2C2C; /* 修正：直接使用颜色值 */
    position: relative;
    transition: none;
    box-shadow:
        4px 4px 0 0 #8B8B8B, /* 修正：直接使用值 */
        8px 8px 0 0 #2C2C2C; /* 8px = 4px * 2 */
}

.tag::before {
    content: '';
    position: absolute;
    top: 2px;
    left: 2px;
    right: 4px; /* 修正：2px + 2px = 4px */
    height: 2px;
    background: rgba(255, 255, 255, 0.6);
}

.tag:hover {
    transform: translate(-2px, -2px);
    box-shadow:
        3px 3px 0 0 #8B8B8B, /* 2px * 1.5 = 3px */
        5px 5px 0 0 #2C2C2C, /* 2px * 2.5 = 5px */
        7px 7px 0 0 #8B8B8B; /* 2px * 3.5 = 7px */
}
</style>