import { resolve } from 'node:path';
import { defineConfig } from 'vite';
import fullReload from 'vite-plugin-full-reload';
import autoprefixer from 'autoprefixer';
import pixrem from 'pixrem';
import postcssPresetEnv from 'postcss-preset-env';

// This variable should mirror the one from config/settings/production.py
{%- if cookiecutter.use_whitenoise == 'n' %}
{%- if cookiecutter.cloud_provider == 'AWS' %}
const s3BucketName = process.env.DJANGO_AWS_STORAGE_BUCKET_NAME;
const awsS3Domain = process.env.DJANGO_AWS_S3_CUSTOM_DOMAIN
  ? process.env.DJANGO_AWS_S3_CUSTOM_DOMAIN
  : `${s3BucketName}.s3.amazonaws.com`;
const staticUrl = `https://${awsS3Domain}/static/`;
{%- elif cookiecutter.cloud_provider == 'GCP' %}
const staticUrl = `https://storage.googleapis.com/${process.env.DJANGO_GCP_STORAGE_BUCKET_NAME}/static/`;
{%- elif cookiecutter.cloud_provider == 'Azure' %}
const staticUrl = `https://${process.env.DJANGO_AZURE_ACCOUNT_NAME}.blob.core.windows.net/static/`;
{%- endif %}
{%- else %}
const staticUrl = '/static/';
{%- endif %}

const appDir = '{{cookiecutter.project_slug}}';

// This should mirror DJANGO_VITE["default"]["static_url_prefix"] in config/settings/base.py
const staticUrlPrefix = 'vite_bundles';

// django-vite serves dev assets from STATIC_URL + static_url_prefix, so the dev
// server has to be mounted there too. In production, `base` only rewrites the
// references between built files (CSS url(), dynamic imports, ...) because
// django-vite renders the script and link tags itself.
const devBase = `/static/${staticUrlPrefix}/`;
const buildBase = `${staticUrl}${staticUrlPrefix}/`;

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
      plugins: [postcssPresetEnv(), autoprefixer(), pixrem()],
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
