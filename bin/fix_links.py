#!/usr/bin/env python3
"""
Fix common dead links in Hugo blog markdown files.

This script will fix known patterns of dead links.
"""

import os
import re
from pathlib import Path
from collections import defaultdict

# Define link replacements
LINK_REPLACEMENTS = {
    # Fix /cloud/cloud-exit/ -> /cloud/exit/
    '/cloud/cloud-exit/': '/cloud/exit/',
    
    # Fix /blog/ prefixes (should be removed)
    '/blog/cloud/': '/cloud/',
    '/blog/db/': '/db/',
    '/blog/pg/': '/pg/',
    
    # Fix specific broken links
    '/cloud/aliyun-ecs-pigsty/': '/cloud/cheap-ecs/',
    '/db/k8s': '/db/db-in-k8s/',
    '/zh/docs/': 'https://pigsty.io/zh/docs/',  # External Pigsty docs
    '/en/docs/': 'https://pigsty.io/docs/',     # External Pigsty docs
    
    # Fix image paths that should be absolute
    '](/img/blog/hero/': '](/',
    '](/img/blog/cloud/': '](/cloud/',
    '](/img/blog/db/': '](/db/',
    '](/img/blog/pg/': '](/pg/',
    '/img/pigsty/': 'https://pigsty.io/img/',
    
    # Fix non-existent pages
    '/cloud/hardware-bonus': '/cloud/bonus/',
    '/db/pg-is-best/': '/pg/pg-is-best/',
}

def fix_links_in_file(file_path):
    """Fix links in a single file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return 0
        
    original_content = content
    changes = 0
    
    # Apply replacements
    for old_link, new_link in LINK_REPLACEMENTS.items():
        if old_link in content:
            count = content.count(old_link)
            content = content.replace(old_link, new_link)
            changes += count
            print(f"  Replaced {count} instances of '{old_link}' with '{new_link}'")
    
    # Write back if changed
    if content != original_content:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Fixed {changes} links in {file_path}")
        except Exception as e:
            print(f"Error writing {file_path}: {e}")
            return 0
            
    return changes

def main():
    """Fix links in all markdown files."""
    content_dir = Path("content")
    total_changes = 0
    files_changed = 0
    
    print("Fixing dead links in markdown files...")
    print("=" * 60)
    
    for md_file in content_dir.rglob("*.md"):
        if md_file.name.startswith("_"):
            continue
            
        changes = fix_links_in_file(md_file)
        if changes > 0:
            total_changes += changes
            files_changed += 1
            
    print("=" * 60)
    print(f"Summary: Fixed {total_changes} links in {files_changed} files")

if __name__ == "__main__":
    main()