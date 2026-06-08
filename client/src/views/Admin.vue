<script setup lang="ts">
import { ref, computed } from 'vue'
import Layout from '@/components/layout/Layout.vue'
import PixelButton from '@/components/ui/PixelButton.vue'
import CrudModal from '@/components/common/CrudModal.vue'
import {
    usePostStore, usePostCategoryStore, usePostTagStore,
    useDexStore, useDexGenreStore, useMediaStore, useMediaTagStore
} from '@/store'
// import type {
//     PostResponse, PostListItem, PostCategoryResponse, PostTagResponse, DexEntryResponse, DexGenreResponse
// } from '@/types'

const postStore = usePostStore()
const postCategoryStore = usePostCategoryStore()
const postTagStore = usePostTagStore()
const dexStore = useDexStore()
const dexGenreStore = useDexGenreStore()
const mediaStore = useMediaStore()
const mediaTagStore = useMediaTagStore()


// 当前激活的管理模块
const activeTab = ref<'posts' | 'postCategories' | 'postTags' | 'dexs' | 'dexGenres' | 'medias' | 'mediaTags'>('posts')

// 为每个 tab 创建独立的响应式数据引用
const postsData = computed(() => postStore.allPosts || [])
const postCategoriesData = computed(() => postCategoryStore.postCategories || [])
const postTagsData = computed(() => postTagStore.postTags || [])
const dexEntriesData = computed(() => dexStore.dexEntries || [])
const dexGenresData = computed(() => dexGenreStore.dexGenres || [])
const mediasData = computed(() => mediaStore.medias || [])
const mediaTagsData = computed(() => mediaTagStore.mediaTags || [])

// 计算当前显示的数据
const currentData = computed(() => {
    switch (activeTab.value) {
        case 'posts': return postsData.value
        case 'postCategories': return postCategoriesData.value
        case 'postTags': return postTagsData.value
        case 'dexs': return dexEntriesData.value
        case 'dexGenres': return dexGenresData.value
        case 'medias': return mediasData.value
        case 'mediaTags': return mediaTagsData.value
        default: return []
    }
})

// 获取当前数据类型对应的名称
const currentDataType = computed(() => {
    switch (activeTab.value) {
        case 'posts': return '文章'
        case 'postCategories': return '分类'
        case 'postTags': return '标签'
        case 'dexs': return '图鉴条目'
        case 'dexGenres': return '题材'
        case 'medias': return '媒体'
        case 'mediaTags': return '媒体标签'
        default: return ''
    }
})

// ===== 新增：CrudModal 相关状态 =====
const showModal = ref(false)
const modalMode = ref<'create' | 'update'>('create')
const editingItem = ref<any>(null)

// 打开新建模态框
function openCreateModal() {
    modalMode.value = 'create'
    editingItem.value = null
    showModal.value = true
}

// 打开编辑模态框
function openEditModal(item: any) {
    modalMode.value = 'update'

    let processedItem = { ...item }

    if (activeTab.value === 'posts') {
        processedItem = {
            ...item,
            categoryId: item.category?.id,
            tagIds: item.tags?.map((t: any) => t.id) || []
        }
    }

    if (activeTab.value === 'dexs') {
        processedItem = {
            ...item,
            genreIds: item.genres?.map((g: any) => g.id) || []
        }
    }

    if (activeTab.value === 'medias') {
        processedItem = {
            ...item,
            tagIds: item.tags?.map((t: any) => t.id) || [],
        }
    }


    editingItem.value = processedItem
    showModal.value = true
}

// 处理模态框成功后的回调
async function handleModalSuccess() {
    showModal.value = false
    // 根据当前模块刷新数据
    switch (activeTab.value) {
        case 'posts':
            await postStore.getAllPosts()
            break
        case 'postCategories':
            await postCategoryStore.getPostCategories()
            break
        case 'postTags':
            await postTagStore.getPostTags()
            break
        case 'dexs':
            await dexStore.getDexEntries()
            break
        case 'dexGenres':
            await dexGenreStore.getDexGenres()
            break
        case 'medias':
            await mediaStore.getMedias()
            break
        case 'mediaTags':
            await mediaTagStore.getMediaTags()
            break
        default:
            break
    }
}

