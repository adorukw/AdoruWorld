import asyncio
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import async_session, init_db
from app.models import (PostCategory, PostTag, Post, post_to_post_tags,
                        DexEntry, DexGenre, dex_to_dex_genres, Media, MediaTypeEnum, media_to_media_tags, MediaTag)
import re

categories = [
    {"id": '1', "name": '技术笔记', "slug": 'tech', "description": '编程、开发、技术教程',
        "count": 12, "icon": '💻', "color": '#3C5AA6'},
    {"id": '2', "name": '生活随笔', "slug": 'life', "description": '日常记录、思考、见闻',
        "count": 8, "icon": '🌸', "color": '#FF7300'},
    {"id": '3', "name": '开发日志', "slug": 'projects', "description": '个人项目开发日志',
        "count": 5, "icon": '🚀', "color": '#FF0000'},
    {"id": '4', "name": '读书笔记', "slug": 'reading', "description": '书籍阅读心得',
        "count": 6, "icon": '📚', "color": '#7B5BA6'},
    {"id": '5', "name": '游戏人生', "slug": 'gaming', "description": '游戏评测、心得',
        "count": 4, "icon": '🎮', "color": '#FFDE00'},
    {"id": '6', "name": '创意思考', "slug": 'creative', "description": '设计、艺术、创意分享',
        "count": 3, "icon": '✨', "color": '#9CBB0F'}
]

tags = [
    {"id": '1', "name": 'Vue', "slug": 'vue', "color": '#42b883', "count": 8},
    {"id": '2', "name": 'TypeScript', "slug": 'typescript',
        "color": '#3178c6', "count": 6},
    {"id": '3', "name": 'React', "slug": 'react', "color": '#61dafb', "count": 4},
    {"id": '4', "name": 'Node.js', "slug": 'nodejs', "color": '#68a063', "count": 5},
    {"id": '5', "name": '前端', "slug": 'frontend', "color": '#FF7300', "count": 10},
    {"id": '6', "name": '后端', "slug": 'backend', "color": '#3C5AA6', "count": 4},
    {"id": '7', "name": 'CSS', "slug": 'css', "color": '#264de4', "count": 3},
    {"id": '8', "name": '像素艺术', "slug": 'pixel-art', "color": '#FFDE00', "count": 2},
    {"id": '9', "name": '游戏开发', "slug": 'game-dev', "color": '#FF0000', "count": 3},
    {"id": '10', "name": '生活', "slug": 'life', "color": '#9CBB0F', "count": 8}
]

