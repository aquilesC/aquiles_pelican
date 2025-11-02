# Aquiles Personal Website

A static website built with Pelican, styled with TailwindCSS, inspired by GatesNotes design principles.

## Project Overview

This is a personal publishing platform combining essays, work experience, and projects. The design emphasizes reading comfort, clean typography, and a modern editorial aesthetic.

## Tech Stack

- **Static Site Generator**: Pelican (Python)
- **Templating**: Jinja2
- **Styling**: TailwindCSS
- **Form Handling**: Netlify Forms
- **Deployment**: Static hosting (Netlify compatible)

## Project Structure

```
aquiles_pelican/
├── content/              # Content files (articles, pages)
│   ├── pages/           # Static pages (work, contact, etc.)
│   └── articles/        # Blog articles
├── themes/              # Custom Pelican theme
│   └── aquiles_theme/
│       ├── templates/   # Jinja2 templates
│       ├── static/      # CSS, JS, images
│       └── theme.conf  # Theme metadata
├── pelicanconf.py       # Pelican configuration
├── publishconf.py       # Production settings
├── requirements.txt     # Python dependencies
├── package.json         # Node dependencies (TailwindCSS)
├── tailwind.config.js   # TailwindCSS configuration
└── design_brief.json    # Design specifications

```

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js 14+
- npm or yarn

### Installation

1. Activate the virtual environment (if using `.venv`):
```bash
source .venv/bin/activate
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Install Node dependencies:
```bash
npm install
```

4. Build TailwindCSS:
```bash
npm run build:css
```

5. Generate the site:
```bash
pelican content -s pelicanconf.py
```

6. Serve locally (optional):
```bash
pelican --listen
```

## Development

### Content Management

- Write articles in `content/articles/` using Markdown
- Create pages in `content/pages/` using Markdown
- Articles support metadata (title, date, tags, categories, etc.)

### Styling

- TailwindCSS is configured with design tokens from `design_brief.json`
- Build CSS: `npm run build:css`
- Watch mode: `npm run watch:css`

### Design System

The design follows specifications in `design_brief.json`:
- Color palette: Blue accent (#1E88E5), high contrast text
- Typography: Serif headings, neutral sans body (18px base)
- Layout: 12-column grid, max-width 1200px
- Spacing: Consistent scale (4px to 48px)

## Deployment

The site generates static HTML files to `output/` directory.

For Netlify deployment:
1. Set build command: `pelican content -s publishconf.py && npm run build:css`
2. Set publish directory: `output`
3. Netlify Forms will automatically process forms

## Features

- Home page with featured content
- Articles/blog listing
- Work experience showcase
- Contact form (Netlify Forms)
- Responsive design
- Accessibility features (AA/AAA contrast)
- SEO optimized

## License

Personal project - All rights reserved

