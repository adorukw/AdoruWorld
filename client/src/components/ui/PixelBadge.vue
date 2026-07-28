<script setup lang="ts">
import { computed } from "vue";

const props = defineProps<{
    name: string;
    color?: string;
    count?: number;
    active?: boolean;
}>();

const tagStyle = computed(() => ({
    backgroundColor: props.active ? props.color : `${props.color}20`,
    borderColor: props.color,
    color: props.active ? "#fff" : props.color,
}));
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
    padding: 4px 10px;
    border: 2px solid #2c2c2c;
    box-shadow: 3px 3px 0 0 #2c2c2c;
    transition: all 0.1s ease;
}

.tag:hover {
    transform: translate(-1px, -1px);
    box-shadow: 4px 4px 0 0 #2c2c2c;
}

.tag:active {
    transform: translate(1px, 1px);
    box-shadow: 2px 2px 0 0 #2c2c2c;
}
</style>
