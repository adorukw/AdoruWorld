import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
    {
        path: '/',
        name: 'Home',
        component: () => import('@/views/Home.vue'),
        meta: { title: '首页' }
    },
    {
        path: '/post/:slug',
        name: 'Post',
        component: () => import('@/views/PostDetail.vue'),
        meta: { title: '文章详情' }
    },
    {
        path: '/post-search',
        name: 'PostSearch',
        component: () => import('@/views/PostSearch.vue'),
        meta: { title: '搜索' }
    },
    {
        path: '/dex',
        name: 'Dex',
        component: () => import('@/views/Dex.vue'),
        meta: { title: '图鉴' }
    },
    {
        path: '/dex/:slug',
        name: 'DexDetail',
        component: () => import('@/views/DexDetail.vue'),
        meta: { title: '图鉴详情' }
    },
    {
        path: '/archives',
        name: 'Archives',
        component: () => import('@/views/Archives.vue'),
        meta: { title: '归档' }
    },
    {
        path: '/projects',
        name: 'Projects',
        component: () => import('@/views/Projects.vue'),
        meta: { title: '项目' }
    },
    {
        path: '/admin',
        name: 'Admin',
        component: () => import('@/views/Admin.vue'),
    }
    // {
    //     path: '/edit',
    //     name: 'Edit',
    //     component: () => import('@/views/E.vue'),
    // }
]

const router = createRouter({
    history: createWebHistory(),
    routes,
    scrollBehavior(to, from, savedPosition) {
        if (savedPosition) return savedPosition
        else return { top: 0 }
    }
})

router.beforeEach((to) => {
    const title = to.meta.title as string
    document.title = title ? `${title} | AdoruWorld` : 'AdoruWorld'
})

export default router