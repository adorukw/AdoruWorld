<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute} from 'vue-router'
import { marked } from 'marked'
import hljs from 'highlight.js'
import 'highlight.js/styles/atom-one-dark.css'
import Layout from '@/components/layout/Layout.vue'
import PostCard from '@/components/ui/PostCard.vue'
import PixelButton from '@/components/ui/PixelButton.vue'
import { usePostStore } from '@/store'

const postStore = usePostStore()
const { allPosts } = postStore

const route = useRoute()

const readingProgress = ref(0)

const post = computed(() => {
    const foundPost = allPosts.find(p => p.slug === route.params.slug)
    if (!foundPost) {
        console.error('未找到文章')
    }
    return foundPost
})

watch(() => route.params.slug, async (newSlug, oldSlug) => {
    if (newSlug !== oldSlug && post.value) {
        try {
            await postStore.incrementViews(post.value.id)
        }
        catch (err) {
            console.error('获取文章失败:', err)
        }
    }
}, { immediate: true })

const relatedPosts = computed(() => {
    if (!post.value) return []
    return allPosts
        .filter(p => {
            if (p.id === post.value?.id) return false
            const sharedTags = p.tags.map(t => t.name).filter(tag => post.value?.tags.map(t => t.name).includes(tag))
            return sharedTags.length > 0
        })
        .slice(0, 3)
})

// ==========================================
// 1. 使用现代的 marked.use() 替代旧版 API
// ==========================================
marked.use({
    breaks: true,
    gfm: true,
    renderer: {
        // 在 marked.use 中直接覆盖 code 渲染方法
        code({ text, lang }) {
            const language = lang || ''
            const validLang = !!(language && hljs.getLanguage(language))
            const highlighted = validLang
                ? hljs.highlight(text, { language }).value
                : hljs.highlightAuto(text).value

            // 使用 encodeURIComponent 避免代码中的引号破坏 HTML 结构
            const encodedCode = encodeURIComponent(text)
            const langText = language ? language.toUpperCase() : 'CODE'

            return `
                <div class="code-wrapper">
                    <div class="code-header">
                        <span class="code-lang">${langText}</span>
                        <button class="copy-btn pixel-btn-small" data-code="${encodedCode}">
                            复制
                        </button>
                    </div>
                    <pre><code class="hljs ${language}">${highlighted}</code></pre>
                </div>
            `
        }
    }
})

// ==========================================
// 2. 使用 marked.parse() 进行解析
// ==========================================
const renderedContent = computed(() => {
    if (!post.value) return ''

    // 防御性处理：有时候从后端/数据库取出的数据，真正的换行符变成了字面字符串 "\\n"
    // 这会导致 marked 无法识别代码块标记。这里做一下正则替换，确保换行符正常。
    const safeContent = post.value.content.replace(/\\n/g, '\n')

    // 注意：新版必须调用 marked.parse()，不能直接调用 marked()
    return marked.parse(safeContent) as string
})

const handleContentClick = async (e: MouseEvent) => {
    const target = e.target as HTMLElement

    if (target.classList.contains('copy-btn')) {
        const encodedCode = target.getAttribute('data-code')
        if (encodedCode) {
            try {
                const code = decodeURIComponent(encodedCode)
                await navigator.clipboard.writeText(code)

                // 视觉反馈
                const originalText = target.innerText
                target.innerText = '已复制!'
                target.classList.add('copied')

                setTimeout(() => {
                    target.innerText = originalText
                    target.classList.remove('copied')
                }, 2000)
            } catch (err) {
                console.error('复制失败:', err)
                target.innerText = '失败'
            }
        }
    }
}

const handleScroll = () => {
    const scrollTop = window.scrollY
    const docHeight = document.documentElement.scrollHeight - window.innerHeight
    readingProgress.value = Math.min(100, Math.round((scrollTop / docHeight) * 100))
}

const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: 'smooth' })
}

onMounted(() => {
    window.addEventListener('scroll', handleScroll)
})

watch(() => route.params.slug, () => {
    window.scrollTo(0, 0)
    readingProgress.value = 0
})

watch(readingProgress, (newValue, oldValue) => {
    console.log(`阅读进度从 ${oldValue}% 变为 ${newValue}%`)
})
</script>

