#!/usr/bin/env python3
"""
Hugo Hero 图片转换为 Featured 图片脚本

遍历 content/misc 目录下的文章（目录/index.md），如果 YAML FRONT MATTER 中存在 hero 字段，
比如 /hero/statistic.jpg，而且不存在 featured 图片文件（任何名为 featured 开头的图片），
那么就从 hero/ 中将对应的图片复制到文章目录下，命名为 featured + 图片原本的后缀。

使用方法：
    python bin/hero.py [--dry-run] [--auto]
"""

import os
import sys
import shutil
import argparse
import re
from pathlib import Path


def parse_yaml_frontmatter(content):
    """解析 YAML front matter"""
    # 查找 YAML front matter（以 --- 开始和结束）
    pattern = r'^---\s*\n(.*?)\n---\s*\n'
    match = re.match(pattern, content, re.DOTALL)
    
    if not match:
        return {}
    
    yaml_content = match.group(1)
    result = {}
    
    # 简单解析 YAML（只处理简单的 key: value 格式）
    for line in yaml_content.split('\n'):
        line = line.strip()
        if ':' in line and not line.startswith('#'):
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip().strip('"\'')
            result[key] = value
    
    return result


def has_featured_image(article_dir):
    """检查文章目录是否已有 featured 图片"""
    article_path = Path(article_dir)
    
    # 检查是否存在以 featured 开头的图片文件
    image_extensions = ['.jpg', '.jpeg', '.jpe', '.png', '.webp', '.gif', '.svg']
    
    for file_path in article_path.iterdir():
        if file_path.is_file():
            filename = file_path.name.lower()
            if filename.startswith('featured'):
                # 检查是否为图片文件
                for ext in image_extensions:
                    if filename.endswith(ext):
                        return True, file_path
    
    return False, None


def process_article(article_dir, hero_dir, dry_run=False):
    """处理单个文章目录"""
    article_path = Path(article_dir)
    index_file = article_path / 'index.md'
    
    if not index_file.exists():
        return False, f"index.md 不存在于 {article_dir}"
    
    # 读取文章内容
    try:
        with open(index_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return False, f"读取 {index_file} 失败: {e}"
    
    # 解析 YAML front matter
    frontmatter = parse_yaml_frontmatter(content)
    
    # 检查是否有 hero 字段
    hero_field = frontmatter.get('hero')
    if not hero_field:
        return False, "没有 hero 字段"
    
    # 检查是否已有 featured 图片
    has_featured, existing_featured = has_featured_image(article_dir)
    if has_featured:
        return False, f"已存在 featured 图片: {existing_featured.name}"
    
    # 解析 hero 路径（例如：/hero/statistic.jpg）
    if not hero_field.startswith('/hero/'):
        return False, f"hero 字段格式不正确: {hero_field}"
    
    hero_filename = hero_field[6:]  # 去掉 '/hero/' 前缀
    hero_source = Path(hero_dir) / hero_filename
    
    if not hero_source.exists():
        return False, f"hero 图片不存在: {hero_source}"
    
    # 获取文件扩展名
    extension = hero_source.suffix
    featured_filename = f"featured{extension}"
    featured_target = article_path / featured_filename
    
    if dry_run:
        return True, f"[DRY-RUN] 将复制 {hero_source} -> {featured_target}"
    
    # 复制文件
    try:
        shutil.copy2(hero_source, featured_target)
        return True, f"成功复制 {hero_filename} -> {featured_filename}"
    except Exception as e:
        return False, f"复制失败: {e}"


def process_all_articles(misc_dir, hero_dir, dry_run=False):
    """处理所有文章"""
    misc_path = Path(misc_dir)
    
    if not misc_path.exists():
        print(f"错误：目录 {misc_dir} 不存在")
        return False
    
    if not Path(hero_dir).exists():
        print(f"错误：hero 目录 {hero_dir} 不存在")
        return False
    
    # 查找所有文章目录（包含 index.md 的目录）
    article_dirs = []
    for item in misc_path.iterdir():
        if item.is_dir() and not item.name.startswith('.'):
            index_file = item / 'index.md'
            if index_file.exists():
                article_dirs.append(item)
    
    if not article_dirs:
        print("没有找到包含 index.md 的文章目录")
        return True
    
    print(f"找到 {len(article_dirs)} 个文章目录")
    print("-" * 60)
    
    success_count = 0
    total_processed = 0
    
    for article_dir in sorted(article_dirs):
        article_name = article_dir.name
        success, message = process_article(article_dir, hero_dir, dry_run)
        
        if success:
            print(f"✓ {article_name}: {message}")
            success_count += 1
            total_processed += 1
        else:
            print(f"- {article_name}: {message}")
            total_processed += 1
    
    print("-" * 60)
    if dry_run:
        print(f"预览完成！共 {success_count} 个文章需要处理（共检查了 {total_processed} 个文章）")
    else:
        print(f"处理完成！成功处理了 {success_count} 个文章（共检查了 {total_processed} 个文章）")
    
    return True


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="Hugo Hero 图片转换为 Featured 图片脚本"
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='仅显示将要处理的文章，不执行实际复制'
    )
    parser.add_argument(
        '--auto',
        action='store_true',
        help='自动执行，不进行交互确认'
    )
    
    args = parser.parse_args()
    
    # 获取脚本所在目录的父目录（项目根目录）
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    misc_dir = project_root / 'content' / 'misc'
    hero_dir = project_root / 'hero'
    
    print("Hugo Hero 图片转换为 Featured 图片脚本")
    print(f"文章目录：{misc_dir}")
    print(f"Hero 目录：{hero_dir}")
    print("=" * 60)
    
    if not args.dry_run and not args.auto:
        try:
            response = input("是否继续处理？(y/N): ").strip().lower()
            if response not in ['y', 'yes']:
                print("取消处理")
                return
        except (EOFError, KeyboardInterrupt):
            print("\n取消处理")
            return
    
    success = process_all_articles(misc_dir, hero_dir, args.dry_run)
    
    if not success:
        sys.exit(1)


if __name__ == '__main__':
    main()