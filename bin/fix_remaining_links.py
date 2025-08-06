#!/usr/bin/env python3
"""
Fix remaining broken link patterns.
"""

import os
import re
from pathlib import Path

# Additional link replacements for remaining issues
ADDITIONAL_REPLACEMENTS = {
    # Fix /cloud/cloud/flare pattern
    '/cloud/cloud/flare': '/cloud/cloudflare',
    
    # Fix specific pages that might have been renamed
    '/cloud/drop-rds/': '/cloud/drop-rds/',
    '/cloud/cheap-ecs/': '/cloud/ecs/',
    '/cloud/wordpress-drama/': '/cloud/wordpress-drama/',
    '/cloud/kubesphere-rugpull/': '/cloud/kubesphere-rugpull/',
    '/cloud/luo-live': '/cloud/aliyun/',
    
    # Fix legacy URLs
    '/db/pg-in-docker/': '/db/docker-db/',
    
    # Add missing trailing slashes
    '/cloud/odyssey': '/cloud/odyssey/',
    '/cloud/bonus': '/cloud/bonus/',
    '/cloud/profit': '/cloud/profit/',
    '/cloud/sla': '/cloud/sla/',
    '/cloud/aliyun': '/cloud/aliyun/',
    '/cloud/exit': '/cloud/exit/',
    '/cloud/paradigm': '/cloud/paradigm/',
    '/cloud/cdn': '/cloud/cdn/',
}

def fix_links_in_file(file_path):
    """Fix links in a single markdown file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"  ✗ Error reading {file_path}: {e}")
        return 0
    
    original_content = content
    replacements = 0
    
    # Apply direct replacements
    for old_link, new_link in ADDITIONAL_REPLACEMENTS.items():
        # Check both with and without trailing slash
        for variant in [old_link, old_link + '/', old_link.rstrip('/')]:
            count = content.count(variant)
            if count > 0:
                # Only replace if the new link is different
                if variant != new_link:
                    content = content.replace(variant, new_link)
                    replacements += count
                    print(f"  Replaced {count} instances of '{variant}' with '{new_link}'")
    
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
    """Main function to fix remaining links."""
    print("Fixing remaining link issues in markdown files...")
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