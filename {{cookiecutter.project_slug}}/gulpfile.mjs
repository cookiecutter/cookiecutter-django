////////////////////////////////
// Setup
////////////////////////////////

// Gulp and package
import { src, dest, parallel, series, task, watch } from 'gulp';
import pjson from './package.json' with {type: 'json'};

// Plugins
import autoprefixer from 'autoprefixer';
import browserSyncLib from 'browser-sync';
import concat from 'gulp-concat';
import tildeImporter from 'node-sass-tilde-importer';
import cssnano from 'cssnano';
import pixrem from 'pixrem';
import plumber from 'gulp-plumber';
import postcss from 'gulp-postcss';
import rename from 'gulp-rename';
import gulpSass from 'gulp-sass';
import * as dartSass from 'sass';
import gulUglifyES from 'gulp-uglify-es';
import { spawn } from 'node:child_process';

const browserSync = browserSyncLib.create();
const reload = browserSync.reload;
const sass = gulpSass(dartSass);
const uglify = gulUglifyES.default;

// Relative paths function
function pathsConfig() {
  const appName = `./${pjson.name}`;
  const vendorsRoot = 'node_modules';

  return {
    vendorsJs: [
      `${vendorsRoot}/@popperjs/core/dist/umd/popper.js`,
      `${vendorsRoot}/bootstrap/dist/js/bootstrap.js`,
    ],
    app: appName,
    templates: `${appName}/templates`,
    css: `${appName}/static/css`,
    sass: `${appName}/static/sass`,
    fonts: `${appName}/static/fonts`,
    images: `${appName}/static/images`,
    js: `${appName}/static/js`,
  };
}

const paths = pathsConfig();

////////////////////////////////
// Tasks
////////////////////////////////

// Styles autoprefixing and minification
function styles() {
  const processCss = [
    autoprefixer(), // adds vendor prefixes
    pixrem(), // add fallbacks for rem units
  ];

  const minifyCss = [
    cssnano({ preset: 'default' }), // minify result
  ];

  return src(`${paths.sass}/project.scss`)
    .pipe(
      sass({
        importer: tildeImporter,
        includePaths: [paths.sass],
      }).on('error', sass.logError),
    )
    .pipe(plumber()) // Checks for errors
    .pipe(postcss(processCss))
    .pipe(dest(paths.css))
    .pipe(rename({ suffix: '.min' }))
    .pipe(postcss(minifyCss)) // Minifies the result
    .pipe(dest(paths.css));
}

// Javascript minification
function scripts() {
  return src(`${paths.js}/project.js`)
    .pipe(plumber()) // Checks for errors
    .pipe(uglify()) // Minifies the js
    .pipe(rename({ suffix: '.min' }))
    .pipe(dest(paths.js));
}

// Vendor Javascript minification
function vendorScripts() {
  return src(paths.vendorsJs, { sourcemaps: true })
    .pipe(concat('vendors.js'))
    .pipe(dest(paths.js))
    .pipe(plumber()) // Checks for errors
    .pipe(uglify()) // Minifies the js
    .pipe(rename({ suffix: '.min' }))
    .pipe(dest(paths.js, { sourcemaps: '.' }));
}

// Image compression
async function imgCompression() {
  const imagemin = (await import("gulp-imagemin")).default;
  return src(`${paths.images}/*`)
    .pipe(imagemin()) // Compresses PNG, JPEG, GIF and SVG images
    .pipe(dest(paths.images));
}

{%- if cookiecutter.use_async == 'y' -%}
// Run django server
function asyncRunServer() {
  const cmd = spawn(
    'gunicorn',
    ['config.asgi', '-k', 'uvicorn_worker.UvicornWorker', '--reload'],
    {stdio: 'inherit'},
  );
  cmd.on('close', function (code) {
    console.log('gunicorn exited with code ' + code);
  })
}
{%- else %}
// Run django server
function runServer(cb) {
  const cmd = spawn('python', ['manage.py', 'runserver'], { stdio: 'inherit' });
  cmd.on('close', function (code) {
    console.log('runServer exited with code ' + code);
    cb(code);
  });
}
{%- endif %}

// Browser sync server for live reload
function initBrowserSync() {
  browserSync.init(
    [`${paths.css}/*.css`, `${paths.js}/*.js`, `${paths.templates}/*.html`],
    {
      {%- if cookiecutter.use_docker == 'y' %}
      // https://www.browsersync.io/docs/options/#option-open
      // Disable as it doesn't work from inside a container
      open: false,
      {%- endif %}
      // https://www.browsersync.io/docs/options/#option-proxy
      proxy: {
        {%- if cookiecutter.use_docker == 'n' %}
        target: '127.0.0.1:8000',
        {%- else %}
        target: 'django:8000',
        {%- endif %}
        proxyReq: [
          function (proxyReq, req) {
            // Assign proxy 'host' header same as current request at Browsersync server
            proxyReq.setHeader('Host', req.headers.host);
          },
        ],
      },
    },
  );
}

// Watch
function watchPaths() {
  watch(`${paths.sass}/*.scss`{% if cookiecutter.windows == 'y' %}, { usePolling: true }{% endif %}, styles);
  watch(`${paths.templates}/**/*.html`{% if cookiecutter.windows == 'y' %}, { usePolling: true }{% endif %}).on('change', reload);
  watch([`${paths.js}/*.js`, `!${paths.js}/*.min.js`]{% if cookiecutter.windows == 'y' %}, { usePolling: true }{% endif %}, scripts).on(
    'change',
    reload,
  );
}

// Generate all assets
const build = parallel(styles, scripts, vendorScripts, imgCompression);

// Set up dev environment
{%- if cookiecutter.use_docker == 'n' %}
{%- if cookiecutter.use_async == 'y' %}
const dev = parallel(asyncRunServer, initBrowserSync, watchPaths);
{%- else %}
const dev = parallel(runServer, initBrowserSync, watchPaths);
{%- endif %}
{%- else %}
const dev = parallel(initBrowserSync, watchPaths);
{%- endif %}

task('default', series(build, dev));
task('build', build);
task('dev', dev);