posts = [
    {
        "id": '1',
        "slug": 'vue3-pixel-blog',
        "title": '使用Vue 3构建像素风格博客',
        "description": '本文介绍如何使用Vue 3和Tailwind CSS构建一个口袋妖怪风格的像素艺术博客，包括技术选型、实现细节和部署方案。',
        "content": """# 使用Vue 3构建像素风格博客

## 前言

作为一个口袋妖怪的忠实粉丝，我一直想要创建一个具有GBA时代风格的个人博客。在这篇文章中，我将分享如何使用Vue 3和Tailwind CSS来实现这个目标。

## 技术选型

- **框架**: Vue 3 + Composition API
- **构建工具**: Vite
- **样式方案**: Tailwind CSS + 自定义像素样式
- **状态管理**: Pinia
- **路由**: Vue Router

## 设计系统

### 配色方案

我们采用了Gen 3口袋妖怪的典型配色：

```css
--color-pokemon-blue: #3C5AA6;
--color-pokemon-red: #FF0000;
--color-pokemon-yellow: #FFDE00;
--color-pokemon-green: #9CBB0F;
```

### 像素边框效果

```css
.pixel-border {
  border: 4px solid var(--color-pokemon-black);
  box-shadow: 4px 4px 0 var(--color-pokemon-dark-gray);
}
```

## 总结

通过这个项目，我们不仅实现了一个功能完整的博客系统，还创造了一个独特的视觉体验。""",
        "cover_image": 'https://picsum.photos/seed/pixel-blog/800/400',
        "createdAt": '2024-01-15',
        "updatedAt": '2024-01-20',
        "published": True,
        "category": '技术笔记',
        "tags": ['Vue', 'TypeScript', '前端', '像素艺术'],
        "readingTime": 8,
        "wordCount": 2500,
        "views": 1234,
        "featured": True
    },
    {
        "id": '2',
        "slug": 'typescript-advanced-patterns',
        "title": 'TypeScript高级类型模式详解',
        "description": '深入探讨TypeScript中的高级类型模式，包括条件类型、映射类型、模板字面量类型等高级特性的实际应用。',
        "content": """# TypeScript高级类型模式详解

## 条件类型

条件类型允许我们根据类型关系进行条件判断：

\`\`\`typescript
type IsString<T> = T extends string ? true : false;

type A = IsString<string>; // true
type B = IsString<number>; // false
\`\`\`

## 映射类型

映射类型可以基于现有类型创建新类型：

\`\`\`typescript
type Readonly<T> = {
  readonly [P in keyof T]: T[P];
};
\`\`\`

## 总结

掌握这些高级类型模式，可以让你的TypeScript代码更加类型安全和可维护。""",
        "cover_image": 'https://picsum.photos/seed/typescript/800/400',
        "createdAt": '2024-01-10',
        "updatedAt": '2024-01-12',
        "published": True,
        "category": '技术笔记',
        "tags": ['TypeScript', '前端'],
        "readingTime": 12,
        "wordCount": 3800,
        "views": 856,
        "featured": True
    },
    {
        "id": '3',
        "slug": 'life-in-2024',
        "title": '2024年生活回顾',
        "description": '回顾2024年的生活点滴，记录成长与变化，展望未来的方向。',
        "content": """# 2024年生活回顾

## 年初计划

2024年初，我给自己定下了几个目标：

1. 学习一门新技能
2. 完成一个个人项目
3. 保持健康的生活方式

## 完成情况

### 技术成长

今年我深入学习了Vue 3和TypeScript，并完成了这个像素风格的博客项目。

### 生活变化

搬了新家，养了一只猫，生活变得更加充实。

## 展望2025

新的一年，希望能够继续保持学习的热情，创造更多有价值的内容。""",
        "cover_image": 'https://picsum.photos/seed/life-2024/800/400',
        "createdAt": '2024-12-31',
        "updatedAt": '2024-12-31',
        "published": True,
        "category": '生活随笔',
        "tags": ['生活'],
        "readingTime": 5,
        "wordCount": 1200,
        "views": 432,
        "featured": False
    },
    {
        "id": '4',
        "slug": 'nodejs-best-practices',
        "title": 'Node.js最佳实践指南',
        "description": '总结Node.js开发中的最佳实践，包括项目结构、错误处理、性能优化等方面。',
        "content": """# Node.js最佳实践指南

## 项目结构

推荐的项目结构：

\`\`\`
src/
├── controllers/
├── services/
├── models/
├── middlewares/
├── utils/
└── app.ts
\`\`\`

## 错误处理

使用统一的错误处理中间件：

\`\`\`typescript
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ error: 'Something went wrong!' });
});
\`\`\`

## 性能优化

- 使用集群模式
- 启用压缩
- 使用缓存
- 优化数据库查询""",
        "cover_image": 'https://picsum.photos/seed/nodejs/800/400',
        "createdAt": '2024-02-05',
        "updatedAt": '2024-02-08',
        "published": True,
        "category": '技术笔记',
        "tags": ['Node.js', '后端'],
        "readingTime": 10,
        "wordCount": 2800,
        "views": 678,
        "featured": False
    },
    {
        "id": '5',
        "slug": 'game-dev-diary-1',
        "title": '独立游戏开发日记：第一周',
        "description": '记录我开发第一款独立游戏的第一周经历，从构思到原型实现。',
        "content": """# 独立游戏开发日记：第一周

## 游戏概念

我决定开发一款像素风格的冒险游戏，灵感来自经典的口袋妖怪系列。

## 技术选择

- 游戏引擎: Phaser 3
- 语言: TypeScript
- 美术: Aseprite

## 本周进展

### 完成的工作

1. 搭建了基础项目框架
2. 实现了角色移动
3. 创建了第一个测试地图

### 遇到的挑战

- 地图碰撞检测的实现
- 动画帧同步问题

## 下周计划

- 添加NPC交互
- 实现战斗系统原型""",
        "cover_image": 'https://picsum.photos/seed/game-dev/800/400',
        "createdAt": '2024-03-01',
        "updatedAt": '2024-03-01',
        "published": True,
        "category": '项目记录',
        "tags": ['游戏开发', 'TypeScript'],
        "readingTime": 6,
        "wordCount": 1500,
        "views": 345,
        "featured": False
    },
    {
        "id": '6',
        "slug": 'reading-clean-code',
        "title": '《代码整洁之道》读书笔记',
        "description": '分享阅读《代码整洁之道》的心得体会，总结编写整洁代码的关键原则。',
        "content": """# 《代码整洁之道》读书笔记

## 核心原则

### 有意义的命名

变量、函数、类的名称应该表达其意图：

\`\`\`typescript
// 不好的命名
const d = new Date();

// 好的命名
const currentDate = new Date();
\`\`\`

### 函数应该短小

函数应该只做一件事，做好这件事，只做这一件事。

### 注释

最好的注释是不需要注释。代码应该自我解释。

## 实践建议

1. 保持代码格式一致
2. 遵循团队规范
3. 及时重构
4. 编写测试

## 总结

整洁的代码是专业程序员的基本素养，需要持续练习和改进。""",
        "cover_image": 'https://picsum.photos/seed/clean-code/800/400',
        "createdAt": '2024-02-20',
        "updatedAt": '2024-02-22',
        "published": True,
        "category": '读书笔记',
        "tags": ['前端', '后端'],
        "readingTime": 7,
        "wordCount": 1800,
        "views": 567,
        "featured": False
    }
]

