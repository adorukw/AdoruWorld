<script setup lang="ts">
import { computed, ref, onMounted, watch } from "vue";
import Layout from "@/components/layout/Layout.vue";
import PixelBadge from "@/components/ui/PixelBadge.vue";
import PixelButton from "@/components/ui/PixelButton.vue";
import { usePostStore } from "@/store";
import type { PostCategoryResponse, PostTagResponse } from "@/types";

const postStore = usePostStore();

const dateFrom = ref("");
const dateTo = ref("");
const selectedCategory = ref("all");
const selectedTags = ref<string[]>([]);

const allCategories = computed(() => {
    const seen = new Set<string>();
    const list: PostCategoryResponse[] = [];
    postStore.archives.forEach((am) => {
        am.posts.forEach((post) => {
            if (post.category && !seen.has(post.category.slug)) {
                seen.add(post.category.slug);
                list.push(post.category);
            }
        });
    });
    return list;
});

const allTags = computed(() => {
    const seen = new Set<string>();
    const list: PostTagResponse[] = [];
    postStore.archives.forEach((am) => {
        am.posts.forEach((post) => {
            post.tags.forEach((tag) => {
                if (!seen.has(tag.slug)) {
                    seen.add(tag.slug);
                    list.push(tag);
                }
            });
        });
    });
    return list;
});

// ── 日期筛选用的分离值（年/月/日分别控制） ──
// 起始日期
const fromYear = ref<number | "">("");
const fromMonth = ref<number | "">("");
const fromDay = ref<number | "">("");
// 截止日期
const toYear = ref<number | "">("");
const toMonth = ref<number | "">("");
const toDay = ref<number | "">("");

// ── 可选的年份列表（从归档数据里提取） ──
const availableYears = computed(() => {
    const years = new Set<number>();
    postStore.archives.forEach((am) => years.add(am.year));
    return Array.from(years).sort((a, b) => b - a); // 降序
});

// ── 根据选中的年/月计算该月天数 ──
const daysInMonth = (year: number | "", month: number | "") => {
    if (year === "" || month === "") return 31;
    return new Date(year, month, 0).getDate();
};

// ── 把分离的年/月/日同步回 dateFrom / dateTo（字符串） ──
// 注意：当任意一个字段为空时，设空字符串（不清除，而是让筛选忽略该项）
watch([fromYear, fromMonth, fromDay], () => {
    if (
        fromYear.value !== "" &&
        fromMonth.value !== "" &&
        fromDay.value !== ""
    ) {
        const m = String(fromMonth.value).padStart(2, "0");
        const d = String(fromDay.value).padStart(2, "0");
        dateFrom.value = `${fromYear.value}-${m}-${d}`;
    } else {
        dateFrom.value = "";
    }
});

watch([toYear, toMonth, toDay], () => {
    if (toYear.value !== "" && toMonth.value !== "" && toDay.value !== "") {
        const m = String(toMonth.value).padStart(2, "0");
        const d = String(toDay.value).padStart(2, "0");
        dateTo.value = `${toYear.value}-${m}-${d}`;
    } else {
        dateTo.value = "";
    }
});

// ── 清空日期时一并清掉分离值 ──
const clearDates = () => {
    fromYear.value = "";
    fromMonth.value = "";
    fromDay.value = "";
    toYear.value = "";
    toMonth.value = "";
    toDay.value = "";
};

// ── 在清除全部筛选时也要清日期 ──

const filteredArchives = computed(() => {
    return postStore.archives
        .map((am) => ({
            year: am.year,
            month: am.month,
            posts: am.posts.filter((post) => {
                // ① 日期范围
                if (
                    dateFrom.value &&
                    new Date(post.createdAt) < new Date(dateFrom.value)
                )
                    return false;
                if (dateTo.value) {
                    const end = new Date(dateTo.value);
                    end.setHours(23, 59, 59, 999);
                    if (new Date(post.createdAt) > end) return false;
                }
                // ② 分类
                if (
                    selectedCategory.value !== "all" &&
                    post.category?.slug !== selectedCategory.value
                )
                    return false;
                // ③ 标签（多选，满足任一）
                if (
                    selectedTags.value.length > 0 &&
                    !post.tags.some((t) => selectedTags.value.includes(t.slug))
                )
                    return false;
                return true;
            }),
        }))
        .filter((am) => am.posts.length > 0); // 去掉被筛空的月
});

const hasActiveFilters = computed(
    () =>
        dateFrom.value !== "" ||
        dateTo.value !== "" ||
        selectedCategory.value !== "all" ||
        selectedTags.value.length > 0,
);

onMounted(async () => {
    await postStore.getArchives();
});

