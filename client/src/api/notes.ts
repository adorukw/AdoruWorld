/**
 * 笔记 API 模块
 *
 * 直接从 GitHub API 读取 adorukw/Note 仓库的 Markdown 文件。
 * 无需后端参与，纯前端搞定。
 *
 * 工作原理：
 * 1. Tree API → 一次请求拿到整个仓库的目录结构（所有文件路径）
 * 2. Contents API → 按路径读取某个 .md 文件的原始内容
 * 3. marked 渲染 → 把 Markdown 转成 HTML 展示
 *
 * 参考 GitHub API 文档：
 * https://docs.github.com/en/rest/git/trees
 * https://docs.github.com/en/rest/repos/contents
 */

const GITHUB_OWNER = "adorukw";
const GITHUB_REPO = "Note";
const GITHUB_BRANCH = "main";

const GITHUB_API = `https://api.github.com/repos/${GITHUB_OWNER}/${GITHUB_REPO}`;
const GITHUB_RAW = `https://raw.githubusercontent.com/${GITHUB_OWNER}/${GITHUB_REPO}/${GITHUB_BRANCH}`;

// ──────────────────────────────────────────
// 类型定义
// ──────────────────────────────────────────

/** GitHub Tree API 返回的节点 */
export interface GitHubTreeNode {
  path: string;
  mode: string;
  type: "tree" | "blob";
  sha: string;
  size?: number;
  url: string;
}

/** GitHub Tree API 完整响应 */
interface GitHubTreeResponse {
  sha: string;
  url: string;
  tree: GitHubTreeNode[];
  truncated: boolean;
}

/** GitHub Contents API 返回的单个文件 */
interface GitHubContentResponse {
  name: string;
  path: string;
  sha: string;
  size: number;
  url: string;
  html_url: string;
  git_url: string;
  download_url: string | null;
  type: "file" | "dir";
  content?: string;
  encoding?: string;
}

/** 我们前端用的文件节点（扁平化的目录树条目） */
export interface NoteFileNode {
  path: string;
  name: string;
  type: "file" | "dir";
  depth: number;
  /** 仅 .md 文件有内容路径 */
  contentUrl?: string;
}

/** 按目录层级组织的树节点（用于 FileTree 组件递归渲染） */
export interface NoteTreeNode {
  name: string;
  path: string;
  type: "file" | "dir";
  children: NoteTreeNode[];
  filePath?: string;
}

// ──────────────────────────────────────────
// API 函数
// ──────────────────────────────────────────

/**
 * 获取仓库完整文件树
 *
 * 使用 Git Trees API，?recursive=1 可以一次性拿到所有文件和目录。
 * 比反复请求 Contents API 快得多，而且只需要 1 次请求（节省 API 配额）。
 *
 * 速率限制（未认证）：60 次/小时 → 一次 tree 请求就够了
 * 速率限制（带 token）：5000 次/小时
 */
export async function fetchNoteTree(): Promise<NoteTreeNode[]> {
  const url = `${GITHUB_API}/git/trees/${GITHUB_BRANCH}?recursive=1`;

  const res = await fetch(url);

  if (!res.ok) {
    throw new Error(`GitHub API 请求失败: ${res.status} ${res.statusText}`);
  }

  const data: GitHubTreeResponse = await res.json();

  if (data.truncated) {
    console.warn("⚠️ 仓库文件过多，GitHub Tree API 返回结果被截断");
  }

  // 过滤出 .md 文件和目录，排除 .git 相关文件和 Obsidian 配置
  const filtered = data.tree.filter((node) => {
    // 排除隐藏文件和目录
    if (node.path.startsWith(".")) return false;
    if (node.path.includes("/.")) return false;
    // 只保留目录 或 .md 文件
    if (node.type === "tree") return true;
    return node.path.endsWith(".md");
  });

  // 构建层级树结构
  return buildTree(filtered);
}

/**
 * 从 /contents API 读取单个 .md 文件的内容（base64 解码）
 */
