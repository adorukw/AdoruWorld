export interface SearchResultItem {
  id: string;
  type: "post" | "dex" | "media";
  title: string;
  slug: string;
  description: string;
  coverImage: string;
  createdAt: string;
  matchedFields: string[];
  entityData: Record<string, any>;
}

export interface SearchResponse {
  items: SearchResultItem[];
  total: number;
  skip: number;
  limit: number;
}
