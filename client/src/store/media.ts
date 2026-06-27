import { defineStore } from "pinia";
import { ref } from "vue";
import { mediaApi as api } from "@/api";
import type {
  MediaResponse,
  MediaCreate,
  MediaUpdate,
  MediaUploadResponse,
} from "@/types";

export const useMediaStore = defineStore("media", () => {
  const medias = ref<MediaResponse[]>([]);
  const currentMedia = ref<MediaResponse | null>(null);
  const loading = ref(false);
  const error = ref<string | null>(null);

  const uploadMedia = async (file: File): Promise<MediaUploadResponse> => {
    loading.value = true;
    error.value = null;
    try {
      const res = await api.upload(file);
      return res;
    } catch (err: any) {
      error.value = err.message || "上传媒体失败";
      throw err;
    } finally {
      loading.value = false;
    }
  };

  const getMedias = async (parms?: {
    mediaType?: string;
    tag_slug?: string;
    skip?: number;
    limit?: number;
  }) => {
    loading.value = true;
    error.value = null;
    try {
      const res = await api.list(parms);
      medias.value = res;
      return res;
    } catch (err: any) {
      error.value = err.message || "获取媒体失败";
      throw err;
    } finally {
      loading.value = false;
    }
  };

  const getMediaBySlug = async (slug: string) => {
    loading.value = true;
    error.value = null;
    try {
      currentMedia.value = await api.getBySlug(slug);
    } catch (err: any) {
      error.value = err.message || "获取媒体详情失败";
    } finally {
      loading.value = false;
    }
  };

  const getMediaById = async (id: string) => {
    loading.value = true;
    error.value = null;
    try {
      currentMedia.value = await api.getById(id);
    } catch (err: any) {
      error.value = err.message || "获取媒体详情失败";
    } finally {
      loading.value = false;
    }
  };

  const createMedia = async (data: MediaCreate) => {
    loading.value = true;
    error.value = null;
    try {
      const newMedia = await api.create(data);
      medias.value.push(newMedia);
      return newMedia;
    } catch (err: any) {
      error.value = err.message || "创建媒体失败";
      throw err;
    } finally {
      loading.value = false;
    }
  };

  const updateMedia = async (id: string, data: MediaUpdate) => {
    loading.value = true;
    error.value = null;
    try {
      const updatedMedia = await api.update(id, data);
      const index = medias.value.findIndex((m) => m.id === id);
      if (index !== -1) {
        medias.value[index] = updatedMedia;
      }
      if (currentMedia.value && currentMedia.value.id === id) {
        currentMedia.value = updatedMedia;
      }
      return updatedMedia;
    } catch (err: any) {
      error.value = err.message || "更新媒体失败";
      throw err;
    } finally {
      loading.value = false;
    }
  };

  const deleteMedia = async (id: string) => {
    loading.value = true;
    error.value = null;
    try {
      await api.delete(id);
      medias.value = medias.value.filter((item) => item.id !== id);
      if (currentMedia.value?.id === id) {
        currentMedia.value = null;
      }
    } catch (err: any) {
      error.value = err.message || "删除媒体失败";
      throw err;
    } finally {
      loading.value = false;
    }
  };

  return {
    medias,
    currentMedia,
    loading,
    error,
    uploadMedia,
    getMedias,
    getMediaBySlug,
    getMediaById,
    createMedia,
    updateMedia,
    deleteMedia,
  };

  // 组合方法：上传文件并创建媒体记录
  // const uploadAndCreateMedia = async (file: File, additionalData: Omit<MediaCreate, 'filePath' | 'fileSize' | 'mimeType' | 'mediaType' | 'extension'>) => {
  //     loading.value = true
  //     error.value = null
  //     try {
  //         // 1. 上传文件
  //         const uploadResult = await api.upload(file)

  //         // 2. 创建媒体记录
  //         const mediaData: MediaCreate = {
  //             ...additionalData,
  //             filePath: uploadResult.filePath,
  //             fileSize: uploadResult.fileSize,
  //             mimeType: uploadResult.mimeType,
  //             mediaType: uploadResult.mediaType,
  //             extension: uploadResult.extension
  //         }

  //         const newMedia = await api.create(mediaData)
  //         mediaItems.value.unshift(newMedia)
  //         return newMedia
  //     }
  //     catch (err: any) {
  //         error.value = err.message || '上传并创建媒体失败'
  //         throw err
  //     }
  //     finally {
  //         loading.value = false
  //     }
  // }
});
