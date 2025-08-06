#!/usr/bin/env python3
"""
Fix triple slash issues in markdown links.
"""

import os
import re
from pathlib import Path

def fix_triple_slashes_in_file(file_path):
    """Fix triple slashes in links in a single markdown file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"  ✗ Error reading {file_path}: {e}")
        return 0
    
    original_content = content
    replacements = 0
    
    # Replace triple slashes with single slash
    pattern = r'///+'
    matches = re.findall(pattern, content)
    if matches:
        content = re.sub(pattern, '/', content)
        replacements = len(matches)
        print(f"  Fixed {replacements} triple-slash issues")
    
    # Save if changes were made
    if content != original_content:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Fixed {replacements} triple-slash links in {file_path}")
            return replacements
        except Exception as e:
            print(f"  ✗ Error writing {file_path}: {e}")
            return 0
    
    return 0

def main():
    """Main function to fix all triple slash links."""
    print("Fixing triple slash issues in markdown files...")
    print("=" * 60)
    
    total_files = 0
    total_fixes = 0
    
    # Find all markdown files
    for md_file in Path('content').rglob('*.md'):
        if md_file.name.startswith('_'):
            continue
            
        fixes = fix_triple_slashes_in_file(md_file)
        if fixes > 0:
            total_files += 1
            total_fixes += fixes
    
    print("=" * 60)
    print(f"Summary: Fixed {total_fixes} triple-slash links in {total_files} files")

if __name__ == "__main__":
    main()