dexEntries = [
    {
        "id": '1',
        "slug": 'pokemon-horizons',
        "title": '宝可梦 地平线',
        "originalTitle": 'ポケットモンスター',
        "coverImage": 'https://picsum.photos/seed/pokemon-anime/300/400',
        "category": 'anime',
        "status": 'watching',
        "rating": 9,
        "startDate": '2023-04-14',
        "comment": '新一代宝可梦动画，莉可和罗伊的冒险故事非常精彩！',
        "creator": 'OLM',
        "year": 2023,
        "genre": ['冒险', '奇幻']
    },
    {
        "id": '2',
        "slug": 'spirited-away',
        "title": '千与千寻',
        "originalTitle": '千と千尋の神隠し',
        "coverImage": 'https://picsum.photos/seed/spirited-away/300/400',
        "category": 'movie',
        "status": 'completed',
        "rating": 10,
        "startDate": '2020-06-15',
        "finishDate": '2020-06-15',
        "comment": '宫崎骏的巅峰之作，每次看都有新的感悟。',
        "creator": '宫崎骏',
        "year": 2001,
        "genre": ['奇幻', '冒险']
    },
    {
        "id": '3',
        "slug": 'breaking-bad',
        "title": '绝命毒师',
        "originalTitle": 'Breaking Bad',
        "coverImage": 'https://picsum.photos/seed/breaking-bad/300/400',
        "category": 'tv',
        "status": 'completed',
        "rating": 10,
        "startDate": '2022-01-10',
        "finishDate": '2022-03-20',
        "comment": '神剧！人物塑造和剧情发展都堪称完美。',
        "creator": 'Vince Gilligan',
        "year": 2008,
        "genre": ['犯罪', '剧情']
    },
    {
        "id": '4',
        "slug": 'pokemon-scarlet-violet',
        "title": '宝可梦 朱/紫',
        "originalTitle": 'ポケットモンスター・スカーレット・バイオレット',
        "coverImage": 'https://picsum.photos/seed/pokemon-sv/300/400',
        "category": 'game',
        "status": 'completed',
        "rating": 8,
        "startDate": '2022-11-18',
        "finishDate": '2023-02-28',
        "comment": '开放世界宝可梦，虽然技术问题多但游戏性很棒！',
        "creator": 'Game Freak',
        "year": 2022,
        "genre": ['RPG', '冒险']
    },
    {
        "id": '5',
        "slug": 'harry-potter-series',
        "title": '哈利·波特系列',
        "originalTitle": 'Harry Potter',
        "coverImage": 'https://picsum.photos/seed/harry-potter/300/400',
        "category": 'book',
        "status": 'completed',
        "rating": 10,
        "startDate": '2015-06-01',
        "finishDate": '2016-08-15',
        "comment": '陪伴我成长的经典，魔法世界永远令人向往。',
        "creator": 'J.K. Rowling',
        "year": 1997,
        "genre": ['奇幻', '冒险']
    },
    {
        "id": '6',
        "slug": 'radiohead-ok-computer',
        "title": 'OK Computer',
        "originalTitle": 'OK Computer',  # ✅ 新增：添加原名
        "coverImage": 'https://picsum.photos/seed/ok-computer/300/400',
        "category": 'music',
        "status": 'completed',
        "rating": 10,
        "startDate": '2021-03-10',
        "comment": 'Radiohead的巅峰之作，每一首歌都是艺术品。',
        "creator": 'Radiohead',
        "year": 1997,
        "genre": ['另类摇滚', '艺术摇滚']
    },
    {
        "id": '7',
        "slug": 'elden-ring',
        "title": '艾尔登法环',
        "originalTitle": 'ELDEN RING',
        "coverImage": 'https://picsum.photos/seed/elden-ring/300/400',
        "category": 'game',
        "status": 'completed',
        "rating": 10,
        "startDate": '2022-02-25',
        "finishDate": '2022-05-15',
        "comment": '宫崎英高与乔治·R·R·马丁的完美合作，年度最佳！',
        "creator": 'FromSoftware',
        "year": 2022,
        "genre": ['动作RPG', '开放世界']
    },
    {
        "id": '8',
        "slug": 'your-name',
        "title": '你的名字。',
        "originalTitle": '君の名は。',
        "coverImage": 'https://picsum.photos/seed/your-name/300/400',
        "category": 'movie',
        "status": 'completed',
        "rating": 9,
        "startDate": '2016-12-02',
        "finishDate": '2016-12-02',
        "comment": '新海诚的视觉盛宴，故事也很动人。',
        "creator": '新海诚',
        "year": 2016,
        "genre": ['爱情', '奇幻']
    },
    {
        "id": '9',
        "slug": 'steins-gate',
        "title": '命运石之门',
        "originalTitle": 'STEINS;GATE',
        "coverImage": 'https://picsum.photos/seed/steins-gate/300/400',
        "category": 'anime',
        "status": 'completed',
        "rating": 10,
        "startDate": '2021-07-01',
        "finishDate": '2021-07-15',
        "comment": '神作！前期铺垫后期爆发，剧情设计太精妙了。',
        "creator": 'WHITE FOX',
        "year": 2011,
        "genre": ['科幻', '悬疑']
    },
    {
        "id": '10',
        "slug": 'zelda-totk',
        "title": '塞尔达传说 王国之泪',
        "originalTitle": 'ゼルダの伝説 ティアーズ オブ ザ キングダム',
        "coverImage": 'https://picsum.photos/seed/zelda-totk/300/400',
        "category": 'game',
        "status": 'playing',
        "rating": 4,
        "startDate": '2023-05-12',
        "comment": '旷野之息的续作，建造系统太有趣了！',
        "creator": 'Nintendo',
        "year": 2023,
        "genre": ['动作冒险', '开放世界']
    },
    {
        "id": '11',
        "slug": 'dune-part2',
        "title": '沙丘2',
        "originalTitle": 'Dune: Part Two',
        "coverImage": 'https://picsum.photos/seed/dune2/300/400',
        "category": 'movie',
        "status": 'completed',
        "rating": 9,
        "startDate": '2024-03-01',
        "finishDate": '2024-03-01',
        "comment": '维伦纽瓦的史诗巨作，视觉效果震撼！',
        "creator": 'Denis Villeneuve',
        "year": 2024,
        "genre": ['科幻', '史诗']
    },
    {
        "id": '12',
        "slug": 'pink-floyd-dark-side',
        "title": 'The Dark Side of the Moon',
        "originalTitle": 'The Dark Side of the Moon',
        "coverImage": 'https://picsum.photos/seed/dark-side/300/400',
        "category": 'music',
        "status": 'completed',
        "rating": 10,
        "startDate": '2020-05-20',
        "comment": '摇滚史上最伟大的专辑之一，必须完整聆听。',
        "creator": 'Pink Floyd',
        "year": 1973,
        "genre": ['前卫摇滚']
    },
    {
        "id": '13',
        "slug": 'attack-on-titan',
        "title": '进击的巨人',
        "originalTitle": '進撃の巨人',
        "coverImage": 'https://picsum.photos/seed/aot/300/400',
        "category": 'anime',
        "status": 'completed',
        "rating": 10,
        "startDate": '2020-01-01',
        "finishDate": '2023-11-04',
        "comment": '史诗级作品，结局虽然争议但整体是神作。',
        "creator": 'MAPPA / Wit Studio',
        "year": 2013,
        "genre": ['动作冒险', '黑暗奇幻']
    },
    {
        "id": '14',
        "slug": 'three-body-problem',
        "title": '三体',
        "originalTitle": '三体',  # ✅ 新增：添加原名
        "coverImage": 'https://picsum.photos/seed/three-body/300/400',
        "category": 'book',
        "status": 'completed',
        "rating": 10,
        "startDate": '2019-04-01',
        "finishDate": '2019-06-15',
        "comment": '中国科幻的巅峰之作，想象力令人震撼。',
        "creator": '刘慈欣',
        "year": 2008,
        "genre": ['科幻']
    },
    {
        "id": '15',
        "slug": 'persona-5-royal',
        "title": '女神异闻录5 皇家版',
        "originalTitle": 'ペルソナ5 ザ・ロイヤル',
        "coverImage": 'https://picsum.photos/seed/p5r/300/400',
        "category": 'game',
        "status": 'completed',
        "rating": 10,
        "startDate": '2022-08-01',
        "finishDate": '2022-10-15',
        "comment": 'P5天下第一！音乐、美术、剧情都是顶级。',
        "creator": 'ATLUS',
        "year": 2020,
        "genre": ['RPG', '回合制']
    }
]

