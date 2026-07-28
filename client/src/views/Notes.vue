<script setup lang="ts">
/**
 * 笔记页面
 *
 * 从 GitHub 仓库 adorukw/Note 读取所有 .md 文件，
 * 左栏显示目录树，右栏渲染 Markdown 内容。
 *
 * 核心逻辑：
 *   1. onMounted → fetchNoteTree() 拿到完整文件树（1 次 API 调用）
 *   2. 点击文件 → fetchNoteContentRaw() 读取 raw 内容
 *   3. marked.parse() → 渲染为 HTML
 *
 * 数据流：
 *   GitHub Tree API → 树形结构 → FileTree 组件
 *          ↓ 点击文件
 *   raw.githubusercontent.com → Markdown 文本 → marked → HTML
 */

import { ref, computed, onMounted, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import { marked } from "marked";
import hljs from "highlight.js";
import "highlight.js/styles/atom-one-dark.css";
import Layout from "@/components/layout/Layout.vue";
import FileTree from "@/components/ui/FileTree.vue";
import { fetchNoteTree, fetchNoteContentRaw } from "@/api/notes";
import type { NoteTreeNode } from "@/api/notes";

// ──────────────────────────────────────────
// 状态
// ──────────────────────────────────────────

const route = useRoute();
const router = useRouter();

/** 文件树（从 GitHub API 获取） */
const treeNodes = ref<NoteTreeNode[]>([]);
/** 文件树加载状态 */
const treeLoading = ref(true);
/** 文件树加载错误 */
const treeError = ref<string | null>(null);

/** 当前选中的文件路径 */
const activeFilePath = ref<string | null>(null);
/** 当前笔记的原始 Markdown */
const noteContent = ref<string | null>(null);
/** 笔记内容加载状态 */
const contentLoading = ref(false);
/** 笔记内容加载错误 */
const contentError = ref<string | null>(null);

// ──────────────────────────────────────────
// 生命周期
// ──────────────────────────────────────────

onMounted(async () => {
    await loadTree();

    // 如果 URL 中有路径参数（如 /notes/技术笔记/Python/系统教程.md）
    // 则自动加载对应文件
    const raw = route.params.path;
    const pathParam = Array.isArray(raw) ? raw.join("/") : raw;
    if (pathParam) {
        loadNote(decodeURIComponent(pathParam));
    }
});

// 监听路由变化（点击笔记内链接或浏览器前进/后退）
watch(
    () => route.params.path,
    (newPath) => {
        if (newPath) {
            const pathParam = Array.isArray(newPath)
                ? newPath.join("/")
                : newPath;
            loadNote(decodeURIComponent(pathParam));
        } else {
            // 回到了 /notes，清空内容
            noteContent.value = null;
            activeFilePath.value = null;
        }
    },
);

// ──────────────────────────────────────────
// 函数
// ──────────────────────────────────────────

/**
 * 加载文件树
 */
async function loadTree() {
    treeLoading.value = true;
    treeError.value = null;
    try {
        treeNodes.value = await fetchNoteTree();
    } catch (err: any) {
        console.error("加载文件树失败:", err);
        treeError.value = err.message || "加载笔记目录失败，请稍后重试";
    } finally {
        treeLoading.value = false;
    }
}

/**
 * 选中某个笔记文件 → 加载内容并更新 URL
 */
async function loadNote(filePath: string) {
    if (activeFilePath.value === filePath && noteContent.value) {
        return; // 已经是这个文件，无需重复加载
    }

    activeFilePath.value = filePath;
    noteContent.value = null;
    contentLoading.value = true;
    contentError.value = null;

    // 更新 URL（实现可分享链接和浏览器前进后退）
    router.replace({ path: `/notes/${filePath}` });

    try {
        const content = await fetchNoteContentRaw(filePath);
        noteContent.value = content;
    } catch (err: any) {
        console.error("加载笔记内容失败:", err);
        contentError.value = err.message || "读取笔记失败";
    } finally {
        contentLoading.value = false;
    }
}

/**
 * 处理文件选择事件（从 FileTree 组件传来）
 */
function onFileSelect(filePath: string) {
    loadNote(filePath);
}

// ──────────────────────────────────────────
// Markdown 渲染
// ──────────────────────────────────────────

const slugify = (text: string) => {
    return text
        .toLowerCase()
        .replace(/[^\w\u4e00-\u9fa5]+/g, "-")
        .replace(/^-+|-+$/g, "");
};

// 配置 marked 渲染器（与 PostDetail 保持一致的风格）
marked.use({
    breaks: true,
    gfm: true,
    renderer: {
        heading({ text, depth }) {
            const id = slugify(text);
            return `<h${depth} id="${id}" style="scroll-margin-top: 130px">${text}</h${depth}>`;
        },
        code({ text, lang }) {
            const language = lang || "";
            const validLang = !!(language && hljs.getLanguage(language));
            const highlighted = validLang
                ? hljs.highlight(text, { language }).value
                : hljs.highlightAuto(text).value;

            const encodedCode = encodeURIComponent(text);
            const langText = language ? language.toUpperCase() : "CODE";

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
      `;
        },
    },
});

const renderedContent = computed(() => {
    if (!noteContent.value) return "";
    return marked.parse(noteContent.value) as string;
});

/** 文件名（不含后缀），显示在面包屑里 */
const currentFileName = computed(() => {
    if (!activeFilePath.value) return "";
    const parts = activeFilePath.value.split("/");
    const last = parts[parts.length - 1];
    return last.replace(/\.md$/, "");
});

/** 当前文件所在目录路径（面包屑用） */
const currentFolderPath = computed(() => {
    if (!activeFilePath.value) return "";
    const parts = activeFilePath.value.split("/");
    parts.pop(); // 去掉文件名
    return parts.join(" / ");
});

/** 文件总数统计 */
const totalFiles = computed(() => countFiles(treeNodes.value));
function countFiles(nodes: NoteTreeNode[]): number {
    let count = 0;
    for (const node of nodes) {
        if (node.type === "file") count++;
        count += countFiles(node.children);
    }
    return count;
}

/** 复制按钮点击处理 */
async function handleContentClick(e: MouseEvent) {
    const target = e.target as HTMLElement;

    if (target.classList.contains("copy-btn")) {
        const encodedCode = target.getAttribute("data-code");
        if (encodedCode) {
            try {
                const code = decodeURIComponent(encodedCode);
                await navigator.clipboard.writeText(code);

                const originalText = target.innerText;
                target.innerText = "已复制!";
                target.classList.add("copied");

                setTimeout(() => {
                    target.innerText = originalText;
                    target.classList.remove("copied");
                }, 2000);
            } catch (err) {
                console.error("复制失败:", err);
                target.innerText = "失败";
            }
        }
    }
}
</script>

<template>
    <Layout>
        <div class="notes-page">
            <!-- ========== 左栏：目录树 ========== -->
            <aside class="notes-sidebar">
                <div class="sidebar-header">
                    <h2 class="sidebar-title">📓 笔记目录</h2>
                </div>

                <!-- 文件树加载中 -->
                <div v-if="treeLoading" class="sidebar-status">
                    <div class="loading-spinner"></div>
                    <span>正在读取笔记仓库...</span>
                </div>

                <!-- 文件树加载失败 -->
                <div v-else-if="treeError" class="sidebar-status sidebar-error">
                    <span>❌ {{ treeError }}</span>
                    <button class="retry-btn" @click="loadTree">重试</button>
                </div>

                <!-- 正常显示文件树 -->
                <div v-else class="sidebar-tree">
                    <FileTree
                        :nodes="treeNodes"
                        :active-path="activeFilePath"
                        :level="0"
                        @select="onFileSelect"
                    />
                </div>
            </aside>

            <!-- ========== 右栏：笔记内容 ========== -->
            <main class="notes-content">
                <!-- 未选择任何笔记时显示欢迎页 -->
                <div
                    v-if="!activeFilePath && !contentLoading"
                    class="welcome-screen"
                >
                    <div class="welcome-card">
                        <div class="welcome-icon">📓</div>
                        <h1 class="welcome-title">笔记</h1>
                        <p class="welcome-desc">
                            从左侧目录选择一个笔记开始阅读吧 ✨
                        </p>
                        <div class="welcome-stats">
                            <div class="stat-item">
                                <span class="stat-number">{{
                                    totalFiles
                                }}</span>
                                <span class="stat-label">篇笔记</span>
                            </div>
                            <div class="stat-item">
                                <span class="stat-number">{{
                                    treeNodes.length ? "GitHub" : "—"
                                }}</span>
                                <span class="stat-label">数据源</span>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 内容加载中 -->
                <div v-else-if="contentLoading" class="content-status">
                    <div class="loading-spinner"></div>
                    <span>正在加载笔记...</span>
                </div>

                <!-- 内容加载失败 -->
                <div
                    v-else-if="contentError"
                    class="content-status content-error"
                >
                    <span>❌ {{ contentError }}</span>
                    <button
                        class="retry-btn"
                        @click="loadNote(activeFilePath!)"
                    >
                        重试
                    </button>
                </div>

                <!-- 正常显示笔记内容 -->
                <article v-else-if="noteContent" class="note-article">
                    <!-- 面包屑导航 -->
                    <div class="note-breadcrumb">
                        <router-link to="/notes" class="breadcrumb-link"
                            >笔记</router-link
                        >
                        <span v-if="currentFolderPath" class="breadcrumb-sep"
                            >/</span
                        >
                        <span
                            v-if="currentFolderPath"
                            class="breadcrumb-folder"
                            >{{ currentFolderPath }}</span
                        >
                        <span class="breadcrumb-sep">/</span>
                        <span class="breadcrumb-current">{{
                            currentFileName
                        }}</span>
                    </div>

                    <!-- Markdown 渲染内容 -->
                    <div class="note-body">
                        <div
                            class="prose prose-lg max-w-none note-content"
                            v-html="renderedContent"
                            @click="handleContentClick"
                        />
                    </div>
                </article>
            </main>
        </div>
    </Layout>
</template>

<style scoped>
/* ──────────────────────────────
   整体布局
   ────────────────────────────── */
.notes-page {
    display: flex;
    min-height: calc(100vh - 140px);
    /* 减去 header + footer 的大致高度 */
    background: #fafafa;
}

/* ──────────────────────────────
   左栏：侧边栏
   ────────────────────────────── */
.notes-sidebar {
    width: 300px;
    min-width: 300px;
    background: white;
    border-right: 3px solid #000;
    display: flex;
    flex-direction: column;
    overflow: hidden;
}

.sidebar-header {
    padding: 16px;
    border-bottom: 3px solid #000;
    background: #f8f8f8;
}

.sidebar-title {
    font-size: 18px;
    font-weight: 700;
    margin: 0;
    color: #111;
}

.sidebar-tree {
    flex: 1;
    overflow-y: auto;
    padding: 8px 4px;
}

.sidebar-status {
    padding: 24px 16px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 12px;
    color: #666;
    font-size: 14px;
    text-align: center;
}

.sidebar-error {
    color: #dc2626;
}

.retry-btn {
    padding: 6px 16px;
    background: #111;
    color: white;
    border: 2px solid #000;
    border-radius: 6px;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.15s;
}

.retry-btn:hover {
    background: #333;
}

/* ──────────────────────────────
   右栏：内容区
   ────────────────────────────── */
.notes-content {
    flex: 1;
    overflow-y: auto;
    padding: 0;
}

/* ──────────────────────────────
   欢迎页
   ────────────────────────────── */
.welcome-screen {
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: calc(100vh - 140px);
    padding: 40px;
}

.welcome-card {
    text-align: center;
    background: white;
    border: 4px solid #000;
    border-radius: 16px;
    padding: 48px 40px;
    max-width: 480px;
    box-shadow: 8px 8px 0 0 rgba(0, 0, 0, 1);
}

.welcome-icon {
    font-size: 64px;
    margin-bottom: 16px;
}

.welcome-title {
    font-size: 28px;
    font-weight: 800;
    margin: 0 0 12px 0;
    color: #111;
}

.welcome-desc {
    font-size: 15px;
    color: #666;
    margin: 0 0 32px 0;
    line-height: 1.6;
}

.welcome-stats {
    display: flex;
    justify-content: center;
    gap: 32px;
}

.stat-item {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.stat-number {
    font-size: 24px;
    font-weight: 800;
    color: #111;
}

.stat-label {
    font-size: 13px;
    color: #888;
    margin-top: 4px;
}

/* ──────────────────────────────
   加载状态
   ────────────────────────────── */
.content-status {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 16px;
    min-height: 400px;
    color: #666;
    font-size: 15px;
}

.content-error {
    color: #dc2626;
}

.loading-spinner {
    width: 32px;
    height: 32px;
    border: 3px solid #e5e7eb;
    border-top: 3px solid #111;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
}

@keyframes spin {
    to {
        transform: rotate(360deg);
    }
}

/* ──────────────────────────────
   笔记正文
   ────────────────────────────── */
.note-article {
    max-width: 880px;
    margin: 0 auto;
    padding: 32px 40px 80px;
}

.note-breadcrumb {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 14px;
    padding-bottom: 16px;
    margin-bottom: 24px;
    border-bottom: 2px solid #e5e7eb;
    flex-wrap: wrap;
}

.breadcrumb-link {
    color: #0369a1;
    text-decoration: none;
    font-weight: 600;
}

.breadcrumb-link:hover {
    text-decoration: underline;
}

.breadcrumb-sep {
    color: #999;
    font-size: 12px;
}

.breadcrumb-folder {
    color: #666;
}

.breadcrumb-current {
    color: #111;
    font-weight: 700;
}

/* ──────────────────────────────
   Markdown 内容样式
   ────────────────────────────── */
.note-body {
    background: white;
    border: 3px solid #000;
    border-radius: 12px;
    padding: 32px 40px;
    box-shadow: 6px 6px 0 0 rgba(0, 0, 0, 0.8);
}

.note-content {
    color: #1a1a1a;
}

/* 复用 PostDetail 的 Markdown 样式 */
.note-content :deep(h1),
.note-content :deep(h2),
.note-content :deep(h3),
.note-content :deep(h4) {
    color: #000;
    font-weight: 700;
    line-height: 1.4;
}

.note-content :deep(h1) {
    font-size: 2rem;
    margin: 2.5rem 0 1.5rem;
    padding-bottom: 0.5rem;
    border-bottom: 4px solid #000;
}

.note-content :deep(h2) {
    font-size: 1.5rem;
    margin: 2rem 0 1rem;
    display: flex;
    align-items: center;
}

.note-content :deep(h2)::before {
    content: "";
    display: inline-block;
    width: 12px;
    height: 12px;
    background-color: #ffde00;
    border: 2px solid #000;
    margin-right: 10px;
    flex-shrink: 0;
}

.note-content :deep(h3) {
    font-size: 1.25rem;
    color: #3c5aa6;
    margin: 1.5rem 0 0.75rem;
}

.note-content :deep(p) {
    line-height: 1.8;
    margin-bottom: 1.25rem;
    font-size: 1.05rem;
}

.note-content :deep(a) {
    color: #3c5aa6 !important;
    text-decoration: none;
    border-bottom: 2px solid #3c5aa6;
    font-weight: bold;
    transition: all 0.2s ease;
}

.note-content :deep(a:hover) {
    color: #ff7300 !important;
    border-bottom-color: #ff7300;
    background-color: #fff4ec;
}

.note-content :deep(ul),
.note-content :deep(ol) {
    margin: 1.25rem 0;
    padding-left: 2rem;
}

.note-content :deep(li) {
    margin: 0.5rem 0;
    line-height: 1.6;
}

.note-content :deep(img) {
    max-width: 100%;
    border: 4px solid #000;
    border-radius: 8px;
    margin: 2rem auto;
    display: block;
    box-shadow: 4px 4px 0 0 rgba(0, 0, 0, 0.1);
}

.note-content :deep(blockquote) {
    margin: 1.5rem 0;
    padding: 1rem 1.5rem;
    border-left: 6px solid #ffde00;
    background: #fafafa;
    border-radius: 0 8px 8px 0;
    color: #555;
    font-style: italic;
}

.note-content :deep(table) {
    width: 100%;
    border-collapse: collapse;
    margin: 2rem 0;
    box-shadow: 4px 4px 0 0 rgba(0, 0, 0, 1);
}

.note-content :deep(th),
.note-content :deep(td) {
    border: 3px solid #000;
    padding: 1rem;
    text-align: left;
}

.note-content :deep(th) {
    background: #ffde00;
    font-size: 1rem;
    font-weight: bold;
}

/* 代码块 */
.note-content :deep(.code-wrapper) {
    position: relative;
    margin: 2rem 0;
    background: #1e1e1e;
    border: 4px solid #000;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 4px 4px 0 0 rgba(0, 0, 0, 1);
}

.note-content :deep(.code-header) {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #2d2d2d;
    padding: 0.5rem 1rem;
    border-bottom: 2px solid #000;
}

.note-content :deep(.code-lang) {
    color: #a0a0a0;
    font-weight: bold;
    font-family: monospace;
}

.note-content :deep(.copy-btn) {
    background: #4a4a4a;
    color: #fff;
    border: 2px solid #000;
    padding: 0.2rem 0.6rem;
    font-size: 0.75rem;
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.1s;
    font-family: monospace;
}

.note-content :deep(.copy-btn:hover) {
    background: #5a5a5a;
}

.note-content :deep(.copy-btn:active) {
    transform: translateY(1px);
}

.note-content :deep(.copy-btn.copied) {
    background: #34d399;
    color: #000;
}

.note-content :deep(pre) {
    margin: 0;
    padding: 1.25rem;
    overflow-x: auto;
    background: transparent !important;
}

.note-content :deep(code) {
    font-size: 0.9rem;
    font-family: Consolas, Monaco, "Andale Mono", "Ubuntu Mono", monospace;
    line-height: 1.5;
}

.note-content :deep(:not(pre) > code) {
    background: #f4f4f4;
    color: #e83e8c;
    padding: 0.2rem 0.4rem;
    border-radius: 4px;
    border: 1px solid #ccc;
    font-size: 0.875rem;
}
</style>