<template>
    <Layout>
        <template v-if="post">
            <div class="sticky top-20 left-0 right-0 z-40 px-4 py-2 bg-white border-b-4 border-black">
                <div class="relative w-full h-6 bg-gray-200 border-2 border-black">
                    <!-- 黄色填充进度 -->
                    <div class="absolute top-0 left-0 h-full bg-yellow-400 transition-all duration-150 ease-out"
                        :style="{ width: `${readingProgress}%` }"></div>

                    <!-- 网格纹理（可选） -->
                    <div class="absolute inset-0 opacity-20" style="background-image: repeating-linear-gradient(
                        45deg,transparent, transparent 4px,rgba(0,0,0,0.1) 4px,rgba(0,0,0,0.1) 8px)">
                    </div>

                    <!-- 百分比文字 -->
                    <div class="absolute inset-0 flex items-center justify-center">
                        <span class="text-xs font-bold text-black! mix-blend-difference">
                            {{ readingProgress }}%
                        </span>
                    </div>
                </div>
            </div>

            <article>
                <header class="relative py-4 overflow-hidden pb-24">

                    <div class="max-w-4xl mx-auto px-4 relative z-10 text-center">
                        <div class="pixel-text text-3xl md:text-4xl mb-6 leading-relaxed text-black drop-shadow-md">
                            {{ post.title }}
                        </div>
                        <div class="flex flex-wrap justify-center items-center gap-4 font-medium text-gray-800 ">
                            <span class="flex items-center gap-1 bg-white/70 px-2 py-1 rounded border border-black/20">
                                📅 {{ post.createdAt }}
                            </span>
                            <span class="flex items-center gap-1 bg-white/70 px-2 py-1 rounded border border-black/20">
                                👀 {{ post.wordCount }} 字
                            </span>
                            <span class="flex items-center gap-1 bg-white/70 px-2 py-1 rounded border border-black/20">
                                ⏳ {{ post.readingTime }} 分钟阅读
                            </span>
                            <span class="flex items-center gap-1 bg-white/70 px-2 py-1 rounded border border-black/20">
                                👀 {{ post.views }} 次阅读
                            </span>
                        </div>
                    </div>
                </header>

                <div class="max-w-6xl mx-auto px-4 -mt-16 relative z-20 pb-12">
                    <div
                        class="bg-white border-4 border-black rounded-xl p-6 md:p-10 shadow-[8px_8px_0px_0px_rgba(0,0,0,1)]">

                        <div v-if="post.coverImage" class="mb-8">
                            <img :src="post.coverImage" :alt="post.title"
                                class="w-full h-64 md:h-96 object-cover border-4 border-black rounded-lg shadow-[4px_4px_0px_0px_rgba(0,0,0,0.2)]" />
                        </div>

                        <div class="flex flex-wrap gap-2 mb-8 border-b-2 border-gray-100 pb-6">
                            <span v-for="tag in (post.tags.map(tag => tag.name))" :key="tag"
                                class="tag bg-sky-100 border-2 border-black hover:bg-sky-500 hover:text-white cursor-pointer transition-colors px-3 py-1 font-bold rounded">
                                #{{ tag }}
                            </span>
                        </div>

                        <div class="prose prose-lg max-w-none article-content" v-html="renderedContent"
                            @click="handleContentClick" />

                        <div class="mt-12 pt-8 border-t-4 border-black border-dashed">
                            <div
                                class="bg-gray-100 border-4 border-black p-4 rounded-lg mb-8 text-center shadow-[4px_4px_0px_0px_rgba(0,0,0,0.1)]">
                                <p class="pixel-text text-sm mb-0">
                                    感谢阅读！如果这篇文章对你有帮助，欢迎分享给更多人。 🚀
                                </p>
                            </div>

                            <div class="flex flex-wrap gap-4 justify-center">
                                <PixelButton @click="scrollToTop">
                                    返回顶部
                                </PixelButton>
                                <PixelButton>
                                    <router-link to="/">
                                        返回首页
                                    </router-link>
                                </PixelButton>
                            </div>
                        </div>
                    </div>
                </div>

                <section v-if="relatedPosts.length"
                    class="py-12 overflow-hidden relative border-t-4 border-black bg-white">
                    <div class="absolute inset-0 gold-pattern opacity-10"></div>
                    <div class="max-w-6xl mx-auto px-4 relative z-10">
                        <h2 class="pixel-text text-2xl mb-8 flex items-center justify-center gap-3">
                            <span>📖</span> 相关文章
                        </h2>
                        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                            <router-link v-for="relatedPost in relatedPosts" :key="relatedPost.id"
                                :to="`/post/${relatedPost.slug}`"
                                class="block transform transition-transform hover:-translate-y-2">
                                <PostCard :title="relatedPost.title" :cover-image="relatedPost.coverImage"
                                    :tags="relatedPost.tags.map(tag => tag.name)" :date="relatedPost.createdAt"
                                    :reading-time="relatedPost.readingTime" />
                            </router-link>
                        </div>
                    </div>
                </section>
            </article>
        </template>

        <template v-else>
            <div class="min-h-[60vh] flex items-center justify-center bg-gray-50">
                <div
                    class="text-center bg-white border-4 border-black p-10 rounded-xl shadow-[8px_8px_0px_0px_rgba(0,0,0,1)]">
                    <div class="text-6xl mb-4">🔍</div>
                    <h2 class="pixel-text text-2xl mb-4 font-bold">文章未找到</h2>
                    <p class="mb-8 text-gray-600 font-medium">看起来这篇文章不存在或已被丢进了异次元。</p>
                    <router-link to="/"
                        class="pixel-btn bg-sky text-white border-4 border-black px-6 py-2 shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] hover:bg-sky-600 transition-all">
                        返回首页
                    </router-link>
                </div>
            </div>
        </template>
    </Layout>
