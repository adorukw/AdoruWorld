import type { PostCategoryResponse } from "./post-category";
import type { PostTagResponse } from "./post-tag";
import type { SeriesResponse, PostLink } from "./series";

export interface PostResponse {
  id: string;
  slug: string;
  title: string;
  description?: string;
  content: string;
  coverImage?: string;
  createdAt: string;
  updatedAt: string;
  published: boolean;
  featured: boolean;
  category: PostCategoryResponse;
  tags: PostTagResponse[];
  series?: SeriesResponse;
  seriesOrder?: number;
  prevPost?: PostLink;
  nextPost?: PostLink;
  readingTime: number;
  wordCount: number;
  views: number;
}

export interface PostArchiveResponse {
  id: string;
  slug: string;
  title: string;
  description?: string;
  coverImage?: string;
  createdAt: string;
  updatedAt: string;
  published: boolean;
  featured: boolean;
  category: PostCategoryResponse;
  tags: PostTagResponse[];
  readingTime: number;
  wordCount: number;
  views: number;
}

export interface ArchiveItem {
  year: number;
  month: number;
  posts: PostArchiveResponse[];
}

export interface PostCreate {
  title: string;
  slug: string;
  description?: string;
  content: string;
  coverImage?: string;
  published?: boolean;
  featured?: boolean;
  categoryId: string;
  tagIds: string[];
  seriesId?: string;
  seriesOrder?: number;
}

export interface PostUpdate {
  title?: string;
  slug?: string;
  description?: string;
  content?: string;
  coverImage?: string;
  published?: boolean;
  featured?: boolean;
  categoryId?: string;
  tagIds?: string[];
  seriesId?: string;
  seriesOrder?: number;
}
