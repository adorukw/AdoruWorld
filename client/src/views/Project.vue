<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import Layout from '@/components/layout/Layout.vue'
import PixelButton from '@/components/ui/PixelButton.vue'
import SkyCloud from '@/components/ui/SkyCloud.vue'

interface GitHubRepo {
    id: number
    name: string
    full_name: string
    description: string | null
    html_url: string
    homepage: string | null
    language: string | null
    stargazers_count: number
    forks_count: number
    topics: string[]
    updated_at: string
    pushed_at: string
    fork: boolean
    archived: boolean
}

interface GitHubUser {
    login: string
    avatar_url: string
    html_url: string
    public_repos: number
    followers: number
    following: number
}

// ── 状态 ──
const repos = ref<GitHubRepo[]>([])
const user = ref<GitHubUser | null>(null)
const loading = ref(true)
const error = ref<string | null>(null)

// ── 过滤掉 fork 仓库，取前 10 个 ──
const filteredRepos = computed(() =>
    repos.value
        .filter(r => !r.fork)
        .slice(0, 10)
)

// ── 相对时间 ──
function timeAgo(dateStr: string): string {
    if (!dateStr) return ''
    const now = Date.now()
    const then = new Date(dateStr).getTime()
    const diff = Math.floor((now - then) / 1000)
    if (diff < 60) return '刚刚'
    if (diff < 3600) return `${Math.floor(diff / 60)} 分钟前`
    if (diff < 86400) return `${Math.floor(diff / 3600)} 小时前`
    if (diff < 2592000) return `${Math.floor(diff / 86400)} 天前`
    if (diff < 31536000) return `${Math.floor(diff / 2592000)} 个月前`
    return `${Math.floor(diff / 31536000)} 年前`
}

// ── 语言配色 ──
const langColors: Record<string, string> = {
    TypeScript: '#3178c6',
    JavaScript: '#f7df1e',
    Python: '#3572a5',
    Vue: '#4fc08d',
    HTML: '#e34c26',
    CSS: '#563d7c',
    Java: '#b07219',
    Go: '#00add8',
    Rust: '#dea584',
    Shell: '#89e051',
    Dockerfile: '#384d54',
    PHP: '#4f5d95',
    C: '#555555',
    'C++': '#f34b7d',
    Ruby: '#701516',
    Kotlin: '#a97bff',
    Swift: '#f05138',
    Dart: '#00b4ab',
    Lua: '#000080',
}

function langColor(lang: string | null): string {
    if (!lang) return '#888'
    return langColors[lang] ?? '#6b7280'
}
onMounted(async () => {
    try {
        const [userRes, reposRes] = await Promise.all([
            fetch('https://api.github.com/users/adorukw'),
            fetch('https://api.github.com/users/adorukw/repos?sort=updated&per_page=10'),
        ])
        if (!userRes.ok || !reposRes.ok) {
            throw new Error(`GitHub API 响应异常 ${userRes.status} / ${reposRes.status}`)
        }
        user.value = await userRes.json()
        repos.value = await reposRes.json()
    } catch (e) {
        error.value = e instanceof Error ? e.message : '获取 GitHub 数据失败'
        console.error('GitHub fetch error:', e)
    } finally {
        loading.value = false
    }
})

function reloadPage() {
    window.location.reload()
}
</script>

