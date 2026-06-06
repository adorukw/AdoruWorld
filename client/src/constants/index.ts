import type { NavItem, DexCategoryInfo, DexStatusInfo, MediaTypeInfo } from '@/types'

export const navItems: NavItem[] = [
    { name: '首页', path: '/', icon: '🏠' },
    { name: '图鉴', path: '/dex', icon: '📖' },
    { name: '归档', path: '/archives', icon: '📚' },
    { name: '项目', path: '/projects', icon: '🏗️' },
    { name: '我的', path: '/me', icon: '👤' },
    { name: '管理', path: '/admin', icon: '🛠️' },
    { name: '编辑', path: '/edit', icon: '📝' }
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