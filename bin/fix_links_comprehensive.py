#!/usr/bin/env python3
"""
Comprehensive link fixer for Hugo blog markdown files.
"""

import os
import re
from pathlib import Path
from collections import defaultdict

# Extended comprehensive link replacements
LINK_REPLACEMENTS = {
    # External documentation links
    '/zh/docs/': 'https://pigsty.io/zh/docs/',
    '/en/docs/': 'https://pigsty.io/docs/',
    
    # Fix blog prefix issues
    '/blog/cloud/': '/cloud/',
    '/blog/db/': '/db/', 
    '/blog/pg/': '/pg/',
    
    # Specific page mappings
    '/cloud/aliyun-ecs-pigsty/': '/cloud/cheap-ecs/',
    '/cloud/cloud-exit/': '/cloud/exit/',
    '/db/k8s': '/db/db-in-k8s/',
    
    # Fix image paths to external site
    '/img/pigsty/': 'https://pigsty.io/img/',
    
    # Common broken internal links
    '/cloud/ecs#pig-slaughtering-scam-pricing': '/cloud/ebs/#pig-slaughtering-scam-pricing',
    '/cloud/ecs#杀猪盘的价格': '/cloud/ebs/#杀猪盘的价格',
    '/cloud/ecs/#impact-of-instance-families-on-pricing': '/cloud/ecs/#实例族对价格的影响',
    '/cloud/ecs/#实例族对价格的影响': '/cloud/ecs/#实例族对价格的影响',
    
    # Common broken links to odyssey sections
    '/cloud/odyssey#02-22-five-values-guiding-cloud-exit': '/cloud/odyssey/#02-22-指导下云的五条价值观',
    '/cloud/odyssey#02-22-指导下云的五条价值观': '/cloud/odyssey/#02-22-指导下云的五条价值观',
    
    # DBA vs RDS section fixes
    '/cloud/dba-vs-rds#dba-work-and-automated-management': '/cloud/dba-vs-rds/#dba的工作与自动化管控',
    '/cloud/dba-vs-rds#dba的工作与自动化管控': '/cloud/dba-vs-rds/#dba的工作与自动化管控',
    '/cloud/dba-vs-rds#云数据库的模式与新挑战': '/cloud/dba-vs-rds/#云数据库的模式与新挑战',
    
    # Other common fixes
    '/pg/pg-performance': '/pg/pg-performence/',
    '/dev/llm-and-pgvector/': '/pg/llm-and-pgvector/',
    '/dev/llm-and-pgvector': '/pg/llm-and-pgvector/',
    '/db/oracle-killed-mysql': '/db/mysql-is-dead/',
    
    # GPL links
    '/db/goodbye-gpl#促进软件自由的法律工具': '/db/goodbye-gpl/#促进软件自由的法律工具',
    
    # SLA section links
    '/cloud/sla.md#disappearing-reliability': '/cloud/sla/#消失的可靠性',
    '/cloud/sla.md#消失的可靠性': '/cloud/sla/#消失的可靠性',
    
    # Remove trailing /cloud links
    '/cloud': '/cloud/',
}

# Additional patterns for regex-based replacements
REGEX_PATTERNS = [
    # Fix internal image paths that should be relative
    (r'!\[([^\]]*)\]\(/img/cloud/([^)]+)\)', r'![\1](\2)'),
    (r'!\[([^\]]*)\]\(/img/db/([^)]+)\)', r'![\1](\2)'),
    (r'!\[([^\]]*)\]\(/img/pg/([^)]+)\)', r'![\1](\2)'),
    
    # Fix images in root that should be relative
    (r'!\[([^\]]*)\]\(/([^/][^)]+\.(jpg|jpeg|png|gif|webp|svg))\)', r'![\1](\2)'),
]

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
    for old_link, new_link in LINK_REPLACEMENTS.items():
        count = content.count(old_link)
        if count > 0:
            content = content.replace(old_link, new_link)
            replacements += count
            print(f"  Replaced {count} instances of '{old_link}' with '{new_link}'")
    
    # Apply regex patterns
    for pattern, replacement in REGEX_PATTERNS:
        matches = re.findall(pattern, content)
        if matches:
            content = re.sub(pattern, replacement, content)
            replacements += len(matches)
            print(f"  Fixed {len(matches)} image paths matching pattern")
    
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
    """Main function to fix all links."""
    print("Comprehensive link fixing for markdown files...")
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