#!/usr/bin/env python3
"""
Script to process markdown files in the content directory with 4 passes:
1. Remove files ending with .it.md 
2. Remove files ending with .ja.md
3. Rename files ending with plain .md (without prefixes) to .en.md
4. Rename files ending with zh-cn.md to .md
"""

import os
from pathlib import Path

def process_markdown_files(content_dir):
    """Process all markdown files in the content directory with 4 passes"""
    content_path = Path(content_dir)
    
    if not content_path.exists():
        print(f"Content directory '{content_dir}' does not exist!")
        return
    
    # Pass 1: Remove .it.md files
    print("Pass 1: Removing .it.md files...")
    removed_it_count = 0
    
    for md_file in content_path.rglob("*.it.md"):
        print(f"Removing: {md_file}")
        md_file.unlink()
        removed_it_count += 1
    
    print(f"Removed {removed_it_count} .it.md files.\n")
    
    # Pass 2: Remove .ja.md files
    print("Pass 2: Removing .ja.md files...")
    removed_jp_count = 0
    
    for md_file in content_path.rglob("*.ja.md"):
        print(f"Removing: {md_file}")
        md_file.unlink() 
        removed_jp_count += 1
    
    print(f"Removed {removed_jp_count} .ja.md files.\n")
    
    # Pass 3: Rename plain .md files to .en.md
    print("Pass 3: Renaming plain .md files to .en.md...")
    en_renamed_count = 0
    
    for md_file in content_path.rglob("*.md"):
        # Skip files that already have language suffixes
        if (md_file.name.endswith('.zh.md') or 
            md_file.name.endswith('.en.md') or 
            md_file.name.endswith('.ja.md') or
            md_file.name.endswith('.zh-cn.md')):
            continue
        
        # Only rename files that end with plain .md
        if md_file.name.endswith('.md'):
            new_name = md_file.with_name(md_file.name.replace(".md", ".en.md"))
            print(f"Renaming: {md_file} -> {new_name}")
            md_file.rename(new_name)
            en_renamed_count += 1
    
    print(f"Renamed {en_renamed_count} plain .md files to .en.md.\n")
    
    # Pass 4: Rename zh-cn.md files to .md (after .en.md renaming is done)
    print("Pass 4: Renaming zh-cn.md files to .md...")
    zh_renamed_count = 0
    
    for md_file in content_path.rglob("*.zh-cn.md"):
        new_name = md_file.with_name(md_file.name.replace(".zh-cn.md", ".md"))
        print(f"Renaming: {md_file} -> {new_name}")
        md_file.rename(new_name)
        zh_renamed_count += 1
    
    print(f"Renamed {zh_renamed_count} zh-cn.md files to .md.\n")
    
    print("Processing complete!")
    print(f"Total .it.md files removed: {removed_it_count}")
    print(f"Total .ja.md files removed: {removed_jp_count}")
    print(f"Total .md files renamed to .en.md: {en_renamed_count}")
    print(f"Total zh-cn.md files renamed to .md: {zh_renamed_count}")

if __name__ == "__main__":
    # Process the content directory
    content_directory = "content"
    process_markdown_files(content_directory)