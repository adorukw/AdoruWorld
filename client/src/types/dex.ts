import type { DexGenreResponse } from "./dex-genre";
import type { MediaResponse } from "./media";

export type DexCategory =
  "anime" | "movie" | "tv" | "game" | "book" | "music" | "other";

export type DexStatus =
  | "completed"
  | "watching"
  | "playing"
  | "reading"
  | "listening"
  | "doing"
  | "dropped"
  | "planned";

export interface DexCategoryInfo {
  id: DexCategory;
  name: string;
  slug: string;
  icon: string;
  color: string;
  bgColor: string;
}

export interface DexStatusInfo {
  id: DexStatus;
  name: string;
  slug: string;
  icon: string;
  color: string;
}

export interface DexResponse {
  id: string;
  slug: string;
  title: string;
  originalTitle?: string;
  coverImage: string;
  category: DexCategory;
  status: DexStatus;
  rating: number;
  startDate?: string;
  finishDate?: string;
  comment?: string;
  summary?: string;
  creator?: string;
  year?: number;
  externalUrl?: string;
  genres?: DexGenreResponse[];
  medias?: MediaResponse[];
}

export interface DexCreate {
  slug: string;
  title: string;
  originalTitle?: string;
  coverImage: string;
  category: DexCategory;
  status: DexStatus;
  rating: number;
  startDate?: string;
  finishDate?: string;
  comment?: string;
  summary?: string;
  creator?: string;
  year?: number;
  externalUrl?: string;
  genreIds?: string[];
  mediaIds?: string[];
}

export interface DexUpdate {
  slug?: string;
  title?: string;
  originalTitle?: string;
  coverImage?: string;
  category?: DexCategory;
  status?: DexStatus;
  rating?: number;
  startDate?: string;
  finishDate?: string;
  comment?: string;
  summary?: string;
  creator?: string;
  year?: number;
  externalUrl?: string;
  genreIds?: string[];
  mediaIds?: string[];
}

export interface DexStats {
  total: number;
  byCategory: Record<string, number>;
  byStatus: Record<string, number>;
  averageRating: number;
}
