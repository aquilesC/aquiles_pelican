# Cloudflare Pages Deployment Configuration

This document provides the configuration details for deploying this Pelican site to Cloudflare Pages.

## Build Settings

Configure these in the Cloudflare Pages dashboard under **Build settings**:

### Build Configuration
- **Framework preset**: None (or "Static Site")
- **Build command**: 
  ```bash
  pip install -r requirements.txt && npm ci && npm run build:css && pelican content -s publishconf.py
  ```
- **Build output directory**: `output`
- **Root directory**: (leave empty or set to `/`)

### Environment Variables

Set these in the Cloudflare Pages dashboard under **Settings > Environment variables**:

#### Production
- `PYTHON_VERSION`: `3.13`
- `NODE_VERSION`: `20`
- `NPM_FLAGS`: `--prefer-offline --no-audit`

#### Preview Deploys (optional)
- `PYTHON_VERSION`: `3.13`
- `NODE_VERSION`: `20`
- `NPM_FLAGS`: `--prefer-offline --no-audit`

### Build Command by Context

#### Production (main branch)
```bash
pip install -r requirements.txt && npm ci && npm run build:css && pelican content -s publishconf.py
```

#### Preview Deploys (pull requests, branches)
```bash
pip install -r requirements.txt && npm ci && npm run build:css && pelican content -s pelicanconf.py
```

Note: Production uses `publishconf.py` (with absolute URLs), while previews use `pelicanconf.py` (with relative URLs).

## Files Included

### `_headers` File
Located in `content/extra/_headers`, this file is automatically copied to the output root and provides:
- Security headers (X-Frame-Options, X-XSS-Protection, etc.)
- Cache control headers for static assets

### `_redirects` File
Located in `content/extra/_redirects`, this file is automatically copied to the output root for URL redirects. Add redirects as needed using the format:
```
/old-path /new-path 301
```

## Deployment Steps

1. **Connect Repository**
   - Go to Cloudflare Dashboard > Pages
   - Click "Create a project" > "Connect to Git"
   - Select your repository

2. **Configure Build Settings**
   - Use the build command and settings specified above
   - Set the output directory to `output`
   - Add environment variables as listed

3. **Deploy**
   - Cloudflare will automatically build and deploy on every push to the main branch
   - Preview deployments are created for pull requests

## Custom Domain

After deployment:
1. Go to **Custom domains** in the Pages project settings
2. Add your domain (e.g., `www.aquiles.me`)
3. Update DNS records as instructed by Cloudflare

## Build Optimization

- Uses `npm ci` instead of `npm install` for faster, reproducible builds
- Python dependencies are cached between builds automatically
- Node modules are cached between builds automatically

## Troubleshooting

### Build Fails
- Verify Python version matches `runtime.txt` (3.13)
- Check that all dependencies in `requirements.txt` are valid
- Ensure `package.json` and `package-lock.json` are committed

### Missing Headers/Redirects
- Verify `EXTRA_PATH_METADATA` in `pelicanconf.py` includes the `_headers` and `_redirects` entries
- Check that files exist in `content/extra/`

### CSS Not Building
- Ensure TailwindCSS is installed: `npm ci`
- Check `package.json` scripts are correct
- Verify `tailwind.config.js` exists