dexGenres = [
    {

        "name": "冒险",
        "slug": "adventure",
        "color": "#FF6B6B"  # 红色系
    },
    {

        "name": "奇幻",
        "slug": "fantasy",
        "color": "#4ECDC4"  # 青绿色系
    },
    {

        "name": "犯罪",
        "slug": "crime",
        "color": "#45B7D1"  # 蓝色系
    },
    {

        "name": "剧情",
        "slug": "drama",
        "color": "#96CEB4"  # 绿色系
    },
    {

        "name": "RPG",
        "slug": "rpg",
        "color": "#FFEAA7"  # 黄色系
    },
    {

        "name": "另类摇滚",
        "slug": "alternative-rock",
        "color": "#DDA0DD"  # 紫色系
    },
    {

        "name": "艺术摇滚",
        "slug": "art-rock",
        "color": "#98D8C8"  # 薄荷绿系
    },
    {

        "name": "动作RPG",
        "slug": "action-rpg",
        "color": "#F7DC6F"  # 金黄色系
    },
    {

        "name": "开放世界",
        "slug": "open-world",
        "color": "#BB8FCE"  # 淡紫色系
    },
    {

        "name": "爱情",
        "slug": "romance",
        "color": "#85C1E9"  # 天蓝色系
    },
    {

        "name": "科幻",
        "slug": "sci-fi",
        "color": "#F1948A"  # 粉红色系
    },
    {

        "name": "悬疑",
        "slug": "mystery",
        "color": "#7FB3D5"  # 钢蓝色系
    },
    {

        "name": "动作冒险",
        "slug": "action-adventure",
        "color": "#82E0AA"  # 翠绿色系
    },
    {

        "name": "史诗",
        "slug": "epic",
        "color": "#F8C471"  # 橙色系
    },
    {

        "name": "前卫摇滚",
        "slug": "progressive-rock",
        "color": "#D7BDE2"  # 薰衣草色系
    },
    {

        "name": "黑暗奇幻",
        "slug": "dark-fantasy",
        "color": "#85929E"  # 灰蓝色系
    },
    {

        "name": "回合制",
        "slug": "turn-based",
        "color": "#A3E4D7"  # 青绿色系
    }
]