export async function fetchNoteContent(filePath: string): Promise<string> {
  const encodedPath = filePath.split("/").map(encodeURIComponent).join("/");
  const url = `${GITHUB_API}/contents/${encodedPath}`;

  const res = await fetch(url);

  if (!res.ok) {
    throw new Error(`读取笔记失败: ${res.status} ${res.statusText}`);
  }

  const data: GitHubContentResponse = await res.json();

  if (data.encoding === "base64" && data.content) {
    // GitHub API 返回 base64，需要解码
    return atob(data.content.replace(/\n/g, ""));
  }

  throw new Error("无法解析文件内容");
}

/**
 * 直接从 raw.githubusercontent.com 获取 .md 文件内容
 * 更简单，不需要 base64 解码，但需要自己 handle 网络错误
 */
export async function fetchNoteContentRaw(filePath: string): Promise<string> {
  const encodedPath = filePath.split("/").map(encodeURIComponent).join("/");
  const url = `${GITHUB_RAW}/${encodedPath}`;

  const res = await fetch(url);

  if (!res.ok) {
    throw new Error(`读取笔记失败: ${res.status} ${res.statusText}`);
  }

  return res.text();
}

// ──────────────────────────────────────────
// 辅助函数
// ──────────────────────────────────────────

/**
 * 扁平 Tree API 节点 → 嵌套树结构
 *
 * 例如输入：
 *   ["技术笔记/前端/Vue3/系统教程.md", "技术笔记/Python/系统教程.md"]
 *
 * 输出：
 *   {
 *     name: "技术笔记",
 *     children: [
 *       { name: "前端", children: [{ name: "Vue3", children: [{ name: "系统教程.md", type: "file" }] }] },
 *       { name: "Python", children: [{ name: "系统教程.md", type: "file" }] }
 *     ]
 *   }
 */
function buildTree(nodes: GitHubTreeNode[]): NoteTreeNode[] {
  const root: NoteTreeNode[] = [];

  for (const node of nodes) {
    const parts = node.path.split("/");
    let currentLevel = root;

    for (let i = 0; i < parts.length; i++) {
      const part = parts[i];
      const isLast = i === parts.length - 1;

      // 对于文件节点，只看 .md 文件
      if (isLast && node.type === "blob") {
        // 已经过滤过了，直接添加
        const existing = currentLevel.find((n) => n.name === part);
        if (!existing) {
          currentLevel.push({
            name: part,
            path: node.path,
            type: "file",
            children: [],
            filePath: node.path,
          });
        }
        break;
      }

      // 目录节点
      if (isLast && node.type === "tree") {
        const existing = currentLevel.find((n) => n.name === part);
        if (!existing) {
          currentLevel.push({
            name: part,
            path: node.path,
            type: "dir",
            children: [],
          });
        }
        break;
      }

      // 中间目录，找或创建
      if (!isLast) {
        let dir = currentLevel.find((n) => n.name === part && n.type === "dir");
        if (!dir) {
          dir = {
            name: part,
            path: parts.slice(0, i + 1).join("/"),
            type: "dir",
            children: [],
          };
          currentLevel.push(dir);
        }
        currentLevel = dir.children;
      }
    }
  }

  // 排序：目录在前，文件在后，各自按名称排序
  return sortTree(root);
}

/**
 * 排序：目录先于文件，各自按名称字母/拼音排序
 */
function sortTree(nodes: NoteTreeNode[]): NoteTreeNode[] {
  const dirs = nodes
    .filter((n) => n.type === "dir")
    .sort((a, b) => a.name.localeCompare(b.name, "zh-CN"));
  const files = nodes
    .filter((n) => n.type === "file")
    .sort((a, b) => a.name.localeCompare(b.name, "zh-CN"));

  // 递归排序子目录
  for (const dir of dirs) {
    dir.children = sortTree(dir.children);
  }

  return [...dirs, ...files];
}
