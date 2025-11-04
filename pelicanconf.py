#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Aquiles'
SITENAME = 'Aquiles'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'America/New_York'

DEFAULT_LANG = 'en'

# Feed settings
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Theme settings
THEME = 'themes/aquiles_theme'

# Template settings
DIRECT_TEMPLATES = ['index', 'archives']
PAGINATED_TEMPLATES = {'index': None, 'tag': None, 'category': None, 'author': None, 'archives': None}
DEFAULT_PAGINATION = 10
ARCHIVES_SAVE_AS = 'articles/index.html'
ARCHIVES_URL = 'articles/'

# URL settings
ARTICLE_URL = 'articles/{slug}/'
ARTICLE_SAVE_AS = 'articles/{slug}/index.html'
PAGE_URL = '{slug}/'
PAGE_SAVE_AS = '{slug}/index.html'
TAG_URL = 'tag/{slug}/'
TAG_SAVE_AS = 'tag/{slug}/index.html'
CATEGORY_URL = 'category/{slug}/'
CATEGORY_SAVE_AS = 'category/{slug}/index.html'

# Static files
# Images in content/images/ will be copied to output/images/
# Reference them in markdown as: ![alt text](/images/filename.png)
STATIC_PATHS = ['images', 'extra']
EXTRA_PATH_METADATA = {
    'extra/robots.txt': {'path': 'robots.txt'},
    'extra/favicon.ico': {'path': 'favicon.ico'},
    'extra/_headers': {'path': '_headers'},
    'extra/_redirects': {'path': '_redirects'},
}

# Exclude templates folder from being parsed as articles/pages
ARTICLE_EXCLUDES = ['templates']
PAGE_EXCLUDES = ['templates']

# Plugin settings
# pelican-yaml-metadata plugin handles YAML frontmatter (--- delimited)
PLUGINS = ['yaml_metadata']

# Markdown extensions
MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.codehilite': {'css_class': 'highlight'},
        'markdown.extensions.extra': {},
        'markdown.extensions.meta': {},
        'markdown.extensions.smarty': {},
    },
    'output_format': 'html5',
}

# Metadata
DEFAULT_METADATA = {
    'status': 'published',
}

# Date format
DEFAULT_DATE_FORMAT = '%B %d, %Y'

# SEO
SITESUBTITLE = 'Personal Editorial Website'
DISPLAY_PAGES_ON_MENU = True
DISPLAY_CATEGORIES_ON_MENU = False
DISPLAY_TAGS_ON_MENU = False

# Custom settings
SITE_TITLE = 'Aquiles'
SITE_DESCRIPTION = 'Personal website featuring essays, work experience, and projects'
TWITTER_USERNAME = None
GITHUB_USERNAME = None

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

