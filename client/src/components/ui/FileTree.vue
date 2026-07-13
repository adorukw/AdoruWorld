<script setup lang="ts">
import { ref } from 'vue'
import type { NoteTreeNode } from '@/api/notes'

const props = defineProps<{
  nodes: NoteTreeNode[]
  activePath: string | null
  level?: number
}>()

const emit = defineEmits<{
  select: [path: string]
}>()

// 记录每个目录的展开/折叠状态（用路径做 key）
const expandedDirs = ref<Set<string>>(new Set())

// 默认展开第一层目录
const defaultExpanded = new Set<string>()
if (props.nodes.length > 0) {
  for (const node of props.nodes) {
    if (node.type === 'dir') {
      defaultExpanded.add(node.path)
    }
  }
}
// 只在首次加载时设置默认展开
if (expandedDirs.value.size === 0 && props.level === 0) {
  expandedDirs.value = defaultExpanded
}

function toggleDir(path: string) {
  if (expandedDirs.value.has(path)) {
    expandedDirs.value.delete(path)
  } else {
    expandedDirs.value.add(path)
  }
  // 触发响应式更新
  expandedDirs.value = new Set(expandedDirs.value)
}

function handleSelect(node: NoteTreeNode) {
  if (node.type === 'file') {
    emit('select', node.filePath || node.path)
  } else {
    toggleDir(node.path)
  }
}

function getIcon(node: NoteTreeNode): string {
  if (node.type === 'dir') {
    return expandedDirs.value.has(node.path) ? '📂' : '📁'
  }
  // 根据文件名推断图标
  const name = node.name.toLowerCase()
  if (name.startsWith('readme')) return '📖'
  if (name.includes('教程') || name.includes('指南') || name.includes('guide')) return '📗'
  if (name.includes('笔记') || name.includes('note')) return '📝'
  if (name.includes('配置') || name.includes('config')) return '⚙️'
  return '📄'
}
</script>

<template>
  <ul class="file-tree" :style="{ paddingLeft: level && level > 0 ? '16px' : '0' }">
    <li v-for="node in nodes" :key="node.path" class="file-tree-item">
      <!-- 目录节点 -->
      <div
        v-if="node.type === 'dir'"
        class="tree-node dir-node"
        :class="{ 'is-expanded': expandedDirs.has(node.path) }"
        @click="toggleDir(node.path)"
      >
        <span class="toggle-icon">{{ expandedDirs.has(node.path) ? '▼' : '▶' }}</span>
        <span class="node-icon">{{ getIcon(node) }}</span>
        <span class="node-name">{{ node.name }}</span>
        <span class="node-count">{{ node.children.filter(c => c.type === 'file').length }}</span>
      </div>

      <!-- 文件节点 -->
      <div
        v-else
        class="tree-node file-node clickable"
        :class="{ 'is-active': activePath === (node.filePath || node.path) }"
        @click="handleSelect(node)"
      >
        <span class="toggle-icon" style="visibility: hidden;">▶</span>
        <span class="node-icon">{{ getIcon(node) }}</span>
        <span class="node-name">{{ node.name.replace(/\.md$/, '') }}</span>
      </div>

      <!-- 递归渲染子目录 -->
      <FileTree
        v-if="node.type === 'dir' && expandedDirs.has(node.path)"
        :nodes="node.children"
        :active-path="activePath"
        :level="(level || 0) + 1"
        @select="(path: string) => emit('select', path)"
      />
    </li>
  </ul>
</template>

<style scoped>
.file-tree {
  list-style: none;
  margin: 0;
  padding: 0;
}

.file-tree-item {
  list-style: none;
}

.tree-node {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 4px 8px;
  border-radius: 6px;
  cursor: default;
  font-size: 14px;
  line-height: 1.6;
  transition: background-color 0.15s ease;
  user-select: none;
}

.tree-node:hover {
  background-color: #f0f0f0;
}

.dir-node {
  font-weight: 600;
  color: #333;
}

.dir-node.is-expanded {
  color: #000;
}

.file-node {
  color: #555;
}

.file-node.clickable {
  cursor: pointer;
}

.file-node.is-active {
  background-color: #e0f2fe;
  color: #0369a1;
  font-weight: 600;
  border: 1px solid #7dd3fc;
}

.file-node.is-active:hover {
  background-color: #dbeafe;
}

.toggle-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 16px;
  height: 16px;
  font-size: 10px;
  color: #999;
  flex-shrink: 0;
}

.node-icon {
  font-size: 16px;
  flex-shrink: 0;
}

.node-name {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  flex: 1;
}

.node-count {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 18px;
  height: 18px;
  padding: 0 4px;
  font-size: 11px;
  font-weight: 700;
  background: #e5e7eb;
  border-radius: 999px;
  color: #666;
  flex-shrink: 0;
}
</style>
