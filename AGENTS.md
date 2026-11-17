# Project Agent Guidelines

## Python Virtual Environment
- **Always activate the virtual environment before running any Python commands or tools**:
  ```bash
  source .venv/bin/activate
  ```
  Alternatively, explicitly use `.venv/bin/python`, `.venv/bin/pip`, or `.venv/bin/pelican`.
- Never install Python packages globally or outside `.venv`.
- The Python version is pinned in `.python-version` / `runtime.txt` to match Cloudflare's build image (currently 3.14.8). Build the venv with a uv-managed interpreter so Homebrew upgrades cannot break it:
  ```bash
  uv venv --seed --python "$(cat .python-version)" .venv && .venv/bin/pip install -r requirements.txt
  ```

## Project Overview
- Static website built with Pelican and TailwindCSS.
- Node.js / npm is used for building and compiling TailwindCSS styles.
- Main theme is located in `themes/aquiles_theme/`.

## Key Commands
- CSS build: `npm run build:css`
- Site generation: `source .venv/bin/activate && make html` (or `make publish`)
- Open Graph images: `source .venv/bin/activate && make og-images`
- Development server: `source .venv/bin/activate && make serve`
- Link checking: `source .venv/bin/activate && make check-links` (or `make check-links-internal`)
