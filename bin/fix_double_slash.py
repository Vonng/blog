#!/usr/bin/env python3
"""
Fix double slash issues in markdown links.
"""

import os
import re
from pathlib import Path

def fix_double_slashes_in_file(file_path):
    """Fix double slashes in links in a single markdown file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"  ✗ Error reading {file_path}: {e}")
        return 0
    
    original_content = content
    replacements = 0
    
    # Pattern to find markdown links with double slashes
    link_pattern = r'\[([^\]]*)\]\((/[^)]+//[^)]+)\)'
    
    # Find all matches
    matches = list(re.finditer(link_pattern, content))
    
    if matches:
        # Replace double slashes with single slashes
        for match in reversed(matches):  # Reverse to maintain positions
            link_text = match.group(1)
            link_url = match.group(2)
            # Replace // with / in the URL (but not in http:// or https://)
            fixed_url = re.sub(r'(?<!:)//', '/', link_url)
            if fixed_url != link_url:
                new_link = f'[{link_text}]({fixed_url})'
                old_link = match.group(0)
                content = content[:match.start()] + new_link + content[match.end():]
                replacements += 1
                print(f"  Fixed: {link_url} → {fixed_url}")
    
    # Save if changes were made
    if content != original_content:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Fixed {replacements} double-slash links in {file_path}")
            return replacements
        except Exception as e:
            print(f"  ✗ Error writing {file_path}: {e}")
            return 0
    
    return 0

def main():
    """Main function to fix all double slash links."""
    print("Fixing double slash issues in markdown files...")
    print("=" * 60)
    
    total_files = 0
    total_fixes = 0
    
    # Find all markdown files
    for md_file in Path('content').rglob('*.md'):
        if md_file.name.startswith('_'):
            continue
            
        fixes = fix_double_slashes_in_file(md_file)
        if fixes > 0:
            total_files += 1
            total_fixes += fixes
    
    print("=" * 60)
    print(f"Summary: Fixed {total_fixes} double-slash links in {total_files} files")

if __name__ == "__main__":
    main()