</template>

<style scoped>
/* =========================================
   文章正文排版 (保证可读性与像素风融合)
   ========================================= */
.article-content {
    color: #1a1a1a;
}

.article-content :deep(h1),
.article-content :deep(h2),
.article-content :deep(h3),
.article-content :deep(h4) {
    color: #000000;
    font-weight: 700;
    line-height: 1.4;
}

.article-content :deep(h1) {
    font-size: 2rem;
    margin: 2.5rem 0 1.5rem;
    padding-bottom: 0.5rem;
    border-bottom: 4px solid #000000;
}

.article-content :deep(h2) {
    font-size: 1.5rem;
    margin: 2rem 0 1rem;
    display: flex;
    align-items: center;
}

.article-content :deep(h2)::before {
    content: '';
    display: inline-block;
    width: 12px;
    height: 12px;
    background-color: #FFDE00;
    border: 2px solid #000;
    margin-right: 10px;
}

.article-content :deep(h3) {
    font-size: 1.25rem;
    color: #3C5AA6;
    margin: 1.5rem 0 0.75rem;
}

.article-content :deep(p) {
    line-height: 1.8;
    margin-bottom: 1.25rem;
    font-size: 1.05rem;
}

.article-content :deep(a) {
    color: #3C5AA6 !important;
    text-decoration: none;
    border-bottom: 2px solid #3C5AA6;
    font-weight: bold;
    transition: all 0.2s ease;
}

.article-content :deep(a:hover) {
    color: #FF7300 !important;
    border-bottom-color: #FF7300;
    background-color: #fff4ec;
}

.article-content :deep(ul),
.article-content :deep(ol) {
    margin: 1.25rem 0;
    padding-left: 2rem;
}

.article-content :deep(li) {
    margin: 0.5rem 0;
    line-height: 1.6;
}

.article-content :deep(img) {
    max-width: 100%;
    border: 4px solid #000000;
    border-radius: 8px;
    margin: 2rem auto;
    display: block;
    box-shadow: 4px 4px 0px 0px rgba(0, 0, 0, 0.1);
}

.article-content :deep(blockquote) {
    margin: 1.5rem 0;
    padding: 1rem 1.5rem;
    border-left: 6px solid #FFDE00;
    background: #fafafa;
    border-radius: 0 8px 8px 0;
    color: #555;
    font-style: italic;
}

.article-content :deep(table) {
    width: 100%;
    border-collapse: collapse;
    margin: 2rem 0;
    box-shadow: 4px 4px 0px 0px rgba(0, 0, 0, 1);
}

.article-content :deep(th),
.article-content :deep(td) {
    border: 3px solid #000000;
    padding: 1rem;
    text-align: left;
}

.article-content :deep(th) {
    background: #FFDE00;
    font-size: 1rem;
    font-weight: bold;
}

/* =========================================
   代码块美化与复制按钮样式
   ========================================= */
.article-content :deep(.code-wrapper) {
    position: relative;
    margin: 2rem 0;
    background: #1e1e1e;
    border: 4px solid #000000;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 4px 4px 0px 0px rgba(0, 0, 0, 1);
}

.article-content :deep(.code-header) {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #2d2d2d;
    padding: 0.5rem 1rem;
    border-bottom: 2px solid #000000;
}

.article-content :deep(.code-lang) {
    color: #a0a0a0;
    font-weight: bold;
    font-family: monospace;
}

.article-content :deep(.copy-btn) {
    background: #4a4a4a;
    color: #ffffff;
    border: 2px solid #000000;
    padding: 0.2rem 0.6rem;
    font-size: 0.75rem;
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.1s;
    font-family: monospace;
}

.article-content :deep(.copy-btn:hover) {
    background: #5a5a5a;
    transform: translateY(-1px);
}

.article-content :deep(.copy-btn:active) {
    transform: translateY(1px);
}

.article-content :deep(.copy-btn.copied) {
    background: #34d399;
    /* 成功绿色 */
    color: #000;
}

.article-content :deep(pre) {
    margin: 0;
    padding: 1.25rem;
    overflow-x: auto;
    background: transparent !important;
}

.article-content :deep(code) {
    font-size: 0.9rem;
    font-family: Consolas, Monaco, 'Andale Mono', 'Ubuntu Mono', monospace;
    line-height: 1.5;
}

/* 行内代码样式 */
.article-content :deep(:not(pre) > code) {
    background: #f4f4f4;
    color: #e83e8c;
    padding: 0.2rem 0.4rem;
    border-radius: 4px;
    border: 1px solid #ccc;
    font-size: 0.875rem;
}
</style>