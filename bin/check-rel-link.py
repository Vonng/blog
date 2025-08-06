#!/usr/bin/env python3

import os
import re
import sys
import argparse
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
    
    def __init__(self, content_dir: str = "content", check_language_consistency: bool = False):
        self.content_dir = Path(content_dir)
        self.content_map: Dict[str, Path] = {}  # Hugo URL -> file path
        self.all_links: List[LinkInfo] = []
        self.broken_links: List[BrokenLink] = []
        self.check_language_consistency = check_language_consistency
        
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
        
        # Store language info if present
        lang_suffix = None
        
        # Remove .md extension and handle index files
        if parts[-1].endswith('.md'):
            filename = parts[-1][:-3]
            
            # Check for language suffix (e.g., index.en, index.zh)
            if '.' in filename:
                base, suffix = filename.rsplit('.', 1)
                if suffix in ['en', 'zh']:
                    lang_suffix = suffix
                    filename = base
            
            parts[-1] = filename
            
        # Handle index files
        if parts[-1] == 'index':
            parts = parts[:-1]
        elif parts[-1] == '_index':
            # Section pages
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
            
            # For language-specific files, create additional mappings
            filename = md_file.name
            if filename.endswith('.en.md'):
                # English version - map with /en/ prefix for Hugo multilingual sites
                # Extract the path parts
                parts = list(md_file.relative_to(self.content_dir).parts)
                # Create English URL with /en/ prefix
                en_url = '/en/' + '/'.join(parts[:-1]) + '/'
                en_url = en_url.replace('//', '/').rstrip('/') or '/'
                if en_url != '/':
                    en_url = en_url + '/'
                self.content_map[en_url] = md_file
                self.content_map[en_url.rstrip('/')] = md_file
                
            elif filename == 'index.md' or filename == '_index.md':
                # Chinese default file - this is the primary content
                # Also map with /zh/ prefix if needed
                parts = list(md_file.relative_to(self.content_dir).parts)
                zh_url = '/zh/' + '/'.join(parts[:-1]) + '/'
                zh_url = zh_url.replace('//', '/').rstrip('/') or '/'
                if zh_url != '/':
                    zh_url = zh_url + '/'
                self.content_map[zh_url] = md_file
                self.content_map[zh_url.rstrip('/')] = md_file
            
            # For multilingual sites with language folders
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
        source_filename = source_path.name
        
        # Determine if source is English or Chinese
        is_source_english = source_filename.endswith('.en.md')
        
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
            target_file = self.content_map[target_url_no_anchor]
            
            # If source is English and language consistency check is enabled
            if is_source_english and self.check_language_consistency:
                target_filename = target_file.name
                # If target is Chinese (index.md), check if English version exists
                if target_filename == 'index.md' or target_filename == '_index.md':
                    en_target = target_file.parent / target_filename.replace('.md', '.en.md')
                    if en_target.exists():
                        # English version exists, warn about language inconsistency
                        return BrokenLink(
                            link=link,
                            reason="Language inconsistency: English page linking to Chinese version (English version available)",
                            expected_path=str(en_target)
                        )
            return None  # Link is valid
        
        # Try with trailing slash
        if not target_url_no_anchor.endswith('/'):
            if target_url_no_anchor + '/' in self.content_map:
                target_file = self.content_map[target_url_no_anchor + '/']
                
                # Check language consistency if enabled
                if is_source_english and self.check_language_consistency:
                    target_filename = target_file.name
                    if target_filename == 'index.md' or target_filename == '_index.md':
                        en_target = target_file.parent / target_filename.replace('.md', '.en.md')
                        if en_target.exists():
                            return BrokenLink(
                                link=link,
                                reason="Language inconsistency: English page linking to Chinese version (English version available)",
                                expected_path=str(en_target)
                            )
                return None  # Link is valid
        
        # Try without trailing slash
        if target_url_no_anchor.endswith('/'):
            if target_url_no_anchor[:-1] in self.content_map:
                target_file = self.content_map[target_url_no_anchor[:-1]]
                
                # Check language consistency if enabled
                if is_source_english and self.check_language_consistency:
                    target_filename = target_file.name
                    if target_filename == 'index.md' or target_filename == '_index.md':
                        en_target = target_file.parent / target_filename.replace('.md', '.en.md')
                        if en_target.exists():
                            return BrokenLink(
                                link=link,
                                reason="Language inconsistency: English page linking to Chinese version (English version available)",
                                expected_path=str(en_target)
                            )
                return None  # Link is valid
        
        # Check if it might be a static file or asset
        if any(target_url_no_anchor.endswith(ext) for ext in ['.jpg', '.png', '.gif', '.pdf', '.webp', '.jpeg', '.svg']):
            # Could be an asset file - skip for now
            return None
        
        # For English source files, check if the target exists but only in Chinese
        if is_source_english:
            # Try to find the Chinese version
            for url_variant in [target_url_no_anchor, target_url_no_anchor + '/', target_url_no_anchor.rstrip('/')]:
                if url_variant in self.content_map:
                    target_file = self.content_map[url_variant]
                    if target_file.name in ['index.md', '_index.md']:
                        # Found Chinese version, but no English version
                        en_target = target_file.parent / target_file.name.replace('.md', '.en.md')
                        if not en_target.exists():
                            return BrokenLink(
                                link=link,
                                reason="English version not found (linking from English page to Chinese-only content)",
                                expected_path=str(en_target)
                            )
        
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
    
    def run(self, debug=False):
        """Run the complete link checking process."""
        print(f"Hugo Relative Link Checker")
        print(f"Content directory: {self.content_dir.absolute()}")
        if self.check_language_consistency:
            print("Language consistency checking: ENABLED")
        print("=" * 60)
        
        # Build content map
        self.build_content_map()
        
        if debug:
            print("\nSample URL mappings:")
            for url in sorted(self.content_map.keys())[:20]:
                print(f"  {url} -> {self.content_map[url].name}")
        
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
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Check relative links in Hugo content')
    parser.add_argument('--check-language', '-l', action='store_true',
                        help='Enable language consistency checking (warn when English pages link to Chinese versions)')
    parser.add_argument('--content-dir', '-d', default='content',
                        help='Path to content directory (default: content)')
    args = parser.parse_args()
    
    # Check if content directory exists
    content_dir = Path(args.content_dir)
    if not content_dir.exists():
        print(f"Error: Content directory '{content_dir}' not found!")
        print("Please run this script from the Hugo project root.")
        sys.exit(1)
    
    # Create and run checker
    checker = HugoLinkChecker(str(content_dir), check_language_consistency=args.check_language)
    exit_code = checker.run()
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()