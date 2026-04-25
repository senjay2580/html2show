#!/usr/bin/env node
/**
 * 自动扫描 pages/ 目录, 生成 manifest.json
 * - 提取 <title> / <h1> / .sub 作为 name/desc
 * - 提取 .eyebrow 作为分类标签
 * - 子目录会被识别为 folder 节点
 *
 * 触发: GitHub Actions push 时自动跑
 * 本地: node scripts/build-manifest.js
 */

const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const PAGES_DIR = path.join(ROOT, 'pages');
const MANIFEST_PATH = path.join(ROOT, 'manifest.json');

// 现有 manifest.json: 用作元数据增强 (color/icon/tags 优先用现有的)
let existing = {};
try {
  existing = JSON.parse(fs.readFileSync(MANIFEST_PATH, 'utf-8'));
} catch {}

function findExistingByPath(node, path) {
  if (!node) return null;
  if (node.path === path) return node;
  for (const c of node.children || []) {
    const r = findExistingByPath(c, path);
    if (r) return r;
  }
  return null;
}

function extract(html) {
  const titleM = html.match(/<title>([^<]+)<\/title>/i);
  const h1M = html.match(/<h1[^>]*>([\s\S]*?)<\/h1>/i);
  const subM = html.match(/class="sub"[^>]*>([^<]+)</i);
  const eyebrowM = html.match(/class="eyebrow"[^>]*>([^<]+)</i);

  const stripTags = s => (s || '').replace(/<[^>]+>/g, '').trim();
  return {
    title: stripTags(titleM ? titleM[1] : ''),
    h1: stripTags(h1M ? h1M[1] : ''),
    sub: stripTags(subM ? subM[1] : ''),
    eyebrow: stripTags(eyebrowM ? eyebrowM[1] : '')
  };
}

function readPage(filePath, relPath) {
  let meta = { title: '', h1: '', sub: '', eyebrow: '' };
  try {
    meta = extract(fs.readFileSync(filePath, 'utf-8'));
  } catch (e) {
    console.warn('⚠️  读取失败:', filePath);
  }
  const stat = fs.statSync(filePath);
  const fileName = path.basename(filePath, '.html');
  const cleanTitle = (meta.title || '').split('·')[0].trim();

  // 找已有节点拿 tags / color 等
  const existingNode = findExistingByPath(existing.tree, relPath);

  return {
    name: meta.h1 || cleanTitle || fileName,
    type: 'page',
    path: relPath,
    icon: existingNode?.icon || 'file-text',
    desc: meta.sub || cleanTitle || '',
    tags: existingNode?.tags || (meta.eyebrow ? [meta.eyebrow.split('·')[0].trim()] : []),
    color: existingNode?.color,
    updated: stat.mtime.toISOString().slice(0, 10)
  };
}

function scanDir(dir, virtualPath) {
  if (!fs.existsSync(dir)) return [];
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  const items = [];

  // 子目录
  entries
    .filter(e => e.isDirectory() && !e.name.startsWith('.') && !e.name.startsWith('_'))
    .sort((a, b) => a.name.localeCompare(b.name))
    .forEach(entry => {
      const sub = '/' + entry.name;
      const full = path.join(dir, entry.name);
      const children = scanDir(full, virtualPath + sub);
      const existingFolder = findExistingByPath(existing.tree, virtualPath + sub);
      items.push({
        name: existingFolder?.name || entry.name,
        type: 'folder',
        path: virtualPath + sub,
        icon: existingFolder?.icon || 'folder',
        color: existingFolder?.color,
        desc: existingFolder?.desc || '',
        children
      });
    });

  // .html 文件
  entries
    .filter(e => e.isFile() && e.name.endsWith('.html'))
    .sort((a, b) => a.name.localeCompare(b.name))
    .forEach(entry => {
      const full = path.join(dir, entry.name);
      // 公开 URL 路径 (相对于仓库根, 浏览器能访问)
      const urlPath =
        path.relative(ROOT, full).replace(/\\/g, '/');
      items.push(readPage(full, urlPath));
    });

  return items;
}

const tree = {
  name: '全部',
  type: 'folder',
  path: '/',
  icon: 'library',
  children: scanDir(PAGES_DIR, '')
};

// 把已有的根级元数据继承下来 (比如手写的 description)
const manifest = {
  name: existing.name || 'html2show',
  version: existing.version || '1.0.0',
  description: existing.description || 'Apple/Karpathy 风教学 HTML 知识图集合',
  generated: new Date().toISOString(),
  tree
};

fs.writeFileSync(MANIFEST_PATH, JSON.stringify(manifest, null, 2) + '\n');

const totalPages = (function count(n) {
  if (n.type === 'page') return 1;
  return (n.children || []).reduce((s, c) => s + count(c), 0);
})(tree);

console.log(`✓ manifest.json 已生成`);
console.log(`  · 顶层 ${tree.children.length} 项`);
console.log(`  · 总页面 ${totalPages}`);
