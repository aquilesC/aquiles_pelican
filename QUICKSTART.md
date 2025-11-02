# Quick Start Guide

## Initial Setup

1. **Activate the virtual environment:**
   ```bash
   source .venv/bin/activate
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Node dependencies:**
   ```bash
   npm install
   ```

4. **Build TailwindCSS:**
   ```bash
   npm run build:css
   ```

5. **Generate the site:**
   ```bash
   pelican content -s pelicanconf.py
   ```

6. **Preview locally (optional):**
   ```bash
   cd output && python -m pelican.server
   ```
   Then visit http://localhost:8000

## Development Workflow

### Adding New Articles

Create a new Markdown file in `content/articles/` with metadata:

```markdown
Title: My Article Title
Slug: my-article-slug
Date: 2024-01-20
Category: Category Name
Tags: tag1, tag2
Summary: Brief summary of the article

# Article Content

Your article content goes here in Markdown format.
```

### Adding New Pages

Create a new Markdown file in `content/pages/`:

```markdown
Title: Page Title
Slug: page-slug
Date: 2024-01-20

# Page Content

Your page content here.
```

### Customizing Pages

- **Work page**: Edit `content/pages/work.md`
- **Contact page**: The form template is in `themes/aquiles_theme/templates/contact.html`
- **Homepage**: Edit `themes/aquiles_theme/templates/index.html`

### Building CSS

- **One-time build**: `npm run build:css`
- **Watch mode** (auto-rebuild on changes): `npm run watch:css`

## Using Make

For convenience, you can use the Makefile:

```bash
make html        # Build site + CSS
make css         # Build CSS only
make watch       # Watch CSS
make serve       # Serve locally
make clean       # Remove output directory
make publish     # Build for production
```

## Netlify Deployment

1. Push your code to a Git repository
2. Connect the repository to Netlify
3. Netlify will automatically:
   - Install dependencies
   - Build CSS
   - Generate the site
   - Process forms

The `netlify.toml` file is already configured for this workflow.

## Customization

### Design Tokens

Edit `tailwind.config.js` to customize colors, typography, and spacing according to `design_brief.json`.

### Navigation

Edit `themes/aquiles_theme/templates/includes/header.html` to modify navigation links.

### Site Settings

Edit `pelicanconf.py` to change:
- Site name and author
- URLs and paths
- Feed settings
- Social media usernames

## Next Steps

1. Replace sample content with your own
2. Add your work experience to `content/pages/work.md`
3. Customize the homepage in `themes/aquiles_theme/templates/index.html`
4. Add your social media handles in `pelicanconf.py`
5. Add a favicon to `content/extra/favicon.ico`

