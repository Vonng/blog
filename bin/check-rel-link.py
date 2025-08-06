#!/usr/bin/env python3

import os
import re
import sys
from pathlib import Path
from urllib.parse import urlparse, urljoin
from typing import Dict, List, Set, Tuple
from dataclasses import dataclass
import glob


@dataclass
class LinkInfo:
    """Information about a link found in a markdown file."""
    source_file: str
    line_number: int
    link_text: str
    url: str
    is_relative: bool
    is_anchor_only: bool


@dataclass
class BrokenLink:
    """A broken relative link."""
    link: LinkInfo
    reason: str
    expected_path: str = None


class HugoLinkChecker:
    """Check relative links in Hugo content following Hugo URL rules."""
    
    def __init__(self, content_dir: str = "content"):
        self.content_dir = Path(content_dir)
        self.content_map: Dict[str, Path] = {}  # Hugo URL -> file path
        self.all_links: List[LinkInfo] = []
        self.broken_links: List[BrokenLink] = []
        
        # Regex patterns for extracting links
        # Matches both regular links [text](url) and image links ![alt](url)
        self.markdown_link_pattern = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)|(?<!!)\[([^\]]*)\]\(([^)]+)\)')
        # Pattern to extract anchors/headings from markdown
        self.heading_pattern = re.compile(r'^#{1,6}\s+(.+)$', re.MULTILINE)
        # Pattern for manually defined anchors {#anchor-id}
        self.manual_anchor_pattern = re.compile(r'\{#([^}]+)\}')
        
    def hugo_url_from_path(self, file_path: Path) -> str:
        """Convert a file path to Hugo URL format."""
        # Get relative path from content directory
        rel_path = file_path.relative_to(self.content_dir)
        parts = list(rel_path.parts)
        
        # Remove .md extension and handle index files
        if parts[-1].endswith('.md'):
            parts[-1] = parts[-1][:-3]
            
        # Handle index files
        if parts[-1] == 'index' or parts[-1].startswith('index.'):
            parts = parts[:-1]
        elif parts[-1] == '_index' or parts[-1].startswith('_index.'):
            # Section pages
            parts[-1] = parts[-1].replace('_index', '')
            if parts[-1] == '' or parts[-1] == '.en' or parts[-1] == '.zh':
                parts = parts[:-1]
        
        # Build URL
        url = '/' + '/'.join(parts) + '/'
        # Clean up double slashes and trailing slashes
        url = re.sub(r'/+', '/', url)
        if url != '/' and url.endswith('/'):
            url = url  # Keep trailing slash for Hugo
        
        return url
    
    def build_content_map(self):
        """Build a map of all content files and their Hugo URLs."""
        print("Building content map...")
        
        # Find all .md files in content directory
        for md_file in self.content_dir.rglob('*.md'):
            hugo_url = self.hugo_url_from_path(md_file)
            self.content_map[hugo_url] = md_file
            
            # Also map without trailing slash for flexibility
            if hugo_url.endswith('/') and hugo_url != '/':
                self.content_map[hugo_url[:-1]] = md_file
            
            # For multilingual sites, also map language-specific URLs
            parts = list(md_file.relative_to(self.content_dir).parts)
            if len(parts) > 0 and parts[0] in ['en', 'zh']:
                # Also create mapping without language prefix for internal references
                non_lang_parts = parts[1:]
                if non_lang_parts:
                    non_lang_path = self.content_dir / Path(*non_lang_parts)
                    if non_lang_path != md_file:
                        alt_url = self.hugo_url_from_path(Path(self.content_dir.name) / Path(*non_lang_parts))
                        # Map alternative URL patterns
                        if alt_url not in self.content_map:
                            self.content_map[alt_url] = md_file
        
        print(f"Found {len(set(self.content_map.values()))} content files")
        print(f"Generated {len(self.content_map)} URL mappings")
    
    def extract_links_from_file(self, file_path: Path) -> List[LinkInfo]:
        """Extract all links from a markdown file."""
        links = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Extract markdown links
            for line_num, line in enumerate(content.split('\n'), 1):
                for match in self.markdown_link_pattern.finditer(line):
                    # Handle both image and regular links
                    if match.group(2):  # Image link
                        link_text = match.group(1)
                        url = match.group(2)
                    else:  # Regular link
                        link_text = match.group(3)
                        url = match.group(4)
                    
                    if url:
                        # Parse URL to determine if it's relative
                        parsed = urlparse(url)
                        is_relative = not parsed.scheme and not parsed.netloc
                        is_anchor_only = url.startswith('#')
                        
                        # Skip mailto: links and other protocols
                        if parsed.scheme in ['mailto', 'tel', 'javascript']:
                            continue
                        
                        # Only process relative URLs (including anchor-only)
                        if is_relative:
                            links.append(LinkInfo(
                                source_file=str(file_path),
                                line_number=line_num,
                                link_text=link_text or '',
                                url=url,
                                is_relative=is_relative,
                                is_anchor_only=is_anchor_only
                            ))
        
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
        
        return links
    
    def resolve_relative_url(self, base_file: Path, relative_url: str) -> str:
        """Resolve a relative URL from a base file to an absolute Hugo URL."""
        # Get the Hugo URL of the base file
        base_hugo_url = self.hugo_url_from_path(base_file)
        
        # Handle anchor-only links
        if relative_url.startswith('#'):
            return base_hugo_url + relative_url
        
        # Remove any anchors for file resolution
        url_without_anchor = relative_url.split('#')[0]
        anchor = '#' + relative_url.split('#')[1] if '#' in relative_url else ''
        
        # If URL starts with /, it's absolute
        if url_without_anchor.startswith('/'):
            resolved = url_without_anchor
        else:
            # Relative URL - resolve from base
            resolved = urljoin(base_hugo_url, url_without_anchor)
        
        # Normalize the URL
        resolved = re.sub(r'/+', '/', resolved)
        
        # Add back anchor if present
        return resolved + anchor
    
    def check_link(self, link: LinkInfo) -> BrokenLink:
        """Check if a relative link is valid."""
        source_path = Path(link.source_file)
        
        # Handle anchor-only links (always valid for now)
        if link.is_anchor_only:
            # TODO: Could check if anchor exists in the same file
            return None
        
        # Resolve the relative URL to absolute Hugo URL
        target_url = self.resolve_relative_url(source_path, link.url)
        
        # Remove anchor for file checking
        target_url_no_anchor = target_url.split('#')[0]
        
        # Check if the target exists in our content map
        if target_url_no_anchor in self.content_map:
            return None  # Link is valid
        
        # Try with trailing slash
        if not target_url_no_anchor.endswith('/'):
            if target_url_no_anchor + '/' in self.content_map:
                return None  # Link is valid
        
        # Try without trailing slash
        if target_url_no_anchor.endswith('/'):
            if target_url_no_anchor[:-1] in self.content_map:
                return None  # Link is valid
        
        # Check if it might be a static file or asset
        if any(target_url_no_anchor.endswith(ext) for ext in ['.jpg', '.png', '.gif', '.pdf', '.webp', '.jpeg', '.svg']):
            # Could be an asset file - skip for now
            return None
        
        # Link is broken
        return BrokenLink(
            link=link,
            reason="Target page not found",
            expected_path=target_url_no_anchor
        )
    
    def scan_all_content(self):
        """Scan all markdown files for links."""
        print("\nScanning content files for relative links...")
        
        for md_file in self.content_dir.rglob('*.md'):
            links = self.extract_links_from_file(md_file)
            self.all_links.extend(links)
        
        print(f"Found {len(self.all_links)} relative links in total")
    
    def check_all_links(self):
        """Check all found links for validity."""
        print("\nChecking link validity...")
        
        for link in self.all_links:
            broken = self.check_link(link)
            if broken:
                self.broken_links.append(broken)
        
        print(f"Found {len(self.broken_links)} broken links")
    
    def report_results(self):
        """Print a report of broken links."""
        if not self.broken_links:
            print("\n✅ No broken relative links found!")
            return
        
        print(f"\n❌ Found {len(self.broken_links)} broken relative links:\n")
        
        # Group by source file
        by_file = {}
        for broken in self.broken_links:
            source = broken.link.source_file
            if source not in by_file:
                by_file[source] = []
            by_file[source].append(broken)
        
        # Report by file
        for file_path, broken_list in sorted(by_file.items()):
            # file_path is already an absolute path, make it relative to cwd
            try:
                rel_path = Path(file_path).relative_to(Path.cwd())
            except ValueError:
                # If can't make relative, just use the path as is
                rel_path = file_path
            print(f"\n📄 {rel_path}")
            
            for broken in sorted(broken_list, key=lambda x: x.link.line_number):
                print(f"  Line {broken.link.line_number}: [{broken.link.link_text}]({broken.link.url})")
                print(f"    → {broken.reason}")
                if broken.expected_path:
                    print(f"    → Expected: {broken.expected_path}")
        
        # Print summary
        print("\n" + "=" * 60)
        print("SUMMARY")
        print("=" * 60)
        print(f"Total files scanned: {len(set(l.source_file for l in self.all_links))}")
        print(f"Total relative links found: {len(self.all_links)}")
        print(f"Total broken links: {len(self.broken_links)}")
        print(f"Files with broken links: {len(by_file)}")
        
        # Analyze common patterns
        patterns = {}
        for broken in self.broken_links:
            if broken.expected_path:
                if '/zh/docs/' in broken.expected_path:
                    patterns['External docs links (/zh/docs/)'] = patterns.get('External docs links (/zh/docs/)', 0) + 1
                elif '/en/pg' in broken.expected_path or '/en/db' in broken.expected_path or '/en/cloud' in broken.expected_path:
                    patterns['Missing English category pages (/en/pg, /en/db, /en/cloud)'] = patterns.get('Missing English category pages (/en/pg, /en/db, /en/cloud)', 0) + 1
                elif broken.link.url.endswith(('.JPG', '.jpg', '.png', '.mp4')):
                    patterns['Missing media files'] = patterns.get('Missing media files', 0) + 1
                elif '{{<' in broken.link.url:
                    patterns['Hugo shortcode in URL'] = patterns.get('Hugo shortcode in URL', 0) + 1
        
        if patterns:
            print("\nCommon issues:")
            for pattern, count in sorted(patterns.items(), key=lambda x: x[1], reverse=True):
                print(f"  • {pattern}: {count}")
    
    def run(self):
        """Run the complete link checking process."""
        print(f"Hugo Relative Link Checker")
        print(f"Content directory: {self.content_dir.absolute()}")
        print("=" * 60)
        
        # Build content map
        self.build_content_map()
        
        # Scan all content
        self.scan_all_content()
        
        # Check all links
        self.check_all_links()
        
        # Report results
        self.report_results()
        
        # Return exit code
        return 1 if self.broken_links else 0


def main():
    """Main entry point."""
    # Check if content directory exists
    content_dir = Path("content")
    if not content_dir.exists():
        print(f"Error: Content directory '{content_dir}' not found!")
        print("Please run this script from the Hugo project root.")
        sys.exit(1)
    
    # Create and run checker
    checker = HugoLinkChecker(str(content_dir))
    exit_code = checker.run()
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()