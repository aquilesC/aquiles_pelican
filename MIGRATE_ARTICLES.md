# Article Migration Guide

I've created Markdown template files for all 19 articles from your WordPress site. Here's what has been done:

## Created Files

### Already Completed (with content):
1. ✅ `solve-or-remove-a-problem.md` - Full content converted
2. ✅ `effectual-reasoning-a-framework-for-aspiring-scipreneurs.md` - Full content converted

### Templates Created (need content):
3. `entrepreneurial-mindset-for-scientists.md`
4. `do-things-that-can-scale.md`
5. `how-to-incentivize-scipreneurship.md`
6. `professors-can-enable-scipreneurs.md`
7. `my-story-as-a-founder-from-scientist-to-entrepreneur.md`
8. `mentor-consultant-coach-partner-who-do-you-need-right-now.md`
9. `empowering-young-scientists-rethinking-academic-entrepreneurship.md`
10. `exciting-vesicles-the-field-where-biology-meets-technology.md`
11. `the-path-to-surface-enhanced-raman-for-exosome-characterization.md`
12. `how-it-feels-quitting-your-own-startup.md`
13. `the-things-i-miss-the-most-from-my-time-as-a-phd.md`
14. `there-and-back-again-13-years-apart.md`
15. `what-does-the-creation-of-altos-labs-mean.md`
16. `how-to-write-a-good-cover-letter-for-a-job.md`
17. `how-to-present-yourself-in-a-cv.md`
18. `how-to-write-a-programming-book.md`
19. `after-a-failure-revert-to-the-last-known-working-state.md`

## How to Add Content

### Option 1: Manual Copy-Paste (Recommended)
1. Open each article on https://www.aquiles.me
2. Copy the main content (excluding header/footer)
3. Open the corresponding `.md` file in `content/articles/`
4. Replace the `<!-- TODO: Add content from WordPress site -->` section with the content
5. Format as Markdown (convert headings, lists, links, etc.)

### Option 2: Use WordPress Export
1. Go to WordPress Admin → Tools → Export
2. Export all posts
3. Use a tool like `wordpress-to-markdown` converter
4. Import the converted markdown files

### Option 3: Use a Web Scraper
You can use a Python script with libraries like `requests` and `beautifulsoup4` to fetch content:

```python
import requests
from bs4 import BeautifulSoup

url = "https://www.aquiles.me/solve-or-remove-a-problem/"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Find the main article content
article_content = soup.find('article') or soup.find(class_='entry-content')
# Extract and convert to markdown
```

## Markdown Format Tips

- **Headings**: Use `#`, `##`, `###` for headings
- **Bold**: `**text**` or `__text__`
- **Italic**: `*text*` or `_text_`
- **Links**: `[text](url)`
- **Lists**: Use `-` or `*` for unordered, numbers for ordered
- **Code**: `` `code` `` for inline, triple backticks for blocks

## Metadata Fields

Each file has metadata at the top:
- `Title`: Article title
- `Slug`: URL-friendly version (auto-generated from URL)
- `Date`: Publication date (needs to be updated)
- `Category`: Main category
- `Tags`: Comma-separated tags (needs to be updated)
- `Summary`: Brief description for listings (needs to be added)

## Next Steps

1. Fill in the content for each template file
2. Update dates, tags, and summaries
3. Add any images to `content/images/` and reference them
4. Regenerate the site: `pelican content -s pelicanconf.py`
5. Review and polish the content

## Notes

- Original WordPress URLs are preserved in comments at the bottom of each file
- Dates are set to 2024-01-01 as placeholder - update with actual publication dates
- Tags are empty - add relevant tags from your WordPress site
- Images will need to be downloaded and placed in `content/images/`

