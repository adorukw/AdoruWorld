export * from "./post-category";
export * from "./post-tag";
export * from "./post";
export * from "./dex";
export * from "./dex-genre";
export * from "./media";
export * from "./media-tag";
export * from "./form.ts";

export interface TocItem {
  id: string;
  text: string;
  level: number;
  children: TocItem[];
}

export interface NavItem {
  name: string;
  path: string;
  icon?: string;
}

export interface SocialLink {
  name: string;
  url: string;
  icon?: string;
}

export interface SiteStats {
  totalPosts: number;
  totalWords: number;
  totalViews: number;
  runningDays: number;
}

export interface Author {
  name: string;
  avatar: string;
  bio: string;
  location: string;
  social: {
    github?: string;
    email?: string;
  };
}

export interface Project {
  id: string;
  name: string;
  description?: string;
  tech: string[];
  link?: string;
  github?: string;
  image?: string;
  status: "completed" | "in-progress" | "archived";
}
