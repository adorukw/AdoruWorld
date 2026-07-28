<script setup lang="ts">
import type { TocItem } from "@/types";

defineProps<{
    items: TocItem[];
}>();

function handleClick(e: MouseEvent, id: string) {
    e.preventDefault();
    const el = document.getElementById(id);
    if (el) {
        el.scrollIntoView({ behavior: "smooth", block: "start" });
    }
}
</script>

<template>
    <ul class="space-y-1">
        <li v-for="item in items" :key="item.id">
            <a
                :href="`#${item.id}`"
                class="block py-1 px-2 rounded hover:bg-sky-100 transition-colors border-l-2 border-transparent hover:border-sky-500"
                :style="{ paddingLeft: `${(item.level - 1) * 12 + 8}px` }"
                @click="(e) => handleClick(e, item.id)"
            >
                {{ item.text }}
            </a>
            <TocTree v-if="item.children?.length" :items="item.children" />
        </li>
    </ul>
</template>
