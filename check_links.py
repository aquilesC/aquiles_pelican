#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Link Checker for Pelican Static Site.

Validates both internal and external links across:
1. Rendered HTML pages in output/ (compiled from content/ and templates/)
2. Theme templates in themes/*/templates/

Features:
- Fast concurrent external link checking with realistic browser headers
- Internal path and anchor (#hash) resolution
- Source mapping from output HTML back to content/ markdown files
- Smart handling of anti-bot protections and local DNS adblockers
- Categorized reporting (Broken, Warnings/Anti-bot blocked, OK)
- Configurable via CLI flags and Makefile
"""

import argparse
import concurrent.futures
import os
import re
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("Error: beautifulsoup4 is required. Run 'pip install beautifulsoup4'.", file=sys.stderr)
    sys.exit(1)


# ANSI Color Codes
COLOR_RESET = "\033[0m"
COLOR_BOLD = "\033[1m"
COLOR_RED = "\033[31m"
COLOR_GREEN = "\033[32m"
COLOR_YELLOW = "\033[33m"
COLOR_BLUE = "\033[34m"
COLOR_CYAN = "\033[36m"
COLOR_DIM = "\033[2m"

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)

# Known hosts that block automated requests with 403/999/429
ANTI_BOT_DOMAINS = {
    "linkedin.com",
    "www.linkedin.com",
    "twitter.com",
    "x.com",
    "stackexchange.com",
    "stackoverflow.com",
    "academia.stackexchange.com",
    "doi.org",
    "ieeexplore.ieee.org",
    "nature.com",
    "sciencedirect.com",
    "cloudflare.com",
}

# Known tracking/analytics domains (e.g. Google Analytics / GTM) often blocked by VPNs / DNS sinkholes
IGNORE_DOMAINS = {
    "googletagmanager.com",
    "www.googletagmanager.com",
    "google-analytics.com",
    "www.google-analytics.com",
    "analytics.google.com",
    "doubleclick.net",
}


def load_pelican_settings(base_dir: Path) -> dict:
    """Extract key settings from pelicanconf.py safely without side effects."""
    conf_file = base_dir / "pelicanconf.py"
    settings = {
        "SITEURL": "https://www.aquiles.me",
        "SITENAME": "Aquiles Carattino",
        "LINKEDIN_USERNAME": "aquic",
        "GITHUB_USERNAME": "aquilesC",
        "TWITTER_USERNAME": "",
        "FEED_ALL_RSS": "feed.rss",
        "FEED_ALL_ATOM": "",
    }
    if conf_file.exists():
        with open(conf_file, "r", encoding="utf-8") as f:
            content = f.read()
        for key in list(settings.keys()):
            match = re.search(r'^\s*' + key + r'\s*=\s*[\'"]([^\'"]*)[\'"]', content, re.MULTILINE)
            if match:
                settings[key] = match.group(1)
    return settings


class LinkOccurrence:
    def __init__(self, source_file: str, line_num: Optional[int], tag: str, raw_url: str, src_md: Optional[str] = None):
        self.source_file = source_file
        self.line_num = line_num
        self.tag = tag
        self.raw_url = raw_url
        self.src_md = src_md

    def format_location(self) -> str:
        loc = f"{self.source_file}:{self.line_num}" if self.line_num else self.source_file
        if self.src_md:
            return f"{self.src_md} ({loc})"
        return loc


class LinkChecker:
    def __init__(
        self,
        base_dir: Path,
        content_dir: Path,
        output_dir: Path,
        templates_dir: Optional[Path],
        check_external: bool = True,
        check_internal: bool = True,
        check_templates: bool = True,
        check_anchors: bool = True,
        workers: int = 10,
        timeout: float = 10.0,
        strict: bool = False,
        verbose: bool = False,
        ignore_patterns: Optional[List[str]] = None,
    ):
        self.base_dir = base_dir.resolve()
        self.content_dir = content_dir.resolve()
        self.output_dir = output_dir.resolve()
        self.templates_dir = templates_dir.resolve() if templates_dir else None
        self.check_external = check_external
        self.check_internal = check_internal
        self.check_templates = check_templates
        self.check_anchors = check_anchors
        self.workers = workers
        self.timeout = timeout
        self.strict = strict
        self.verbose = verbose
        self.ignore_regexes = [re.compile(p) for p in (ignore_patterns or [])]

        self.settings = load_pelican_settings(self.base_dir)
        self.site_url = self.settings.get("SITEURL", "").rstrip("/")
        parsed_site = urllib.parse.urlparse(self.site_url)
        self.internal_hosts = {
            "localhost",
            "localhost:8000",
            "127.0.0.1",
            "127.0.0.1:8000",
        }
        if parsed_site.netloc:
            self.internal_hosts.add(parsed_site.netloc)
            if parsed_site.netloc.startswith("www."):
                self.internal_hosts.add(parsed_site.netloc[4:])
            else:
                self.internal_hosts.add(f"www.{parsed_site.netloc}")

        # Map slug/path to markdown source file
        self.slug_to_markdown: Dict[str, str] = {}
        self.index_content_files()

        # Page anchor index: rel_html_path -> set of anchor IDs
        self.page_anchors: Dict[str, Set[str]] = {}

        # URL to occurrences mapping
        self.internal_links: Dict[str, List[LinkOccurrence]] = defaultdict(list)
        self.external_links: Dict[str, List[LinkOccurrence]] = defaultdict(list)

        # SSL Context for external checks
        self.ssl_ctx = ssl.create_default_context()

    def index_content_files(self):
        """Index markdown files in content/ to map output paths back to markdown sources."""
        if not self.content_dir.exists():
            return

        for md_file in self.content_dir.glob("**/*.md"):
            rel_md = str(md_file.relative_to(self.base_dir))
            stem = md_file.stem
            self.slug_to_markdown[stem] = rel_md
            try:
                # Read slug from frontmatter if explicitly given
                content = md_file.read_text(encoding="utf-8", errors="replace")
                slug_match = re.search(r"^[Ss]lug:\s*(.+)$", content, re.MULTILINE)
                if slug_match:
                    slug = slug_match.group(1).strip()
                    self.slug_to_markdown[slug] = rel_md
            except Exception:
                pass

    def get_source_markdown(self, rel_html_path: str) -> Optional[str]:
        """Look up corresponding source markdown file for an output HTML path."""
        # e.g. after-a-failure-.../index.html -> slug 'after-a-failure-...'
        parts = rel_html_path.split("/")
        if len(parts) >= 2 and parts[-1] == "index.html":
            slug = parts[-2]
            if slug in self.slug_to_markdown:
                return self.slug_to_markdown[slug]
        stem = Path(rel_html_path).stem
        if stem in self.slug_to_markdown:
            return self.slug_to_markdown[stem]
        return None

    def should_ignore_url(self, url: str) -> bool:
        if not url or url.strip() == "":
            return True
        if url.startswith(("javascript:", "mailto:", "tel:", "data:", "whatsapp:", "sms:")):
            return True
        if url == "#":
            return True
        parsed = urllib.parse.urlparse(url)
        netloc = parsed.netloc.lower()
        if netloc:
            for ignored in IGNORE_DOMAINS:
                if netloc == ignored or netloc.endswith(f".{ignored}"):
                    return True
        for regex in self.ignore_regexes:
            if regex.search(url):
                return True
        return False

    def is_external_url(self, url: str) -> bool:
        parsed = urllib.parse.urlparse(url)
        if parsed.scheme in ("http", "https"):
            if parsed.netloc.lower() not in self.internal_hosts:
                return True
        return False

    def normalize_internal_url(self, url: str) -> str:
        """Strip internal host scheme/domain if present."""
        parsed = urllib.parse.urlparse(url)
        if parsed.scheme in ("http", "https") and parsed.netloc.lower() in self.internal_hosts:
            rel = parsed.path
            if parsed.params:
                rel += f";{parsed.params}"
            if parsed.query:
                rel += f"?{parsed.query}"
            if parsed.fragment:
                rel += f"#{parsed.fragment}"
            return rel or "/"
        return url

    def scan_output_pages(self) -> int:
        """Scan all generated HTML files in output_dir."""
        if not self.output_dir.exists():
            print(f"{COLOR_YELLOW}Warning: Output directory {self.output_dir} does not exist. Run 'make html' first.{COLOR_RESET}")
            return 0

        html_files = sorted(list(self.output_dir.glob("**/*.html")))
        for fpath in html_files:
            rel_path = str(fpath.relative_to(self.output_dir))
            src_md = self.get_source_markdown(rel_path)
            try:
                content = fpath.read_text(encoding="utf-8", errors="replace")
            except Exception as e:
                print(f"{COLOR_RED}Error reading {fpath}: {e}{COLOR_RESET}")
                continue

            soup = BeautifulSoup(content, "html.parser")

            # Index page anchors
            anchors: Set[str] = set()
            for elem in soup.find_all(True):
                elem_id = elem.get("id")
                if elem_id:
                    anchors.add(elem_id)
                if elem.name == "a" and elem.get("name"):
                    anchors.add(elem.get("name"))
            self.page_anchors[rel_path] = anchors

            # Extract links from <a href>
            for a in soup.find_all("a", href=True):
                raw_url = a["href"].strip()
                if self.should_ignore_url(raw_url):
                    continue
                line = getattr(a, "sourceline", None)
                occ = LinkOccurrence(rel_path, line, "a", raw_url, src_md=src_md)
                if self.is_external_url(raw_url):
                    self.external_links[raw_url].append(occ)
                else:
                    norm_url = self.normalize_internal_url(raw_url)
                    self.internal_links[norm_url].append(occ)

            # Check static internal assets referenced by pages
            for img in soup.find_all("img", src=True):
                raw_url = img["src"].strip()
                if not self.should_ignore_url(raw_url) and not self.is_external_url(raw_url):
                    line = getattr(img, "sourceline", None)
                    norm_url = self.normalize_internal_url(raw_url)
                    self.internal_links[norm_url].append(LinkOccurrence(rel_path, line, "img", raw_url, src_md=src_md))

            for link in soup.find_all("link", href=True):
                raw_url = link["href"].strip()
                rel_attr = link.get("rel", [])
                if isinstance(rel_attr, list):
                    rel_attr = " ".join(rel_attr)
                if any(x in rel_attr for x in ("stylesheet", "icon", "preload")):
                    if not self.should_ignore_url(raw_url) and not self.is_external_url(raw_url):
                        line = getattr(link, "sourceline", None)
                        norm_url = self.normalize_internal_url(raw_url)
                        self.internal_links[norm_url].append(LinkOccurrence(rel_path, line, "link", raw_url, src_md=src_md))

            for script in soup.find_all("script", src=True):
                raw_url = script["src"].strip()
                if not self.should_ignore_url(raw_url) and not self.is_external_url(raw_url):
                    line = getattr(script, "sourceline", None)
                    norm_url = self.normalize_internal_url(raw_url)
                    self.internal_links[norm_url].append(LinkOccurrence(rel_path, line, "script", raw_url, src_md=src_md))

        return len(html_files)

    def scan_templates(self) -> int:
        """Scan raw theme templates for static URLs."""
        if not self.templates_dir or not self.templates_dir.exists():
            return 0

        tmpl_files = sorted(list(self.templates_dir.glob("**/*.html")))
        href_pat = re.compile(r"""(?:href|src)=["']([^"']+)["']""")

        for fpath in tmpl_files:
            rel_path = f"template:{fpath.relative_to(self.templates_dir)}"
            try:
                lines = fpath.read_text(encoding="utf-8", errors="replace").splitlines()
            except Exception as e:
                print(f"{COLOR_RED}Error reading template {fpath}: {e}{COLOR_RESET}")
                continue

            for line_idx, line in enumerate(lines, 1):
                for match in href_pat.finditer(line):
                    raw_url = match.group(1).strip()
                    if self.should_ignore_url(raw_url):
                        continue

                    # Skip pure fragments in templates (e.g. #main, #about) as template inheritance
                    # means DOM is assembled across multiple templates; rendered pages validate this.
                    if raw_url.startswith("#"):
                        continue

                    # Interpolate known config variables
                    interpolated = raw_url
                    interpolated = interpolated.replace("{{ SITEURL }}/", "/")
                    interpolated = interpolated.replace("{{ SITEURL }}", "")
                    for k, v in self.settings.items():
                        if k != "SITEURL" and v:
                            interpolated = interpolated.replace(f"{{{{ {k} }}}}", v)

                    # If URL still contains unresolved Jinja variables (e.g. {{ article.url }}),
                    # it is a dynamic expression evaluated and tested on rendered output.
                    if "{{" in interpolated or "{%" in interpolated:
                        continue

                    if not interpolated:
                        interpolated = "/"

                    occ = LinkOccurrence(rel_path, line_idx, "template", raw_url)
                    if self.is_external_url(interpolated):
                        self.external_links[interpolated].append(occ)
                    else:
                        norm_url = self.normalize_internal_url(interpolated)
                        self.internal_links[norm_url].append(occ)

        return len(tmpl_files)

    def resolve_internal_target(self, source_rel: str, url_path: str) -> Tuple[bool, Optional[Path], str]:
        """
        Resolve internal path against output_dir.
        Returns (exists: bool, resolved_target_html: Optional[Path], error_message: str)
        """
        clean_path = url_path.split("?", 1)[0]
        if not clean_path:
            clean_path = "/"

        # Determine target filesystem path
        if source_rel.startswith("template:"):
            target = self.output_dir / clean_path.lstrip("/")
        elif clean_path.startswith("/"):
            target = self.output_dir / clean_path.lstrip("/")
        else:
            src_dir = (self.output_dir / source_rel).parent
            target = (src_dir / clean_path).resolve()

        # Check if target is inside output_dir
        try:
            target.relative_to(self.output_dir)
        except ValueError:
            return False, None, f"Path traverses outside output directory: {target}"

        # 1. Exact file match (image, css, js, html)
        if target.is_file():
            return True, (target if target.suffix == ".html" else None), ""

        # 2. Directory with index.html
        if target.is_dir():
            if (target / "index.html").is_file():
                return True, target / "index.html", ""
            return False, None, f"Directory exists but missing index.html: {target.name}/"

        # 3. Path without .html extension (e.g. /work -> /work/index.html or /work.html)
        if (target / "index.html").is_file():
            return True, target / "index.html", ""
        if target.with_suffix(".html").is_file():
            return True, target.with_suffix(".html"), ""

        return False, None, f"Target file or page not found: {clean_path}"

    def check_all_internal_links(self) -> Tuple[List[dict], int]:
        """Validate all collected internal links, grouped by URL."""
        broken_map: Dict[str, dict] = {}
        checked_count = 0

        for url, occs in self.internal_links.items():
            checked_count += 1
            url_without_frag, frag = urllib.parse.urldefrag(url)

            # Check occurrences
            for occ in occs:
                source_rel = occ.source_file

                # Case 1: Same-page anchor (#heading)
                if not url_without_frag:
                    if self.check_anchors and frag and not source_rel.startswith("template:"):
                        anchors = self.page_anchors.get(source_rel, set())
                        if frag not in anchors:
                            if url not in broken_map:
                                broken_map[url] = {
                                    "url": url,
                                    "type": "Missing Anchor",
                                    "error": f"Anchor '#{frag}' not found on page",
                                    "occs": [],
                                }
                            broken_map[url]["occs"].append(occ)
                    continue

                # Case 2: Link to internal file / page
                exists, target_html, err_msg = self.resolve_internal_target(source_rel, url_without_frag)
                if not exists:
                    if url not in broken_map:
                        broken_map[url] = {
                            "url": url,
                            "type": "Broken Link (404)",
                            "error": err_msg,
                            "occs": [],
                        }
                    broken_map[url]["occs"].append(occ)
                elif self.check_anchors and frag and target_html and not source_rel.startswith("template:"):
                    target_rel = str(target_html.relative_to(self.output_dir))
                    anchors = self.page_anchors.get(target_rel)
                    if anchors is None and target_html.is_file():
                        try:
                            soup = BeautifulSoup(target_html.read_text(encoding="utf-8", errors="replace"), "html.parser")
                            anchors = {e.get("id") for e in soup.find_all(id=True)}
                            anchors.update({e.get("name") for e in soup.find_all("a", attrs={"name": True})})
                            self.page_anchors[target_rel] = anchors
                        except Exception:
                            anchors = set()

                    if anchors is not None and frag not in anchors:
                        if url not in broken_map:
                            broken_map[url] = {
                                "url": url,
                                "type": "Missing Target Anchor",
                                "error": f"Page exists, but anchor '#{frag}' was not found in {target_html.name}",
                                "occs": [],
                            }
                        broken_map[url]["occs"].append(occ)

        return list(broken_map.values()), checked_count

    def check_single_external_url(self, url: str) -> dict:
        """Check status of a single external URL with realistic headers."""
        headers = {
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        }

        parsed = urllib.parse.urlparse(url)
        domain = parsed.netloc.lower()

        # Handle known tracking/ad domains when blocked by local DNS sinkholes
        is_adblock_domain = any(ad in domain for ad in IGNORE_DOMAINS)

        # 1. Try HEAD first
        head_req = urllib.request.Request(url, headers=headers, method="HEAD")
        try:
            with urllib.request.urlopen(head_req, timeout=self.timeout, context=self.ssl_ctx) as resp:
                status = resp.status
                return {"url": url, "status": status, "state": "OK", "msg": f"HTTP {status}"}
        except urllib.error.HTTPError as e:
            # Fallback to GET for 403, 405, 500, 501, 999
            if e.code in (403, 405, 500, 501, 999):
                try:
                    get_headers = {**headers, "Range": "bytes=0-2048"}
                    get_req = urllib.request.Request(url, headers=get_headers, method="GET")
                    with urllib.request.urlopen(get_req, timeout=self.timeout, context=self.ssl_ctx) as gresp:
                        return {"url": url, "status": gresp.status, "state": "OK", "msg": f"HTTP {gresp.status} (via GET)"}
                except urllib.error.HTTPError as ge:
                    is_anti_bot = any(bad in domain for bad in ANTI_BOT_DOMAINS) or ge.code in (403, 429, 999)
                    if is_anti_bot and not self.strict:
                        return {"url": url, "status": ge.code, "state": "WARNING", "msg": f"HTTP {ge.code} (Anti-bot / Protected Host)"}
                    return {"url": url, "status": ge.code, "state": "BROKEN", "msg": f"HTTP {ge.code} {ge.reason}"}
                except Exception as ge:
                    if any(bad in domain for bad in ANTI_BOT_DOMAINS) and not self.strict:
                        return {"url": url, "status": 0, "state": "WARNING", "msg": f"Access restricted: {ge}"}
                    return {"url": url, "status": 0, "state": "BROKEN", "msg": str(ge)}

            return {"url": url, "status": e.code, "state": "BROKEN", "msg": f"HTTP {e.code} {e.reason}"}
        except urllib.error.URLError as e:
            reason_str = str(e.reason)
            if is_adblock_domain and ("nodename nor servname" in reason_str or "Name or service not known" in reason_str):
                return {"url": url, "status": 0, "state": "WARNING", "msg": "Blocked by local DNS / Adblocker"}
            return {"url": url, "status": 0, "state": "BROKEN", "msg": f"URL Error: {e.reason}"}
        except TimeoutError:
            return {"url": url, "status": 0, "state": "BROKEN", "msg": "Request timed out"}
        except Exception as e:
            return {"url": url, "status": 0, "state": "BROKEN", "msg": str(e)}

    def check_all_external_links(self) -> Tuple[List[dict], List[dict], int]:
        """Validate external links concurrently."""
        unique_urls = sorted(list(self.external_links.keys()))
        if not unique_urls:
            return [], [], 0

        print(f"  {COLOR_CYAN}⚡ Checking {len(unique_urls)} unique external links ({self.workers} workers)...{COLOR_RESET}")
        broken_list = []
        warning_list = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.workers) as executor:
            future_to_url = {executor.submit(self.check_single_external_url, url): url for url in unique_urls}
            for future in concurrent.futures.as_completed(future_to_url):
                res = future.result()
                url = res["url"]
                occs = self.external_links[url]
                if res["state"] == "BROKEN":
                    broken_list.append({"url": url, "type": "External Broken", "error": res["msg"], "occs": occs})
                elif res["state"] == "WARNING":
                    warning_list.append({"url": url, "type": "External Warning", "error": res["msg"], "occs": occs})
                elif self.verbose:
                    print(f"    {COLOR_GREEN}✓{COLOR_RESET} {url} ({res['msg']})")

        return broken_list, warning_list, len(unique_urls)


