import type { NavItem, SocialLink, DexCategoryInfo, DexStatusInfo, MediaTypeInfo } from '@/types'

export const navItems: NavItem[] = [
    { name: '首页', path: '/', icon: '🏠' },
    { name: '图鉴', path: '/dex', icon: '📖' },
    { name: '归档', path: '/archives', icon: '📚' },
    // { name: '项目', path: '/projects', icon: '🏗️' },
    // { name: '我的', path: '/me', icon: '👤' },
    { name: '管理', path: '/admin', icon: '🛠️' },
    // { name: '编辑', path: '/edit', icon: '📝' }
]

export const socialLinks: SocialLink[] = [
    {
        name: 'GitHub',
        url: 'https://github.com/adorukw',
        icon: '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/></svg>'
    },
    {
        name: 'B站',
        url: 'https://space.bilibili.com/59931999',
        icon: '<svg role="img" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><title>Bilibili</title><path d="M17.813 4.653h.854c1.51.054 2.769.578 3.773 1.574 1.004.995 1.524 2.249 1.56 3.76v7.36c-.036 1.51-.556 2.769-1.56 3.773s-2.262 1.524-3.773 1.56H5.333c-1.51-.036-2.769-.556-3.773-1.56S.036 18.858 0 17.347v-7.36c.036-1.511.556-2.765 1.56-3.76 1.004-.996 2.262-1.52 3.773-1.574h.774l-1.174-1.12a1.234 1.234 0 0 1-.373-.906c0-.356.124-.658.373-.907l.027-.027c.267-.249.573-.373.92-.373.347 0 .653.124.92.373L9.653 4.44c.071.071.134.142.187.213h4.267a.836.836 0 0 1 .16-.213l2.853-2.747c.267-.249.573-.373.92-.373.347 0 .662.151.929.4.267.249.391.551.391.907 0 .355-.124.657-.373.906zM5.333 7.24c-.746.018-1.373.276-1.88.773-.506.498-.769 1.13-.786 1.894v7.52c.017.764.28 1.395.786 1.893.507.498 1.134.756 1.88.773h13.334c.746-.017 1.373-.275 1.88-.773.506-.498.769-1.129.786-1.893v-7.52c-.017-.765-.28-1.396-.786-1.894-.507-.497-1.134-.755-1.88-.773zM8 11.107c.373 0 .684.124.933.373.25.249.383.569.4.96v1.173c-.017.391-.15.711-.4.96-.249.25-.56.374-.933.374s-.684-.125-.933-.374c-.25-.249-.383-.569-.4-.96V12.44c0-.373.129-.689.386-.947.258-.257.574-.386.947-.386zm8 0c.373 0 .684.124.933.373.25.249.383.569.4.96v1.173c-.017.391-.15.711-.4.96-.249.25-.56.374-.933.374s-.684-.125-.933-.374c-.25-.249-.383-.569-.4-.96V12.44c.017-.391.15-.711.4-.96.249-.249.56-.373.933-.373Z"/></svg>'
    }
]

export const dexCategories: DexCategoryInfo[] = [
    { id: 'anime', name: '动画', slug: 'anime', icon: '📺', color: '#FF6B6B', bgColor: '#FFE8E8' },
    { id: 'movie', name: '电影', slug: 'movie', icon: '🎬', color: '#4ECDC4', bgColor: '#E8FFFE' },
    { id: 'tv', name: '电视剧', slug: 'tv', icon: '📡', color: '#45B7D1', bgColor: '#E8F7FC' },
    { id: 'game', name: '游戏', slug: 'game', icon: '🎮', color: '#96CEB4', bgColor: '#F0FFF4' },
    { id: 'book', name: '书籍', slug: 'book', icon: '📚', color: '#DDA0DD', bgColor: '#FFF0FF' },
    { id: 'music', name: '音乐', slug: 'music', icon: '🎵', color: '#FFB347', bgColor: '#FFF8E8' },
    { id: 'other', name: '其他', slug: 'other', icon: '❓', color: '#607D8B', bgColor: '#E8F7FC' }
]

export const dexStatuses: DexStatusInfo[] = [
    { id: 'completed', name: '已完成', slug: 'completed', icon: '✅', color: '#4CAF50' },
    { id: 'watching', name: '在看', slug: 'watching', icon: '👀', color: '#2196F3' },
    { id: 'playing', name: '在玩', slug: 'playing', icon: '🎮', color: '#9C27B0' },
    { id: 'reading', name: '在读', slug: 'reading', icon: '📖', color: '#795548' },
    { id: 'listening', name: '在听', slug: 'listening', icon: '🎧', color: '#FF9800' },
    { id: 'doing', name: '在做', slug: 'doing', icon: '⚙️', color: '#009688' },
    { id: 'dropped', name: '搁置', slug: 'dropped', icon: '❌', color: '#9E9E9E' },
    { id: 'planned', name: '计划', slug: 'planned', icon: '📋', color: '#607D8B' }
]

export const mediaTypes: MediaTypeInfo[] = [
    { id: 'book', name: '书籍', slug: 'book', icon: '📚', color: '#DDA0DD' },
    { id: 'audio', name: '音频', slug: 'audio', icon: '🎵', color: '#FFB347' },
    { id: 'image', name: '图片', slug: 'image', icon: '🖼️', color: '#E8F7FC' },
    { id: 'video', name: '视频', slug: 'video', icon: '🎥', color: '#4CAF50' }
]