def calculate_reading_time(content: str) -> int:
    """计算文章阅读时长（分钟）"""
    if not content:
        return 0

    # 移除 Markdown 代码块
    content_without_code = re.sub(r'```[\s\S]*?```', '', content)
    content_without_code = re.sub(r'`[^`]+`', '', content_without_code)

    # 统计图片数量
    image_count = len(re.findall(r'!\[.*?\]\(.*?\)', content))

    # 移除 Markdown 标记
    text = re.sub(r'^#+\s*', '', content_without_code, flags=re.MULTILINE)
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    text = re.sub(r'__(.*?)__', r'\1', text)
    text = re.sub(r'_(.*?)_', r'\1', text)
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    text = re.sub(r'^\s*[-*+]\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*\d+\.\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*>\s+', '', text, flags=re.MULTILINE)

    # 计算字符数
    char_count = len(text.strip())

    # 计算阅读时间（每分钟 300 字符）
    base_reading_time = char_count / 300

    # 图片额外时间
    image_time = image_count * 0.2

    total_time = base_reading_time + image_time

    return max(1, int(total_time + 0.99))


async def seed_categories(db: AsyncSession) -> dict[str, str]:
    """播种文章分类，返回 {分类名称: id} 映射"""
    cat_map = {}
    for c in categories:
        obj = PostCategory(
            name=c["name"],
            slug=c["slug"],
            description=c.get("description"),
            icon=c.get("icon"),
            color=c.get("color"),
        )
        db.add(obj)
        await db.flush()
        cat_map[c["name"]] = obj.id
    await db.flush()
    print(f"✅ 导入 {len(categories)} 个文章分类")
    return cat_map


