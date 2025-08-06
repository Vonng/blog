#!/usr/bin/env python3
"""
Comprehensive link checker for Hugo blog that validates internal links and images.
"""

import os
import re
import sys
from pathlib import Path
from collections import defaultdict
from urllib.parse import urlparse

class ComprehensiveLinkChecker:
    def __init__(self, content_dir="content", static_dir="static"):
        self.content_dir = Path(content_dir)
        self.static_dir = Path(static_dir)
        self.errors = []
        self.warnings = []
        self.info = []
        
        # Build maps
        self.valid_urls = set()
        self.valid_files = set()
        self.image_files = set()
        self._build_maps()
        
    def _build_maps(self):
        """Build maps of valid URLs and files."""
        # Map all content URLs
        for md_file in self.content_dir.rglob("*.md"):
            if md_file.name.startswith("_"):
                continue
                
            rel_path = md_file.relative_to(self.content_dir)
            is_english = md_file.name.endswith(".en.md")
            
            # Convert to URL
            url = self._file_to_url(rel_path, is_english)
            self.valid_urls.add(url)
            
            # Add variations
            if url.endswith("/"):
                self.valid_urls.add(url[:-1])
            else:
                self.valid_urls.add(url + "/")
                
        # Map all static files (images)
        if self.static_dir.exists():
            for img_file in self.static_dir.rglob("*"):
                if img_file.is_file():
                    rel_path = img_file.relative_to(self.static_dir)
                    self.image_files.add("/" + str(rel_path))
                    
        # Also check for images in content directories
        for img_file in self.content_dir.rglob("*"):
            if img_file.is_file() and img_file.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg']:
                # Get the directory path relative to content
                content_rel = img_file.relative_to(self.content_dir)
                # Convert to URL path
                parts = list(content_rel.parts[:-1])  # Remove filename
                if len(parts) > 0:
                    url_path = "/" + "/".join(parts) + "/" + img_file.name
                    self.image_files.add(url_path)
                    
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
        
    def check_link(self, link_url, source_file, line_no):
        """Check if a link is valid."""
        # Skip external links and special URLs
        if (link_url.startswith('http://') or 
            link_url.startswith('https://') or
            link_url.startswith('mailto:') or
            link_url.startswith('#') or
            link_url.startswith('javascript:') or
            not link_url):
            return True
            
        # Check absolute paths
        if link_url.startswith('/'):
            # Could be a page URL or an image
            if link_url in self.valid_urls:
                return True
            elif link_url in self.image_files:
                return True
            else:
                # Check if it's a standard image path that might exist
                if any(link_url.endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg']):
                    self.errors.append(f"{source_file}:{line_no} - Missing image: {link_url}")
                else:
                    self.errors.append(f"{source_file}:{line_no} - Dead link: {link_url}")
                return False
        else:
            # Relative links need context resolution
            self.warnings.append(f"{source_file}:{line_no} - Relative link: {link_url}")
            return True
            
    def check_file(self, file_path):
        """Check all links in a single markdown file."""
        file_path = Path(file_path)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            self.errors.append(f"Error reading {file_path}: {e}")
            return
            
        # Check markdown links [text](url)
        link_pattern = r'\[([^\]]*)\]\(([^)]+)\)'
        
        for line_no, line in enumerate(content.split('\n'), 1):
            for match in re.finditer(link_pattern, line):
                link_text = match.group(1)
                link_url = match.group(2)
                self.check_link(link_url, file_path, line_no)
                
        # Check image references ![alt](url)
        img_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
        
        for line_no, line in enumerate(content.split('\n'), 1):
            for match in re.finditer(img_pattern, line):
                img_alt = match.group(1)
                img_url = match.group(2)
                self.check_link(img_url, file_path, line_no)
                
    def generate_report(self):
        """Generate a comprehensive report."""
        print("\n" + "="*80)
        print("HUGO BLOG LINK CHECK REPORT")
        print("="*80)
        
        print(f"\nContent directory: {self.content_dir}")
        print(f"Static directory: {self.static_dir}")
        print(f"Valid URLs found: {len(self.valid_urls)}")
        print(f"Image files found: {len(self.image_files)}")
        
        if self.errors:
            print(f"\n❌ ERRORS ({len(self.errors)}):")
            print("-"*80)
            for error in sorted(self.errors)[:50]:  # Show first 50
                print(error)
            if len(self.errors) > 50:
                print(f"... and {len(self.errors) - 50} more errors")
                
        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            print("-"*80)
            # Group warnings by type
            relative_links = [w for w in self.warnings if "Relative link" in w]
            if relative_links:
                print(f"\nRelative links found: {len(relative_links)}")
                for warning in relative_links[:10]:
                    print(warning)
                if len(relative_links) > 10:
                    print(f"... and {len(relative_links) - 10} more relative links")
                    
        print("\n" + "="*80)
        print(f"SUMMARY: {len(self.errors)} errors, {len(self.warnings)} warnings")
        print("="*80)
        
        return len(self.errors) == 0
        
    def check_all(self):
        """Check all markdown files."""
        md_files = list(self.content_dir.rglob("*.md"))
        
        print(f"Checking {len(md_files)} markdown files...")
        
        for i, md_file in enumerate(md_files):
            if md_file.name.startswith("_"):
                continue
            if i % 50 == 0:
                print(f"Progress: {i}/{len(md_files)} files checked...")
            self.check_file(md_file)
            
        return self.generate_report()

if __name__ == "__main__":
    checker = ComprehensiveLinkChecker()
    success = checker.check_all()
    
    # Write errors to file for easier fixing
    if checker.errors:
        with open("link_errors.txt", "w") as f:
            f.write("Link Errors Found:\n")
            f.write("==================\n\n")
            for error in sorted(checker.errors):
                f.write(error + "\n")
        print("\nErrors written to link_errors.txt")
        
    sys.exit(0 if success else 1)