module.exports = (grunt) ->
  appConfig = grunt.file.readJSON("package.json")

  # Load grunt tasks automatically
  # see: https://github.com/sindresorhus/load-grunt-tasks
  require("load-grunt-tasks")(grunt)

  # Time how long tasks take. Can help when optimizing build times
  # see: https://npmjs.org/package/time-grunt
  require("time-grunt")(grunt)
  pathsConfig = (appName) ->
    @app = appName or appConfig.name
    app: @app
    templates: @app + "/templates"
    css: @app + "/static/css"
    sass: @app + "/static/sass"
    fonts: @app + "/static/fonts"
    images: @app + "/static/images"
    js: @app + "/static/js"
    manageScript: @app + "/manage.py"

  grunt.initConfig
    paths: pathsConfig()
    pkg: appConfig

    # see: https://github.com/gruntjs/grunt-contrib-watch
    watch:
      gruntfile:
        files: ["Gruntfile.coffee"]

      compass:
        files: ["<%= paths.sass %>/**/*.{scss,sass}"]
        tasks: ["compass:server"]

      livereload:
        files: [
          "<%= paths.js %>/**/*.js"
          "<%= paths.sass %>/**/*.{scss,sass}"
          "<%= paths.app %>/**/*.html"
        ]
        options:
          spawn: false
          livereload: true


    # see: https://github.com/gruntjs/grunt-contrib-compass
    compass:
      options:
        sassDir: "<%= paths.sass %>"
        cssDir: "<%= paths.css %>"
        fontsDir: "<%= paths.fonts %>"
        imagesDir: "<%= paths.images %>"
        relativeAssets: false
        assetCacheBuster: false
        raw: "Sass::Script::Number.precision = 10\n"

      dist:
        options:
          environment: "production"

      server:
        options: {}

    # see: https://npmjs.org/package/grunt-bg-shell
    bgShell:
      _defaults:
        bg: true

      runDjango:
        cmd: "python <%= paths.manageScript %> runserver"

  grunt.registerTask "serve", [
    "bgShell:runDjango"
    "watch"
  ]
  grunt.registerTask "build", ["compass:dist"]
  grunt.registerTask "default", ["build"]
  return