async def seed_tags(db: AsyncSession) -> dict[str, str]:
    """播种文章标签，返回 {标签名称: id} 映射"""
    tag_map = {}
    for t in tags:
        obj = PostTag(
            name=t["name"],
            slug=t["slug"],
            color=t.get("color"),
        )
        db.add(obj)
        await db.flush()
        tag_map[t["name"]] = obj.id
    await db.flush()
    print(f"✅ 导入 {len(tags)} 个文章标签")
    return tag_map


async def seed_posts(db: AsyncSession, cat_map: dict[str, str], tag_map: dict[str, str]):
    """播种文章（依赖分类和标签映射）"""
    for p in posts:
        content = p["content"]
        reading_time = calculate_reading_time(content)
        word_count = len(content.strip())

        post = Post(
            slug=p["slug"],
            title=p["title"],
            description=p.get("description"),
            content=p["content"],
            cover_image=p.get("cover_image"),

            # 状态字段
            published=p.get("published", True),
            featured=p.get("featured", False),

            # 统计字段
            reading_time=reading_time,
            word_count=word_count,
            views=p.get("views", 0),

            # 关联字段
            category_id=cat_map[p["category"]],
        )
        db.add(post)
        await db.flush()

        # 关联标签
        for tag_name in p["tags"]:
            tag_id = tag_map[tag_name]
            await db.execute(
                post_to_post_tags.insert().values(
                    post_id=post.id,
                    post_tag_id=tag_id
                )
            )
    print(f"✅ 导入 {len(posts)} 篇文章")


async def seed_dex_genres(db: AsyncSession) -> dict[str, str]:
    """播种图鉴题材，返回 {题材名称: id} 映射"""
    genre_map = {}
    for genre in dexGenres:
        dexGenre = DexGenre(
            name=genre["name"],
            slug=genre["slug"],
            color=genre["color"],
        )
        db.add(dexGenre)
        await db.flush()
        genre_map[genre["name"]] = dexGenre.id
    await db.flush()
    print(f"✅ 导入 {len(dexGenres)} 个图鉴题材")
    return genre_map


async def seed_dex_entries(db: AsyncSession, genre_map: dict[str, str]):
    """播种图鉴条目（依赖题材映射）"""
    for d in dexEntries:
        dexEntry = DexEntry(
            slug=d["slug"],
            title=d["title"],
            original_title=d["originalTitle"],
            cover_image=d["coverImage"],
            category=d["category"],
            status=d["status"],
            rating=d["rating"],
            start_date=d.get("startDate"),
            finish_date=d.get("finish_date"),
            comment=d.get("comment"),
            creator=d.get("creator"),
            year=d.get("year"),
            summary=d.get("summary"),
        )
        db.add(dexEntry)
        await db.flush()

        for genre_name in d["genre"]:
            genre_id = genre_map[genre_name]
            await db.execute(
                dex_to_dex_genres.insert().values(
                    dex_entry_id=dexEntry.id,
                    dex_genre_id=genre_id
                )
            )
    print(f"✅ 导入 {len(dexEntries)} 个图鉴条目")


async def seed():
    """一键播种所有数据"""
    await init_db()
    async with async_session() as db:
        print("🧹 清空现有数据...")
        await db.execute(post_to_post_tags.delete())
        await db.execute(dex_to_dex_genres.delete())
        await db.execute(media_to_media_tags.delete())
        await db.execute(Post.__table__.delete())
        await db.execute(PostTag.__table__.delete())
        await db.execute(PostCategory.__table__.delete())
        await db.execute(DexEntry.__table__.delete())
        await db.execute(DexGenre.__table__.delete())
        await db.execute(Media.__table__.delete())
        await db.execute(MediaTag.__table__.delete())
        await db.commit()
        print("✅ 数据清空完成")

        cat_map = await seed_categories(db)
        tag_map = await seed_tags(db)
        # await seed_posts(db, cat_map, tag_map)
        genre_map = await seed_dex_genres(db)
        # await seed_dex_entries(db, genre_map)

        await db.commit()
        print("✅ 数据导入完成")

if __name__ == "__main__":
    asyncio.run(seed())
