////////////////////////////////
// Setup
////////////////////////////////

// Gulp and package
const { src, dest, parallel, series, watch } = require('gulp')
const pjson = require('./package.json')

// Plugins
const autoprefixer = require('autoprefixer')
const browserSync = require('browser-sync').create()
{% if cookiecutter.custom_bootstrap_compilation == 'y' %}
const concat = require('gulp-concat')
{% endif %}
const cssnano = require ('cssnano')
const imagemin = require('gulp-imagemin')
const pixrem = require('pixrem')
const plumber = require('gulp-plumber')
const postcss = require('gulp-postcss')
const reload = browserSync.reload
const rename = require('gulp-rename')
const sass = require('gulp-sass')
const spawn = require('child_process').spawn
const uglify = require('gulp-uglify-es').default

// Relative paths function
function pathsConfig(appName) {
  this.app = `./${pjson.name}`
  const vendorsRoot = 'node_modules'

  return {
    {%- if cookiecutter.custom_bootstrap_compilation == 'y' %}
    bootstrapSass: `${vendorsRoot}/bootstrap/scss`,
    vendorsJs: [
      `${vendorsRoot}/jquery/dist/jquery.slim.js`,
      `${vendorsRoot}/popper.js/dist/umd/popper.js`,
      `${vendorsRoot}/bootstrap/dist/js/bootstrap.js`,
    ],
    {%- endif %}
    app: this.app,
    templates: `${this.app}/templates`,
    css: `${this.app}/static/css`,
    sass: `${this.app}/static/sass`,
    fonts: `${this.app}/static/fonts`,
    images: `${this.app}/static/images`,
    js: `${this.app}/static/js`,
  }
}

var paths = pathsConfig()

////////////////////////////////
// Tasks
////////////////////////////////

// Styles autoprefixing and minification
function styles() {
  var processCss = [
      autoprefixer(), // adds vendor prefixes
      pixrem(),       // add fallbacks for rem units
  ]

  var minifyCss = [
      cssnano({ preset: 'default' })   // minify result
  ]

  return src(`${paths.sass}/project.scss`)
    .pipe(sass({
      includePaths: [
        {%- if cookiecutter.custom_bootstrap_compilation == 'y' %}
        paths.bootstrapSass,
        {%- endif %}
        paths.sass
      ]
    }).on('error', sass.logError))
    .pipe(plumber()) // Checks for errors
    .pipe(postcss(processCss))
    .pipe(dest(paths.css))
    .pipe(rename({ suffix: '.min' }))
    .pipe(postcss(minifyCss)) // Minifies the result
    .pipe(dest(paths.css))
}

// Javascript minification
function scripts() {
  return src(`${paths.js}/project.js`)
    .pipe(plumber()) // Checks for errors
    .pipe(uglify()) // Minifies the js
    .pipe(rename({ suffix: '.min' }))
    .pipe(dest(paths.js))
}

{%- if cookiecutter.custom_bootstrap_compilation == 'y' %}
// Vendor Javascript minification
function vendorScripts() {
  return src(paths.vendorsJs)
    .pipe(concat('vendors.js'))
    .pipe(dest(paths.js))
    .pipe(plumber()) // Checks for errors
    .pipe(uglify()) // Minifies the js
    .pipe(rename({ suffix: '.min' }))
    .pipe(dest(paths.js))
}
{%- endif %}

// Image compression
function imgCompression() {
  return src(`${paths.images}/*`)
    .pipe(imagemin()) // Compresses PNG, JPEG, GIF and SVG images
    .pipe(dest(paths.images))
}

{%- if cookiecutter.use_async == 'y' -%}
// Run django server
function asyncRunServer() {
  var cmd = spawn('gunicorn', [
      'config.asgi', '-k', 'uvicorn.workers.UvicornWorker', '--reload'
      ], {stdio: 'inherit'}
  )
  cmd.on('close', function(code) {
    console.log('gunicorn exited with code ' + code)
  })
}
{%- else %}
// Run django server
function runServer(cb) {
  var cmd = spawn('python', ['manage.py', 'runserver'], {stdio: 'inherit'})
  cmd.on('close', function(code) {
    console.log('runServer exited with code ' + code)
    cb(code)
  })
}
{%- endif %}

// Browser sync server for live reload
function initBrowserSync() {
    browserSync.init(
      [
        `${paths.css}/*.css`,
        `${paths.js}/*.js`,
        `${paths.templates}/*.html`
      ], {
        // https://www.browsersync.io/docs/options/#option-proxy
        {%- if cookiecutter.use_docker == 'n' %}
        proxy: 'localhost:8000'
        {%- else %}
        proxy:  {
          target: 'django:8000',
          proxyReq: [
            function(proxyReq, req) {
              // Assign proxy "host" header same as current request at Browsersync server
              proxyReq.setHeader('Host', req.headers.host)
            }
          ]
        },
        // https://www.browsersync.io/docs/options/#option-open
        // Disable as it doesn't work from inside a container
        open: false
        {%- endif %}
      }
    )
}

// Watch
function watchPaths() {
  watch(`${paths.sass}/*.scss`{% if cookiecutter.windows == 'y' %}, { usePolling: true }{% endif %}, styles)
  watch(`${paths.templates}/**/*.html`{% if cookiecutter.windows == 'y' %}, { usePolling: true }{% endif %}).on("change", reload)
  watch([`${paths.js}/*.js`, `!${paths.js}/*.min.js`]{% if cookiecutter.windows == 'y' %}, { usePolling: true }{% endif %}, scripts).on("change", reload)
}

// Generate all assets
const generateAssets = parallel(
  styles,
  scripts,
  {%- if cookiecutter.custom_bootstrap_compilation == 'y' %}vendorScripts,{% endif %}
  imgCompression
)

// Set up dev environment
const dev = parallel(
  {%- if cookiecutter.use_docker == 'n' %}
  {%- if cookiecutter.use_async == 'y' %}
  asyncRunServer,
  {%- else %}
  runServer,
  {%- endif %}
  {%- endif %}
  initBrowserSync,
  watchPaths
)

exports.default = series(generateAssets, dev)
exports["generate-assets"] = generateAssets
exports["dev"] = dev
