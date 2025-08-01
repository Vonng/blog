#!/usr/bin/env python3
"""
Hugo 单页面文章转换为 Page Bundle 脚本

遍历 content/misc 目录下的 *.md 文件（index 和 _index 开头的除外），
创建同名目录，然后将 .md 文件移动到该目录下的 index.md

使用方法：
    python bin/wrap.py
"""

import os
import sys
import shutil
import argparse
from pathlib import Path


def convert_to_page_bundle(misc_dir, auto_confirm=False):
    """将单页面文章转换为 page bundle 格式"""
    misc_path = Path(misc_dir)
    
    if not misc_path.exists():
        print(f"错误：目录 {misc_dir} 不存在")
        return False
    
    # 查找所有需要转换的 .md 文件
    md_files = []
    for file_path in misc_path.glob('*.md'):
        filename = file_path.name
        # 排除 index.md 和 _index.md
        if not filename.startswith('index') and not filename.startswith('_index'):
            md_files.append(file_path)
    
    if not md_files:
        print("没有找到需要转换的 .md 文件")
        return True
    
    print(f"找到 {len(md_files)} 个文件需要转换：")
    for file_path in md_files:
        print(f"  - {file_path.name}")
    
    # 确认是否继续
    if not auto_confirm:
        try:
            response = input("\n是否继续转换？(y/N): ").strip().lower()
            if response not in ['y', 'yes']:
                print("取消转换")
                return False
        except (EOFError, KeyboardInterrupt):
            print("\n取消转换")
            return False
    else:
        print("\n自动确认转换...")
    
    # 执行转换
    success_count = 0
    for file_path in md_files:
        try:
            # 获取文件名（不含扩展名）
            stem = file_path.stem
            
            # 创建同名目录
            bundle_dir = misc_path / stem
            if bundle_dir.exists():
                print(f"警告：目录 {stem}/ 已存在，跳过 {file_path.name}")
                continue
            
            bundle_dir.mkdir()
            print(f"创建目录：{stem}/")
            
            # 移动文件到目录中的 index.md
            target_file = bundle_dir / 'index.md'
            shutil.move(str(file_path), str(target_file))
            print(f"移动：{file_path.name} -> {stem}/index.md")
            
            success_count += 1
            
        except Exception as e:
            print(f"转换 {file_path.name} 时出错：{e}")
    
    print(f"\n转换完成！成功转换了 {success_count} 个文件")
    return True


def show_conversion_preview(misc_dir):
    """显示转换预览，不执行实际转换"""
    misc_path = Path(misc_dir)
    
    if not misc_path.exists():
        print(f"错误：目录 {misc_dir} 不存在")
        return False
    
    # 查找所有需要转换的 .md 文件
    md_files = []
    for file_path in misc_path.glob('*.md'):
        filename = file_path.name
        # 排除 index.md 和 _index.md
        if not filename.startswith('index') and not filename.startswith('_index'):
            md_files.append(file_path)
    
    if not md_files:
        print("没有找到需要转换的 .md 文件")
        return True
    
    print(f"找到 {len(md_files)} 个文件需要转换：")
    print()
    for file_path in md_files:
        stem = file_path.stem
        print(f"  {file_path.name} -> {stem}/index.md")
    
    print(f"\n预览完成！共 {len(md_files)} 个文件需要转换")
    print("使用 --auto 参数可以直接执行转换")
    return True


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="Hugo 单页面文章转换为 Page Bundle 脚本"
    )
    parser.add_argument(
        '--auto', 
        action='store_true', 
        help='自动确认转换，不进行交互提示'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='仅显示将要转换的文件，不执行实际转换'
    )
    
    args = parser.parse_args()
    
    # 获取脚本所在目录的父目录（项目根目录）
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    misc_dir = project_root / 'content' / 'misc'
    
    print("Hugo 单页面文章转换为 Page Bundle 脚本")
    print(f"目标目录：{misc_dir}")
    print("-" * 50)
    
    if args.dry_run:
        success = show_conversion_preview(misc_dir)
    else:
        success = convert_to_page_bundle(misc_dir, args.auto)
    
    if success:
        if not args.dry_run:
            print("\n转换完成！")
            print("提示：转换后你可能需要运行 'hugo server' 来验证结果")
    else:
        print("\n转换失败！")
        sys.exit(1)


if __name__ == '__main__':
    main()