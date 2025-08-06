#!/usr/bin/env python3
"""
Fix bare directory links (like /cloud/ and /db/).
"""

import os
import re
from pathlib import Path

def fix_bare_links_in_file(file_path):
    """Fix bare directory links in a single markdown file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"  ✗ Error reading {file_path}: {e}")
        return 0
    
    original_content = content
    replacements = 0
    
    # Fix patterns like [text](/cloud/) -> remove the link entirely or point to index
    # Pattern: [text](/cloud/) or [text](/db/)
    bare_link_pattern = r'\[([^\]]+)\]\(/(cloud|db)/\)'
    
    matches = re.findall(bare_link_pattern, content)
    for match in matches:
        old_pattern = f"[{match[0]}](/{match[1]}/)"
        # Just remove the link markup, keep the text
        new_pattern = match[0]
        content = content.replace(old_pattern, new_pattern)
        replacements += 1
        print(f"  Fixed bare link: [{match[0]}](/{match[1]}/) → {match[0]}")
    
    # Fix specific incorrect links
    specific_fixes = {
        '/admin/replication-plan/': 'https://pigsty.io/docs/administration/backup/',
        '/docs/reference/compatibility': 'https://pigsty.io/docs/reference/compatibility',
        '/docs/setup/prepare/': 'https://pigsty.io/docs/setup/prepare/',
        '/docs/setup/provision/': 'https://pigsty.io/docs/setup/provision/',
        '/docs/setup/install': 'https://pigsty.io/docs/setup/install',
        '/docs/concept/arch/#singleton-meta': 'https://pigsty.io/docs/concept/arch/#singleton-meta',
        '/docs/infra#infrayml': 'https://pigsty.io/docs/infra#infrayml',
        '/fzb': 'https://vonng.com/fzb',
        '/cn/blog/misc/理解互联网/': 'https://vonng.com/cn/blog/misc/understand-internet/',
    }
    
    for old_link, new_link in specific_fixes.items():
        if old_link in content:
            content = content.replace(old_link, new_link)
            replacements += content.count(old_link)
            print(f"  Fixed: {old_link} → {new_link}")
    
    # Save if changes were made
    if content != original_content:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Fixed {replacements} bare links in {file_path}")
            return replacements
        except Exception as e:
            print(f"  ✗ Error writing {file_path}: {e}")
            return 0
    
    return 0

def main():
    """Main function to fix all bare links."""
    print("Fixing bare directory links in markdown files...")
    print("=" * 60)
    
    total_files = 0
    total_fixes = 0
    
    # Find all markdown files
    for md_file in Path('content').rglob('*.md'):
        if md_file.name.startswith('_'):
            continue
            
        fixes = fix_bare_links_in_file(md_file)
        if fixes > 0:
            total_files += 1
            total_fixes += fixes
    
    print("=" * 60)
    print(f"Summary: Fixed {total_fixes} bare links in {total_files} files")

if __name__ == "__main__":
    main()