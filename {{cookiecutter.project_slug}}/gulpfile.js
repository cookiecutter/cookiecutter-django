const gulp = require('gulp')
const pump = require('pump')
const sass = require('gulp-sass')
const pjson = require('./package.json')
const autoprefixer = require('gulp-autoprefixer')
const cleanCSS = require('gulp-clean-css')
const rename = require('gulp-rename')
const pixrem = require('gulp-pixrem')
const concat = require('gulp-concat')
const uglify = require('gulp-uglify')
const imagemin = require('gulp-imagemin')
const clean = require('gulp-clean')
const spawn = require('child_process').spawn
const runSequence = require('run-sequence')
const browserSync = require('browser-sync').create()
const pathsConfig = function (appName) {
  this.paths = {}

  this.paths['app'] = './' + (appName || pjson.name)

  this.paths['static'] = this.paths['app'] + '/static'

  this.paths['build'] = this.paths['static'] + '/build'

  this.paths['buildImages'] = this.paths['build'] + '/images'
  this.paths['images'] = this.paths['static'] + '/images'
  this.paths['images_files'] = this.paths['images'] + '/*'
  this.paths['buildImagesFavicons'] = this.paths['buildImages'] + '/favicons'
  this.paths['imagesFavicons'] = this.paths['images'] + '/favicons'
  this.paths['imagesFavicons_files'] = this.paths['imagesFavicons'] + '/*'

  this.paths['build_scriptsFileName'] = 'scripts.js'
  this.paths['scripts'] = this.paths['static'] + '/scripts'
  this.paths['scripts_files'] = this.paths['scripts'] + '/**/*'
  this.paths['scriptsJs'] = this.paths['scripts'] + '/js'
  this.paths['scriptsJs_files'] = this.paths['scriptsJs'] + '/*.js'

  this.paths['build_stylesFileName'] = 'styles.css'
  this.paths['styles'] = this.paths['static'] + '/styles'
  this.paths['styles_files'] = this.paths['styles'] + '/**/*'
  this.paths['stylesSass'] = this.paths['styles'] + '/sass'
  this.paths['stylesSass_files'] = this.paths['stylesSass'] + '/*.scss'
  this.paths['stylesCss'] = this.paths['styles'] + '/css'
  this.paths['stylesCss_files'] = this.paths['stylesCss'] + '/*.css'

  this.paths['templates'] = this.paths['app'] + '/templates'
  this.paths['templates_files'] = this.paths['templates'] + '/**/*.html'

  return this.paths
}
const paths = pathsConfig()

// region images
gulp.task('favicons-images', function (cb) {
  pump([gulp.src(paths.imagesFavicons_files),
      gulp.dest(paths.buildImagesFavicons)],
    cb)
})

gulp.task('nonfavicons-images', function (cb) {
  pump([gulp.src(paths.images_files),
      imagemin(),
      gulp.dest(paths.buildImages)],
    cb)
})

gulp.task('images', function () {
  runSequence(['favicons-images', 'nonfavicons-images'])
})
// endregion

// region scripts
gulp.task('js-scripts', function (cb) {
  pump([gulp.src(paths.scriptsJs_files),
      concat(paths.build_scriptsFileName),
      uglify(),
      rename({suffix: '.min'}),
      gulp.dest(paths.build)],
    cb)
})

gulp.task('scripts', function () {
  runSequence('js-scripts')
})
// endregion

// region styles
gulp.task('sass-styles', function (cb) {
  pump([gulp.src(paths.stylesSass_files),
      sass(),
      gulp.dest(paths.stylesCss)],
    cb
  )
})

gulp.task('css-styles', function (cb) {
  pump([gulp.src(paths.stylesCss_files),
      concat(paths.build_stylesFileName),
      autoprefixer({browsers: ['last 2 versions']}),
      pixrem(),
      cleanCSS({rebaseTo: '../../'}),
      rename({suffix: '.min'}),
      gulp.dest(paths.build)],
    cb)
})

gulp.task('styles', function () {
  runSequence('sass-styles', 'css-styles')
})
// endregion

// region build
gulp.task('build', function () {
  runSequence(['images', 'scripts', 'styles'])
})

gulp.task('clean-build', function (cb) {
  pump([gulp.src(paths.build),
      clean()],
    cb)
})
// endregion

gulp.task('init-browserSync', function () {
  browserSync.init({
    host: 'localhost:8000'
  })
})

gulp.task('watch', function () {
  gulp.watch(paths.images_files, ['images']).on('change', browserSync.reload)
  gulp.watch(paths.scripts_files, ['scripts']).on('change', browserSync.reload)
  gulp.watch(paths.styles_files, ['styles']).on('change', browserSync.reload)
  gulp.watch(paths.templates_files).on('change', browserSync.reload)
})

gulp.task('default', function () {
  runSequence('build', 'init-browserSync', 'watch')
})
