#!/usr/bin/env python3
"""检查 Hugo 博客中的站内死链接 - 仅检查本站内容"""

import os
import re
from pathlib import Path
from collections import defaultdict

CONTENT_DIR = Path("content")

# 外部站点路径前缀（不检查）
EXTERNAL_PREFIXES = (
    '/docs/',      # pigsty.io 文档
    '/zh/docs/',   # pigsty.io 中文文档
    '/en/docs/',   # pigsty.io 英文文档
)

def get_all_content_files():
    """获取所有 markdown 文件"""
    files = set()
    for md_file in CONTENT_DIR.rglob("*.md"):
        rel_path = md_file.relative_to(CONTENT_DIR)
        files.add(str(rel_path))
        # 添加各种可能的 URL 形式
        parts = str(rel_path).replace('.md', '').replace('/index', '').replace('/_index', '')
        files.add(parts)
        files.add(parts + '/')
    return files

def get_all_paths():
    """获取所有可能的 URL 路径"""
    paths = set()
    for md_file in CONTENT_DIR.rglob("*.md"):
        rel = md_file.relative_to(CONTENT_DIR)
        # 去掉 .md 后缀
        p = str(rel).replace('.md', '')
        # 去掉 index 和 _index
        p = p.replace('/index.en', '').replace('/index.zh', '').replace('/index', '')
        p = p.replace('/_index.en', '').replace('/_index.zh', '').replace('/_index', '')
        p = p.rstrip('/')

        # 添加各种形式
        paths.add(p)
        paths.add('/' + p)
        paths.add('/' + p + '/')
        paths.add('/en/' + p)
        paths.add('/en/' + p + '/')
        paths.add('/zh/' + p)
        paths.add('/zh/' + p + '/')

        # 带 blog 前缀的形式
        paths.add('/blog/' + p)
        paths.add('/blog/' + p + '/')
        paths.add('/en/blog/' + p)
        paths.add('/en/blog/' + p + '/')
        paths.add('/zh/blog/' + p)
        paths.add('/zh/blog/' + p + '/')

    return paths

def extract_internal_links(file_path):
    """从 markdown 文件中提取站内链接"""
    links = []
    try:
        content = file_path.read_text(encoding='utf-8')
    except:
        return links

    # Markdown 链接: [text](url)
    md_links = re.findall(r'\[([^\]]*)\]\(([^)]+)\)', content)
    for text, url in md_links:
        # 跳过外部链接
        if url.startswith(('http://', 'https://', 'mailto:', '#', 'tel:', 'ftp://', 'git://', 'data:')):
            continue
        # 跳过图片文件
        if url.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.ico', '.pdf')):
            continue
        # 跳过外部文档站点
        if any(url.startswith(prefix) for prefix in EXTERNAL_PREFIXES):
            continue
        # 跳过 Hugo shortcode 模板
        if '{{' in url:
            continue
        links.append((url, text))

    return links

def check_link_exists(link, all_paths):
    """检查链接目标是否存在"""
    # 移除锚点和查询参数
    clean_link = link.split('#')[0].split('?')[0].rstrip('/')
    if not clean_link:
        return True

    # 检查路径是否存在
    if clean_link in all_paths or clean_link + '/' in all_paths:
        return True

    # 尝试不带 /en/ 或 /zh/ 前缀
    for prefix in ['/en/', '/zh/', '/en/blog/', '/zh/blog/', '/blog/']:
        if clean_link.startswith(prefix):
            stripped = clean_link[len(prefix)-1:]  # 保留开头的 /
            if stripped in all_paths or stripped + '/' in all_paths:
                return True

    return False

def main():
    all_paths = get_all_paths()
    broken_links = defaultdict(list)

    for md_file in CONTENT_DIR.rglob("*.md"):
        links = extract_internal_links(md_file)
        for link, text in links:
            if not check_link_exists(link, all_paths):
                rel_path = str(md_file.relative_to(CONTENT_DIR))
                broken_links[rel_path].append((link, text))

    if broken_links:
        print("=== 站内死链接 ===\n")
        total = 0
        for source, links in sorted(broken_links.items()):
            print(f"{source}:")
            for link, text in links:
                short_text = (text[:25] + '..') if len(text) > 25 else text
                print(f"  → {link}")
                total += 1
            print()
        print(f"共 {len(broken_links)} 个文件, {total} 个死链接")
    else:
        print("未发现死链接")

if __name__ == "__main__":
    main()