<template>
    <Layout>
        <!-- ── 页头 ── -->
        <section class="relative py-16 overflow-hidden border-b-2 border-dashed">
            <SkyCloud />
            <div class="max-w-6xl mx-auto px-4 text-center relative z-10">
                <h1 class="pixel-text text-2xl mb-4 drop-shadow-sm">🚀 项目</h1>
                <p class="t">GitHub 上的足迹 &amp; 个人作品集</p>
            </div>
        </section>

        <!-- ════════════════════════════════════════════ -->
        <!-- GitHub 贡献热图                                  -->
        <!-- ════════════════════════════════════════════ -->
        <section class="py-12">
            <div class="max-w-6xl mx-auto px-4">
                <div class="pixel-card p-6">
                    <div class="flex items-center gap-3 mb-6">
                        <span class="text-2xl">📅</span>
                        <h2 class="pixel-text text-lg">GitHub 贡献热图</h2>
                    </div>

                    <!-- 用户信息概要 -->
                    <div v-if="!loading && user" class="flex flex-wrap items-center gap-6 mb-6 text-sm">
                        <a :href="user.html_url" target="_blank"
                            class="flex items-center gap-2 hover:opacity-80 transition-opacity">
                            <img :src="user.avatar_url" alt="avatar"
                                class="w-10 h-10 rounded-full border-2 border-black pixel-card" />
                            <span class="pixel-text">{{ user.login }}</span>
                        </a>
                        <span class="flex items-center gap-1">
                            <span class="text-base">📦</span>
                            <span><strong>{{ user.public_repos }}</strong> 公开仓库</span>
                        </span>
                        <span class="flex items-center gap-1">
                            <span class="text-base">👥</span>
                            <span><strong>{{ user.followers }}</strong> 粉丝</span>
                        </span>
                        <span class="flex items-center gap-1">
                            <span class="text-base">👣</span>
                            <span><strong>{{ user.following }}</strong> 关注</span>
                        </span>
                    </div>

                    <!-- 贡献图 -->
                    <div v-if="!loading" class="overflow-hidden rounded border-2 border-black/20 bg-white/50 p-1">
                        <img src="https://ghchart.rshah.org/adorukw" alt="adorukw's GitHub contribution chart"
                            class="w-full h-auto pixelated"
                            style="image-rendering: pixelated; image-rendering: crisp-edges;" />
                    </div>

                    <!-- 加载中 -->
                    <div v-if="loading" class="py-12 text-center">
                        <span class="pixel-text text-sm t">🔄 加载贡献数据中...</span>
                    </div>

                    <!-- 错误 -->
                    <div v-if="error" class="py-6 text-center">
                        <p class="pixel-text text-sm text-red-600">{{ error }}</p>
                    </div>
                </div>
            </div>
        </section>

        <!-- ════════════════════════════════════════════ -->
        <!-- GitHub 公开仓库                                  -->
        <!-- ════════════════════════════════════════════ -->
        <section class="pb-12">
            <div class="max-w-6xl mx-auto px-4">
                <div class="flex items-center gap-3 mb-6">
                    <span class="text-2xl">📂</span>
                    <h2 class="pixel-text text-lg">公开仓库</h2>
                </div>

                <!-- 加载骨架 -->
                <div v-if="loading" class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div v-for="i in 4" :key="i" class="pixel-card p-5 animate-pulse">
                        <div class="h-5 bg-gray-200 rounded w-3/4 mb-4"></div>
                        <div class="h-3 bg-gray-100 rounded w-full mb-2"></div>
                        <div class="h-3 bg-gray-100 rounded w-1/2 mb-4"></div>
                        <div class="flex gap-2">
                            <div class="h-4 bg-gray-200 rounded w-12"></div>
                            <div class="h-4 bg-gray-200 rounded w-12"></div>
                        </div>
                    </div>
                </div>

                <!-- 仓库列表 -->
                <div v-else-if="!error" class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div v-for="repo in filteredRepos" :key="repo.id"
                        class="pixel-card p-5 group transition-all duration-100
              hover:-translate-x-0.5 hover:-translate-y-0.5
              hover:shadow-[6px_6px_0_0_#2c2c2c] active:translate-x-1 active:translate-y-1 active:shadow-[2px_2px_0_0_#2c2c2c]">
                        <!-- 标题 + Star -->
                        <div class="flex items-start justify-between gap-2 mb-2">
                            <a :href="repo.html_url" target="_blank" class="pixel-text text-sm text-[#3b4cca] hover:text-[#4a5fd8] truncate
                  underline decoration-dotted underline-offset-2">
                                {{ repo.name }}
                            </a>
                            <div class="flex items-center gap-2 shrink-0 text-xs">
                                <span class="flex items-center gap-0.5" title="Stars">
                                    ⭐ {{ repo.stargazers_count }}
                                </span>
                                <span class="flex items-center gap-0.5" title="Forks">
                                    🍴 {{ repo.forks_count }}
                                </span>
                            </div>
                        </div>

                        <!-- 描述 -->
                        <p v-if="repo.description" class="text-xs t line-clamp-2 mb-3 leading-relaxed">
                            {{ repo.description }}
                        </p>

                        <!-- 语言 + 更新时间 -->
                        <div class="flex flex-wrap items-center gap-x-4 gap-y-1 text-xs">
                            <span v-if="repo.language" class="flex items-center gap-1.5">
                                <span class="inline-block w-2.5 h-2.5 rounded-full border border-black/30"
                                    :style="{ backgroundColor: langColor(repo.language) }"></span>
                                {{ repo.language }}
                            </span>
                            <span class="t">🕐 {{ timeAgo(repo.pushed_at) }}</span>
                            <span v-if="repo.archived"
                                class="px-2 py-0.5 border border-black/30 bg-gray-100 text-xs t">📦 已归档</span>
                        </div>

                        <!-- Topics -->
                        <div v-if="repo.topics && repo.topics.length" class="flex flex-wrap gap-1.5 mt-3">
                            <span v-for="topic in repo.topics.slice(0, 4)" :key="topic" class="px-2 py-0.5 text-[10px] leading-none
                  border border-black/30 bg-[#e8f0fe] text-[#1967d2]">
                                {{ topic }}
                            </span>
                            <span v-if="repo.topics.length > 4" class="px-2 py-0.5 text-[10px] leading-none t">+{{
                                repo.topics.length - 4 }}</span>
                        </div>
                    </div>
                </div>

                <!-- 错误提示 -->
                <div v-else class="pixel-card p-8 text-center">
                    <p class="text-lg mb-2">😅 加载 GitHub 仓库失败了</p>
                    <p class="text-xs t mb-4">{{ error }}</p>
                    <PixelButton color="blue" @click="reloadPage()">
                        重试
                    </PixelButton>
                </div>
            </div>
        </section>
    </Layout>
</template>

<style scoped>
/* 确保像素风格的图片渲染 */
.pixelated {
    image-rendering: pixelated;
    image-rendering: crisp-edges;
}
</style>
