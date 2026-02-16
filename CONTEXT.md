# Project Context & Workflows

## Styling & TailwindCSS
This project uses **TailwindCSS** for styling.

### Important Rules
- **NEVER edit `themes/aquiles_theme/static/css/style.css` directly.** This file is auto-generated.
- **ALWAYS edit `themes/aquiles_theme/static/css/src/input.css`** for any styling changes.

### Workflow
1.  Modify `themes/aquiles_theme/static/css/src/input.css`.
2.  The `npm run watch:css` script (if running) will automatically rebuild `style.css`.
3.  If not running, you can manually build with `npm run build:css`.

## Development Commands
- `npm run watch:css`: Watches `input.css` and rebuilds `style.css` on change.
- `pelican content -s pelicanconf.py -r`: Runs Pelican in autoreload mode.
- `python -m http.server`: Serves the `output` directory.
