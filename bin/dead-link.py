#!/usr/bin/env python3

import os
import re
import glob
from typing import Dict, List, Set, Tuple
from urllib.parse import urlparse, urljoin
from pathlib import Path
from dataclasses import dataclass


@dataclass
class LinkReference:
    """Represents a link reference found in a file."""
    file_path: str
    line_number: int
    link_text: str
    url: str
    link_type: str  # 'markdown' or 'html'


@dataclass
class DeadLink:
    """Represents a dead link."""
    reference: LinkReference
    error_type: str  # 'missing_file', 'missing_anchor'
    target_file: str = None


class FumaDocsLinkChecker:
    """Link checker for Fuma Docs with Next.js routing."""
    
    def __init__(self, content_dir: str = "content"):
        self.content_dir = content_dir
        self.file_to_url_map: Dict[str, str] = {}  # file path -> URL
        self.url_to_file_map: Dict[str, str] = {}  # URL -> file path
        self.file_anchors: Dict[str, Set[str]] = {}  # file path -> set of anchors
        self.all_links: List[LinkReference] = []
        self.dead_links: List[DeadLink] = []
        
        # Regex patterns for extracting links
        self.markdown_link_pattern = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)|(?<!!)\[([^\]]*)\]\(([^)]+)\)')
        self.html_link_pattern = re.compile(r'href=["\']([^"\']+)["\']')
        self.anchor_pattern = re.compile(r'^#+\s+(.+)$', re.MULTILINE)
        self.manual_anchor_pattern = re.compile(r'\[#([^\]]+)\]')
    
    def build_file_index(self):
        """Build index of all MDX files and their corresponding URLs."""
        print("Building file index...")
        
        # Find all MDX files
        mdx_files = glob.glob(f"{self.content_dir}/**/*.mdx", recursive=True)
        
        for file_path in mdx_files:
            url = self._file_path_to_url(file_path)
            self.file_to_url_map[file_path] = url
            self.url_to_file_map[url] = file_path
            
            # For index files, also map the URL without trailing slash
            # This handles the implicit index routing in Next.js/Fumadocs
            if url.endswith("/") and url != "/":
                url_without_slash = url.rstrip("/")
                self.url_to_file_map[url_without_slash] = file_path
            
            # Extract anchors from this file
            self._extract_anchors(file_path)
        
        print(f"Found {len(mdx_files)} MDX files")
        print(f"Generated {len(self.url_to_file_map)} URL mappings")
    
    def _file_path_to_url(self, file_path: str) -> str:
        """Convert file path to URL according to Fuma Docs routing rules."""
        # Remove content/ prefix and .mdx suffix
        relative_path = file_path.replace(self.content_dir + "/", "").replace(".mdx", "")
        
        # Handle docs/ prefix - content/docs/* maps to /*
        if relative_path.startswith("docs/"):
            relative_path = relative_path[5:]  # Remove "docs/" prefix
        
        # Handle localization - extract .zh/.cn etc. suffixes
        locale_suffix = ""
        if ".zh" in relative_path:
            relative_path = relative_path.replace(".zh", "")
            locale_suffix = "/zh"
        elif ".cn" in relative_path:
            relative_path = relative_path.replace(".cn", "")
            locale_suffix = "/zh"  # cn maps to zh
        
        # Handle (name) bracket omission routing
        # e.g., docs/(home)/index -> docs/
        # e.g., docs/(home)/about -> docs/about
        relative_path = re.sub(r'/\([^)]+\)', '', relative_path)
        
        # Handle index files
        if relative_path.endswith("/index"):
            relative_path = relative_path.replace("/index", "/")
        elif relative_path == "index" or relative_path == "":
            relative_path = "/"
        
        # Ensure leading slash for non-root paths
        if relative_path and not relative_path.startswith("/"):
            relative_path = "/" + relative_path
        
        # Add locale prefix if present
        if locale_suffix:
            if relative_path == "/":
                relative_path = locale_suffix + "/"
            else:
                relative_path = locale_suffix + relative_path
        
        return relative_path
    
    def _url_to_file_path(self, url: str) -> str:
        """Convert URL back to file path according to Fuma Docs routing rules."""
        # Handle locale prefixes
        locale_suffix = ""
        if url.startswith("/zh/"):
            locale_suffix = ".zh"
            url = url[3:]  # Remove /zh prefix
        elif url == "/zh":
            locale_suffix = ".zh"
            url = "/"
        
        # Handle root URL
        if url == "/" or url == "":
            base_path = "docs/index"
        else:
            # Remove leading slash and convert to file path
            clean_url = url.lstrip("/")
            
            # For URLs ending with /, try both direct file and index file
            if clean_url.endswith("/"):
                clean_url = clean_url.rstrip("/")
                # First try direct file (e.g., /pgsql/ -> pgsql.mdx)
                direct_path = f"docs/{clean_url}"
                direct_full_path = direct_path + locale_suffix + ".mdx"
                direct_candidate = f"{self.content_dir}/{direct_full_path}"
                if direct_candidate in self.file_to_url_map:
                    return direct_candidate
                
                # Then try index file (e.g., /pgsql/ -> pgsql/index.mdx)
                base_path = f"docs/{clean_url}/index"
            else:
                # For URLs without trailing slash, could be either direct file or index
                base_path = f"docs/{clean_url}"
        
        # Add locale suffix if present
        full_path = base_path + locale_suffix + ".mdx"
        
        # Check if this exact file exists
        candidate_path = f"{self.content_dir}/{full_path}"
        if candidate_path in self.file_to_url_map:
            return candidate_path
        
        # If not found and doesn't end with /index, try index file pattern
        if not base_path.endswith("/index") and not base_path.endswith("index"):
            index_path = base_path + "/index" + locale_suffix + ".mdx"
            candidate_index_path = f"{self.content_dir}/{index_path}"
            if candidate_index_path in self.file_to_url_map:
                return candidate_index_path
        
        return None
    
    def _extract_anchors(self, file_path: str):
        """Extract all anchors from a file."""
        anchors = set()
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Extract markdown headers with improved regex
                # Match headers from # to ###### with optional leading/trailing spaces
                header_pattern = re.compile(r'^#{1,6}\s+(.+?)(?:\s*{[^}]*})?\s*$', re.MULTILINE)
                header_matches = header_pattern.findall(content)
                
                for header in header_matches:
                    # Remove any trailing {#custom-id} if present
                    header = re.sub(r'\s*{#[^}]*}\s*$', '', header)
                    anchor = self._header_to_anchor(header)
                    if anchor:  # Only add non-empty anchors
                        anchors.add(anchor)
                
                # Extract manual anchors [#anchor-id]
                manual_anchors = self.manual_anchor_pattern.findall(content)
                for anchor in manual_anchors:
                    if anchor:  # Only add non-empty anchors
                        anchors.add(anchor)
                
                # Extract HTML id attributes
                html_id_pattern = re.compile(r'id=["\']([^"\']+)["\']')
                html_ids = html_id_pattern.findall(content)
                for html_id in html_ids:
                    if html_id:
                        anchors.add(html_id)
        
        except Exception as e:
            print(f"Warning: Could not read {file_path}: {e}")
        
        self.file_anchors[file_path] = anchors
    
    def _header_to_anchor(self, header_text: str) -> str:
        """Convert header text to anchor ID following common web framework rules."""
        # Handle special cases for programming languages
        special_cases = {
            'C++': 'c-1',
            'C#': 'c-2',
            'F#': 'f-sharp',
            '.NET': 'net',
        }
        
        if header_text.strip() in special_cases:
            return special_cases[header_text.strip()]
        
        # Step 1: Handle markdown links [text](url) - keep only the text part
        clean_text = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', header_text)
        
        # Step 2: Remove backticks but preserve the content
        clean_text = re.sub(r'`([^`]*)`', r'\1', clean_text)
        
        # Step 3: Remove other markdown formatting (bold, italic, etc.) but keep underscores
        clean_text = re.sub(r'[*{}]', '', clean_text)
        
        # Step 4: Remove remaining brackets and parentheses
        clean_text = re.sub(r'[\[\]()]', '', clean_text)
        
        # Step 5: Remove HTML tags if any
        clean_text = re.sub(r'<[^>]+>', '', clean_text)
        
        # Step 6: Convert to lowercase
        clean_text = clean_text.lower()
        
        # Step 7: Remove punctuation but keep underscores and basic word characters
        # This handles cases like pg_stat_statements correctly
        clean_text = re.sub(r'[^\w\s-]', '', clean_text)
        
        # Step 9: Replace multiple spaces/whitespace with single space
        clean_text = re.sub(r'\s+', ' ', clean_text)
        
        # Step 10: Replace spaces with hyphens, but keep underscores
        anchor = clean_text.replace(' ', '-')
        
        # Step 11: Replace multiple consecutive hyphens with single hyphen
        anchor = re.sub(r'-+', '-', anchor)
        
        # Step 12: Remove leading/trailing hyphens
        anchor = anchor.strip('-')
        
        # Step 13: Handle edge cases - if anchor is empty, generate a fallback
        if not anchor:
            anchor = 'heading'
        
        return anchor
    
    def _test_anchor_generation(self):
        """Test anchor generation with common cases."""
        test_cases = [
            ("Basic Header", "basic-header"),
            ("`code block` in header", "code-block-in-header"),
            ("Header with `multiple` `code` blocks", "header-with-multiple-code-blocks"),
            ("Header with **bold** text", "header-with-bold-text"),
            ("Header with *italic* text", "header-with-italic-text"),
            ("Header with [link](url)", "header-with-link"),
            ("Header with (parentheses)", "header-with-parentheses"),
            ("Header with dots... and commas,", "header-with-dots-and-commas"),
            ("Header with 'quotes' and \"double quotes\"", "header-with-quotes-and-double-quotes"),
            ("Header with numbers 123", "header-with-numbers-123"),
            ("Header with @ # $ % special chars", "header-with-special-chars"),
            ("Multiple    spaces   between words", "multiple-spaces-between-words"),
            ("  Leading and trailing spaces  ", "leading-and-trailing-spaces"),
            ("UPPERCASE HEADER", "uppercase-header"),
            ("MiXeD cAsE hEaDeR", "mixed-case-header"),
            ("", "heading"),  # Empty case
            ("---", "heading"),  # Only punctuation
            ("How to use `pg_stat_statements`?", "how-to-use-pg_stat_statements"),
            ("What is PostgreSQL v15.4?", "what-is-postgresql-v154"),
            ("File: config.yaml", "file-configyaml"),
            ("C++", "c-1"),
            ("C#", "c-2"),
            ("F#", "f-sharp"),
            (".NET", "net"),
            ("C", "c"),
            ("Python", "python"),
        ]
        
        print("Testing anchor generation...")
        for header, expected in test_cases:
            result = self._header_to_anchor(header)
            status = "✓" if result == expected else "✗"
            if result != expected:
                print(f"{status} '{header}' -> '{result}' (expected: '{expected}')")
        print("Anchor generation test completed.")
    
    def extract_all_links(self):
        """Extract all internal links from all MDX files."""
        print("Extracting links...")
        
        for file_path in self.file_to_url_map.keys():
            self._extract_links_from_file(file_path)
        
        print(f"Found {len(self.all_links)} internal links")
    
    def _extract_links_from_file(self, file_path: str):
        """Extract links from a single file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
                for line_num, line in enumerate(lines, 1):
                    # Extract markdown links
                    markdown_matches = self.markdown_link_pattern.findall(line)
                    for match in markdown_matches:
                        if len(match) == 4:  # Regular link [text](url)
                            link_text, url = match[2], match[3]
                        else:  # Image link ![alt](url)
                            link_text, url = match[0], match[1]
                        
                        if self._is_internal_link(url):
                            self.all_links.append(LinkReference(
                                file_path=file_path,
                                line_number=line_num,
                                link_text=link_text,
                                url=url,
                                link_type='markdown'
                            ))
                    
                    # Extract HTML links
                    html_matches = self.html_link_pattern.findall(line)
                    for url in html_matches:
                        if self._is_internal_link(url):
                            self.all_links.append(LinkReference(
                                file_path=file_path,
                                line_number=line_num,
                                link_text='',
                                url=url,
                                link_type='html'
                            ))
        
        except Exception as e:
            print(f"Warning: Could not read {file_path}: {e}")
    
    def _is_internal_link(self, url: str) -> bool:
        """Check if URL is an internal relative link."""
        parsed = urlparse(url)
        
        # Skip external links (with scheme or netloc)
        if parsed.scheme or parsed.netloc:
            return False
        
        # Skip mailto, tel, etc.
        if url.startswith(('mailto:', 'tel:', 'javascript:')):
            return False
        
        # Skip empty or anchor-only links
        if not url or url.startswith('#'):
            return False
        
        return True
    
    def check_links(self):
        """Check all extracted links for validity."""
        print("Checking links...")
        
        for link_ref in self.all_links:
            self._check_single_link(link_ref)
        
        dead_file_links = [dl for dl in self.dead_links if dl.error_type == 'missing_file']
        dead_anchor_links = [dl for dl in self.dead_links if dl.error_type == 'missing_anchor']
        
        print(f"Found {len(dead_file_links)} dead file links")
        print(f"Found {len(dead_anchor_links)} dead anchor links")
    
    def _check_single_link(self, link_ref: LinkReference):
        """Check a single link for validity."""
        url = link_ref.url
        
        # Split URL and anchor
        if '#' in url:
            url_part, anchor_part = url.split('#', 1)
        else:
            url_part, anchor_part = url, None
        
        # Normalize URL path
        if not url_part:
            # Anchor-only link, refers to current file
            target_file = link_ref.file_path
        else:
            # Resolve relative URL
            current_url = self.file_to_url_map[link_ref.file_path]
            target_url = self._resolve_relative_url(current_url, url_part)
            
            # First try direct lookup in URL map (includes implicit routing)
            target_file = self.url_to_file_map.get(target_url)
            
            # If not found, try reverse mapping function as fallback
            if not target_file:
                target_file = self._url_to_file_path(target_url)
            
            if not target_file:
                self.dead_links.append(DeadLink(
                    reference=link_ref,
                    error_type='missing_file',
                    target_file=target_url
                ))
                return
        
        # Check anchor if present
        if anchor_part and target_file:
            if target_file in self.file_anchors:
                if anchor_part not in self.file_anchors[target_file]:
                    self.dead_links.append(DeadLink(
                        reference=link_ref,
                        error_type='missing_anchor',
                        target_file=target_file
                    ))
    
    def _resolve_relative_url(self, current_url: str, target_url: str) -> str:
        """Resolve relative URL against current URL."""
        # Use urljoin to properly resolve relative paths
        resolved = urljoin(current_url, target_url)
        return resolved
    
    def print_results(self, debug=False):
        """Print dead link results."""
        print("\n" + "="*80)
        print("DEAD LINK ANALYSIS RESULTS")
        print("="*80)
        
        # Group dead links by type
        dead_file_links = [dl for dl in self.dead_links if dl.error_type == 'missing_file']
        dead_anchor_links = [dl for dl in self.dead_links if dl.error_type == 'missing_anchor']
        
        if dead_file_links:
            print(f"\n🔴 MISSING FILES ({len(dead_file_links)} issues):")
            print("-" * 50)
            for dead_link in dead_file_links:
                ref = dead_link.reference
                print(f"File: {ref.file_path}:{ref.line_number}")
                print(f"Link: {ref.url}")
                print(f"Target: {dead_link.target_file}")
                print(f"Type: {ref.link_type}")
                if ref.link_text:
                    print(f"Text: {ref.link_text}")
                print()
        
        if dead_anchor_links:
            print(f"\n🔴 MISSING ANCHORS ({len(dead_anchor_links)} issues):")
            print("-" * 50)
            for dead_link in dead_anchor_links:
                ref = dead_link.reference
                anchor = ref.url.split('#', 1)[1] if '#' in ref.url else 'unknown'
                print(f"File: {ref.file_path}:{ref.line_number}")
                print(f"Link: {ref.url}")
                print(f"Target file: {dead_link.target_file}")
                print(f"Missing anchor: #{anchor}")
                print(f"Type: {ref.link_type}")
                if ref.link_text:
                    print(f"Text: {ref.link_text}")
                
                # Show available anchors in target file
                if dead_link.target_file in self.file_anchors:
                    available = list(self.file_anchors[dead_link.target_file])
                    if available:
                        if debug:
                            print(f"Available anchors: {', '.join(sorted(available))}")
                        else:
                            # Show only first few anchors to avoid clutter
                            available_sorted = sorted(available)
                            if len(available_sorted) > 5:
                                print(f"Available anchors: {', '.join(available_sorted[:5])}, ... ({len(available_sorted)} total)")
                            else:
                                print(f"Available anchors: {', '.join(available_sorted)}")
                    else:
                        print("No anchors found in target file")
                print()
        
        if not self.dead_links:
            print("\n✅ No dead links found!")
        
        print(f"\nSUMMARY:")
        print(f"- Total files scanned: {len(self.file_to_url_map)}")
        print(f"- Total links checked: {len(self.all_links)}")
        print(f"- Dead file links: {len(dead_file_links)}")
        print(f"- Dead anchor links: {len(dead_anchor_links)}")
        print(f"- Total issues: {len(self.dead_links)}")
    
    def run(self, test_anchors=False, debug=False):
        """Run the complete link checking process."""
        print("Starting dead link analysis...")
        print(f"Content directory: {self.content_dir}")
        
        if test_anchors:
            self._test_anchor_generation()
            return
        
        self.build_file_index()
        self.extract_all_links()
        self.check_links()
        self.print_results(debug=debug)


def main():
    """Main entry point."""
    import sys
    
    # Parse simple command line arguments
    test_anchors = "--test-anchors" in sys.argv
    debug = "--debug" in sys.argv
    help_requested = "--help" in sys.argv or "-h" in sys.argv
    
    if help_requested:
        print("Dead Link Checker for Fuma Docs")
        print("Usage: python dead-link.py [options]")
        print()
        print("Options:")
        print("  --test-anchors    Test anchor generation rules")
        print("  --debug          Show detailed debug information")
        print("  --help, -h       Show this help message")
        return 0
    
    # Check if content directory exists
    content_dir = "content"
    if not os.path.exists(content_dir):
        print(f"Error: Content directory '{content_dir}' not found")
        print("Please run this script from the project root directory")
        return 1
    
    checker = FumaDocsLinkChecker(content_dir)
    checker.run(test_anchors=test_anchors, debug=debug)
    
    return 0


if __name__ == "__main__":
    exit(main())