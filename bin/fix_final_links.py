#!/usr/bin/env python3
"""
Final comprehensive link fixes for remaining patterns.
"""

import os
import re
from pathlib import Path

def fix_links_in_file(file_path):
    """Fix remaining link patterns in a single markdown file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"  ✗ Error reading {file_path}: {e}")
        return 0
    
    original_content = content
    replacements = 0
    
    # Fix double slashes at end of links
    double_slash_pattern = r'\[([^\]]+)\]\((/[^)]+)//\)'
    matches = re.findall(double_slash_pattern, content)
    for match in matches:
        old_link = f"[{match[0]}]({match[1]}//)"
        new_link = f"[{match[0]}]({match[1]}/)"
        content = content.replace(old_link, new_link)
        replacements += 1
        print(f"  Fixed: {match[1]}// → {match[1]}/")
    
    # Fix bare /cloud/ link
    bare_cloud_pattern = r'\[([^\]]+)\]\(/cloud/\)'
    if re.search(bare_cloud_pattern, content):
        content = re.sub(bare_cloud_pattern, r'[\1](/cloud/)', content)
        replacements += re.findall(bare_cloud_pattern, original_content).__len__()
        print(f"  Fixed bare /cloud/ links")
    
    # Fix missing pages
    missing_links = {
        '/cloud/cdn//': '/cloud/',
        '/cloud/paradigm//': '/cloud/',
        '/cloud/drop-rds//': '/cloud/rds-failure/',
        '/cloud/dba-vs-rds/': '/cloud/rds/',
        '/db/docker-db/': '/db/',
    }
    
    for old_link, new_link in missing_links.items():
        if old_link in content:
            content = content.replace(old_link, new_link)
            replacements += content.count(old_link)
            print(f"  Fixed: {old_link} → {new_link}")
    
    # Save if changes were made
    if content != original_content:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Fixed {replacements} links in {file_path}")
            return replacements
        except Exception as e:
            print(f"  ✗ Error writing {file_path}: {e}")
            return 0
    
    return 0

def main():
    """Main function to fix all remaining link issues."""
    print("Fixing final link issues in markdown files...")
    print("=" * 60)
    
    total_files = 0
    total_fixes = 0
    
    # Find all markdown files
    for md_file in Path('content').rglob('*.md'):
        if md_file.name.startswith('_'):
            continue
            
        fixes = fix_links_in_file(md_file)
        if fixes > 0:
            total_files += 1
            total_fixes += fixes
    
    print("=" * 60)
    print(f"Summary: Fixed {total_fixes} links in {total_files} files")

if __name__ == "__main__":
    main()