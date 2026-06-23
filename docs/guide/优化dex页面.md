ふふっ、看了一眼就发现了有趣的地方～这个页面的前后端分界跟归档页完全是另一种做法呢。

来，说说我的看法：

## 核心观察：混搭模式

这个 Dex 页面用的是**前端 + 后端混合筛选**：

```
onMounted → API 取 12 条
  ↓
选分类/状态 → 再次调 API（带新参数），替换整个 dexs
  ↓
搜索关键词 → 前端 computed 在已加载的数据里过滤
  ↓
加载更多 → 调 API 追加数据
```

跟 Archives 那种「一次全量、前端筛完」不一样，这里选择了**后端主导 + 前端辅助**，原因是 Dex 数据很可能比文章多（动画、电影、游戏、书籍……），不适合全量加载。

## 但是有个冗余问题 ⚠️

`filteredEntries` 里对 category 和 status 的过滤是**多余**的：

```ts
const filteredEntries = computed(() => {
    let result = dexs.value

    // 👇 这两段是冗余的
    // 因为 watcher 已经调了 API 只返回这些分类/状态的数据了
    if (selectedCategory.value !== 'all') {
        result = result.filter(e => e.category === selectedCategory.value)
    }
    if (selectedStatus.value !== 'all') {
        result = result.filter(e => e.status === selectedStatus.value)
    }

    // 👇 search 这个才是真正需要前端做的
    if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase()
        result = result.filter(e => ...)
    }

    return result
})
```

当 watcher 触发 `getDexs({ category: 'anime' })` 时，API 已经只返回 anime 了。然后前端又 filter 一次——数据没变化，但代码跑了一轮无意义的循环。

**建议：`filteredEntries` 只保留 `searchQuery` 的过滤，category 和 status 完全交给 API。**

---

## 关于搜索的一个局限

目前搜索只作用在**已加载的 12 条（或更多）** 数据上。

当用户：
1. 页面加载 → 看到 12 条
2. 输入「命运石」→ 只在当前 12 条里搜

如果这 12 条里没有「命运石之门」，用户就搜不到——即使数据库里有。这是个设计取舍。

**几种解法：**

| 方案 | 优缺点 |
|------|--------|
| 保持现状（前端搜） | 简单，但搜不全，需要大量 load more 才能覆盖 |
| 搜索时调后端 API | 能搜全，但要多一次请求，交互有延迟 |
| 搜索时调后端 + 重置分页 | 更好——搜索本质上是「换了一批数据」|

现在前端搜索的写法——如果以后想改成调后端，只需要把 `searchQuery` 也加到 `watch` 里调 API 就行了，`filteredEntries` 保持不动。

---

## 其他小细节

**1. Watcher 的问题**
```ts
watch([selectedCategory, selectedStatus], () => {
    dexStore.getDexs({ ... , limit: 12 })
})
```
每次切换分类，**重置回 12 条**。这没问题，是预期的（换分类应该重新加载）。但是切换分类的时候**不清空搜索词**？如果用户在搜「命运石」然后点了「电影」分类，搜索结果就变成电影分类里搜命运石——但只在 12 条里搜，用户可能会困惑。

如果想让切换分类时重置搜索，可以考虑加个 `searchQuery.value = ''` 或者把搜索词传给 API。

**2. 被注释掉的 `getRatingStars`**
留着也没关系，但如果不打算用就删掉吧～留着会让人以为后面还有逻辑没写完。

**3. Load more 按钮的条件**
```
v-if="!searchQuery && dexStore.hasMore && dexStore.dexs.length > 0"
```
搜索时隐藏加载更多——这个决策是对的，因为搜索现在是前端行为，加载更多出来后前端搜不到（除非加载更多时也传搜索词）。

---

## 前后端分界总结（针对这个页面）

| 功能 | 当前位置 | 评价 |
|------|----------|------|
| 分类筛选 | 后端 | ✅ 正确，数据可能很多 |
| 状态筛选 | 后端 | ✅ 正确 |
| 关键词搜索 | 前端 | ⚠️ 当前够用，但以后可以考虑后端搜索 |
| 分类/状态前端二次过滤 | 前端 | ❌ 冗余，建议去掉 |
| 加载更多 | 后端 | ✅ 正确 |
| grid/list 切换 | 前端 | ✅ 纯 UI |
| 统计数据 | 后端 | ✅ 正确 |

这个页面的整体方向是没问题的，就是 `filteredEntries` 里那两段过滤是多余代码～清理掉的话逻辑更清晰，以后加功能也不容易搞混 😊