// 删除处理函数
async function handleDelete(item: any) {
    if (!confirm(`确定要删除 "${item.name || item.title}" 吗？`)) return

    try {
        switch (activeTab.value) {
            case 'posts':
                await postStore.deletePost(item.id)
                break
            case 'postCategories':
                await postCategoryStore.deletePostCategory(item.id)
                break
            case 'postTags':
                await postTagStore.deletePostTag(item.id)
                break
            case 'dexs':
                await dexStore.deleteDexEntry(item.id)
                break
            case 'dexGenres':
                await dexGenreStore.deleteDexGenre(item.id)
                break
            case 'medias':
                await mediaStore.deleteMedia(item.id)
                break
            case 'mediaTags':
                await mediaTagStore.deleteMediaTag(item.id)
                break
        }
        // 删除成功后刷新数据
        await handleModalSuccess()
    } catch (error) {
        console.error('删除失败:', error)
        alert('删除失败')
    }
}
</script>

<template>
    <Layout>
        <!-- 页面标题区域 -->
        <section class="relative py-12 overflow-hidden border-b-4 border-dashed">
            <div class="absolute inset-0 bg-linear-to-r from-sky-light via-white to-gold-light"></div>
            <div class="max-w-6xl mx-auto px-4 text-center relative z-10">
                <h1 class="pixel-text text-2xl md:text-3xl mb-4 drop-shadow-sm">⚙️ 内容管理</h1>
                <p class="text-lg">管理你的文章、分类、标签、图鉴、图鉴题材以及媒体库等内容。</p>
            </div>
        </section>

        <!-- 主要内容区域 -->
        <section class="py-8">
            <div class="max-w-6xl mx-auto px-4">
                <!-- 选项卡导航 -->
                <div class="flex flex-wrap gap-2 mb-8 p-4 bg-white/80 rounded-lg border-4 border-black">
                    <button @click="activeTab = 'posts'" class="pixel-btn px-4 py-2 transition-all"
                        :class="activeTab === 'posts' ? 'bg-sky text-white' : 'bg-white hover:bg-gray-100'">
                        📝 文章
                    </button>
                    <button @click="activeTab = 'postCategories'" class="pixel-btn px-4 py-2 transition-all"
                        :class="activeTab === 'postCategories' ? 'bg-sky text-white' : 'bg-white hover:bg-gray-100'">
                        📁 文章分类
                    </button>
                    <button @click="activeTab = 'postTags'" class="pixel-btn px-4 py-2 transition-all"
                        :class="activeTab === 'postTags' ? 'bg-sky text-white' : 'bg-white hover:bg-gray-100'">
                        🏷️ 文章标签
                    </button>
                    <button @click="activeTab = 'dexs'" class="pixel-btn px-4 py-2 transition-all"
                        :class="activeTab === 'dexs' ? 'bg-sky text-white' : 'bg-white hover:bg-gray-100'">
                        📖 图鉴
                    </button>
                    <button @click="activeTab = 'dexGenres'" class="pixel-btn px-4 py-2 transition-all"
                        :class="activeTab === 'dexGenres' ? 'bg-sky text-white' : 'bg-white hover:bg-gray-100'">
                        🎭 图鉴题材
                    </button>
                    <button @click="activeTab = 'medias'" class="pixel-btn px-4 py-2 transition-all"
                        :class="activeTab === 'medias' ? 'bg-sky text-white' : 'bg-white hover:bg-gray-100'">
                        媒体库
                    </button>
                    <button @click="activeTab = 'mediaTags'" class="pixel-btn px-4 py-2 transition-all"
                        :class="activeTab === 'mediaTags' ? 'bg-sky text-white' : 'bg-white hover:bg-gray-100'">
                        媒体标签
                    </button>
                </div>

                <!-- 操作栏 -->
                <div class="flex justify-between items-center mb-6">
                    <div class="text-sm text-gray-600">
                        共 {{ currentData.length }} 条记录
                    </div>
                    <PixelButton @click="openCreateModal" class="bg-grass text-white">
                        ➕ 新增{{ currentDataType }}
                    </PixelButton>
                </div>

                <!-- 数据表格 -->
                <div class="pixel-card overflow-hidden border-4 border-black">
                    <div class="overflow-x-auto">
                        <table class="w-full">
                            <!-- 表头 -->
                            <thead class="bg-gray-100 border-b-4 border-black">
                                <tr>
                                    <!-- 文章表头 -->
                                    <template v-if="activeTab === 'posts'">
                                        <th class="p-4 text-left pixel-text text-sm">标题</th>
                                        <th class="p-4 text-left pixel-text text-sm">分类</th>
                                        <th class="p-4 text-left pixel-text text-sm">标签</th>
                                        <th class="p-4 text-left pixel-text text-sm">创建时间</th>
                                        <th class="p-4 text-left pixel-text text-sm">状态</th>
                                    </template>

                                    <!-- 分类表头 -->
                                    <template v-if="activeTab === 'postCategories'">
                                        <th class="p-4 text-left pixel-text text-sm">名称</th>
                                        <th class="p-4 text-left pixel-text text-sm">别名</th>
                                        <th class="p-4 text-left pixel-text text-sm">图标</th>
                                        <th class="p-4 text-left pixel-text text-sm">文章数</th>
                                    </template>

                                    <!-- 标签表头 -->
                                    <template v-if="activeTab === 'postTags'">
                                        <th class="p-4 text-left pixel-text text-sm">名称</th>
                                        <th class="p-4 text-left pixel-text text-sm">别名</th>
                                        <th class="p-4 text-left pixel-text text-sm">颜色</th>
                                        <th class="p-4 text-left pixel-text text-sm">使用次数</th>
                                    </template>

                                    <!-- 图鉴表头 -->
                                    <template v-if="activeTab === 'dexs'">
                                        <th class="p-4 text-left pixel-text text-sm">标题</th>
                                        <th class="p-4 text-left pixel-text text-sm">类别</th>
                                        <th class="p-4 text-left pixel-text text-sm">状态</th>
                                        <th class="p-4 text-left pixel-text text-sm">评分</th>
                                    </template>

                                    <!-- 题材表头 -->
                                    <template v-if="activeTab === 'dexGenres'">
                                        <th class="p-4 text-left pixel-text text-sm">名称</th>
                                        <th class="p-4 text-left pixel-text text-sm">颜色</th>
                                    </template>

                                    <!-- 媒体表头 -->
                                    <template v-if="activeTab === 'medias'">
                                        <th class="p-4 text-left pixel-text text-sm">名称</th>
                                        <th class="p-4 text-left pixel-text text-sm">类型</th>
                                        <th class="p-4 text-left pixel-text text-sm">大小</th>
                                        <th class="p-4 text-left pixel-text text-sm">标签</th>
                                    </template>

                                    <!-- 媒体标签 -->
                                    <template v-if="activeTab === 'mediaTags'">
                                        <th class="p-4 text-left pixel-text text-sm">名称</th>
                                        <th class="p-4 text-left pixel-text text-sm">颜色</th>
                                    </template>

                                    <th class="p-4 text-left pixel-text text-sm">操作</th>
                                </tr>
                            </thead>

                            <!-- 表体 -->
                            <tbody>
                                <!-- 文章管理 -->
                                <tr v-if="activeTab === 'posts'" v-for="item in postsData" :key="item.id"
                                    class="border-b-2 border-gray-200 hover:bg-gray-50 transition-colors">
                                    <td class="p-4 font-medium">{{ item.title }}</td>
                                    <td class="p-4">
                                        <span class="px-2 py-1 border-2 border-black rounded text-xs">
                                            {{ item.category.name }}
                                        </span>
                                    </td>
                                    <td class="p-4">
                                        <div class="flex flex-wrap gap-1">
                                            <span v-for="tag in item.tags" :key="tag.id"
                                                class="px-2 py-0.5 bg-gold-light border border-black rounded text-xs">
                                                {{ tag.name }}
                                            </span>
                                        </div>
                                    </td>
                                    <td class="p-4 text-sm">{{ item.createdAt }}</td>
                                    <td class="p-4">
                                        <span :class="`px-2 py-1 border-2 border-black rounded text-xs pixel-text`">
                                            {{ item.published ? '已发布' : '未发布' }}
                                        </span>
                                    </td>
                                    <td class="p-4">
                                        <div class="flex gap-2">
                                            <button @click="openEditModal(item)"
                                                class="pixel-btn-small bg-blue-500 text-white">编辑</button>
                                            <button @click="handleDelete(item)"
                                                class="pixel-btn-small bg-red-500 text-white">删除</button>
                                        </div>
                                    </td>
                                </tr>

                                <!-- 分类管理 -->
                                <tr v-if="activeTab === 'postCategories'" v-for="item in postCategoriesData"
                                    :key="item.id"
                                    class="border-b-2 border-gray-200 hover:bg-gray-50 transition-colors">
                                    <td class="p-4 font-medium">{{ item.name }}</td>
                                    <td class="p-4 text-sm text-gray-600">{{ item.slug }}</td>
                                    <td class="p-4">{{ item.icon }}</td>
                                    <td class="p-4">
                                        <span class="px-2 py-1 bg-grass-light border-2 border-black rounded text-xs">
                                            {{ item.count }} 篇
                                        </span>
                                    </td>
                                    <td class="p-4">
                                        <div class="flex gap-2">
                                            <button @click="openEditModal(item)"
                                                class="pixel-btn-small bg-blue-500 text-white">编辑</button>
                                            <button @click="handleDelete(item)"
                                                class="pixel-btn-small bg-red-500 text-white">删除</button>
                                        </div>
                                    </td>
                                </tr>

                                <!-- 标签管理 -->
                                <tr v-if="activeTab === 'postTags'" v-for="item in postTagsData" :key="item.id"
                                    class="border-b-2 border-gray-200 hover:bg-gray-50 transition-colors">
                                    <td class="p-4 font-medium">{{ item.name }}</td>
                                    <td class="p-4 text-sm text-gray-600">{{ item.slug }}</td>
                                    <td class="p-4">
                                        <div class="flex items-center gap-2">
                                            <div class="w-6 h-6 rounded border-2 border-black"
                                                :style="{ backgroundColor: item.color }"></div>
                                            <span class="text-sm font-mono">{{ item.color }}</span>
                                        </div>
                                    </td>
                                    <td class="p-4">
                                        <span class="px-2 py-1 bg-gold-light border-2 border-black rounded text-xs">
                                            {{ item.count }} 次
                                        </span>
                                    </td>
                                    <td class="p-4">
                                        <div class="flex gap-2">
                                            <button @click="openEditModal(item)"
                                                class="pixel-btn-small bg-blue-500 text-white">编辑</button>
                                            <button @click="handleDelete(item)"
                                                class="pixel-btn-small bg-red-500 text-white">删除</button>
                                        </div>
                                    </td>
                                </tr>

                                <!-- 图鉴管理 -->
                                <tr v-if="activeTab === 'dexs'" v-for="item in dexEntriesData" :key="item.id"
                                    class="border-b-2 border-gray-200 hover:bg-gray-50 transition-colors">
                                    <td class="p-4 font-medium">{{ item.title }}</td>
                                    <td class="p-4">
                                        <span class="px-2 py-1 bg-purple-200 border-2 border-black rounded text-xs">
                                            {{ item.category }}
                                        </span>
                                    </td>
                                    <td class="p-4">
                                        <span :class="`px-2 py-1 border-2 border-black rounded text-xs pixel-text`">
                                            {{ item.status }}
                                        </span>
                                    </td>
                                    <td class="p-4">
                                        <div class="flex flex-wrap gap-1">
                                            <span v-for="genre in item.genres" :key="genre.id"
                                                class="px-2 py-0.5 bg-gold-light border border-black rounded text-xs">
                                                {{ genre.name }}
                                            </span>
                                        </div>
                                    </td>
                                    <td class="p-4">
                                        <div class="flex gap-2">
                                            <button @click="openEditModal(item)"
                                                class="pixel-btn-small bg-blue-500 text-white">编辑</button>
                                            <button @click="handleDelete(item)"
                                                class="pixel-btn-small bg-red-500 text-white">删除</button>
                                        </div>
                                    </td>
                                </tr>

                                <!-- 题材管理 -->
                                <tr v-if="activeTab === 'dexGenres'" v-for="item in dexGenresData" :key="item.id"
                                    class="border-b-2 border-gray-200 hover:bg-gray-50 transition-colors">
                                    <td class="p-4 font-medium">{{ item.name }}</td>
                                    <td class="p-4">
                                        <div class="flex items-center gap-2">
                                            <div class="w-6 h-6 rounded border-2 border-black"
                                                :style="{ backgroundColor: item.color }"></div>
                                            <span class="text-sm font-mono">{{ item.color }}</span>
                                        </div>
                                    </td>
                                    <td class="p-4">
                                        <div class="flex gap-2">
                                            <button @click="openEditModal(item)"
                                                class="pixel-btn-small bg-blue-500 text-white">编辑</button>
                                            <button @click="handleDelete(item)"
                                                class="pixel-btn-small bg-red-500 text-white">删除</button>
                                        </div>
                                    </td>
                                </tr>

                                <!-- 媒体库管理 -->
                                <tr v-if="activeTab === 'medias'" v-for="item in mediasData" :key="item.id"
                                    class="border-b-2 border-gray-200 hover:bg-gray-50 transition-colors">
                                    <td class="p-4 font-medium">{{ item.title }}</td>
                                    <td class="p-4">
                                        <span class="px-2 py-1 bg-purple-200 border-2 border-black rounded text-xs">
                                            {{ item.mediaType }}
                                        </span>
                                    </td>
                                    <td class="p-4">
                                        <span :class="`px-2 py-1 border-2 border-black rounded text-xs pixel-text`">
                                            {{ item.fileSize }}
                                        </span>
                                    </td>
                                    <td class="p-4">
                                        <div class="flex flex-wrap gap-1">
                                            <span v-for="tag in item.tags" :key="tag.id"
                                                class="px-2 py-0.5 bg-gold-light border border-black rounded text-xs">
                                                {{ tag.name }}
                                            </span>
                                        </div>
                                    </td>
                                    <td class="p-4">
                                        <div class="flex gap-2">
                                            <button @click="openEditModal(item)"
                                                class="pixel-btn-small bg-blue-500 text-white">编辑</button>
                                            <button @click="handleDelete(item)"
                                                class="pixel-btn-small bg-red-500 text-white">删除</button>
                                        </div>
                                    </td>
                                </tr>

                                <!-- 媒体标签管理 -->
                                <tr v-if="activeTab === 'mediaTags'" v-for="item in mediaTagsData" :key="item.id"
                                    class="border-b-2 border-gray-200 hover:bg-gray-50 transition-colors">
                                    <td class="p-4 font-medium">{{ item.name }}</td>
                                    <td class="p-4">
                                        <div class="flex items-center gap-2">
                                            <div class="w-6 h-6 rounded border-2 border-black"
                                                :style="{ backgroundColor: item.color }"></div>
                                            <span class="text-sm font-mono">{{ item.color }}</span>
                                        </div>
                                    </td>
                                    <td class="p-4">
                                        <div class="flex gap-2">
                                            <button @click="openEditModal(item)"
                                                class="pixel-btn-small bg-blue-500 text-white">编辑</button>
                                            <button @click="handleDelete(item)"
                                                class="pixel-btn-small bg-red-500 text-white">删除</button>
                                        </div>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <!-- 空状态 -->
                    <div v-if="currentData.length === 0" class="text-center py-16">
                        <div class="text-6xl mb-4">📭</div>
                        <h3 class="pixel-text text-lg mb-2">暂无数据</h3>
                        <p class="text-gray-600 mb-6">点击上方按钮添加新内容</p>
                    </div>
                </div>

                <!-- 分页 -->
                <div class="flex justify-center mt-8">
                    <div class="flex gap-2">
                        <button class="pixel-btn-small bg-white">上一页</button>
                        <button class="pixel-btn-small bg-sky text-white">1</button>
                        <button class="pixel-btn-small bg-white">2</button>
                        <button class="pixel-btn-small bg-white">3</button>
                        <button class="pixel-btn-small bg-white">下一页</button>
                    </div>
                </div>
            </div>
        </section>

        <!-- ===== 新增：CrudModal 组件 ===== -->
        <CrudModal v-if="showModal" :module="activeTab" :mode="modalMode" :initial-data="editingItem"
            @success="handleModalSuccess" @close="showModal = false" />
    </Layout>
</template>

<style scoped>
.pixel-btn-small:hover {
    transform: translate(-1px, -1px);
    box-shadow: 2px 2px 0px 0px rgba(0, 0, 0, 1);
}

.pixel-btn-small:active {
    transform: translate(1px, 1px);
    box-shadow: none;
}

/* 表格行悬停效果 */
tbody tr:hover {
    background-color: rgba(135, 206, 235, 0.1);
}

/* 模态框动画 */
.fixed {
    animation: fadeIn 0.2s ease-out;
}

@keyframes fadeIn {
    from {
        opacity: 0;
    }

    to {
        opacity: 1;
    }
}
</style>