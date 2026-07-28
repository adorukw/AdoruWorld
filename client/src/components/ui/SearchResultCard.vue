<script setup lang="ts">
import type { SearchResultItem } from "@/types";
import { computed } from "vue";
import { dexCategories, mediaTypes } from "@/constants";

const props = defineProps<{
    item: SearchResultItem;
}>();

// const routerLink = computed(() => {
//     const { type, slug } = props.item
//     if (type === 'post') return `/posts/${slug}`
//     if (type === 'dex') return `/dexes/${slug}`
//     return '/admin/medias'
// })

// 从 entityData 里提取分类/标签用于展示
const categoryName = computed(() => {
    if (props.item.type === "post")
        return props.item.entityData?.category?.name || "未分类";
    if (props.item.type === "dex") {
        const cat = dexCategories.find(
            (c) => c.id === props.item.entityData?.category,
        );
        return cat?.name || props.item.entityData?.category || "未分类";
    }
    return "";
});

const categoryIcon = computed(() => {
    if (props.item.type === "post") return "📝";
    if (props.item.type === "dex") {
        const cat = dexCategories.find(
            (c) => c.id === props.item.entityData?.category,
        );
        return cat?.icon || "📖";
    }
    const mt = mediaTypes.find(
        (m) => m.id === props.item.entityData?.media_type,
    );
    return mt?.icon || "📁";
});

const tags = computed(() => {
    const data = props.item.entityData;
    if (props.item.type === "post") return data?.tags || [];
    if (props.item.type === "dex") return data?.genres || [];
    if (props.item.type === "media") return data?.tags || [];
    return [];
});

const typeLabel = computed(() => {
    return { post: "文章", dex: "图鉴", media: "媒体" }[props.item.type];
});
</script>

<template>
    <div>
        <div
            class="block pixel-card bg-white p-4 hover:-translate-y-1 hover:shadow-[6px_6px_0px_0px_rgba(0,0,0,0.8)] transition-all group"
        >
            <div class="flex gap-4">
                <!-- 左侧封面区 -->
                <div
                    v-if="item.coverImage"
                    class="w-28 h-28 shrink-0 border-2 border-black overflow-hidden"
                >
                    <img
                        :src="item.coverImage"
                        :alt="item.title"
                        class="w-full h-full object-cover"
                    />
                </div>

                <!-- 右侧信息 -->
                <div class="flex-1 min-w-0">
                    <!-- 类型徽章 + 分类 -->
                    <div class="flex items-center gap-2 mb-2">
                        <span
                            class="text-xs px-2 py-0.5 border-2 border-black shadow-[2px_2px_0px_0px_rgba(0,0,0,0.5)]"
                            :class="{
                                'bg-blue-500 text-white': item.type === 'post',
                                'bg-red-500 text-white': item.type === 'dex',
                                'bg-green-500 text-white':
                                    item.type === 'media',
                            }"
                        >
                            {{ categoryIcon }} {{ typeLabel }}
                        </span>
                        <span
                            v-if="categoryName"
                            class="text-xs px-2 py-0.5 bg-gray-100 border-2 border-black"
                        >
                            {{ categoryName }}
                        </span>
                    </div>

                    <!-- 标题 -->
                    <h3
                        class="text-base font-bold text-black mb-1 line-clamp-2 group-hover:text-sky-600 transition-colors"
                    >
                        {{ item.title }}
                    </h3>

                    <!-- 描述 -->
                    <p
                        v-if="item.description"
                        class="text-sm text-gray-600 mb-2 line-clamp-2"
                    >
                        {{ item.description }}
                    </p>

                    <!-- 匹配字段提示（做了高亮） -->
                    <div
                        v-if="item.matchedFields.length > 0"
                        class="flex flex-wrap gap-1 mb-2"
                    >
                        <span
                            class="text-xs text-yellow-700 bg-yellow-100 px-1.5 py-0.5"
                        >
                            🔍 匹配: {{ item.matchedFields.join(", ") }}
                        </span>
                    </div>

                    <!-- 标签行 -->
                    <div v-if="tags.length > 0" class="flex flex-wrap gap-1">
                        <span
                            v-for="t in tags.slice(0, 4)"
                            :key="t.id || t.name"
                            class="text-xs px-1.5 py-0.5 bg-gray-50 border border-gray-300"
                        >
                            #{{ t.name }}
                        </span>
                        <span
                            v-if="tags.length > 4"
                            class="text-xs text-gray-500"
                        >
                            +{{ tags.length - 4 }}
                        </span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.pixel-card {
    border: 4px solid #000;
    box-shadow: 4px 4px 0 0 rgba(0, 0, 0, 0.8);
}
</style>
