import { resolve } from 'node:path';
import { defineConfig } from 'vite';
import fullReload from 'vite-plugin-full-reload';
import autoprefixer from 'autoprefixer';
import postcssPresetEnv from 'postcss-preset-env';

const appDir = '{{cookiecutter.project_slug}}';

// This should mirror DJANGO_VITE["default"]["static_url_prefix"] in config/settings/base.py
const staticUrlPrefix = 'vite_bundles';

// django-vite serves dev assets from STATIC_URL + static_url_prefix, so the dev
// server has to be mounted there too. In production, a relative `base` makes the
// references between built files (CSS url(), dynamic imports, ...) resolve at
// runtime, wherever the static files are served from, because django-vite
// renders the script and link tags itself.
const devBase = `/static/${staticUrlPrefix}/`;
const buildBase = './';

export default defineConfig(({ command }) => ({
  base: command === 'serve' ? devBase : buildBase,
  plugins: [fullReload([`${appDir}/templates/**/*.html`])],
  build: {
    manifest: 'manifest.json',
    outDir: resolve(import.meta.dirname, appDir, 'static', staticUrlPrefix),
    emptyOutDir: true,
    sourcemap: true,
    rollupOptions: {
      input: {
        project: resolve(import.meta.dirname, appDir, 'static/js/project.js'),
        vendors: resolve(import.meta.dirname, appDir, 'static/js/vendors.js'),
      },
    },
  },
  css: {
    postcss: {
      plugins: [postcssPresetEnv(), autoprefixer()],
    },
  },
  server: {
    port: 5173,
    {%- if cookiecutter.use_docker == 'y' %}
    // Listen on all interfaces so the dev server is reachable from the host
    host: true,
    // The browser reaches the dev server through the port published by Compose
    origin: 'http://localhost:5173',
    {%- endif %}
    {%- if cookiecutter.windows == 'y' %}
    watch: {
      usePolling: true,
    },
    {%- endif %}
  },
}));
