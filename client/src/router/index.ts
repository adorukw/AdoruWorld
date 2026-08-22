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
    meta: { title: "后台管理", requiresAuth: true, roles: ["admin", "editor"] },
  },
  {
    path: "/login",
    name: "Login",
    component: () => import("@/views/Login.vue"),
    meta: { title: "登录" },
  },
  {
    path: "/register",
    name: "Register",
    component: () => import("@/views/Register.vue"),
    meta: { title: "注册" },
  },
  {
    path: "/search",
    name: "Search",
    component: () => import("@/views/GlobalSearch.vue"),
    meta: { title: "搜索" },
  },
  {
    path: "/notes",
    name: "Notes",
    component: () => import("@/views/Notes.vue"),
    meta: { title: "笔记" },
  },
  {
    path: "/notes/:path*",
    name: "NoteDetail",
    component: () => import("@/views/Notes.vue"),
    meta: { title: "笔记" },
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

router.beforeEach(async (to) => {
  const title = to.meta.title as string;
  document.title = title ? `${title} | AdoruWorld` : "AdoruWorld";

  // 路由守卫只是体验层优化；真正的安全边界在后端 Depends
  if (to.meta.requiresAuth) {
    const { useAuthStore } = await import("@/store");
    const auth = useAuthStore();
    if (!auth.isLoggedIn) {
      return { name: "Login", query: { redirect: to.fullPath } };
    }
    // 首次进入守卫路由时拉取用户信息判断角色
    if (!auth.user) {
      const user = await auth.fetchMe();
      if (!user) return { name: "Login" };
    }
    const roles = (to.meta.roles as string[]) ?? [];
    if (roles.length && !roles.includes(auth.user!.role)) {
      return { name: "Home" };
    }
  }
});

export default router;