def print_broken_section(title: str, items: List[dict], is_warning: bool = False):
    color = COLOR_YELLOW if is_warning else COLOR_RED
    icon = "⚠" if is_warning else "✗"
    print(f"\n{color}{COLOR_BOLD}{icon} {title} ({len(items)}):{COLOR_RESET}")

    for item in items:
        url = item["url"]
        err = item["error"]
        print(f"  {color}• {COLOR_BOLD}{url}{COLOR_RESET}")
        print(f"    {COLOR_DIM}Reason: {err}{COLOR_RESET}")

        occs = item.get("occs", [])
        if "occ" in item and not occs:
            occs = [item["occ"]]

        if occs:
            header_count = f"({len(occs)} places)" if len(occs) > 1 else "(1 place)"
            print(f"    {COLOR_DIM}Referenced in {header_count}:{COLOR_RESET}")
            for occ in occs[:5]:
                print(f"      - {occ.format_location()} (<{occ.tag}>)")
            if len(occs) > 5:
                print(f"      - ... and {len(occs) - 5} more")


def main():
    parser = argparse.ArgumentParser(
        description="Check broken internal and external links across Pelican pages and theme templates."
    )
    parser.add_argument("--base-dir", type=Path, default=Path("."), help="Project root directory")
    parser.add_argument("--content-dir", type=Path, default=Path("content"), help="Pelican content directory")
    parser.add_argument("--output-dir", type=Path, default=Path("output"), help="Pelican output directory")
    parser.add_argument(
        "--templates-dir",
        type=Path,
        default=Path("themes/aquiles_theme/templates"),
        help="Theme templates directory",
    )
    parser.add_argument("--internal-only", action="store_true", help="Only check internal links (fast, offline)")
    parser.add_argument("--external-only", action="store_true", help="Only check external links")
    parser.add_argument("--skip-templates", action="store_true", help="Skip checking templates directory")
    parser.add_argument("--skip-anchors", action="store_true", help="Skip checking #hash anchor existence")
    parser.add_argument("--strict", action="store_true", help="Treat 403 anti-bot warnings as broken links")
    parser.add_argument("--workers", type=int, default=10, help="Number of concurrent workers for external links")
    parser.add_argument("--timeout", type=float, default=10.0, help="Timeout in seconds for external requests")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output for passed links")
    parser.add_argument("--no-fail", action="store_true", help="Do not exit with code 1 if broken links are found")
    parser.add_argument("--ignore", nargs="*", default=[], help="Regex patterns of URLs to ignore")

    args = parser.parse_args()

    check_internal = not args.external_only
    check_external = not args.internal_only
    check_templates = not args.skip_templates

    print(f"\n{COLOR_BOLD}{COLOR_CYAN}🔍 Pelican Site Link Checker{COLOR_RESET}")
    print(f"  Root:      {args.base_dir.resolve()}")
    print(f"  Content:   {args.content_dir.resolve()}")
    print(f"  Output:    {args.output_dir.resolve()}")
    if check_templates and args.templates_dir:
        print(f"  Templates: {args.templates_dir.resolve()}")
    print("")

    start_time = time.time()

    checker = LinkChecker(
        base_dir=args.base_dir,
        content_dir=args.content_dir,
        output_dir=args.output_dir,
        templates_dir=args.templates_dir if check_templates else None,
        check_external=check_external,
        check_internal=check_internal,
        check_templates=check_templates,
        check_anchors=not args.skip_anchors,
        workers=args.workers,
        timeout=args.timeout,
        strict=args.strict,
        verbose=args.verbose,
        ignore_patterns=args.ignore,
    )

    # 1. Scan output pages
    page_count = checker.scan_output_pages()
    print(f"  📄 Scanned {COLOR_BOLD}{page_count}{COLOR_RESET} HTML pages in output")

    # 2. Scan templates
    tmpl_count = 0
    if check_templates:
        tmpl_count = checker.scan_templates()
        print(f"  🎨 Scanned {COLOR_BOLD}{tmpl_count}{COLOR_RESET} theme template files")

    print(
        f"  🔗 Discovered {COLOR_BOLD}{len(checker.internal_links)}{COLOR_RESET} unique internal links, "
        f"{COLOR_BOLD}{len(checker.external_links)}{COLOR_RESET} unique external links\n"
    )

    # 3. Check internal links
    broken_internal: List[dict] = []
    checked_internal_count = 0
    if check_internal:
        print(f"  {COLOR_CYAN}Checking internal links & anchors...{COLOR_RESET}")
        broken_internal, checked_internal_count = checker.check_all_internal_links()
        if not broken_internal:
            print(f"    {COLOR_GREEN}✓ All {checked_internal_count} internal links and anchors are valid!{COLOR_RESET}")
        else:
            print_broken_section("BROKEN INTERNAL LINKS", broken_internal)

    # 4. Check external links
    broken_external: List[dict] = []
    warning_external: List[dict] = []
    checked_external_count = 0
    if check_external:
        broken_external, warning_external, checked_external_count = checker.check_all_external_links()
        if warning_external:
            print_broken_section("EXTERNAL WARNINGS (Anti-bot / Rate-limited / Protected)", warning_external, is_warning=True)
        if broken_external:
            print_broken_section("BROKEN EXTERNAL LINKS", broken_external)
        elif not warning_external:
            print(f"    {COLOR_GREEN}✓ All {checked_external_count} external links responded successfully!{COLOR_RESET}")

    elapsed = time.time() - start_time
    total_broken = len(broken_internal) + len(broken_external)

    print(f"\n{COLOR_BOLD}━━━━━━━━━━━━━━━━━━━━━━━━ Summary ━━━━━━━━━━━━━━━━━━━━━━━━{COLOR_RESET}")
    print(f"  Time elapsed:       {elapsed:.2f}s")
    print(f"  Pages checked:      {page_count} HTML files (+ {tmpl_count} templates)")
    if check_internal:
        int_status = f"{COLOR_GREEN}All Valid{COLOR_RESET}" if not broken_internal else f"{COLOR_RED}{len(broken_internal)} Broken{COLOR_RESET}"
        print(f"  Internal Links:     {checked_internal_count} checked ({int_status})")
    if check_external:
        ext_status = f"{COLOR_GREEN}All Valid{COLOR_RESET}" if not broken_external else f"{COLOR_RED}{len(broken_external)} Broken{COLOR_RESET}"
        if warning_external:
            ext_status += f", {COLOR_YELLOW}{len(warning_external)} Warnings{COLOR_RESET}"
        print(f"  External Links:     {checked_external_count} checked ({ext_status})")

    if total_broken > 0:
        print(f"\n{COLOR_RED}{COLOR_BOLD}Result: ❌ Found {total_broken} broken link target(s).{COLOR_RESET}\n")
        if not args.no_fail:
            sys.exit(1)
    else:
        print(f"\n{COLOR_GREEN}{COLOR_BOLD}Result: ✨ Passed! No broken links found.{COLOR_RESET}\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
