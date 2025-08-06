#!/usr/bin/env python3
"""
Check all relative links in Hugo blog markdown files for dead links.

Hugo URL mapping rules:
- content/cloud/index.md -> /cloud/
- content/cloud/ebs/index.md -> /cloud/ebs/
- content/cloud/ebs/index.en.md -> /en/cloud/ebs/
"""

import os
import re
import sys
from pathlib import Path
from collections import defaultdict

class LinkChecker:
    def __init__(self, content_dir="content"):
        self.content_dir = Path(content_dir)
        self.errors = []
        self.warnings = []
        self.checked_links = 0
        
        # Build a map of all valid URLs
        self.valid_urls = set()
        self.file_to_url = {}
        self._build_url_map()
        
    def _build_url_map(self):
        """Build a map of all valid URLs from markdown files."""
        for md_file in self.content_dir.rglob("*.md"):
            if md_file.name.startswith("_"):
                continue
                
            # Get relative path from content dir
            rel_path = md_file.relative_to(self.content_dir)
            
            # Determine if it's English version
            is_english = md_file.name.endswith(".en.md")
            
            # Convert to URL
            url = self._file_to_url(rel_path, is_english)
            self.valid_urls.add(url)
            self.file_to_url[str(md_file)] = url
            
            # Also add without trailing slash
            if url.endswith("/"):
                self.valid_urls.add(url[:-1])
            else:
                self.valid_urls.add(url + "/")
                
    def _file_to_url(self, rel_path, is_english):
        """Convert file path to Hugo URL."""
        parts = list(rel_path.parts)
        
        # Handle index files
        if parts[-1] == "index.md" or parts[-1] == "index.en.md":
            parts = parts[:-1]
        elif parts[-1].endswith(".md"):
            # Regular .md file (not index)
            parts[-1] = parts[-1].replace(".en.md", "").replace(".md", "")
            
        # Build URL
        if len(parts) == 0:
            url = "/" if not is_english else "/en/"
        else:
            url = "/" + "/".join(parts) + "/"
            if is_english:
                url = "/en" + url
                
        return url
        
    def check_file(self, file_path):
        """Check all links in a single markdown file."""
        file_path = Path(file_path)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            self.errors.append(f"Error reading {file_path}: {e}")
            return
            
        # Get source URL for this file
        rel_path = file_path.relative_to(self.content_dir)
        is_english = file_path.name.endswith(".en.md")
        source_url = self._file_to_url(rel_path, is_english)
        
        # Find all markdown links [text](url)
        link_pattern = r'\[([^\]]*)\]\(([^)]+)\)'
        matches = re.finditer(link_pattern, content)
        
        line_num = 0
        for line_no, line in enumerate(content.split('\n'), 1):
            for match in re.finditer(link_pattern, line):
                link_text = match.group(1)
                link_url = match.group(2)
                self.checked_links += 1
                
                # Skip external links, anchors, and special URLs
                if (link_url.startswith('http://') or 
                    link_url.startswith('https://') or
                    link_url.startswith('mailto:') or
                    link_url.startswith('#') or
                    link_url.startswith('javascript:') or
                    not link_url):
                    continue
                    
                # Check relative links
                if link_url.startswith('/'):
                    # Absolute path from root
                    if link_url not in self.valid_urls:
                        self.errors.append(
                            f"{file_path}:{line_no} - Dead link: [{link_text}]({link_url})"
                        )
                else:
                    # Relative path - need to resolve
                    # For now, warn about relative paths as they can be problematic
                    self.warnings.append(
                        f"{file_path}:{line_no} - Relative link (consider using absolute): [{link_text}]({link_url})"
                    )
                    
    def check_all(self):
        """Check all markdown files in content directory."""
        print(f"Scanning {self.content_dir} for markdown files...")
        
        md_files = list(self.content_dir.rglob("*.md"))
        print(f"Found {len(md_files)} markdown files")
        print(f"Built URL map with {len(self.valid_urls)} valid URLs")
        
        for md_file in md_files:
            if md_file.name.startswith("_"):
                continue
            self.check_file(md_file)
            
        # Print summary
        print(f"\nChecked {self.checked_links} links total")
        print(f"Found {len(self.errors)} dead links")
        print(f"Found {len(self.warnings)} warnings")
        
        if self.errors:
            print("\n=== DEAD LINKS ===")
            for error in sorted(self.errors):
                print(error)
                
        if self.warnings:
            print("\n=== WARNINGS ===")
            for warning in sorted(self.warnings)[:20]:  # Show first 20
                print(warning)
            if len(self.warnings) > 20:
                print(f"... and {len(self.warnings) - 20} more warnings")
                
        return len(self.errors) == 0

if __name__ == "__main__":
    checker = LinkChecker()
    success = checker.check_all()
    sys.exit(0 if success else 1)