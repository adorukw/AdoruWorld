export interface SeriesResponse {
  id: string;
  count: number;
  name: string;
  slug: string;
  description?: string;
  coverImage?: string;
}

export interface SeriesCreate {
  name: string;
  slug: string;
  description?: string;
  coverImage?: string;
}

export interface SeriesUpdate {
  name?: string;
  slug?: string;
  description?: string;
  coverImage?: string;
}

export interface SeriesPostResponse {
  id: string;
  slug: string;
  title: string;
  description?: string;
  coverImage?: string;
  createdAt: string;
  updatedAt: string;
  published: boolean;
  readingTime: number;
  wordCount: number;
  views: number;
  featured: boolean;
  seriesOrder?: number;
}

export interface PostLink {
  slug: string;
  title: string;
}