const groupedPosts = computed(() => {
    const groups: {
        [year: number]: {
            year: number;
            month: number;
            posts: (typeof postStore.archives)[0]["posts"];
        }[];
    } = {};

    filteredArchives.value.forEach((item) => {
        if (!groups[item.year]) {
            groups[item.year] = [];
        }
        groups[item.year].push({
            year: item.year,
            month: item.month,
            posts: item.posts,
        });
    });

    return Object.entries(groups)
        .sort((a, b) => Number(b[0]) - Number(a[0]))
        .map(([year, months]) => ({
            year: Number(year),
            months: months.sort((a, b) => b.month - a.month),
        }));
});

const filteredPostsCount = computed(() =>
    filteredArchives.value.reduce((sum, am) => sum + am.posts.length, 0),
);

const monthNames = [
    "一月",
    "二月",
    "三月",
    "四月",
    "五月",
    "六月",
    "七月",
    "八月",
    "九月",
    "十月",
    "十一月",
    "十二月",
];
</script>

<template>
    <Layout>
        <section class="relative py-4 overflow-hidden border-b-4">
            <div class="max-w-6xl mx-auto px-4 relative z-10">
                <div class="text-center">
                    <div class="inline-block mb-4">
                        <div
                            class="w-20 h-20 border-4 mx-auto mb-4 flex items-center justify-center shadow-lg relative overflow-hidden"
                        >
                            <div
                                class="absolute inset-0 bg-linear-to-b from-white/30 to-transparent"
                            ></div>
                            <span class="text-4xl relative z-10">📚</span>
                        </div>
                    </div>
                    <h1
                        class="pixel-text text-2xl md:text-3xl mb-4 drop-shadow-sm"
                    >
                        归档 Archive
                    </h1>
                    <p class="pixel-text text-2xl! max-w-xl mx-auto">
                        按时间浏览所有文章
                    </p>
                </div>
            </div>
        </section>

        <section class="relative py-4 overflow-hidden border-b-4">
            <div class="max-w-4xl mx-auto px-4">
                <div class="space-y-4 p-4 pixel-card pixel-box bg-yellow-100!">
                    <!-- 分类 -->
                    <div>
                        <div class="mb-2">分类</div>
                        <div class="flex flex-wrap gap-2">
                            <!-- <button class="px-3 py-1 pixel-text   border-2 transition-all" :class="selectedCategory === 'all'
                                ? '  bg-sky-dark text-white'
                                : '  hover:bg-black/5'" @click="selectedCategory = 'all'">全部</button> -->
                            <button
                                v-for="cat in allCategories"
                                :key="cat.slug"
                                :class="
                                    selectedCategory === cat.slug
                                        ? '  bg-sky-dark text-white text-sm'
                                        : '  hover:bg-black/5'
                                "
                                @click="
                                    selectedCategory =
                                        selectedCategory === cat.slug
                                            ? 'all'
                                            : cat.slug
                                "
                            >
                                <PixelBadge
                                    :name="cat.name"
                                    :color="cat.color"
                                    :icon="cat.icon"
                                ></PixelBadge>
                            </button>
                            <span v-if="allCategories.length === 0" class="  "
                                >（暂无可筛选分类）</span
                            >
                        </div>
                    </div>

                    <!-- 标签 -->
                    <div>
                        <div class="mb-2">标签</div>
                        <div class="flex flex-wrap gap-2">
                            <button
                                v-for="tag in allTags"
                                :key="tag.slug"
                                :class="
                                    selectedTags.includes(tag.slug)
                                        ? 'bg-sky-light/60  border-sky-dark text-sm'
                                        : '  border-transparent hover:bg-black/5'
                                "
                                @click="
                                    selectedTags = selectedTags.includes(
                                        tag.slug,
                                    )
                                        ? selectedTags.filter(
                                              (s) => s !== tag.slug,
                                          )
                                        : [...selectedTags, tag.slug]
                                "
                            >
                                <PixelBadge
                                    :name="tag.name"
                                    :color="tag.color"
                                ></PixelBadge>
                            </button>
                            <span v-if="allTags.length === 0" class="  "
                                >（暂无可筛选标签）</span
                            >
                        </div>
                    </div>

                    <!-- 日期范围 -->
                    <div>
                        <div class="mb-2">日期范围</div>

                        <!-- 起始日期 -->
                        <div class="flex items-center gap-1 flex-wrap mb-2">
                            <span class="  ">从</span>
                            <!-- 年 -->
                            <select
                                v-model="fromYear"
                                class="pixel-input py-1 px-1 w-20"
                            >
                                <option value="">--</option>
                                <option
                                    v-for="y in availableYears"
                                    :key="y"
                                    :value="y"
                                >
                                    {{ y }} 年
                                </option>
                            </select>
                            <!-- 月 -->
                            <select
                                v-model="fromMonth"
                                class="pixel-input py-1 px-1 w-16"
                            >
                                <option value="">--</option>
                                <option v-for="m in 12" :key="m" :value="m">
                                    {{ String(m).padStart(2, "0") }} 月
                                </option>
                            </select>
                            <!-- 日 -->
                            <select
                                v-model="fromDay"
                                class="pixel-input py-1 px-1 w-16"
                            >
                                <option value="">--</option>
                                <option
                                    v-for="d in daysInMonth(
                                        fromYear,
                                        fromMonth,
                                    )"
                                    :key="d"
                                    :value="d"
                                >
                                    {{ String(d).padStart(2, "0") }} 日
                                </option>
                            </select>
                        </div>

                        <!-- 截止日期 -->
                        <div class="flex items-center gap-1 flex-wrap">
                            <span class="  ">至</span>
                            <select
                                v-model="toYear"
                                class="pixel-input py-1 px-1 w-20"
                            >
                                <option value="">--</option>
                                <option
                                    v-for="y in availableYears"
                                    :key="y"
                                    :value="y"
                                >
                                    {{ y }} 年
                                </option>
                            </select>
                            <select
                                v-model="toMonth"
                                class="pixel-input py-1 px-1 w-16"
                            >
                                <option value="">--</option>
                                <option v-for="m in 12" :key="m" :value="m">
                                    {{ String(m).padStart(2, "0") }} 月
                                </option>
                            </select>
                            <select
                                v-model="toDay"
                                class="pixel-input py-1 px-1 w-16"
                            >
                                <option value="">--</option>
                                <option
                                    v-for="d in daysInMonth(toYear, toMonth)"
                                    :key="d"
                                    :value="d"
                                >
                                    {{ String(d).padStart(2, "0") }} 日
                                </option>
                            </select>
                        </div>
                    </div>
                    <div class="text-right">
                        <button
                            class="px-3 py-1 text-sm hover:underline"
                            @click="
                                dateFrom = '';
                                dateTo = '';
                                selectedCategory = 'all';
                                selectedTags = [];
                                clearDates();
                            "
                        >
                            <PixelButton> ✕清除所有筛选 </PixelButton>
                        </button>
                        <div v-if="hasActiveFilters" class="text-left">
                            筛选结果：共
                            <strong>{{ filteredPostsCount }}</strong> 篇文章
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <section class="py-12">
            <div class="max-w-4xl mx-auto px-4">
                <div
                    v-for="yearGroup in groupedPosts"
                    :key="yearGroup.year"
                    class="mb-12"
                >
                    <div class="flex items-center gap-4 mb-6">
                        <div class="pixel-card pixel-box">
                            <span class="text-lg">{{ yearGroup.year }}</span>
                        </div>
                        <div class="flex-1 h-1 /20"></div>
                    </div>

                    <div
                        v-for="monthGroup in yearGroup.months"
                        :key="`${yearGroup.year}-${monthGroup.month}`"
                        class="mb-8"
                    >
                        <h3 class="text-sm mb-4 flex items-center gap-2">
                            <span class="text-sky-dark">◆</span>
                            {{ monthNames[monthGroup.month - 1] }}
                            <span class="  "
                                >({{ monthGroup.posts.length }}篇)</span
                            >
                        </h3>

                        <div class="space-y-4 ml-4 border-l-4 border-gold pl-6">
                            <router-link
                                v-for="post in monthGroup.posts"
                                :key="post.id"
                                :to="`/post/${post.slug}`"
                                class="pixel-card block pixel-box hover:translate-x-2 transition-transform"
                            >
                                <img
                                    :src="post?.coverImage"
                                    :alt="post.title"
                                    class="border-2 w-full h-48 object-cover transition-transform duration-300 group-hover:scale-105"
                                    style="image-rendering: auto"
                                />
                                <div
                                    class="flex flex-wrap items-start justify-between gap-2"
                                >
                                    <div class="flex-1">
                                        <h4
                                            class="font-medium hover:text-sky-dark transition-colors"
                                        >
                                            {{ post.title }}
                                        </h4>
                                        <div class="flex flex-wrap gap-2 mt-2">
                                            <span
                                                v-for="tag in post.tags.slice(
                                                    0,
                                                    3,
                                                )"
                                                :key="tag.id"
                                                class="px-2 py-0.5 bg-sky-light/50 rounded"
                                            >
                                                #{{ tag.name }}
                                            </span>
                                        </div>
                                    </div>
                                    <div class="text-right">
                                        <div>{{ post.createdAt }}</div>
                                        <div class="mt-1">
                                            {{ post.readingTime }} 分钟
                                        </div>
                                    </div>
                                </div>
                            </router-link>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </Layout>
</template>

<style scoped></style>
