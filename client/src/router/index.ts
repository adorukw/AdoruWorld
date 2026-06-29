import { createRouter, createWebHistory } from "vue-router";
import type { RouteRecordRaw } from "vue-router";

const routes: RouteRecordRaw[] = [
  {
    path: "/",
    name: "Home",
    component: () => import("@/views/Home.vue"),
    meta: { title: "首页" },
  },
  {
    path: "/post/:slug",
    name: "Post",
    component: () => import("@/views/PostDetail.vue"),
    meta: { title: "文章详情" },
  },
  {
    path: "/post-search",
    name: "PostSearch",
    component: () => import("@/views/GlobalSearch.vue"),
    meta: { title: "搜索" },
  },
  {
    path: "/dex",
    name: "Dex",
    component: () => import("@/views/Dex.vue"),
    meta: { title: "图鉴" },
  },
  {
    path: "/dex/:slug",
    name: "DexDetail",
    component: () => import("@/views/DexDetail.vue"),
    meta: { title: "图鉴详情" },
  },
  {
    path: "/archive",
    name: "Archive",
    component: () => import("@/views/Archive.vue"),
    meta: { title: "归档" },
  },
  {
    path: "/project",
    name: "Project",
    component: () => import("@/views/Project.vue"),
    meta: { title: "项目" },
  },
  {
    path: "/admin",
    name: "Admin",
    component: () => import("@/views/admin/index.vue"),
    meta: { title: "后台管理" },
  },
  {
    path: "/search",
    name: "Search",
    component: () => import("@/views/GlobalSearch.vue"),
    meta: { title: "搜索" },
  },
];

const router = createRouter({
  history: createWebHistory("/adoru-world/"),
  routes,
  scrollBehavior(_to, _from, savedPosition) {
    if (savedPosition) return savedPosition;
    else return { top: 0 };
  },
});

router.beforeEach((to) => {
  const title = to.meta.title as string;
  document.title = title ? `${title} | AdoruWorld` : "AdoruWorld";
});

export default router;
