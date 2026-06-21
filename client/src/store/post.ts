import { defineStore } from "pinia";
import { ref } from "vue";
import { api } from "@/api";
import type {
  PostResponse,
  ArchiveItem,
  PostCreate,
  PostUpdate,
} from "@/types";

export const usePostStore = defineStore("post", () => {
  const posts = ref<PostResponse[]>([]);
  const recentPosts = ref<PostResponse[]>([]);
  const featuredPosts = ref<PostResponse[]>([]);
  const relatedPosts = ref<PostResponse[]>([]);
  const currentPost = ref<PostResponse | null>(null);
  const archives = ref<ArchiveItem[]>([]);
  const totalPostsCount = ref<number>(0);
  const totalWordCount = ref<number>(0);
  const totalViewsCount = ref<number>(0);
  const loading = ref(false);
  const error = ref<string | null>(null);

  const getPosts = async (params?: {
    published?: boolean;
    featured?: boolean;
    category?: string;
    tag?: string;
    skip?: number;
    limit?: number;
  }) => {
    loading.value = true;
    error.value = null;
    try {
      posts.value = await api.posts.list(params);
    } catch (err: any) {
      error.value = err.message || "获取文章列表失败";
    } finally {
      loading.value = false;
    }
  };

  const getRecentPosts = async () => {
    loading.value = true;
    error.value = null;
    try {
      const res = await api.posts.list({ published: true });
      recentPosts.value = res
        .sort(
          (a, b) =>
            new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime(),
        )
        .slice(0, 5);
    } catch (err: any) {
      error.value = err.message || "获取最近文章失败";
    } finally {
      loading.value = false;
    }
  };

  const getFeaturedPosts = async () => {
    loading.value = true;
    error.value = null;
    try {
      const res = await api.posts.list({ published: true, featured: true });
      featuredPosts.value = res
        .sort(
          (a, b) =>
            new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime(),
        )
        .slice(0, 5);
    } catch (err: any) {
      error.value = err.message || "获取特色文章失败";
    } finally {
      loading.value = false;
    }
  };

  const getArchives = async () => {
    loading.value = true;
    error.value = null;
    try {
      archives.value = await api.posts.archives();
    } catch (err: any) {
      error.value = err.message || "获取归档失败";
    } finally {
      loading.value = false;
    }
  };

  const getPostBySlug = async (slug: string) => {
    loading.value = true;
    error.value = null;
    try {
      currentPost.value = await api.posts.getBySlug(slug);
    } catch (err: any) {
      error.value = err.message || "获取文章失败";
    } finally {
      loading.value = false;
    }
  };

  const getRelatedPosts = async (slug: string) => {
    loading.value = true;
    error.value = null;
    try {
      const res = await api.posts.getRelated(slug);
      relatedPosts.value = res;
    } catch (err: any) {
      error.value = err.message || "获取相关文章失败";
    } finally {
      loading.value = false;
    }
  };

  const getPostById = async (id: string) => {
    loading.value = true;
    error.value = null;
    try {
      currentPost.value = await api.posts.getById(id);
    } catch (err: any) {
      error.value = err.message || "获取文章失败";
    } finally {
      loading.value = false;
    }
  };

  const createPost = async (data: PostCreate) => {
    loading.value = true;
    error.value = null;
    try {
      const newPost = await api.posts.create(data);
      posts.value.unshift(newPost);
      return newPost;
    } catch (err: any) {
      error.value = err.message || "创建文章失败";
      throw err;
    } finally {
      loading.value = false;
    }
  };

  const updatePost = async (id: string, data: PostUpdate) => {
    loading.value = true;
    error.value = null;
    try {
      const updatedPost = await api.posts.update(id, data);
      const index = posts.value.findIndex((p) => p.id === id);
      if (index !== -1) {
        posts.value[index] = updatedPost;
      }
      if (currentPost.value?.id === id) {
        currentPost.value = updatedPost;
      }
      return updatedPost;
    } catch (err: any) {
      error.value = err.message || "更新文章失败";
      throw err;
    } finally {
      loading.value = false;
    }
  };

  const deletePost = async (id: string) => {
    loading.value = true;
    error.value = null;
    try {
      await api.posts.delete(id);
      posts.value = posts.value.filter((p) => p.id !== id);
      if (currentPost.value?.id === id) {
        currentPost.value = null;
      }
    } catch (err: any) {
      error.value = err.message || "删除文章失败";
      throw err;
    } finally {
      loading.value = false;
    }
  };

  const incrementViews = async (id: string) => {
    loading.value = true;
    error.value = null;
    try {
      await api.posts.incrementViews(id);
    } catch (err: any) {
      error.value = err.message || "增加文章阅读量失败";
    } finally {
      loading.value = false;
    }
  };

  const getTotalPostsCount = async () => {
    loading.value = true;
    error.value = null;
    try {
      const count = await api.posts.totalPostsCount();
      totalPostsCount.value = count;
    } catch (err: any) {
      error.value = err.message || "获取文章数量失败";
    } finally {
      loading.value = false;
    }
  };

  const getTotalWords = async () => {
    loading.value = true;
    error.value = null;
    try {
      const count = await api.posts.totalWords();
      totalWordCount.value = count;
    } catch (err: any) {
      error.value = err.message || "获取文章总字数失败";
    } finally {
      loading.value = false;
    }
  };

  const getTotalViews = async () => {
    loading.value = true;
    error.value = null;
    try {
      const count = await api.posts.totalViews();
      totalViewsCount.value = count;
    } catch (err: any) {
      error.value = err.message || "获取文章总阅读量失败";
    } finally {
      loading.value = false;
    }
  };

  // 返回所有需要暴露的内容
  return {
    posts,
    currentPost,
    relatedPosts,
    archives,
    loading,
    error,
    totalPostsCount,
    totalWordCount,
    totalViewsCount,

    featuredPosts,
    recentPosts,

    getPosts,
    getRecentPosts,
    getFeaturedPosts,
    getArchives,
    getPostBySlug,
    getRelatedPosts,
    getPostById,
    createPost,
    updatePost,
    deletePost,
    incrementViews,
    getTotalPostsCount,
    getTotalWords,
    getTotalViews,
  };
});
