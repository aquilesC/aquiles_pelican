#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Generate Open Graph (OG) images for articles.
Reads article markdown files, extracts title and summary,
and generates OG images using an SVG template.
"""

import os
import re
import glob
import argparse
from pathlib import Path
import cairosvg
from typing import Dict, Optional


# Design system colors
ACCENT_COLOR = "#1E88E5"
TEXT_PRIMARY = "#111111"
TEXT_SECONDARY = "#4A4A4A"
BACKGROUND_COLOR = "#FFFFFF"

# OG image dimensions (standard Open Graph size)
OG_WIDTH = 1200
OG_HEIGHT = 630

# Paths
ARTICLES_DIR = Path("content/articles")
OUTPUT_DIR = Path("content/images/og")
TEMPLATE_PATH = Path("og_template.svg")


def parse_article_metadata(md_file: Path) -> Dict[str, Optional[str]]:
    """Parse Pelican-style metadata from markdown file."""
    metadata = {
        "title": None,
        "summary": None,
        "slug": None
    }
    
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract metadata (key: value format)
    title_match = re.search(r'^Title:\s*(.+)$', content, re.MULTILINE)
    summary_match = re.search(r'^Summary:\s*(.+)$', content, re.MULTILINE)
    slug_match = re.search(r'^Slug:\s*(.+)$', content, re.MULTILINE)
    
    if title_match:
        metadata["title"] = title_match.group(1).strip()
    if summary_match:
        metadata["summary"] = summary_match.group(1).strip()
    if slug_match:
        metadata["slug"] = slug_match.group(1).strip()
    
    return metadata


def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """Truncate text to max length, adding suffix if truncated."""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)].rsplit(' ', 1)[0] + suffix


def escape_svg_text(text: str) -> str:
    """Escape special characters for SVG."""
    return (text
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&apos;"))


def wrap_text(text: str, max_width: int, font_size: int = 48) -> list:
    """Simple text wrapping for SVG (approximate character width)."""
    # Approximate: characters per line = max_width / (font_size * 0.6)
    chars_per_line = int(max_width / (font_size * 0.6))
    words = text.split()
    lines = []
    current_line = []
    current_length = 0
    
    for word in words:
        word_length = len(word) + 1  # +1 for space
        if current_length + word_length > chars_per_line and current_line:
            lines.append(" ".join(current_line))
            current_line = [word]
            current_length = word_length
        else:
            current_line.append(word)
            current_length += word_length
    
    if current_line:
        lines.append(" ".join(current_line))
    
    return lines[:5]  # Max 5 lines for title, 3 for summary


def generate_svg_content(title: str, summary: Optional[str]) -> str:
    """Generate SVG content from template with title and summary."""
    # Truncate and escape text
    title_truncated = truncate_text(title, 80)
    title_lines = wrap_text(title_truncated, OG_WIDTH - 160, font_size=64)
    
    summary_text = ""
    summary_lines = []
    if summary:
        summary_truncated = truncate_text(summary, 150)
        summary_lines = wrap_text(summary_truncated, OG_WIDTH - 160, font_size=32)
    
    # Build SVG
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{OG_WIDTH}" height="{OG_HEIGHT}" xmlns="http://www.w3.org/2000/svg">
  <!-- Background -->
  <rect width="{OG_WIDTH}" height="{OG_HEIGHT}" fill="{BACKGROUND_COLOR}"/>
  
  <!-- Accent bar on left -->
  <rect x="0" y="0" width="8" height="{OG_HEIGHT}" fill="{ACCENT_COLOR}"/>
  
  <!-- Title -->
  <g transform="translate(80, 140)">
'''
    
    # Add title lines
    for i, line in enumerate(title_lines):
        svg += f'''    <text x="0" y="{i * 85}" font-family="Georgia, serif" font-size="64" font-weight="700" fill="{TEXT_PRIMARY}">
      {escape_svg_text(line)}
    </text>
'''
    
    svg += '  </g>\n'
    
    # Add summary if available
    if summary_lines:
        svg += '  <!-- Summary -->\n'
        svg += f'  <g transform="translate(80, {200 + len(title_lines) * 85})">\n'
        for i, line in enumerate(summary_lines):
            svg += f'''    <text x="0" y="{i * 45}" font-family="system-ui, -apple-system, sans-serif" font-size="32" fill="{TEXT_SECONDARY}">
      {escape_svg_text(line)}
    </text>
'''
        svg += '  </g>\n'
    
    svg += '</svg>\n'
    
    return svg


def generate_og_image(article_file: Path, output_dir: Path, force: bool = False):
    """Generate OG image for a single article."""
    metadata = parse_article_metadata(article_file)
    
    if not metadata["title"]:
        print(f"⚠️  Skipping {article_file.name}: No title found")
        return
    
    if not metadata["slug"]:
        print(f"⚠️  Skipping {article_file.name}: No slug found")
        return
    
    # Output filename
    output_file = output_dir / f"{metadata['slug']}.png"
    
    # Skip if file exists and force is not set
    if output_file.exists() and not force:
        print(f"⏭️  Skipping {metadata['title']}: Image already exists (use --force to regenerate)")
        return
    
    print(f"📝 Processing: {metadata['title']}")
    
    # Generate SVG content
    svg_content = generate_svg_content(metadata["title"], metadata.get("summary"))
    
    # Convert SVG to PNG
    try:
        cairosvg.svg2png(
            bytestring=svg_content.encode('utf-8'),
            write_to=str(output_file),
            output_width=OG_WIDTH,
            output_height=OG_HEIGHT
        )
        print(f"✅ Generated: {output_file}")
    except Exception as e:
        print(f"❌ Error generating {output_file}: {e}")


def generate_default_og_image(output_dir: Path, force: bool = False):
    """Generate default sitewide Open Graph card (1200x630)."""
    output_file = output_dir / "default.png"
    if output_file.exists() and not force:
        print(f"⏭️  Skipping default OG image: already exists (use --force to regenerate)")
        return

    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{OG_WIDTH}" height="{OG_HEIGHT}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#071a36"/>
      <stop offset="50%" stop-color="#0d2f5c"/>
      <stop offset="100%" stop-color="#154a8a"/>
    </linearGradient>
  </defs>
  <rect width="{OG_WIDTH}" height="{OG_HEIGHT}" fill="url(#bg)"/>
  <rect x="0" y="0" width="12" height="{OG_HEIGHT}" fill="#6ab4f8"/>
  <text x="88" y="150" font-family="system-ui, -apple-system, sans-serif" font-size="24" font-weight="600" letter-spacing="3" fill="#6ab4f8">
    DELFT, NETHERLANDS · DEEP-TECH LEADERSHIP
  </text>
  <text x="88" y="255" font-family="Georgia, serif" font-size="76" font-weight="700" fill="#ffffff">
    Aquiles Carattino
  </text>
  <text x="88" y="340" font-family="system-ui, -apple-system, sans-serif" font-size="34" font-weight="500" fill="#e2e8f0">
    Team Lead, Product Development @ Orange Quantum Systems
  </text>
  <text x="88" y="405" font-family="system-ui, -apple-system, sans-serif" font-size="28" fill="#cbd5e1">
    Quantum Chip Testing · Scientific Instrumentation · Ex-Founder &amp; Author
  </text>
  <line x1="88" y1="490" x2="1112" y2="490" stroke="#6ab4f8" stroke-opacity="0.35" stroke-width="2"/>
  <text x="88" y="548" font-family="system-ui, -apple-system, sans-serif" font-size="26" font-weight="600" fill="#ffffff">
    www.aquiles.me
  </text>
  <text x="1112" y="548" text-anchor="end" font-family="system-ui, -apple-system, sans-serif" font-size="24" fill="#94a3b8">
    linkedin.com/in/aquic
  </text>
</svg>
'''
    try:
        cairosvg.svg2png(
            bytestring=svg.encode('utf-8'),
            write_to=str(output_file),
            output_width=OG_WIDTH,
            output_height=OG_HEIGHT
        )
        print(f"✅ Generated default OG image: {output_file}")
    except Exception as e:
        print(f"❌ Error generating {output_file}: {e}")


def main():
    """Main function to generate OG images for all articles."""
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Generate Open Graph (OG) images for articles"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Regenerate images even if they already exist"
    )
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    generate_default_og_image(OUTPUT_DIR, force=args.force)
    
    # Find all markdown files in articles directory
    article_files = list(ARTICLES_DIR.glob("*.md"))
    
    if not article_files:
        print(f"⚠️  No markdown files found in {ARTICLES_DIR}")
        return
    
    print(f"🎨 Generating OG images for {len(article_files)} articles...\n")
    
    for article_file in sorted(article_files):
        generate_og_image(article_file, OUTPUT_DIR, force=args.force)
    
    print(f"\n✨ Done! Generated images saved to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
